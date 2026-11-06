# FastAPI สถิติผู้เข้าชมสวนสัตว์ ปีงบประมาณ 2569

## เริ่มใช้งานบน Windows (PowerShell หรือ CMD)
แตก ZIP แล้วเปิด Terminal ในโฟลเดอร์ zoo_fastapi ที่มี main.py
ต้องมี Python 3.10 ขึ้นไป

```powershell
py -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe -m uvicorn main:app --host 127.0.0.1 --port 8000
```

เปิด http://127.0.0.1:8000/docs
API: http://127.0.0.1:8000/api/zoo-visitors
ตัวอย่าง 1 แถว: http://127.0.0.1:8000/api/zoo-visitors?limit=1
ปิด server ด้วย Ctrl+C

Linux/macOS: ใช้ python3 -m venv .venv และแทน .venv\Scripts\python.exe ด้วย .venv/bin/python

## ที่มาของข้อมูลจริง
- Dataset: https://data.go.th/dataset/zoo-visitors2569
- Resource ID: 0ecc96cf-d914-42a1-b184-dbbd013c3c9c
- ชื่อทรัพยากร: ข้อมูลรายงานสถิติจำนวนผู้เข้าชมสวนสัตว์ อสส กรกฎาคม 2569
- ไฟล์ต้นฉบับ: data/source.xlsx (ดาวน์โหลด 6 พฤศจิกายน 2026)
- URL ดาวน์โหลดอยู่ใน data/resource_metadata.json และ JSON response
- อ่านชีต statistics จำนวน 63 แถวข้อมูล ไม่รวมแถวหัวตาราง
- คงชื่อคอลัมน์ภาษาไทยและค่าตามต้นฉบับ ไม่มีข้อมูลสมมติ
- source_row บอกเลขแถวใน Excel เช่นแถว 2 คอลัมน์ M = 43190
- ช่องว่างคงเป็น null และศูนย์คงเป็น 0 ห้ามตีความช่องว่างเป็นศูนย์
- เป็น snapshot รายงานกรกฎาคม มีคอลัมน์ตลอดปี แต่ไม่ใช่ยอดสมบูรณ์ทั้งปี
- API อ่านไฟล์ที่แนบมา จึงไม่ต้องมี API Key และไม่เรียกเว็บไซต์ใหม่ทุก request
- SHA-256 ของไฟล์อยู่ใน source.file_sha256 เพื่อช่วยตรวจสอบต้นฉบับ

## ทดสอบใน Postman
1. เปิด Postman > Import > เลือก zoo_visitors.postman_collection.json
2. ตั้ง collection variable base_url เป็น http://127.0.0.1:8000
3. เปิดคำขอ GET Zoo Visitors (one row) > Send
4. ตรวจ HTTP 200 OK, JSON fiscal_year = 2569 และ records มีข้อมูลจริง
5. จับภาพให้เห็น Method GET, URL, Status 200 OK และ Body JSON
6. ตรวจ Test Results: ชุดทดสอบสถานะ ปีงบประมาณ Resource ID และค่าจริงต้องผ่าน

ไฟล์ example_response.json เป็น response ที่ได้จากการทดสอบแอปด้วย TestClient
ไม่ใช่หลักฐานภาพ Postman; ต้องเปิด Postman และจับภาพเอง

## URL ที่ส่งผู้สอนได้
127.0.0.1/localhost ใช้ได้เฉพาะเครื่องตนเอง ไม่ใช่ URL สาธารณะ
ใช้โฮสต์/พอร์ต/โดเมนหรือ tunnel ที่ผู้สอนอนุญาตเท่านั้น
เมื่อมี URL จริง ให้นำ URL หลักมาต่อ /api/zoo-visitors และ /docs
สำหรับ server ที่ได้รับอนุญาต สามารถใช้:
python -m uvicorn main:app --host 0.0.0.0 --port <พอร์ตที่อนุญาต>
ต้องตั้ง firewall/reverse proxy ตามนโยบายโฮสต์ และทดสอบจากอีกเครือข่าย
ห้ามใช้พอร์ตของ n8n หรือเปลี่ยนค่าของ server ส่วนกลางโดยพลการ
ยังไม่ได้ deploy หรือสร้าง URL สาธารณะในชุดงานนี้

## เช็กลิสต์ส่งงาน
- URL API สาธารณะที่เข้าถึงได้
- URL /docs สาธารณะ
- ภาพ Postman จากการทดสอบจริง
- example_response.json
- main.py, requirements.txt, data/source.xlsx และ data/resource_metadata.json
- ไม่จำเป็นต้องเชื่อม MySQL สำหรับคะแนนพื้นฐาน
