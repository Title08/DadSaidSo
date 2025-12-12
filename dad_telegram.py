import telebot
import os
import dad_logic
import dad_printer
from dotenv import load_dotenv

# โหลดค่าจากไฟล์ .env
load_dotenv()

# --- 🔑 ใส่ TOKEN ที่ได้จาก BotFather ตรงนี้ ---
# ดึง Token จาก Environment Variable
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# สร้างบอท
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# สร้างโฟลเดอร์เก็บไฟล์ถ้ายังไม่มี
OUTPUT_FOLDER = 'Output_PDF_Telegram'
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

print("🚀 DadSaidSo Telegram Bot เริ่มทำงานแล้ว... (กด Ctrl+C เพื่อหยุด)")

# --- ส่วนต้อนรับ (เมื่อกด Start) ---
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "สวัสดีครับพ่อ! \nพิมพ์รายละเอียดงานมาได้เลยครับ \nเช่น 'ม 2 รัตนาทิเบต ค่ายหัตวุฒิ 8 คัน คันละ 9000 28-29 มค 69'")

# --- ส่วนทำงานหลัก (เมื่อมีข้อความเข้า) ---
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_text = message.text
    chat_id = message.chat.id
    
    print(f"📩 ข้อความเข้า: {user_text}")

    # 1. ส่งข้อความบอกว่ากำลังทำ (เพื่อให้รู้ว่าบอทไม่ตาย)
    loading_msg = bot.send_message(chat_id, "⏳ กำลังประมวลผลและสร้างเอกสารครับ รอสักครู่...")

    try:
        # 2. ให้ AI คิด (เรียกใช้ dad_logic)
        quotation_data = dad_logic.extract_data_from_text(user_text)
        
        if quotation_data:
            # 3. ตั้งชื่อไฟล์
            ai_filename = quotation_data.get('suggested_filename', 'quotation.pdf')
            # ล้างชื่อไฟล์ให้ปลอดภัย
            safe_filename = ai_filename.replace(" ", "_").replace("/", "-")
            if not safe_filename.endswith(".pdf"): safe_filename += ".pdf"
            
            # Path เต็ม
            save_path = os.path.join(OUTPUT_FOLDER, safe_filename)
            
            # 4. สร้าง PDF (เรียกใช้ dad_printer)
            dad_printer.create_pdf(quotation_data, save_path)
            print(f"✅ สร้างไฟล์เสร็จ: {save_path}")

            # 5. ส่งไฟล์ PDF กลับไปในแชท (พระเอกของเรา!)
            with open(save_path, 'rb') as pdf_file:
                bot.send_document(
                    chat_id, 
                    pdf_file, 
                    caption=f"✅ เรียบร้อยครับ!\nลูกค้า: {quotation_data.get('customer_name')}\nยอดรวม: {quotation_data.get('total_price'):,} บาท",
                    reply_to_message_id=message.message_id
                )
            
            # ลบข้อความ "กำลังประมวลผล" ออก เพื่อความเนียน
            bot.delete_message(chat_id, loading_msg.message_id)
            
        else:
            bot.edit_message_text("❌ AI งงครับพ่อ ขอข้อมูลใหม่อีกทีครับ", chat_id, loading_msg.message_id)

    except Exception as e:
        print(f"❌ Error: {e}")
        bot.edit_message_text(f"เกิดข้อผิดพลาด: {str(e)}", chat_id, loading_msg.message_id)

# สั่งให้บอททำงานตลอดเวลา (Polling)
bot.infinity_polling()