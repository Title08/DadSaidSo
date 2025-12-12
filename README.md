# DadSaidSo v0.2 (GitHub Edition)

โปรแกรมสร้างใบเสนอราคาอัตโนมัติด้วย AI (Gemini) สำหรับธุรกิจรถเช่าเหมา
รองรับการทำงานผ่าน Console และ Telegram Bot

## 📋 ความสามารถ
- แปลงข้อความภาษาธรรมชาติ (เช่น "ไปเชียงใหม่ 3 วัน 2 คัน") เป็นใบเสนอราคา PDF
- ดึงข้อมูลสถานที่และที่อยู่ลูกค้าอัตโนมัติด้วย AI
- คำนวณราคารวมและแปลงเป็นตัวอักษรบาทไทย
- สร้างไฟล์ PDF สวยงามพร้อมส่ง

## 🛠️ การติดตั้ง

1. **Clone โปรเจค**
   ```bash
   git clone https://github.com/yourusername/DadSaidSo.git
   cd DadSaidSo
   ```

2. **ติดตั้ง Library ที่จำเป็น**
   ```bash
   pip install -r requirements.txt
   ```

3. **ตั้งค่า Environment Variables**
   สร้างไฟล์ `.env` ในโฟลเดอร์โปรเจค และใส่ค่า Key ต่างๆ ดังนี้:

   ```env
   # Google Gemini API Key (ขอฟรีที่ aistudio.google.com)
   GEMINI_API_KEY=your_gemini_api_key_here

   # Telegram Bot Token (ถ้าใช้ Telegram)
   TELEGRAM_TOKEN=your_telegram_bot_token_here
   ```

   *หมายเหตุ: โค้ดรองรับการอ่านค่าจาก Environment Variable ของระบบ หรือจะใช้ library `python-dotenv` เพื่ออ่านจากไฟล์ .env ก็ได้ (ในโค้ดตัวอย่างนี้ใช้ `os.getenv` ซึ่งรองรับทั้งคู่)*

## 🚀 วิธีใช้งาน

### 1. ใช้งานผ่าน Console (ทดสอบ)
รันไฟล์ `dad_app.py` เพื่อทดสอบการสร้าง PDF จากข้อความใน Terminal
```bash
python dad_app.py
```

### 2. ใช้งานผ่าน Telegram Bot
รันไฟล์ `dad_telegram.py`
```bash
python dad_telegram.py
```
จากนั้นทักแชทไปที่บอทของคุณแล้วพิมพ์รายละเอียดงานได้เลย

## 📂 โครงสร้างไฟล์
- `dad_logic.py`: สมองหลัก เชื่อมต่อ AI และประมวลผลข้อความ
- `dad_printer.py`: ตัวจัดการเอกสาร สร้างไฟล์ PDF
- `dad_app.py`: โปรแกรมหลักสำหรับรันในเครื่อง
- `dad_telegram.py`: บอทสำหรับ Telegram
- `fonts/`: โฟลเดอร์เก็บฟอนต์ภาษาไทย (TH Sarabun New)

## ⚠️ ข้อควรระวัง
- อย่าอัปโหลดไฟล์ `.env` หรือไฟล์ที่มี API Key ขึ้น GitHub
- ตรวจสอบโควต้าการใช้งาน API ของ Google Gemini

---
พัฒนาโดย [ชื่อของคุณ]
