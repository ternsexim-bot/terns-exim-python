from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


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
