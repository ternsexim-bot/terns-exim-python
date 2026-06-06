"""
Lead capture and CRM storage module for TERNS EXIM.

Phase 1 active  — file-based CSV storage.
Phase 2 ready   — swap save_lead() for Google Sheets by setting
                   GOOGLE_SHEET_ID + GOOGLE_SERVICE_ACCOUNT_JSON env vars.
Phase 3 ready   — set WHATSAPP_ALERT_ENABLED=true + CALLMEBOT_API_KEY to
                   enable real-time WhatsApp notifications.
"""

import csv
import logging
import os
import sys
from datetime import datetime

import requests

logger = logging.getLogger(__name__)

_BASE_DIR  = os.path.dirname(os.path.abspath(__file__))
LEADS_CSV  = os.environ.get('LEADS_CSV_PATH',
                             os.path.join(_BASE_DIR, 'leads.csv'))
FIELDNAMES = ['timestamp', 'name', 'email', 'phone', 'company', 'country', 'product', 'message']

# ── Phase 3 config (disabled until env vars are set) ─────────────────────────
_WA_ENABLED = os.environ.get('WHATSAPP_ALERT_ENABLED', '').lower() == 'true'
_WA_API_KEY = os.environ.get('CALLMEBOT_API_KEY', '')
_WA_PHONE   = os.environ.get('WHATSAPP_PHONE', '916369097465')


# ── Phase 1 & 2: Lead Storage ─────────────────────────────────────────────────

def save_lead(name, phone, email='', product='', message='', company='', country=''):
    """
    Append a lead to leads.csv (Phase 1).
    Returns the lead dict for logging / Phase 3 alerting.

    Phase 2 upgrade path:
        Replace the CSV block below with a Google Sheets API call.
        The returned `lead` dict format stays identical.
    """
    lead = {
        'timestamp': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC'),
        'name':      name,
        'email':     email,
        'phone':     phone,
        'company':   company,
        'country':   country,
        'product':   product or 'General Enquiry',
        'message':   message,
    }

    # ── Phase 1: CSV storage ──────────────────────────────────────────────────
    try:
        # Write header when file is absent OR zero-byte (e.g. pre-created empty file).
        # Checking only isfile() misses the empty-file case and causes DictReader
        # to treat the first data row as the header, returning zero rows on read.
        needs_header = (
            not os.path.isfile(LEADS_CSV)
            or os.path.getsize(LEADS_CSV) == 0
        )
        with open(LEADS_CSV, 'a', newline='', encoding='utf-8') as fh:
            writer = csv.DictWriter(fh, fieldnames=FIELDNAMES)
            if needs_header:
                writer.writeheader()
            writer.writerow(lead)
    except OSError as exc:
        print(f'[LEADS ERROR] Could not write to {LEADS_CSV}: {exc}', file=sys.stderr)
        logger.error('Could not write lead to %s: %s', LEADS_CSV, exc)

    # ── Phase 2 placeholder ───────────────────────────────────────────────────
    # Uncomment and fill in credentials to enable Google Sheets sync:
    #
    # if os.environ.get('GOOGLE_SHEET_ID'):
    #     _append_to_sheet(lead)

    logger.info(
        '[LEAD] %s | Name: %s | Phone: %s | Email: %s | Product: %s',
        lead['timestamp'], name, phone, email, lead['product']
    )
    return lead


# ── Phase 3: WhatsApp Alert ───────────────────────────────────────────────────

def send_whatsapp_alert(lead):
    """
    Send a WhatsApp notification via CallMeBot API (non-blocking).

    To activate:
        1. Follow CallMeBot setup at https://www.callmebot.com/blog/free-api-whatsapp-messages/
        2. Set env vars:  WHATSAPP_ALERT_ENABLED=true
                          CALLMEBOT_API_KEY=<your key>
                          WHATSAPP_PHONE=916369097465   (default already set)
    """
    if not _WA_ENABLED or not _WA_API_KEY:
        return False

    try:
        import urllib.parse
        import urllib.request

        msg = (
            f"New Lead — TERNS EXIM Website\n"
            f"Name: {lead['name']}\n"
            f"Phone: {lead['phone']}\n"
            f"Email: {lead.get('email') or 'N/A'}\n"
            f"Product: {lead.get('product') or 'General Enquiry'}\n"
            f"Message: {lead.get('message') or '—'}\n"
            f"Time: {lead['timestamp']}"
        )
        params = urllib.parse.urlencode({
            'phone':  _WA_PHONE,
            'text':   msg,
            'apikey': _WA_API_KEY,
        })
        url = f'https://api.callmebot.com/whatsapp.php?{params}'
        urllib.request.urlopen(url, timeout=5)
        logger.info('[WA_ALERT] Sent for lead: %s', lead['name'])
        return True
    except Exception as exc:
        logger.warning('[WA_ALERT] Failed (non-blocking): %s', exc)
        return False


# ── Phase 3b: Telegram Alert ──────────────────────────────────────────────────

def send_telegram_alert(lead_data):
    try:
        bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')
        chat_id = os.environ.get('TELEGRAM_CHAT_ID')
        if not bot_token or not chat_id:
            return
        message = (
            "🔩 *New Lead — Terns Exim*\n\n"
            f"👤 *Name:* {lead_data.get('name')}\n"
            f"🏢 *Company:* {lead_data.get('company')}\n"
            f"🌍 *Country:* {lead_data.get('country')}\n"
            f"📞 *Phone:* {lead_data.get('phone')}\n"
            f"📧 *Email:* {lead_data.get('email')}\n"
            f"🔧 *Product:* {lead_data.get('product')}\n"
            f"💬 *Message:* {lead_data.get('message', 'N/A')}\n"
        )
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        requests.post(url, json={
            'chat_id': chat_id,
            'text': message,
            'parse_mode': 'Markdown'
        }, timeout=5)
    except Exception:
        pass
