import google.generativeai as genai
import json
import re
import os
from datetime import datetime
from dotenv import load_dotenv

# โหลดค่าจากไฟล์ .env
load_dotenv()

# --- 🔑 GEMINI API CONFIGURATION ---
# ดึง Key จาก Environment Variable เพื่อความปลอดภัย
API_KEY = os.getenv("GEMINI_API_KEY") 

def get_current_date_context():
    now = datetime.now()
    year_th = now.year + 543
    return f"วันนี้คือวันที่: {now.day}/{now.month}/{year_th} (พ.ศ.)"

def extract_data_from_text(user_input):
    if "YOUR_GEMINI_API_KEY" in API_KEY:
        print("❌ ลืมใส่ GEMINI API KEY ในไฟล์ dad_logic.py ครับ!")
        return None

    print(f"   ... กำลังส่งข้อมูลไปให้ AI (Gemini Pro) คิดและค้นหาข้อมูล...")
    
    try:
        # 1. ตั้งค่า
        genai.configure(api_key=API_KEY)
        
        # *** ใช้รุ่นที่เสถียรใน SDK ปัจจุบัน ***
        model = genai.GenerativeModel('gemini-flash-latest')

        # 2. Prompt (ชุดคำสั่งเลขาอัจฉริยะ)
        prompt = f"""
        You are an expert secretary for a Thai bus rental business.
        {get_current_date_context()}
        
        Task: Extract data from user input and fill in missing info using your internal Knowledge Base.
        
        **CRITICAL RULES:**
        1. **Customer:** - Convert nickname to OFFICIAL name (e.g. "รร.รัตนาทิเบต" -> "ผู้อำนวยการ โรงเรียนรัตนาธิเบศร์").
           - **MUST FIND ADDRESS:** Find the official address of that school/company and put it in "customer_address".
        2. **Destination:** - Convert to OFFICIAL name.
           - **MUST FIND ADDRESS:** Find the location details (District, Province) and put it in "destination_address".
        3. **Date:** Convert informal date to "D Month YYYY" (Thai). "69" = 2569 BE.
        4. **Project Name:** Create a formal project title based on context (e.g. "ม 2" -> "โครงการทัศนศึกษา... มัธยมศึกษาปีที่ 2").
        5. **Filename:** Generate a safe filename (English/Thai alphanumeric), ending in .pdf. Example: "Quotation_SchoolName_28Jan69.pdf".
        6. **Output:** Return ONLY raw JSON object. No Markdown.

        **User Input:** "{user_input}"
        
        **JSON Schema:**
        {{
          "customer_name": "string",
          "customer_address": "string",
          "project_name": "string",
          "destination": "string",
          "destination_address": "string",
          "date_start": "string",
          "date_end": "string",
          "item_description": "string (Default: ค่าจ้างเหมารถบัส พร้อมน้ำมันเชื้อเพลิง)",
          "quantity": int,
          "unit_price": int,
          "total_price": int,
          "remark": "string (Default: ราคานี้ไม่รวมค่าทางด่วน)",
          "suggested_filename": "string"
        }}
        """

        # 3. เรียกใช้งาน
        try:
            response = model.generate_content(prompt)
        except Exception as e:
            # Fallback: ใช้ chat API ซึ่งมักรองรับกว้างกว่า
            chat = model.start_chat()
            response = chat.send_message(prompt)
        
        # 4. แกะ JSON
        if not response.text:
            print("❌ AI ตอบกลับมาว่างเปล่า (อาจจะติด Safety Filter)")
            return None
            
        clean_text = re.sub(r'```json|```', '', response.text).strip()
        data = json.loads(clean_text)
        
        # 5. คำนวณราคา
        qty = data.get('quantity', 0) or 0
        price = data.get('unit_price', 0) or 0
        data['quantity'] = qty
        data['unit_price'] = price
        data['total_price'] = qty * price
        
        return data

    except Exception as e:
        print(f"❌ AI Error: {e}")
        return None