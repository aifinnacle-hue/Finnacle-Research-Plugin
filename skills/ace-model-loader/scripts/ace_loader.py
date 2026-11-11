#!/usr/bin/env python3
# Curated by Vastav Parikh & Yash Master for Finnacle Shah Classes.
# Intellectual property of Finnacle Institute. © 2026 Finnacle Institute. All rights reserved.
# Keep this notice intact in any copy or modified version of this file.
"""
Ace Model -> SQL builder for the indian-equities-financials Supabase database.

This script never connects to a database and never reads keys or .env files.
It parses Ace Equity model workbooks ("<Company>_Ace Model.xlsx") offline and
writes plain .sql files. Claude runs those files, in order, through the user's
Supabase connector (execute_sql), which carries the user's own sign-in.

Usage:
  python3 ace_loader.py parse FILE1.xlsx [FILE2.xlsx ...] [--folder DIR] --out WORKDIR
      Parse every workbook into WORKDIR/parsed/*.json, write WORKDIR/codes.tsv
      (code -> label, statement) and WORKDIR/01_check.sql, a read-only query
      that lists new dictionary entries, new companies and files already loaded.

  python3 ace_loader.py sql WORKDIR [--approve-new] [--skip-hash H ...] [--chunk-chars N]
      Write the load files:
        10_dictionary.sql        new sectors / industries / line items / metrics
                                 (only with --approve-new, after user approval)
        20_<company>_00_header.sql, _NN_<group>.sql, _99_finish.sql
                                 one batch per workbook, idempotent upserts
        30_alerts.sql            open alerts raised since these files were built
      --skip-hash  skip workbooks whose SHA-256 (or a prefix of it) 01_check.sql
                   reported as already_loaded.

Dependency: openpyxl.
"""
import argparse, glob, hashlib, json, math, os, re, sys
from datetime import datetime, timezone

try:
    import openpyxl
except ImportError:
    sys.exit("Missing dependency: pip install openpyxl")

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
# SQL helpers
# ----------------------------------------------------------------------------

REV_FACT_TABLE = {v: k for k, v in FACT_TABLE.items()}
ANNUAL_TABLES = ('fact_pnl_annual', 'fact_balance_sheet_annual', 'fact_cash_flow_annual')
QUARTERLY_TABLES = ('fact_pnl_quarterly', 'fact_balance_sheet_quarterly')
ALL_FACT_TABLES = ANNUAL_TABLES + ('fact_other_annual',) + QUARTERLY_TABLES + ('fact_derived',)


def q(v):
    """SQL literal."""
    if v is None:
        return 'NULL'
    if isinstance(v, bool):
        return 'TRUE' if v else 'FALSE'
    if isinstance(v, int):
        return str(v)
    if isinstance(v, float):
        return repr(v) if math.isfinite(v) else 'NULL'
    s = str(v).replace('\x00', '')
    return "'" + s.replace("'", "''") + "'"


def values_cte(name, cols, rows):
    if not rows:
        nulls = ', '.join(f'NULL::text AS {c}' for c in cols)
        return f'{name} AS (SELECT {nulls} WHERE FALSE)'
    body = ',\n    '.join('(' + ', '.join(q(x) for x in r) + ')' for r in rows)
    return f'{name}({", ".join(cols)}) AS (VALUES\n    {body})'


def finite(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v)


def load_parsed(workdir):
    out = []
    for f in sorted(glob.glob(os.path.join(workdir, 'parsed', '*.json'))):
        with open(f) as fh:
            out.append(json.load(fh))
    if not out:
        sys.exit(f'No parsed workbooks in {workdir}/parsed — run the "parse" step first.')
    return out


# ----------------------------------------------------------------------------
# step 1: parse
# ----------------------------------------------------------------------------

def cmd_parse(a):
    files = list(a.files)
    if a.folder:
        files += sorted(os.path.join(a.folder, f) for f in os.listdir(a.folder)
                        if f.lower().endswith('.xlsx') and not f.startswith('~'))
    if not files:
        sys.exit('no input files')
    os.makedirs(os.path.join(a.out, 'parsed'), exist_ok=True)

    line_items, metrics, sectors, industries, companies, hashes = {}, {}, set(), set(), {}, []
    for f in files:
        try:
            with open(f, 'rb') as fh:
                h = hashlib.sha256(fh.read()).hexdigest()
            p = parse_workbook(f)
        except Exception as e:  # skip the file, keep going
            print(f'SKIP {os.path.basename(f)}: {e}')
            continue
        p['file'], p['hash'] = os.path.basename(f), h
        pr = p['profile']
        with open(os.path.join(a.out, 'parsed', f"{slug(pr['name'])}_{pr['fincode']}.json"), 'w') as fo:
            json.dump(p, fo, default=str)
        for fact in p['facts']:
            st = ('forensic_annual' if fact['table'] == '__forensic__'
                  else REV_FACT_TABLE[fact['table']])
            line_items.setdefault(fact['ace_code'], (fact['label'], st, p['file']))
        for d in p['derived']:
            metrics.setdefault(d['metric_code'], (d['name'], d['category'], p['file']))
        if pr.get('_sector'):
            sectors.add(pr['_sector'])
        if pr.get('_industry'):
            industries.add(pr['_industry'])
        companies[pr['fincode']] = pr['name']
        hashes.append((h, p['file']))
        print(f"PARSED {p['file']}: {pr['name']} [{p['basis']}] "
              f"facts={len(p['facts'])} derived={len(p['derived'])} maxFY={p['max_year']}")
    if not hashes:
        sys.exit('No workbook could be parsed.')

    with open(os.path.join(a.out, 'codes.tsv'), 'w') as fo:
        fo.write('kind\tcode\tlabel\tstatement_or_category\tfirst_seen_in\n')
        for c, (l, st, src) in sorted(line_items.items()):
            fo.write(f'line_item\t{c}\t{l}\t{st}\t{src}\n')
        for c, (n, cat, src) in sorted(metrics.items()):
            fo.write(f'metric\t{c}\t{n}\t{cat}\t{src}\n')

    ctes = [
        values_cte('li', ['c'], [(c,) for c in sorted(line_items)]),
        values_cte('dm', ['c'], [(c,) for c in sorted(metrics)]),
        values_cte('se', ['c'], [(s,) for s in sorted(sectors)]),
        values_cte('ind', ['c'], [(s,) for s in sorted(industries)]),
        values_cte('co', ['f', 'n'], sorted(companies.items())),
        values_cte('fh', ['h', 'f'], hashes),
    ]
    sql = ('-- Read-only check. Writes nothing.\nWITH ' + ',\n'.join(ctes) + '\n'
           "SELECT 'new_line_item' AS kind, li.c AS key FROM li\n"
           '  WHERE NOT EXISTS (SELECT 1 FROM line_items x WHERE x.ace_code = li.c)\n'
           "UNION ALL SELECT 'new_metric', dm.c FROM dm\n"
           '  WHERE NOT EXISTS (SELECT 1 FROM derived_metrics x WHERE x.metric_code = dm.c)\n'
           "UNION ALL SELECT 'new_sector', se.c FROM se\n"
           '  WHERE NOT EXISTS (SELECT 1 FROM sectors x WHERE x.name = se.c)\n'
           "UNION ALL SELECT 'new_industry', ind.c FROM ind\n"
           '  WHERE NOT EXISTS (SELECT 1 FROM industries x WHERE x.name = ind.c)\n'
           "UNION ALL SELECT 'new_company', co.f::text FROM co\n"
           '  WHERE NOT EXISTS (SELECT 1 FROM companies x WHERE x.fincode = co.f)\n'
           "UNION ALL SELECT 'already_loaded', fh.h FROM fh\n"
           "  WHERE EXISTS (SELECT 1 FROM ingestion_batches x WHERE x.file_hash = fh.h AND x.status = 'completed')\n"
           'ORDER BY 1, 2;\n')
    path = os.path.join(a.out, '01_check.sql')
    with open(path, 'w') as fo:
        fo.write(sql)
    print(f'\nWrote {path} ({len(sql):,} chars). Run it through the Supabase connector and save '
          f'the returned rows as {os.path.join(a.out, "check_result.json")} '
          '(a JSON list of {"kind": ..., "key": ...}; [] if no rows).')


# ----------------------------------------------------------------------------
# step 2: build load SQL
# ----------------------------------------------------------------------------

def chunk_sql(payload, inserts, fincode, label, fhash):
    js = json.dumps(payload, separators=(',', ':'))
    tag, k = '$j$', 0
    while tag in js:
        k += 1
        tag = f'$j{k}$'
    head = (
        "WITH p AS (SELECT " + tag + js + tag + "::jsonb AS j),\n"
        "c AS (SELECT t.col, t.ord FROM p, jsonb_array_elements(p.j->'cols') WITH ORDINALITY AS t(col, ord)),\n"
        "v AS (SELECT r.r->>0 AS code, c.col, r.r->1->(c.ord::int - 1) AS val\n"
        "      FROM p, jsonb_array_elements(p.j->'rows') AS r(r) CROSS JOIN c),\n"
        f"co AS (SELECT id FROM companies WHERE fincode = {q(fincode)}),\n"
        f"b AS (SELECT id FROM ingestion_batches WHERE label = {q(label)} AND file_hash = {q(fhash)})"
    )
    parts = [f',\nins{i} AS (\n{ins}\n  RETURNING 1)' for i, ins in enumerate(inserts)]
    tail = '\nSELECT ' + ' + '.join(f'(SELECT count(*) FROM ins{i})' for i in range(len(inserts))) \
           + ' AS rows_written;\n'
    return head + ''.join(parts) + tail


def fact_insert(table, basis, kind, stmt_filter=None):
    num = "(v.val #>> '{}')::numeric"
    where = "jsonb_typeof(v.val) = 'number' AND li.statement <> 'company_master'"
    if stmt_filter:
        where += ' AND ' + stmt_filter
    if kind == 'annual':
        return (f'  INSERT INTO {table} (company_id, line_item_id, basis, value, batch_id, fiscal_year)\n'
                f"  SELECT co.id, li.id, {q(basis)}, {num}, b.id, (v.col->>0)::int\n"
                '  FROM v JOIN line_items li ON li.ace_code = v.code CROSS JOIN co CROSS JOIN b\n'
                f'  WHERE {where}\n'
                '  ON CONFLICT (company_id, line_item_id, fiscal_year, basis)\n'
                '  DO UPDATE SET value = EXCLUDED.value, batch_id = EXCLUDED.batch_id')
    return (f'  INSERT INTO {table} (company_id, line_item_id, basis, value, batch_id,'
            ' period_code, fiscal_year, fiscal_quarter)\n'
            f"  SELECT co.id, li.id, {q(basis)}, {num}, b.id,"
            ' (v.col->>0)::int, (v.col->>1)::int, (v.col->>2)::int\n'
            '  FROM v JOIN line_items li ON li.ace_code = v.code CROSS JOIN co CROSS JOIN b\n'
            f'  WHERE {where}\n'
            '  ON CONFLICT (company_id, line_item_id, period_code, basis)\n'
            '  DO UPDATE SET value = EXCLUDED.value, batch_id = EXCLUDED.batch_id')


def derived_insert(basis, ptype):
    return ('  INSERT INTO fact_derived (company_id, metric_id, period_type, fiscal_year,'
            ' period_code, basis, value, batch_id)\n'
            f"  SELECT co.id, m.id, {q(ptype)}, (v.col->>0)::int, (v.col->>1)::int, {q(basis)},"
            " (v.val #>> '{}')::numeric, b.id\n"
            '  FROM v JOIN derived_metrics m ON m.metric_code = v.code CROSS JOIN co CROSS JOIN b\n'
            "  WHERE jsonb_typeof(v.val) = 'number'\n"
            '  ON CONFLICT (company_id, metric_id, period_type, basis, fiscal_year, period_code)\n'
            '  DO UPDATE SET value = EXCLUDED.value, batch_id = EXCLUDED.batch_id')


def chunks(series, limit):
    """series: {code: {colkey(tuple): value}} -> payloads under ~limit chars."""
    cur, size = [], 0
    for code in sorted(series):
        vals = {k: v for k, v in series[code].items() if finite(v)}
        if not vals:
            continue
        est = len(code) + 12 * len(vals) + 10
        if cur and size + est > limit:
            yield cur
            cur, size = [], 0
        cur.append((code, vals))
        size += est
    if cur:
        yield cur


def payload_of(rows):
    cols = sorted({k for _, vals in rows for k in vals})
    idx = {k: i for i, k in enumerate(cols)}
    out = []
    for code, vals in rows:
        arr = [None] * len(cols)
        for k, v in vals.items():
            arr[idx[k]] = v
        out.append([code, arr])
    return {'cols': [list(k) for k in cols], 'rows': out}


def cmd_sql(a):
    parsed = load_parsed(a.workdir)
    res_path = os.path.join(a.workdir, 'check_result.json')
    if not os.path.exists(res_path):
        sys.exit(f'{res_path} not found. Run 01_check.sql through the Supabase connector first '
                 'and save its rows there.')
    with open(res_path) as fh:
        check = json.load(fh)
    if isinstance(check, dict):
        check = check.get('rows') or check.get('result') or []
    new = {}
    for r in check:
        new.setdefault(r['kind'], set()).add(str(r['key']))
    dict_kinds = ('new_line_item', 'new_metric', 'new_sector', 'new_industry')
    n_new = sum(len(new.get(k, ())) for k in dict_kinds)
    if n_new and not a.approve_new:
        print('STOP: new dictionary entries found (see check_result.json). Show them to the '
              'user; after explicit approval re-run with --approve-new.')
        sys.exit(2)

    loaded = new.get('already_loaded', set())
    skip = set(a.skip_hash or [])
    gen_ts = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S+00')
    tag = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    for old in glob.glob(os.path.join(a.workdir, '[123]*.sql')):
        os.remove(old)
    written = []

    def write(name, text):
        path = os.path.join(a.workdir, name)
        with open(path, 'w') as fo:
            fo.write(text)
        written.append((name, len(text)))

    # dictionary rows (only those 01_check.sql reported as new)
    if n_new:
        li_src, dm_src = {}, {}
        for p in parsed:
            for fact in p['facts']:
                st = ('forensic_annual' if fact['table'] == '__forensic__'
                      else REV_FACT_TABLE[fact['table']])
                li_src.setdefault(fact['ace_code'], (fact['label'], st, p['file']))
            for d in p['derived']:
                dm_src.setdefault(d['metric_code'], (d['name'], d['category']))
        stmts = [f'-- Approved new dictionary entries. Built {gen_ts}.']
        for kind, table in (('new_sector', 'sectors'), ('new_industry', 'industries')):
            names = sorted(new.get(kind, ()))
            if names:
                stmts.append(f'INSERT INTO {table} (name) VALUES '
                             + ', '.join(f'({q(n)})' for n in names)
                             + ' ON CONFLICT (name) DO NOTHING;')
        rows = [(c, *li_src[c][:2], c.startswith('CALC_'), li_src[c][2])
                for c in sorted(new.get('new_line_item', ())) if c in li_src]
        if rows:
            stmts.append('INSERT INTO line_items (ace_code, label, statement, is_calculated, '
                         'first_seen_source) VALUES\n  '
                         + ',\n  '.join('(' + ', '.join(q(x) for x in r) + ')' for r in rows)
                         + '\nON CONFLICT (ace_code) DO NOTHING;')
        rows = [(c, *dm_src[c]) for c in sorted(new.get('new_metric', ())) if c in dm_src]
        if rows:
            stmts.append('INSERT INTO derived_metrics (metric_code, name, category) VALUES\n  '
                         + ',\n  '.join('(' + ', '.join(q(x) for x in r) + ')' for r in rows)
                         + '\nON CONFLICT (metric_code) DO NOTHING;')
        stmts.append("UPDATE ingestion_alerts SET status = 'approved', resolved_at = now()\n"
                     f"WHERE status = 'open' AND created_at >= {q(gen_ts)}::timestamptz\n"
                     "  AND alert_type IN ('new_line_item', 'new_sector', 'new_industry', "
                     "'new_derived_metric');")
        write('10_dictionary.sql', '\n'.join(stmts) + '\n')

    for p in parsed:
        h = p['hash']
        if h in loaded or any(h.startswith(s) for s in skip if len(s) >= 8):
            print(f"SKIP (already loaded): {p['file']}")
            continue
        pr, basis = p['profile'], p['basis']
        fincode = pr['fincode']
        label = f"ace-load {pr['name']} {tag}"
        base = f"20_{slug(pr['name'])[:40]}_{fincode}"

        co_cols = [k for k in pr if not k.startswith('_')]
        sec = f"(SELECT id FROM sectors WHERE name = {q(pr['_sector'])})" if pr.get('_sector') else 'NULL'
        ind = (f"(SELECT id FROM industries WHERE name = {q(pr['_industry'])})"
               if pr.get('_industry') else 'NULL')
        header = (
            f"-- {p['file']} ({h[:12]}). Built {gen_ts}.\n"
            'INSERT INTO ingestion_batches (label, source_file, file_hash, company_fincode, status)\n'
            f"SELECT {q(label)}, {q(p['file'])}, {q(h)}, {q(fincode)}, 'in_progress'\n"
            f'WHERE NOT EXISTS (SELECT 1 FROM ingestion_batches WHERE label = {q(label)}'
            f' AND file_hash = {q(h)});\n'
            f"INSERT INTO companies ({', '.join(co_cols)}, sector_id, industry_id)\n"
            f"VALUES ({', '.join(q(pr[k]) for k in co_cols)}, {sec}, {ind})\n"
            'ON CONFLICT (fincode) DO UPDATE SET '
            + ', '.join(f'{k} = EXCLUDED.{k}' for k in co_cols + ['sector_id', 'industry_id'])
            + ';\n')
        write(f'{base}_00_header.sql', header)

        # group facts; forensic values win over the statement-sheet value for the same key
        forensic, annual, quarterly = {}, {t: {} for t in ANNUAL_TABLES}, {t: {} for t in QUARTERLY_TABLES}
        for fct in p['facts']:
            if fct['table'] == '__forensic__':
                forensic.setdefault(fct['ace_code'], {})[(fct['fiscal_year'],)] = fct['value']
        for fct in p['facts']:
            t, c = fct['table'], fct['ace_code']
            if t in annual:
                if (fct['fiscal_year'],) in forensic.get(c, {}):
                    continue
                annual[t].setdefault(c, {})[(fct['fiscal_year'],)] = fct['value']
            elif t in quarterly:
                pc = fct['period_code']
                quarterly[t].setdefault(c, {})[(pc, fct['fiscal_year'], fq_of(pc))] = fct['value']
        derived = {}
        for d in p['derived']:
            derived.setdefault(d['period_type'], {}).setdefault(d['metric_code'], {})[
                (d['fiscal_year'], d['period_code'])] = d['value']

        n = 0
        groups = [(t, annual[t], [fact_insert(t, basis, 'annual')]) for t in ANNUAL_TABLES]
        groups += [(t, quarterly[t], [fact_insert(t, basis, 'quarterly')]) for t in QUARTERLY_TABLES]
        groups.append(('forensic', forensic, [
            fact_insert('fact_pnl_annual', basis, 'annual', "li.statement = 'pnl_annual'"),
            fact_insert('fact_balance_sheet_annual', basis, 'annual',
                        "li.statement = 'balance_sheet_annual'"),
            fact_insert('fact_cash_flow_annual', basis, 'annual', "li.statement = 'cash_flow_annual'"),
            fact_insert('fact_other_annual', basis, 'annual',
                        "li.statement NOT IN ('pnl_annual', 'balance_sheet_annual', "
                        "'cash_flow_annual')")]))
        for ptype in sorted(derived):
            groups.append((f'derived_{ptype}', derived[ptype], [derived_insert(basis, ptype)]))
        for gname, series, inserts in groups:
            for rows in chunks(series, a.chunk_chars):
                n += 1
                write(f'{base}_{n:02d}_{gname}.sql',
                      f"-- {pr['name']}: {gname}, {len(rows)} codes\n"
                      + chunk_sql(payload_of(rows), inserts, fincode, label, h))

        counts = ',\n    '.join(f"({q(t)}, (SELECT count(*) FROM {t} f WHERE f.batch_id = b.id))"
                                for t in ALL_FACT_TABLES)
        write(f'{base}_99_finish.sql',
              "UPDATE ingestion_batches b SET status = 'completed', completed_at = now(),\n"
              '  stats = COALESCE((SELECT jsonb_object_agg(s.t, s.n) FROM (VALUES\n    '
              + counts + "\n  ) AS s(t, n) WHERE s.n > 0), '{}'::jsonb)\n"
              f'WHERE b.label = {q(label)} AND b.file_hash = {q(h)}\n'
              'RETURNING b.label, b.stats;\n')

    write('30_alerts.sql',
          'SELECT alert_type, severity, entity, message, created_at FROM ingestion_alerts\n'
          f"WHERE status = 'open' AND created_at >= {q(gen_ts)}::timestamptz\n"
          'ORDER BY created_at LIMIT 100;\n')

    with open(os.path.join(a.workdir, 'RUN_ORDER.txt'), 'w') as fo:
        for name, size in written:
            fo.write(f'{name}\t{size}\n')
    print('Run these files through the Supabase connector (execute_sql), in this order:')
    for name, size in written:
        print(f'  {name}  ({size:,} chars)')


def main():
    ap = argparse.ArgumentParser(description='Ace Model -> SQL builder (no DB connection).')
    sub = ap.add_subparsers(dest='cmd', required=True)
    p1 = sub.add_parser('parse')
    p1.add_argument('files', nargs='*')
    p1.add_argument('--folder')
    p1.add_argument('--out', required=True)
    p2 = sub.add_parser('sql')
    p2.add_argument('workdir')
    p2.add_argument('--approve-new', action='store_true')
    p2.add_argument('--skip-hash', nargs='*')
    p2.add_argument('--chunk-chars', type=int, default=30000)
    a = ap.parse_args()
    cmd_parse(a) if a.cmd == 'parse' else cmd_sql(a)


if __name__ == '__main__':
    main()
