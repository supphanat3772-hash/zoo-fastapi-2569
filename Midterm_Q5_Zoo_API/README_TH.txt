ข้อ 5 — พัฒนา RESTful API ด้วย Python และ FastAPI
ข้อมูลรายงานสถิติจำนวนผู้เข้าชมสวนสัตว์ ปีงบประมาณ 2569

1. URL สำหรับตรวจงาน
Swagger UI: https://zoo-fastapi-2569.vercel.app/docs
API: https://zoo-fastapi-2569.vercel.app/api/zoo-visitors
ทดสอบ 1 รายการ: https://zoo-fastapi-2569.vercel.app/api/zoo-visitors?limit=1
Deploy บน Vercel จึงไม่ต้องเปิดเครื่องผู้พัฒนาหรือ Tunnel

2. แหล่งข้อมูลจริง
หน่วยงาน: องค์การสวนสัตว์แห่งประเทศไทย ในพระบรมราชูปถัมภ์
Dataset: https://data.go.th/dataset/zoo-visitors2569
Resource ID: 0ecc96cf-d914-42a1-b184-dbbd013c3c9c
ชื่อทรัพยากร: ข้อมูลรายงานสถิติจำนวนผู้เข้าชมสวนสัตว์ อสส กรกฎาคม 2569
ไฟล์: source_code/data/source.xlsx
ชีต: statistics
Metadata และ URL ดาวน์โหลดต้นฉบับ: source_code/data/resource_metadata.json
อ่านข้อมูลจากไฟล์ XLSX จริงด้วย openpyxl ไม่สร้างตัวเลขสมมติ

3. การทำงาน
GET /api/zoo-visitors คืน JSON ระบุ source, fiscal_year และ records
มีข้อมูลทั้งหมด 63 แถว (ไม่รวมหัวตาราง) และรองรับ limit/offset
ชื่อคอลัมน์และค่าคงตามต้นฉบับ ช่องว่างเป็น null ศูนย์คงเป็น 0
source_row ระบุเลขแถวใน Excel เพื่อสอบทานตัวเลข
ตัวอย่างแถว 2: ผู้ใหญ่ สวนสัตว์เปิดเขาเขียว กรกฎาคม 2569 = 43,190 คน (เซลล์ M2)
รายงานฉบับกรกฎาคมมีคอลัมน์ทั้งปี แต่ไม่ใช่ยอดสมบูรณ์ทั้งปี
GET /docs แสดง Swagger UI สำหรับทดสอบ API

4. หลักฐานและไฟล์แนบ
source_code/ — main.py, requirements.txt และ data/ สำหรับรันแอป
example_response.json — JSON ที่รับจาก URL Vercel จริงเมื่อจัดชุดส่งงาน
zoo_visitors.postman_collection.json — Import เข้า Postman แล้ว Send ได้ทันที
SUBMISSION_URLS.txt — URL สำหรับคัดลอกกรอกแบบส่งงาน
evidence/ — ภาพจริงที่ผู้พัฒนาส่งระหว่างทดสอบ (ไม่ได้สร้างภาพผลทดสอบจำลอง)
ภาพ Swagger ยืนยัน HTTP 200 และข้อมูล 63 แถว
ภาพ Postman ยืนยัน GET ผ่าน URL Vercel, 200 OK และ JSON Response
422 ในส่วนคำอธิบายของ Swagger เป็น schema ของกรณี validation ไม่ใช่ผลผิดพลาดของ request ที่ผ่านแล้ว

5. วิธีรันในเครื่อง Windows (Python 3.13)
เปิด Terminal ภายใน source_code แล้วรันทีละคำสั่ง:
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m uvicorn main:app --host 127.0.0.1 --port 8000
เปิด http://127.0.0.1:8000/docs

6. การ Deploy ที่ใช้งานสำเร็จ
Provider: Vercel / แผน Hobby / Application Preset: FastAPI
Repository: zoo-fastapi-2569 / Branch: main / Root Directory: zoo_fastapi
ใช้การติดตั้ง dependencies จาก requirements.txt โดยระบบ
ไม่ต้องใช้ API Key หรือ MySQL สำหรับการอ่านไฟล์ในงานนี้
เก็บไฟล์ Excel และ resource_metadata.json ไว้ใน data/ ข้าง main.py เสมอ

วันที่จัดชุดส่งงาน: 6 พฤศจิกายน 2569
