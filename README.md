# SheetStarted

เครื่องมือเริ่มต้นสำหรับสร้างใบงานจากไฟล์ PDF หรือรูปภาพ แล้วส่งออกเป็นไฟล์ Word (.docx)
เพื่อช่วยจัดโครงสร้างเนื้อหาให้เหมาะกับบทเรียนในประเทศไทย เช่น คณิตศาสตร์ วิทยาศาสตร์
ภาษาอังกฤษ ภาษาไทย สังคมศึกษา เคมี ฟิสิกส์ และชีววิทยา

## ความสามารถหลัก
- อ่านไฟล์ PDF หรือรูปภาพจากเครื่อง/URL
- ใช้ OCR สำหรับรูปภาพ (รองรับภาษาไทยและอังกฤษ)
- จัดโครงสร้างเป็นหัวข้อใบงาน เช่น สารบรรณ เนื้อหาสรุป แบบฝึกหัด
- รองรับเทมเพลตรายวิชาและกำหนดระดับความยาก/จำนวนแบบฝึกหัด
- ใส่มาตรฐาน/ตัวชี้วัด และแท็กประกอบใบงาน
- แยกใบงานตามสารบัญและรวมไฟล์เป็นชุด (zip)
- ส่งออกเป็นไฟล์ Word
- มีเว็บแอปสำหรับอัปโหลดไฟล์และดาวน์โหลดใบงานทันที

## การติดตั้ง

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

> หมายเหตุ: ต้องติดตั้ง Tesseract OCR และภาษาไทย (`tha`) ในระบบด้วย

## ตัวอย่างการใช้งาน CLI

```bash
python -m sheetstarted.cli \
  --subject "วิทยาศาสตร์" \
  --lesson-title "ระบบสุริยะ" \
  --grade "มัธยมศึกษาปีที่ 1" \
  --difficulty "ปานกลาง" \
  --exercise-count 5 \
  --standard "สาระที่ 2" \
  --indicator "ว 2.1" \
  --tags "ระบบสุริยะ" "ดาวเคราะห์" \
  ./samples/solar.pdf
```

หรือใช้ URL

```bash
python -m sheetstarted.cli \
  --subject "ภาษาอังกฤษ" \
  --lesson-title "Present Simple" \
  https://example.com/book/page1.png
```

แยกใบงานตามสารบัญ และรวมเป็นชุด zip

```bash
python -m sheetstarted.cli \
  --subject "สังคมศึกษา" \
  --lesson-title "ประวัติศาสตร์" \
  --split-by-toc \
  --bundle-zip \
  --output output/history \
  ./samples/history.pdf
```

ผลลัพธ์จะถูกสร้างไว้ที่ `output/worksheet.docx` (ค่าเริ่มต้น)

## การใช้ LLM เพื่อสรุปเนื้อหา
ตั้งค่า `LLM_ENDPOINT` และ (ถ้ามี) `LLM_API_KEY` ก่อนใช้งาน

```bash
export LLM_ENDPOINT="https://your-llm-endpoint.example.com/summarize"
python -m sheetstarted.cli \
  --subject "ชีววิทยา" \
  --lesson-title "เซลล์" \
  --llm-summary \
  ./samples/biology.pdf
```

## เว็บแอป

```bash
python -m sheetstarted.webapp
```

จากนั้นเปิดเบราว์เซอร์ที่ `http://localhost:8000`

## แนวทางการต่อยอด
- เพิ่มโมดูลสรุปเนื้อหาด้วย LLM พร้อมระบบเลือกโมเดล
- เพิ่มเทมเพลตใบงานตามรายวิชาและระดับชั้น
- แยกหัวข้ออัตโนมัติจากสารบัญหนังสือได้แม่นยำขึ้นด้วยการจับคู่หน้า
