from flask import Flask, jsonify, render_template, send_from_directory, request, redirect, url_for
import json
import os
import re
import sys
import threading
import time
import urllib.request

from leads import save_lead, send_whatsapp_alert, send_telegram_alert

app = Flask(__name__)

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 31536000

BASE_URL = os.environ.get('BASE_URL', 'https://ternsexim.com').rstrip('/')

@app.context_processor
def inject_seo():
    path = request.path.rstrip('/') or '/'
    return {'canonical_url': BASE_URL + path}


# ── Static asset routes ───────────────────────────────────────────────────────

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, 'static', 'images'),
        'favicon.png', mimetype='image/png'
    )

@app.route('/robots.txt')
def robots():
    return send_from_directory(
        os.path.join(app.root_path, 'static'),
        'robots.txt', mimetype='text/plain'
    )

@app.route('/sitemap.xml')
def sitemap():
    return send_from_directory(
        os.path.join(app.root_path, 'static'),
        'sitemap.xml', mimetype='application/xml'
    )


# ── Page routes ───────────────────────────────────────────────────────────────

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/export-process')
def export_process():
    return render_template('export_process.html')

@app.route('/fastener-supplier-usa')
def usa():
    return render_template('usa.html')

@app.route('/fastener-supplier-uae')
def uae():
    return render_template('uae.html')

@app.route('/fastener-supplier-uk')
def uk():
    return render_template('uk.html')

@app.route('/fastener-supplier-netherlands')
def netherlands():
    return render_template('netherlands.html')

@app.route('/blog')
def blog_index():
    return render_template('blog_index.html')

@app.route('/blog/bolt-grades-8-8-vs-10-9-vs-12-9')
def blog_bolt_grades():
    return render_template('blog_bolt_grades.html')

@app.route('/blog/how-to-import-fasteners-from-india')
def blog_import_guide():
    return render_template('blog_import_guide.html')

@app.route('/blog/galvanized-vs-zinc-plated-vs-geomet')
def blog_coatings():
    return render_template('blog_coatings.html')

@app.route('/blog/din-iso-astm-fastener-standards')
def blog_standards():
    return render_template('blog_standards.html')

@app.route('/blog/fob-vs-cif-fastener-imports')
def blog_fob_cif():
    return render_template('blog_fob_cif.html')

@app.route('/blog/how-to-verify-indian-fastener-exporter')
def blog_verify_exporter():
    return render_template('blog_verify_exporter.html')

@app.route('/blog/best-fasteners-for-construction')
def blog_construction():
    return render_template('blog_construction.html')

@app.route('/blog/fasteners-for-marine-coastal-corrosion')
def blog_marine():
    return render_template('blog_marine.html')

@app.route('/products')
def products():
    return render_template('products.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/brochure')
def brochure():
    return render_template('brochure.html')

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

@app.route('/screws')
def screws():
    return render_template('screws.html')

@app.route('/thank-you')
def thank_you():
    return render_template('thank_you.html')


# ── Health check ──────────────────────────────────────────────────────────────

@app.route('/health')
def health():
    return jsonify({'status': 'ok'}), 200


# ── Lead capture ──────────────────────────────────────────────────────────────

_PHONE_RE = re.compile(r'^[\d\s+\-()\+]+$')
_EMAIL_RE  = re.compile(r'^[^\s@]+@[^\s@]+\.[^\s@]+$')

def _valid_phone(phone):
    if not _PHONE_RE.match(phone):
        return False
    return 7 <= len(re.sub(r'\D', '', phone)) <= 15

_CRM_API_URL = 'https://terns-exim-api.onrender.com/leads'

def _forward_to_crm(name, phone, email, product, message, company='', country='',
                    quantity='', destination_port=''):
    """Forward lead to CRM API (primary persistent storage). One retry on failure."""
    # Fold quantity and destination_port into the message string so the CRM
    # payload stays at its existing schema — no risk of unknown-field rejection.
    parts = []
    if quantity:
        parts.append(f'Qty: {quantity}')
    if destination_port:
        parts.append(f'Port: {destination_port}')
    if message:
        parts.append(message)
    crm_message = ' | '.join(parts)

    payload = json.dumps({
        'name':             name,
        'phone':            phone,
        'email':            email,
        'company':          company,
        'country':          country,
        'product_interest': product,
        'message':          crm_message,
        'source':           'Website',
        'status':           'New',
    }).encode('utf-8')

    def _attempt():
        req = urllib.request.Request(
            _CRM_API_URL,
            data=payload,
            headers={'Content-Type': 'application/json'},
            method='POST',
        )
        urllib.request.urlopen(req, timeout=10)

    try:
        _attempt()
        print(f'[CRM] Lead saved: {name}')
        return
    except Exception as exc:
        print(f'[CRM WARNING] Attempt 1 failed for "{name}": {exc}', file=sys.stderr)

    time.sleep(2)

    try:
        _attempt()
        print(f'[CRM] Lead saved on retry: {name}')
    except Exception as exc:
        print(
            f'[CRM ERROR] Retry failed for "{name}": {exc}. Lead in CSV backup.',
            file=sys.stderr,
        )

@app.route('/submit-lead', methods=['POST'])
def submit_lead():
    name             = request.form.get('name',             '').strip()
    email            = request.form.get('email',            '').strip()
    phone            = request.form.get('phone',            '').strip()
    company          = request.form.get('company',          '').strip()
    country          = request.form.get('country',          '').strip()
    product          = request.form.get('product',          '').strip()
    message          = request.form.get('message',          '').strip()
    quantity         = request.form.get('quantity',         '').strip()
    destination_port = request.form.get('destination_port', '').strip()

    if (not name or len(name) < 2
            or not email or not _EMAIL_RE.match(email)
            or not phone or not _valid_phone(phone)
            or not company
            or not country):
        return redirect(url_for('contact') + '#enquiry-form')

    lead = save_lead(name, phone, email, product, message,
                     company=company, country=country,
                     quantity=quantity, destination_port=destination_port)
    send_whatsapp_alert(lead)
    send_telegram_alert(lead)
    threading.Thread(
        target=_forward_to_crm,
        args=(name, phone, email, product, message),
        kwargs={'company': company, 'country': country,
                'quantity': quantity, 'destination_port': destination_port},
        daemon=True,
    ).start()
    return redirect(url_for('thank_you'))


# ── Security headers ──────────────────────────────────────────────────────────

@app.after_request
def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    response.headers['Permissions-Policy'] = 'camera=(), microphone=(), geolocation=()'
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; "
        "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
        "font-src 'self' https://fonts.gstatic.com; "
        "script-src 'self' 'unsafe-inline'; "
        "img-src 'self' data: https://flagcdn.com https://ternsexim.com; "
        "connect-src 'self'; "
        "form-action 'self'; "
        "frame-src https://ternsexim-bot.github.io;"
    )
    return response


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=False)
