"""Read the authentic Data.go.th XLSX; never substitute invented statistics."""
from contextlib import asynccontextmanager
from pathlib import Path
import hashlib
import json
from fastapi import FastAPI, Query
from openpyxl import load_workbook

BASE = Path(__file__).resolve().parent

def load_data():
    path = BASE / 'data' / 'source.xlsx'
    meta = json.loads((BASE / 'data' / 'resource_metadata.json').read_text(encoding='utf-8'))
    book = load_workbook(path, read_only=True, data_only=True)
    try:
        sheet = book['statistics']
        headers = [c.value for c in next(sheet.iter_rows())]
        records = []
        for row_number, values in enumerate(sheet.iter_rows(min_row=2, values_only=True), 2):
            if not values[0] or not values[1]:
                continue
            record = {str(h): v for h, v in zip(headers, values) if h is not None}
            if int(record['ปีงบประมาณ']) != 2569:
                raise ValueError('Unexpected fiscal year in source workbook')
            records.append({'source_row': row_number, **record})
        if not records:
            raise ValueError('Source contains no statistics')
        return records, {
            'organization': 'องค์การสวนสัตว์แห่งประเทศไทย ในพระบรมราชูปถัมภ์',
            'dataset': 'zoo-visitors2569',
            'dataset_url': 'https://data.go.th/dataset/zoo-visitors2569',
            'resource_id': meta['id'], 'resource_name': meta['name'],
            'resource_url': meta['url'], 'format': 'XLSX',
            'sheet': 'statistics', 'file_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
            'note': 'อ่านไฟล์ต้นฉบับที่แนบมา คงชื่อคอลัมน์และค่าตามต้นฉบับ; ช่องว่างเป็น null ไม่ใช่ศูนย์; ไม่ใช่ยอดรวมทั้งปี',
        }
    finally:
        book.close()

@asynccontextmanager
async def lifespan(app):
    app.state.records, app.state.source = load_data()
    yield

app = FastAPI(title='Zoo Visitors API — FY 2569', version='1.0.0', lifespan=lifespan)

@app.get('/')
def root():
    return {'api': '/api/zoo-visitors', 'docs': '/docs'}

@app.get('/api/zoo-visitors', summary='สถิติจริงจากไฟล์ XLSX ของ Data.go.th')
def zoo_visitors(limit: int = Query(100, ge=1, le=1000), offset: int = Query(0, ge=0)):
    rows = app.state.records
    page = rows[offset:offset + limit]
    return {'source': app.state.source, 'fiscal_year': 2569,
            'total': len(rows), 'count': len(page), 'offset': offset, 'records': page}
