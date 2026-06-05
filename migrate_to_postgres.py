#!/usr/bin/env python3
"""
One-time migration: SQLite (crm.db) → PostgreSQL.

Run locally BEFORE switching production to PostgreSQL:

    DATABASE_URL=postgresql://user:pass@host/db python migrate_to_postgres.py

Safe: deduplicates on (name, email, created_at). Re-running is harmless.
"""

import os
import sys
import sqlite3
from datetime import datetime


def main():
    db_url = os.environ.get('DATABASE_URL', '').strip()
    if not db_url:
        print('[MIGRATE] ERROR: DATABASE_URL not set. Cannot connect to PostgreSQL.')
        print('  Usage: DATABASE_URL=postgresql://... python migrate_to_postgres.py')
        sys.exit(1)

    if db_url.startswith('postgres://'):
        db_url = db_url.replace('postgres://', 'postgresql://', 1)

    # ── Locate SQLite ──────────────────────────────────────────────────────────
    sqlite_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'crm.db')
    if not os.path.exists(sqlite_path):
        print(f'[MIGRATE] No crm.db found at {sqlite_path}. Nothing to migrate.')
        return

    # ── Read from SQLite ───────────────────────────────────────────────────────
    sq = sqlite3.connect(sqlite_path)
    sq.row_factory = sqlite3.Row
    cur = sq.cursor()

    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='leads'")
    if not cur.fetchone():
        print('[MIGRATE] No leads table in SQLite. Nothing to migrate.')
        sq.close()
        return

    cur.execute('SELECT * FROM leads ORDER BY created_at')
    rows = cur.fetchall()
    sq.close()
    print(f'[MIGRATE] Found {len(rows)} leads in SQLite @ {sqlite_path}')

    if not rows:
        print('[MIGRATE] SQLite leads table is empty. Nothing to migrate.')
        return

    # ── Connect to PostgreSQL ──────────────────────────────────────────────────
    try:
        import psycopg2
        pg = psycopg2.connect(db_url)
        pgc = pg.cursor()
    except ImportError:
        print('[MIGRATE] ERROR: psycopg2 not installed. Run: pip install psycopg2-binary')
        sys.exit(1)
    except Exception as exc:
        print(f'[MIGRATE] ERROR: Cannot connect to PostgreSQL: {exc}')
        sys.exit(1)

    # ── Ensure table exists ────────────────────────────────────────────────────
    pgc.execute("""
        CREATE TABLE IF NOT EXISTS leads (
            id               SERIAL PRIMARY KEY,
            name             VARCHAR(100) NOT NULL,
            email            VARCHAR(120) DEFAULT '',
            phone            VARCHAR(30)  DEFAULT '',
            company          VARCHAR(150) DEFAULT '',
            country          VARCHAR(100) DEFAULT '',
            product_interest VARCHAR(200) DEFAULT '',
            message          TEXT         DEFAULT '',
            status           VARCHAR(30)  DEFAULT 'New',
            source           VARCHAR(50)  DEFAULT 'Website',
            created_at       TIMESTAMP    DEFAULT NOW()
        )
    """)
    pg.commit()

    # ── Insert, skipping duplicates ────────────────────────────────────────────
    inserted = 0
    skipped  = 0

    for row in rows:
        # Dedup: if same name + email + created_at already exists, skip
        pgc.execute(
            'SELECT id FROM leads WHERE name=%s AND email=%s AND created_at=%s',
            (row['name'], row['email'], row['created_at']),
        )
        if pgc.fetchone():
            skipped += 1
            continue

        pgc.execute("""
            INSERT INTO leads
                (name, email, phone, company, country,
                 product_interest, message, status, source, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            row['name'],
            row['email'],
            row['phone'],
            row['company']          if 'company'          in row.keys() else '',
            row['country']          if 'country'          in row.keys() else '',
            row['product_interest'] if 'product_interest' in row.keys() else '',
            row['message'],
            row['status'],
            row['source'],
            row['created_at'],
        ))
        inserted += 1

    pg.commit()
    pgc.close()
    pg.close()

    print(f'[MIGRATE] Complete — inserted: {inserted}, skipped (duplicate): {skipped}')
    print(f'[MIGRATE] PostgreSQL now has leads from SQLite.')


if __name__ == '__main__':
    main()
