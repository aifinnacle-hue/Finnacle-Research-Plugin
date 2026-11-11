#!/usr/bin/env python3
# Curated by Vastav Parikh & Yash Master for Finnacle Shah Classes.
# Intellectual property of Finnacle Institute. © 2026 Finnacle Institute. All rights reserved.
# Keep this notice intact in any copy or modified version of this file.
"""
Ace Model → Supabase loader.

Parses Ace Equity model workbooks ("<Company>_Ace Model.xlsx") and loads them
into the indian-equities-financials Supabase database.

Usage:
  python3 ace_loader.py FILE1.xlsx [FILE2.xlsx ...] [options]
  python3 ace_loader.py --folder /path/to/folder [options]

Options:
  --dry-run        Parse and diff against the DB, print summary, write nothing.
  --approve-new    Insert new dictionary rows (line items / metrics / sectors /
                   industries / companies) that were flagged in a prior dry run,
                   and mark their auto-alerts approved. Without this flag the
                   loader STOPS if unknown dictionary entries are found.
  --force          Re-load a file even if its hash was already loaded.
  --dump-json DIR  Also write parsed records as JSON (one file per workbook).
  --env-file PATH  Read SUPABASE_URL / SUPABASE_SERVICE_ROLE_KEY from this file.

Credentials: env vars SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY (service role
key required — the DB is read-only for other roles).

Exit codes: 0 ok | 2 unknown dictionary entries found (approval needed) | 1 error.
"""
import argparse, hashlib, json, os, re, sys, time
from datetime import datetime, timezone

try:
    import openpyxl
except ImportError:
    sys.exit("Missing dependency: pip install openpyxl requests --break-system-packages")
try:
    import requests
except ImportError:
    requests = None

# ----------------------------------------------------------------------------
# helpers
# ----------------------------------------------------------------------------

def slug(s):
    return re.sub(r'[^A-Za-z0-9]+', '_', str(s).strip().upper()).strip('_')[:60]

def is_num(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)

def year_cols(row, lo=1990, hi=2100):
    """Map column index -> fiscal year for 4-digit-int header cells."""
    return {i: int(v) for i, v in enumerate(row) if is_num(v) and lo <= v <= hi}

def quarter_cols(row):
    """Map column index -> YYYYMM for 6-digit-int header cells."""
    out = {}
    for i, v in enumerate(row):
        if is_num(v) and 199001 <= v <= 210012 and 1 <= int(v) % 100 <= 12:
            out[i] = int(v)
    return out

def fy_of(period_code):
    y, m = period_code // 100, period_code % 100
    return y + 1 if m >= 4 else y

def fq_of(period_code):
    m = period_code % 100
    return {4: 1, 5: 1, 6: 1, 7: 2, 8: 2, 9: 2, 10: 3, 11: 3, 12: 3, 1: 4, 2: 4, 3: 4}[m]

UNIT_OVERRIDES = {  # for auto-registering brand-new line items
    'per_share': ('EPS', 'BOOK', 'NAV'), 'percent': ('_PERC',),
}

# ----------------------------------------------------------------------------
# workbook parsing
# ----------------------------------------------------------------------------

STATEMENT_SHEETS = [  # sheet, statement, calc_prefix
    ('P&L - Ace', 'pnl_annual', 'CALC_PL'),
    ('BS - Ace', 'balance_sheet_annual', 'CALC_BS'),
    ('Cash Flow - Ace', 'cash_flow_annual', 'CALC_CF'),
]
FACT_TABLE = {
    'pnl_annual': 'fact_pnl_annual',
    'balance_sheet_annual': 'fact_balance_sheet_annual',
    'cash_flow_annual': 'fact_cash_flow_annual',
    'forensic_annual': 'fact_other_annual',
    'pnl_quarterly': 'fact_pnl_quarterly',
    'balance_sheet_quarterly': 'fact_balance_sheet_quarterly',
}
DERIVED_SHEETS = [  # sheet, prefix, category, label_col, data_start, period_type
    ('Return Ratios', 'RR', 'return_ratios', 0, 2, 'fy'),
    ('Rolling Return Ratios', 'RR', 'return_ratios', 0, 2, 'ttm'),
    ('BS Ratios', 'BSR', 'bs_ratios', 0, 2, 'fy'),
    ('CF Ratios', 'CFR', 'cf_ratios', 0, 2, 'fy'),
    ('Forensics', 'FOR', 'forensics', 4, 5, 'fy'),
    ('P&L Glance', 'PG', 'pnl_glance', 0, 1, 'fy'),
    ('Rolling P&L Glance', 'PG', 'pnl_glance', 0, 1, 'ttm'),
    ('BS Glance', 'BG', 'bs_glance', 0, 1, 'fy'),
]
BLACKLIST = {'IN CR.', 'DURATION CAGR.', '3Y', '5Y', '8Y', '12Y', 'MIN', 'MAX', 'AVG.',
             'MEDIAN', 'CURRENT', 'DIFFERENCE', 'CHECK', 'FIELD DESCRIPTION', 'PARTICULARS'}

CD_MAP = {  # General-sheet field -> companies column
    'CD_CHAIRMAN': 'chairman', 'CD_MDIR': 'managing_director', 'CD_NAME': 'auditor',
    'CD_HOUSE': 'house', 'CD_SYMBOL': 'nse_symbol', 'CD_BLOOMBERG_CODE': 'bloomberg_code',
    'CD_SCRIP_NAME': 'bse_scrip_name', 'CD_ISIN': 'isin', 'SQC_RATING': 'credit_rating',
}


def parse_workbook(path):
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    sheets = {ws.title: list(ws.iter_rows(values_only=True)) for ws in wb.worksheets
              if ws.title not in ('Universe',)}
    wb.close()

    # --- company profile -----------------------------------------------------
    profile, fincode, basis = {}, None, 'consolidated'
    cni = sheets.get('Company Name Input', [])
    for r in cni:
        if not r or len(r) < 3:
            continue
        key = str(r[1]).strip().lower() if r[1] else ''
        if key == 'fincode' and is_num(r[2]):
            fincode = int(r[2])
        elif key == 'type' and r[2]:
            basis = 'standalone' if 'standalone' in str(r[2]).lower() else 'consolidated'
    gen = sheets.get('General', [])
    for r in gen:
        if not r or len(r) < 3 or not r[1]:
            continue
        code, val = str(r[1]).strip(), r[2]
        if val in (None, 0, '0', ''):
            val = None
        if code == 'CD_COMPNAME':
            profile['name'] = str(val).strip() if val else None
        elif code == 'CD_SECTOR':
            profile['_sector'] = str(val).strip() if val else None
        elif code == 'CD_INDUSTRY':
            profile['_industry'] = str(val).strip() if val else None
        elif code == 'CD_SUBINDUSTRY':
            profile['sub_industry'] = str(val).strip() if val else None
        elif code == 'CD_SCRIPCODE':
            profile['bse_code'] = str(int(val)) if is_num(val) else (str(val).strip() if val else None)
        elif code in CD_MAP:
            profile[CD_MAP[code]] = str(val).strip() if val is not None else None
    if fincode is None and gen and len(gen) > 1 and is_num(gen[1][0]):
        fincode = int(gen[1][0])
    if not profile.get('name'):
        raise ValueError(f'{path}: could not resolve company name (General!CD_COMPNAME)')
    if fincode is None:
        raise ValueError(f'{path}: could not resolve fincode')
    profile['fincode'] = fincode
    profile['preferred_basis'] = basis
    profile['coverage_status'] = 'under_coverage'

    facts = []          # dicts: table, ace_code, label, fiscal_year|period_code, value
    new_items = {}      # ace_code -> (label, statement) candidates not needed here; loader diffs vs DB
    seen_keys = set()

    def emit(table, ace_code, label, value, fiscal_year=None, period_code=None):
        if value is None or (not is_num(value)):
            return
        key = (table, ace_code, fiscal_year, period_code)
        if key in seen_keys:
            return
        seen_keys.add(key)
        facts.append({'table': table, 'ace_code': ace_code, 'label': label,
                      'fiscal_year': fiscal_year, 'period_code': period_code,
                      'value': round(float(value), 6)})

    # --- annual statement sheets ---------------------------------------------
    max_year = 0
    for sheet, stmt, calc_prefix in STATEMENT_SHEETS:
        rows = sheets.get(sheet)
        if not rows:
            continue
        ycols = year_cols(rows[2]) if len(rows) > 2 else {}
        if ycols:
            max_year = max(max_year, max(ycols.values()))
        for r in rows[3:]:
            if not r or not r[0]:
                continue
            label = str(r[0]).strip()
            if label in ('', 'Field Description'):
                continue
            code = str(r[1]).strip() if len(r) > 1 and r[1] and str(r[1]).strip() != 'Field Name' \
                else f'{calc_prefix}_{slug(label)}'
            for ci, yr in ycols.items():
                if ci < len(r):
                    emit(FACT_TABLE[stmt], code, label, r[ci], fiscal_year=yr)

    # --- quarterly sheets -----------------------------------------------------
    for sheet, table in (('Qtrly P&L', 'fact_pnl_quarterly'),
                         ('Qtrly BS', 'fact_balance_sheet_quarterly')):
        rows = sheets.get(sheet)
        if not rows or len(rows) < 4:
            continue
        qcols = quarter_cols(rows[2])
        seen_codes = set()
        for r in rows[3:]:
            if not r or not r[0] or not (len(r) > 1 and r[1]):
                continue
            label, code = str(r[0]).strip(), str(r[1]).strip()
            if label == 'Field Description' or code == 'Field Name':
                continue
            if code in seen_codes:      # second (helper) block of Qtrly P&L — stop
                break
            seen_codes.add(code)
            for ci, pc in qcols.items():
                if ci < len(r):
                    emit(table, code, label, r[ci], fiscal_year=fy_of(pc), period_code=pc)

    # --- Forensic - Ace (raw datapoints; routed by dictionary statement later) -
    rows = sheets.get('Forensic - Ace')
    if rows and len(rows) > 3:
        fycols = year_cols(rows[3])
        for r in rows[4:]:
            if not r or not r[0]:
                continue
            code = str(r[0]).strip()
            if not re.match(r'^[A-Z][A-Z0-9_]+$', code):
                continue
            label = str(r[6]).strip() if len(r) > 6 and r[6] else code
            for ci, yr in fycols.items():
                if ci < len(r):
                    # table decided by loader via dictionary lookup; mark forensic
                    emit('__forensic__', code, label, r[ci], fiscal_year=yr)

    # --- derived sheets ---------------------------------------------------------
    # metric codes are regenerated with the exact same algorithm used to seed
    # derived_metrics: per-sheet dedupe (prefixes are unique per category), so the
    # fy sheet and its rolling twin regenerate IDENTICAL codes.
    derived = []
    company_upper = profile['name'].strip().upper()
    for sheet, prefix, cat, labcol, datastart, ptype in DERIVED_SHEETS:
        rows = sheets.get(sheet)
        if not rows:
            continue
        dseen = set()

        def dkey(name, _seen=None):
            s = dseen if _seen is None else _seen
            base = f'{prefix}_{slug(name)}'
            code, k = base, 2
            while code in s:
                code, k = f'{base}_{k}', k + 1
            s.add(code)
            return code

        ycols = year_cols(rows[2]) if len(rows) > 2 else {}
        prev = None
        for i, r in enumerate(rows, 1):
            label = r[labcol] if len(r) > labcol else None
            if label is None or not isinstance(label, str):
                continue
            label = label.strip()
            up = label.upper()
            if not label or up in BLACKLIST or label.startswith('(') or up.startswith('NOTE'):
                continue
            if up == company_upper or up.endswith(' LTD.') and i <= 2:
                continue
            has_data = any(is_num(v) for v in r[datastart:])
            if not has_data:
                prev = label
                continue
            name = f'{prev} - YoY Change' if up.startswith('CHANGE YOY') and prev else label
            code = dkey(name)
            if not up.startswith('CHANGE YOY'):
                prev = label
            for ci, yr in ycols.items():
                if ci < len(r) and is_num(r[ci]):
                    derived.append({'metric_code': code, 'name': name, 'category': cat,
                                    'period_type': ptype, 'fiscal_year': yr, 'period_code': 0,
                                    'value': round(float(r[ci]), 6)})

    # Fund Flow (block 2: rows 32-41; Current Year / 3Y / 5Y)
    rows = sheets.get('Fund Flow')
    if rows and max_year:
        ffseen = set()
        prefix = 'FF'
        for i, r in enumerate(rows, 1):
            if 32 <= i <= 41 and len(r) > 4 and r[1]:
                name = str(r[1]).strip()
                base = f'FF_{slug(name)}'
                code, k = base, 2
                while code in ffseen:
                    code, k = f'{base}_{k}', k + 1
                ffseen.add(code)
                for val, ptype in ((r[2], 'fy'), (r[3], 'cum_3y'), (r[4], 'cum_5y')):
                    if is_num(val):
                        derived.append({'metric_code': code, 'name': name, 'category': 'fund_flow',
                                        'period_type': ptype, 'fiscal_year': max_year,
                                        'period_code': 0, 'value': round(float(val), 6)})

    # rolling-ttm codes may collide with fy codes on purpose (same metric); dedupe rows
    dd, seen2 = [], set()
    for d in derived:
        k = (d['metric_code'], d['period_type'], d['fiscal_year'], d['period_code'])
        if k not in seen2:
            seen2.add(k)
            dd.append(d)

    return {'profile': profile, 'basis': basis, 'facts': facts, 'derived': dd,
            'max_year': max_year}


# ----------------------------------------------------------------------------
# Supabase REST client
# ----------------------------------------------------------------------------

class DB:
    def __init__(self, url, key):
        self.base = url.rstrip('/') + '/rest/v1'
        self.h = {'apikey': key, 'Authorization': f'Bearer {key}',
                  'Content-Type': 'application/json'}

    def get_all(self, table, select, extra=''):
        out, offset, page = [], 0, 1000
        while True:
            r = requests.get(f'{self.base}/{table}?select={select}{extra}',
                             headers={**self.h, 'Range': f'{offset}-{offset + page - 1}'},
                             timeout=60)
            r.raise_for_status()
            chunk = r.json()
            out += chunk
            if len(chunk) < page:
                return out
            offset += page

    def insert(self, table, rows, on_conflict=None, upsert=False, returning=False):
        if not rows:
            return []
        prefer = []
        if upsert:
            prefer.append('resolution=merge-duplicates')
        prefer.append('return=representation' if returning else 'return=minimal')
        url = f'{self.base}/{table}' + (f'?on_conflict={on_conflict}' if on_conflict else '')
        out = []
        for i in range(0, len(rows), 500):
            r = requests.post(url, headers={**self.h, 'Prefer': ','.join(prefer)},
                              json=rows[i:i + 500], timeout=120)
            if r.status_code >= 300:
                raise RuntimeError(f'{table} insert failed [{r.status_code}]: {r.text[:500]}')
            if returning:
                out += r.json()
        return out

    def patch(self, table, filt, payload):
        r = requests.patch(f'{self.base}/{table}?{filt}',
                           headers={**self.h, 'Prefer': 'return=minimal'},
                           json=payload, timeout=60)
        r.raise_for_status()


# ----------------------------------------------------------------------------
# main
# ----------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('files', nargs='*')
    ap.add_argument('--folder')
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--approve-new', action='store_true')
    ap.add_argument('--force', action='store_true')
    ap.add_argument('--dump-json')
    ap.add_argument('--env-file')
    a = ap.parse_args()

    if a.env_file:
        for line in open(a.env_file):
            if '=' in line and not line.strip().startswith('#'):
                k, v = line.strip().split('=', 1)
                os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))

    files = list(a.files)
    if a.folder:
        files += sorted(os.path.join(a.folder, f) for f in os.listdir(a.folder)
                        if f.lower().endswith('.xlsx') and not f.startswith('~'))
    if not files:
        ap.error('no input files')

    url, key = os.environ.get('SUPABASE_URL'), os.environ.get('SUPABASE_SERVICE_ROLE_KEY')
    online = bool(url and key and requests)
    if not online and not a.dry_run:
        sys.exit('SUPABASE_URL / SUPABASE_SERVICE_ROLE_KEY not set (or requests missing). '
                 'Use --dry-run for offline parsing.')
    db = DB(url, key) if online else None

    # dictionaries
    li_map, dm_map, sec_map, ind_map, co_map, loaded_hashes = {}, {}, {}, {}, {}, set()
    if online:
        li_map = {x['ace_code']: x for x in db.get_all('line_items', 'id,ace_code,statement')}
        dm_map = {x['metric_code']: x['id'] for x in db.get_all('derived_metrics', 'id,metric_code')}
        sec_map = {x['name']: x['id'] for x in db.get_all('sectors', 'id,name')}
        ind_map = {x['name']: x['id'] for x in db.get_all('industries', 'id,name')}
        co_map = {x['fincode']: x['id'] for x in db.get_all('companies', 'id,fincode')}
        loaded_hashes = {x['file_hash'] for x in
                         db.get_all('ingestion_batches', 'file_hash', '&status=eq.completed')}

    parsed, unknown = [], {'line_items': {}, 'metrics': {}, 'sectors': set(),
                           'industries': set(), 'companies': []}
    for f in files:
        fh = hashlib.sha256(open(f, 'rb').read()).hexdigest()
        if fh in loaded_hashes and not a.force:
            print(f'SKIP (already loaded): {os.path.basename(f)}')
            continue
        p = parse_workbook(f)
        p['file'], p['hash'] = f, fh
        parsed.append(p)
        pr = p['profile']
        stmt_of = {c: li_map[c]['statement'] for c in li_map}
        for fact in p['facts']:
            c = fact['ace_code']
            if c not in li_map and c not in unknown['line_items']:
                st = ('forensic_annual' if fact['table'] == '__forensic__' else
                      {v: k for k, v in FACT_TABLE.items()}[fact['table']])
                unknown['line_items'][c] = (fact['label'], st)
        for d in p['derived']:
            if d['metric_code'] not in dm_map and d['metric_code'] not in unknown['metrics']:
                unknown['metrics'][d['metric_code']] = (d['name'], d['category'])
        if pr.get('_sector') and pr['_sector'] not in sec_map:
            unknown['sectors'].add(pr['_sector'])
        if pr.get('_industry') and pr['_industry'] not in ind_map:
            unknown['industries'].add(pr['_industry'])
        if pr['fincode'] not in co_map:
            unknown['companies'].append(f"{pr['name']} (fincode {pr['fincode']})")
        if a.dump_json:
            os.makedirs(a.dump_json, exist_ok=True)
            with open(os.path.join(a.dump_json, slug(pr['name']) + '.json'), 'w') as fo:
                json.dump(p, fo, default=str)
        print(f"PARSED {os.path.basename(f)}: {pr['name']} [{p['basis']}] "
              f"facts={len(p['facts'])} derived={len(p['derived'])} maxFY={p['max_year']}")

    n_unknown = (len(unknown['line_items']) + len(unknown['metrics'])
                 + len(unknown['sectors']) + len(unknown['industries']))
    print('\n--- DIFF vs dictionary ---' if online else '\n--- OFFLINE (no DB diff) ---')
    print(f"new companies : {unknown['companies'] or 'none'}")
    print(f"new sectors   : {sorted(unknown['sectors']) or 'none'}")
    print(f"new industries: {sorted(unknown['industries']) or 'none'}")
    print(f"new line items: {len(unknown['line_items'])} {sorted(unknown['line_items'])[:20]}")
    print(f"new metrics   : {len(unknown['metrics'])} {sorted(unknown['metrics'])[:20]}")

    if a.dry_run:
        print('\nDRY RUN — nothing written.')
        return
    if n_unknown and not a.approve_new:
        print('\nSTOP: unknown dictionary entries found. Review the list above; '
              're-run with --approve-new once approved.')
        sys.exit(2)

    started = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')  # URL-safe (no '+')

    # register approved dictionary rows (DB triggers raise alerts automatically)
    if unknown['sectors']:
        for x in db.insert('sectors', [{'name': s} for s in sorted(unknown['sectors'])],
                           'name', upsert=True, returning=True):
            sec_map[x['name']] = x['id']
    if unknown['industries']:
        rows = [{'name': s} for s in sorted(unknown['industries'])]
        for x in db.insert('industries', rows, 'name', upsert=True, returning=True):
            ind_map[x['name']] = x['id']
    if unknown['line_items']:
        rows = [{'ace_code': c, 'label': l, 'statement': st,
                 'is_calculated': c.startswith('CALC_'),
                 'first_seen_source': os.path.basename(parsed[0]['file'])}
                for c, (l, st) in unknown['line_items'].items()]
        for x in db.insert('line_items', rows, 'ace_code', upsert=True, returning=True):
            li_map[x['ace_code']] = x
    if unknown['metrics']:
        rows = [{'metric_code': c, 'name': n, 'category': cat}
                for c, (n, cat) in unknown['metrics'].items()]
        for x in db.insert('derived_metrics', rows, 'metric_code', upsert=True, returning=True):
            dm_map[x['metric_code']] = x['id']
    if a.approve_new and n_unknown:
        db.patch('ingestion_alerts',
                 f'status=eq.open&created_at=gte.{started}'
                 '&alert_type=in.(new_line_item,new_sector,new_industry,new_derived_metric)',
                 {'status': 'approved', 'resolved_at': datetime.now(timezone.utc).isoformat()})

    grand = {}
    for p in parsed:
        pr, basis = p['profile'], p['basis']
        batch = db.insert('ingestion_batches',
                          [{'label': f"ace-load {pr['name']}",
                            'source_file': os.path.basename(p['file']),
                            'file_hash': p['hash'], 'company_fincode': pr['fincode'],
                            'status': 'in_progress'}], returning=True)[0]
        co_row = {k: v for k, v in pr.items() if not k.startswith('_')}
        co_row['sector_id'] = sec_map.get(pr.get('_sector'))
        co_row['industry_id'] = ind_map.get(pr.get('_industry'))
        cid = db.insert('companies', [co_row], 'fincode', upsert=True, returning=True)[0]['id']
        co_map[pr['fincode']] = cid

        by_table, stats = {}, {}
        for fct in p['facts']:
            li = li_map.get(fct['ace_code'])
            if not li:
                continue
            table = (FACT_TABLE.get(li['statement'], 'fact_other_annual')
                     if fct['table'] == '__forensic__' else fct['table'])
            if li['statement'] == 'company_master':
                continue
            row = {'company_id': cid, 'line_item_id': li['id'], 'basis': basis,
                   'value': fct['value'], 'batch_id': batch['id'],
                   'fiscal_year': fct['fiscal_year']}
            if table in ('fact_pnl_quarterly', 'fact_balance_sheet_quarterly'):
                row['period_code'] = fct['period_code']
                row['fiscal_quarter'] = fq_of(fct['period_code'])
            by_table.setdefault(table, {})[
                (row['line_item_id'], row.get('period_code'), row['fiscal_year'])] = row
        for table, rows in by_table.items():
            oc = ('company_id,line_item_id,period_code,basis'
                  if 'quarterly' in table else 'company_id,line_item_id,fiscal_year,basis')
            db.insert(table, list(rows.values()), oc, upsert=True)
            stats[table] = len(rows)

        drows = {}
        for d in p['derived']:
            mid = dm_map.get(d['metric_code'])
            if not mid:
                continue
            drows[(mid, d['period_type'], d['fiscal_year'], d['period_code'])] = {
                'company_id': cid, 'metric_id': mid, 'period_type': d['period_type'],
                'fiscal_year': d['fiscal_year'], 'period_code': d['period_code'],
                'basis': basis, 'value': d['value'], 'batch_id': batch['id']}
        if drows:
            db.insert('fact_derived', list(drows.values()),
                      'company_id,metric_id,period_type,basis,fiscal_year,period_code', upsert=True)
            stats['fact_derived'] = len(drows)

        db.patch('ingestion_batches', f"id=eq.{batch['id']}",
                 {'status': 'completed', 'stats': stats,
                  'completed_at': datetime.now(timezone.utc).isoformat()})
        grand[pr['name']] = stats
        print(f"LOADED {pr['name']}: {stats}")

    alerts = db.get_all('ingestion_alerts', 'alert_type,severity,entity,message',
                        f'&status=eq.open&created_at=gte.{started}')
    print('\n=== SUMMARY ===')
    print(json.dumps(grand, indent=1))
    if alerts:
        print(f'\nOPEN ALERTS raised during this load ({len(alerts)}) — review required:')
        for al in alerts[:50]:
            print(f"  [{al['severity']}] {al['alert_type']}: {al['message']}")
    else:
        print('\nNo open alerts raised. Clean load.')


if __name__ == '__main__':
    main()
