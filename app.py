import logging
import os
import re
import sys
from datetime import datetime

from flask import Flask, jsonify, render_template, request, redirect, send_from_directory, url_for
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

from leads import save_lead, send_whatsapp_alert

# ── Logging ───────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
)
logger = logging.getLogger(__name__)

# ── Environment detection ─────────────────────────────────────────────────────
# Render sets RENDER=true automatically on all deployed services.
IS_PRODUCTION = os.environ.get('RENDER', '').lower() in ('true', '1', 'yes')

# ── Database configuration ────────────────────────────────────────────────────
_DB_URL = os.environ.get('DATABASE_URL', '').strip()

# Render provides postgres:// but SQLAlchemy requires postgresql://
if _DB_URL.startswith('postgres://'):
    _DB_URL = _DB_URL.replace('postgres://', 'postgresql://', 1)

if IS_PRODUCTION and not _DB_URL:
    logger.critical(
        '[CRITICAL] DATABASE_URL is not set in production. '
        'Refusing to start with ephemeral SQLite. '
        'Link a Render PostgreSQL database via render.yaml (databases section) '
        'or set DATABASE_URL manually in Render Environment Settings.'
    )
    sys.exit(1)

if _DB_URL:
    _DB_URI = _DB_URL
    logger.info('[STARTUP] [DATABASE CONNECTED] PostgreSQL active — data is persistent')
else:
    # SQLite only for local development
    _SQLITE_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'crm.db')
    _DB_URI = f'sqlite:///{_SQLITE_PATH}'
    logger.warning(
        '[STARTUP] No DATABASE_URL set — using SQLite @ %s. '
        'LOCAL DEVELOPMENT ONLY. Do not deploy to production without DATABASE_URL.',
        _SQLITE_PATH,
    )

# ── App ───────────────────────────────────────────────────────────────────────
app = Flask(__name__)

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 31536000
app.config['SQLALCHEMY_DATABASE_URI']   = _DB_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# CORS scoped only to /api/* so the CRM dashboard (Netlify) can reach it
CORS(app, resources={r'/api/*': {'origins': '*'}})


# ── Lead model ────────────────────────────────────────────────────────────────
class Lead(db.Model):
    __tablename__ = 'leads'

    id               = db.Column(db.Integer, primary_key=True)
    name             = db.Column(db.String(100), nullable=False)
    email            = db.Column(db.String(120), default='')
    phone            = db.Column(db.String(30),  default='')
    company          = db.Column(db.String(150), default='')
    country          = db.Column(db.String(100), default='')
    product_interest = db.Column(db.String(200), default='')
    message          = db.Column(db.Text,        default='')
    status           = db.Column(db.String(30),  default='New')
    source           = db.Column(db.String(50),  default='Website')
    created_at       = db.Column(db.DateTime,    default=datetime.utcnow)

    def to_dict(self):
        return {
            'id':               self.id,
            'name':             self.name,
            'email':            self.email,
            'phone':            self.phone,
            'company':          self.company,
            'country':          self.country,
            'product_interest': self.product_interest,
            'message':          self.message,
            'status':           self.status,
            'source':           self.source,
            'created_at':       self.created_at.isoformat() if self.created_at else None,
        }


with app.app_context():
    db.create_all()
    count = Lead.query.count()
    logger.info('[STARTUP] Tables ready. Existing leads in DB: %d', count)


BASE_URL = os.environ.get('BASE_URL', 'https://ternsexim.com').rstrip('/')


@app.context_processor
def inject_seo():
    path = request.path.rstrip('/') or '/'
    return {'canonical_url': BASE_URL + path}


# ── Static / file routes ──────────────────────────────────────────────────────

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, 'static', 'images'),
        'favicon.png', mimetype='image/png',
    )

@app.route('/robots.txt')
def robots():
    return send_from_directory(
        os.path.join(app.root_path, 'static'), 'robots.txt', mimetype='text/plain')

@app.route('/sitemap.xml')
def sitemap():
    return send_from_directory(
        os.path.join(app.root_path, 'static'), 'sitemap.xml', mimetype='application/xml')


# ── Page routes ───────────────────────────────────────────────────────────────

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/products')
def products():
    return render_template('products.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/hex-bolts')
def hex_bolts():
    return render_template('hex_bolts.html')

@app.route('/anchor-bolts')
def anchor_bolts():
    return render_template('anchor_bolts.html')

@app.route('/foundation-bolts')
def foundation_bolts():
    return render_template('foundation_bolts.html')

@app.route('/nuts')
def nuts():
    return render_template('nuts.html')

@app.route('/washers')
def washers():
    return render_template('washers.html')

@app.route('/threaded-rods')
def threaded_rods():
    return render_template('threaded_rods.html')


# ── Lead validation ───────────────────────────────────────────────────────────

_PHONE_CHARS_RE = re.compile(r'^[\d\s+\-()\+]+$')
_EMAIL_RE       = re.compile(r'^[^\s@]+@[^\s@]+\.[^\s@]+$')


def _valid_phone(phone):
    if not _PHONE_CHARS_RE.match(phone):
        return False
    return 7 <= len(re.sub(r'\D', '', phone)) <= 15


# ── Lead submission ───────────────────────────────────────────────────────────

@app.route('/submit-lead', methods=['POST'])
def submit_lead():
    name    = request.form.get('name',    '').strip()
    email   = request.form.get('email',   '').strip()
    phone   = request.form.get('phone',   '').strip()
    company = request.form.get('company', '').strip()
    country = request.form.get('country', '').strip()
    product = request.form.get('product', '').strip()
    message = request.form.get('message', '').strip()

    logger.info('[LEAD SUBMITTED] name=%r email=%r company=%r country=%r product=%r',
                name, email, company, country, product)

    if (not name or len(name) < 2
            or not email or not _EMAIL_RE.match(email)
            or not phone or not _valid_phone(phone)
            or not company
            or not country):
        logger.warning('[LEAD REJECTED] Validation failed — name=%r email=%r phone=%r', name, email, phone)
        return redirect(url_for('contact'))

    # CSV backup (also ephemeral on free Render, but kept for local audit trail)
    lead_dict = save_lead(name, phone, email, product, message, company=company, country=country)
    send_whatsapp_alert(lead_dict)

    # Primary storage — SQLAlchemy (PostgreSQL in production)
    try:
        lead = Lead(
            name=name, email=email, phone=phone,
            company=company, country=country,
            product_interest=product or 'General Enquiry',
            message=message, source='Website', status='New',
        )
        db.session.add(lead)
        db.session.commit()
        logger.info('[LEAD SAVED] id=%d name=%r email=%r db=%s',
                    lead.id, name, email, 'postgresql' if _DB_URL else 'sqlite')
    except Exception as exc:
        db.session.rollback()
        logger.error('[LEAD DB ERROR] %s', exc)

    return redirect(url_for('thank_you'))


@app.route('/thank-you')
def thank_you():
    return render_template('thank_you.html')


# ── CRM REST API ──────────────────────────────────────────────────────────────

@app.route('/api/leads', methods=['GET'])
def api_get_leads():
    status = request.args.get('status')
    query  = Lead.query.order_by(Lead.created_at.desc())
    if status:
        query = query.filter_by(status=status)
    leads = query.all()
    logger.info('[LEAD READ] count=%d filter=%r', len(leads), status)
    return jsonify([l.to_dict() for l in leads])


@app.route('/api/leads', methods=['POST'])
def api_create_lead():
    data = request.get_json() or {}
    if not data.get('name', '').strip():
        return jsonify({'error': 'Name is required'}), 400
    lead = Lead(
        name=data.get('name', '').strip(),
        email=data.get('email', ''),
        phone=data.get('phone', ''),
        company=data.get('company', ''),
        country=data.get('country', ''),
        product_interest=data.get('product_interest', ''),
        message=data.get('message', ''),
        status=data.get('status', 'New'),
        source=data.get('source', 'Manual'),
    )
    db.session.add(lead)
    db.session.commit()
    logger.info('[LEAD SAVED] id=%d name=%r source=api db=%s',
                lead.id, lead.name, 'postgresql' if _DB_URL else 'sqlite')
    return jsonify(lead.to_dict()), 201


@app.route('/api/leads/<int:lead_id>', methods=['PUT'])
def api_update_lead(lead_id):
    lead = db.get_or_404(Lead, lead_id)
    data = request.get_json() or {}
    for field in ['name', 'email', 'phone', 'company', 'country',
                  'product_interest', 'message', 'status', 'source']:
        if field in data:
            setattr(lead, field, data[field])
    db.session.commit()
    return jsonify(lead.to_dict())


@app.route('/api/leads/<int:lead_id>', methods=['DELETE'])
def api_delete_lead(lead_id):
    lead = db.get_or_404(Lead, lead_id)
    db.session.delete(lead)
    db.session.commit()
    return jsonify({'message': 'deleted'})


@app.route('/api/leads/stats', methods=['GET'])
def api_lead_stats():
    statuses = ['New', 'Contacted', 'Negotiation', 'Won', 'Lost']
    data = {'total': Lead.query.count()}
    for s in statuses:
        data[s.lower()] = Lead.query.filter_by(status=s).count()
    logger.info('[CRM LOAD] stats=%s', data)
    return jsonify(data)


@app.route('/api/health', methods=['GET'])
def api_health():
    db_type = 'postgresql' if _DB_URL else 'sqlite'
    try:
        total = Lead.query.count()
        db_ok = True
    except Exception as exc:
        logger.error('[HEALTH] DB check failed: %s', exc)
        total = -1
        db_ok = False
    logger.info('[DATABASE CONNECTED] type=%s ok=%s leads=%d env=%s',
                db_type, db_ok, total, 'production' if IS_PRODUCTION else 'development')
    return jsonify({
        'status':       'ok' if db_ok else 'error',
        'database':     db_type,
        'persistent':   bool(_DB_URL),
        'db_connected': db_ok,
        'total_leads':  total,
        'environment':  'production' if IS_PRODUCTION else 'development',
    })


# ── Security headers ──────────────────────────────────────────────────────────

@app.after_request
def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    if not request.path.startswith('/api/'):
        response.headers['Content-Security-Policy'] = (
            "default-src 'self'; "
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
            "font-src 'self' https://fonts.gstatic.com; "
            "script-src 'self' 'unsafe-inline'; "
            "img-src 'self' data: https://flagcdn.com https://ternsexim.com; "
            "connect-src 'self';"
        )
    return response


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
