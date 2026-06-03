"""
TERNS EXIM - Lead CRM Test Suite
Run with:  python test_leads.py

Safety: uses a temporary file for storage.
        Production leads.csv is never touched.

Storage note: The CRM writes leads.csv (CSV format).
              Your request mentioned leads.json -- the implemented
              storage is CSV, which is tested here.
"""

import csv
import os
import sys
import tempfile

# ── Force UTF-8 output on Windows ────────────────────────────────────────────
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# ── CRITICAL: set the temp CSV path BEFORE importing app / leads ──────────────
# leads.py reads LEADS_CSV_PATH at module-load time, so this must come first.
# We get a unique filename but delete the file so save_lead() writes the header.
_tmp = tempfile.NamedTemporaryFile(suffix='.csv', delete=False)
_tmp.close()
os.unlink(_tmp.name)          # delete so save_lead() creates a fresh file with header
os.environ['LEADS_CSV_PATH'] = _tmp.name

import leads          # LEADS_CSV now points to the temp path
import app as _app    # app imports leads internally; uses the same temp path

# ── Plain-text status markers (safe on all Windows terminals) ─────────────────
def _ok():   return '[OK]'
def _fail(): return '[FAIL]'
def _skip(): return '[SKIP]'

_results: dict = {}

# ── Sample lead reused across tests ───────────────────────────────────────────
_SAMPLE = {
    'name':    'Test User',
    'phone':   '9999999999',
    'email':   'test@example.com',
    'product': 'Hex Bolts M12',
    'message': 'Testing lead system',
}

REQUIRED_FIELDS = ['timestamp', 'name', 'phone', 'email', 'product', 'message']


# =============================================================================
# Test 1 - Route Testing
# =============================================================================

def test_routes():
    """GET each core route; assert HTTP 200."""
    client = _app.app.test_client()
    check_routes = [
        ('/',          'Home'),
        ('/contact',   'Contact'),
        ('/thank-you', 'Thank You'),
        ('/products',  'Products'),
    ]
    all_pass = True
    for path, label in check_routes:
        resp = client.get(path)
        passed = (resp.status_code == 200)
        if not passed:
            all_pass = False
        tag = _ok() if passed else _fail()
        print(f'  {label:12} {path:22} -> {resp.status_code}  {tag}')

    _results['routes'] = all_pass
    print(f'Route Test: {"OK" if all_pass else "FAIL"}  {_ok() if all_pass else _fail()}')
    print()


# =============================================================================
# Test 2 - Lead Form Submission
# =============================================================================

def test_lead_submission():
    """POST sample lead to /submit-lead; expect 302 redirect to /thank-you."""
    client = _app.app.test_client()
    try:
        resp = client.post('/submit-lead', data=_SAMPLE, follow_redirects=False)
        location = resp.headers.get('Location', '')
        passed = (resp.status_code == 302) and ('thank-you' in location)

        if passed:
            print(f'  POST /submit-lead -> {resp.status_code} -> {location}')
            print(f'Lead Submission: SUCCESS  {_ok()}')
        else:
            print(f'  Expected 302 -> /thank-you')
            print(f'  Got      {resp.status_code} -> {location!r}')
            print(f'Lead Submission: FAIL  {_fail()}')

        _results['submission'] = passed

    except Exception as exc:
        print(f'  Exception: {exc}')
        print(f'Lead Submission: FAIL  {_fail()}')
        _results['submission'] = False

    print()


# =============================================================================
# Test 3 - Storage Validation
# =============================================================================

def test_storage():
    """
    Confirm leads.csv exists, is non-empty, and its last row
    matches the sample lead from Test 2.
    Returns the last row dict (or None on failure).
    """
    csv_path = leads.LEADS_CSV

    if not os.path.isfile(csv_path):
        print(f'  leads.csv not found at: {csv_path}')
        _results['storage'] = False
        print(f'Storage Check: FAIL  {_fail()}')
        print()
        return None

    try:
        with open(csv_path, newline='', encoding='utf-8') as fh:
            rows = list(csv.DictReader(fh))
    except Exception as exc:
        print(f'  Could not read CSV: {exc}')
        _results['storage'] = False
        print(f'Storage Check: FAIL  {_fail()}')
        print()
        return None

    if not rows:
        print('  leads.csv exists but contains no data rows.')
        _results['storage'] = False
        print(f'Storage Check: FAIL  {_fail()}')
        print()
        return None

    last = rows[-1]
    name_ok  = last.get('name')  == _SAMPLE['name']
    phone_ok = last.get('phone') == _SAMPLE['phone']
    passed   = name_ok and phone_ok

    if passed:
        print('  Lead stored successfully.')
        print(f'  Name   : {last.get("name")}')
        print(f'  Phone  : {last.get("phone")}')
        print(f'  Email  : {last.get("email")}')
        print(f'  Product: {last.get("product")}')
        print(f'  Total rows in file: {len(rows)}')
    else:
        print('  Last row does not match the submitted test lead.')
        print(f'  Expected name={_SAMPLE["name"]!r}, got {last.get("name")!r}')
        print(f'  Expected phone={_SAMPLE["phone"]!r}, got {last.get("phone")!r}')

    _results['storage'] = passed
    print(f'Storage Check: {"PASS" if passed else "FAIL"}  {_ok() if passed else _fail()}')
    print()
    return last


# =============================================================================
# Test 4 - Data Structure Validation
# =============================================================================

def test_data_structure(row):
    """Verify every required field exists in the stored lead row."""
    if row is None:
        print('  No row to validate - skipping.')
        _results['structure'] = False
        print(f'Data Structure: {_skip()}')
        print()
        return

    missing = [f for f in REQUIRED_FIELDS if f not in row]
    empty   = [f for f in REQUIRED_FIELDS if f in row and row[f] == '']

    for field in REQUIRED_FIELDS:
        value   = row.get(field, '<MISSING>')
        present = (field in row) and (row[field] != '')
        tag     = _ok() if present else _fail()
        print(f'  {field:12} -> {str(value)[:40]:42} {tag}')

    if missing:
        print()
        for f in missing:
            print(f'  WARNING: field {f!r} is missing from stored lead.')
    if empty:
        print()
        for f in empty:
            print(f'  WARNING: field {f!r} is present but empty.')

    passed = (len(missing) == 0)
    _results['structure'] = passed
    print(f'Data Structure: {"PASS" if passed else "FAIL"}  {_ok() if passed else _fail()}')
    print()


# =============================================================================
# Cleanup
# =============================================================================

def _cleanup():
    try:
        if os.path.isfile(_tmp.name):
            os.unlink(_tmp.name)
    except OSError:
        pass


# =============================================================================
# Entry point
# =============================================================================

if __name__ == '__main__':
    div = '=' * 56

    print(div)
    print('  TERNS EXIM - Lead CRM Test Suite')
    print('  Storage: CSV  |  No production data written')
    print(div)
    print()

    try:
        print('-- 1. Route Tests -------------------------------------')
        test_routes()

        print('-- 2. Lead Form Submission ----------------------------')
        test_lead_submission()

        print('-- 3. Storage Validation ------------------------------')
        last_row = test_storage()

        print('-- 4. Data Structure Validation -----------------------')
        test_data_structure(last_row)

    finally:
        _cleanup()

    print(div)
    total  = len(_results)
    passed = sum(1 for v in _results.values() if v)
    print(f'  Results: {passed}/{total} passed')
    print()
    for name, result in _results.items():
        tag = _ok() if result else _fail()
        print(f'    {name:15} {tag}')
    print(div)

    sys.exit(0 if all(_results.values()) else 1)
