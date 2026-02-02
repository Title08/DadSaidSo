"""
DadSaidSo Telegram Bot - Automated Quotation Generator
Powered by Groq Cloud API (Llama models)
"""

import os
import telebot
from dotenv import load_dotenv
import dad_logic
import dad_printer


# ==========================================
# CONFIGURATION
# ==========================================

# Load environment variables
load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
BOT_PASSWORD = os.getenv("BOT_PASSWORD", "dad2514")
OUTPUT_FOLDER = "Output_PDF_Telegram"

# Validate configuration
if not TELEGRAM_TOKEN:
    raise ValueError("❌ TELEGRAM_TOKEN not found in .env file")

# Initialize bot
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Authentication system - stores chat_id of logged-in users
authorized_users = set()

# Create output folder if it doesn't exist
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

print("🚀 DadSaidSo Telegram Bot เริ่มทำงานแล้ว...")
print(f"📂 Output folder: {OUTPUT_FOLDER}")
print("⚙️  Press Ctrl+C to stop\n")


# ==========================================
# HELPER FUNCTIONS
# ==========================================

def is_authenticated(chat_id):
    """Check if user is logged in"""
    return chat_id in authorized_users


def sanitize_filename(filename):
    """Clean and validate filename"""
    safe_name = filename.replace(" ", "_").replace("/", "-").replace("\\", "-")
    if not safe_name.endswith(".pdf"):
        safe_name += ".pdf"
    return safe_name


def send_login_prompt(chat_id):
    """Send login instruction message"""
    return bot.send_message(
        chat_id,
        "🔒 กรุณาล็อกอินก่อนใช้งาน\n\n"
        "พิมพ์: /login [รหัสผ่าน]\n"
        "ตัวอย่าง: /login dad2026"
    )


# ==========================================
# COMMAND HANDLERS
# ==========================================

@bot.message_handler(commands=['start', 'help'])
def command_start(message):
    """Handle /start and /help commands"""
    chat_id = message.chat.id
    
    if is_authenticated(chat_id):
        bot.reply_to(
            message,
            "สวัสดีครับพ่อ! 👋\n\n"
            "📋 วิธีใช้งาน:\n"
            "พิมพ์รายละเอียดงานมาได้เลยครับ\n\n"
            "💡 ตัวอย่าง:\n"
            "'ม 2 รัตนาทิเบต ค่ายหัตวุฒิ 8 คัน คันละ 9000 28-29 มค 69'\n\n"
            "🔐 คำสั่ง:\n"
            "/logout - ออกจากระบบ\n"
            "/help - แสดงคำสั่ง"
        )
    else:
        send_login_prompt(chat_id)


@bot.message_handler(commands=['login'])
def command_login(message):
    """Handle /login command"""
    chat_id = message.chat.id
    
    # Parse password from message
    parts = message.text.split(maxsplit=1)
    
    if len(parts) < 2:
        bot.reply_to(message, "❌ กรุณาใส่รหัสผ่าน\nตัวอย่าง: /login dad2026")
        return
    
    user_password = parts[1].strip()
    
    # Verify password
    if user_password == BOT_PASSWORD:
        authorized_users.add(chat_id)
        bot.reply_to(
            message,
            "✅ ล็อกอินสำเร็จ!\n\n"
            "พิมพ์รายละเอียดงานมาได้เลยครับ\n"
            "เช่น 'ม 2 รัตนาทิเบต ค่ายหัตวุฒิ 8 คัน คันละ 9000 28-29 มค 69'"
        )
        print(f"✅ User {chat_id} logged in successfully")
    else:
        bot.reply_to(message, "❌ รหัสผ่านไม่ถูกต้อง กรุณาลองใหม่อีกครั้ง")
        print(f"⚠️  Failed login attempt from {chat_id}")


@bot.message_handler(commands=['logout'])
def command_logout(message):
    """Handle /logout command"""
    chat_id = message.chat.id
    
    if chat_id in authorized_users:
        authorized_users.remove(chat_id)
        bot.reply_to(message, "👋 ออกจากระบบเรียบร้อยแล้ว")
        print(f"👋 User {chat_id} logged out")
    else:
        bot.reply_to(message, "ℹ️  คุณยังไม่ได้ล็อกอินอยู่แล้ว")


# ==========================================
# MESSAGE HANDLER
# ==========================================

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    """Handle all text messages (main quotation generation)"""
    chat_id = message.chat.id
    user_text = message.text
    
    # Check authentication
    if not is_authenticated(chat_id):
        send_login_prompt(chat_id)
        return
    
    print(f"📩 Message from User {chat_id}: {user_text}")
    
    # Send loading message
    loading_msg = bot.send_message(
        chat_id,
        "⏳ กำลังประมวลผลและสร้างเอกสารครับ รอสักครู่..."
    )
    
    try:
        # Step 1: Extract data using AI
        quotation_data = dad_logic.extract_data_from_text(user_text)
        
        if not quotation_data:
            bot.edit_message_text(
                "❌ AI ไม่สามารถประมวลผลข้อมูลได้\nกรุณาลองใหม่อีกครั้งพร้อมข้อมูลที่ชัดเจนขึ้น",
                chat_id,
                loading_msg.message_id
            )
            return
        
        # Step 2: Generate safe filename
        ai_filename = quotation_data.get('suggested_filename', 'quotation.pdf')
        safe_filename = sanitize_filename(ai_filename)
        save_path = os.path.join(OUTPUT_FOLDER, safe_filename)
        
        # Step 3: Create PDF
        dad_printer.create_pdf(quotation_data, save_path)
        print(f"✅ PDF created: {save_path}")
        
        # Step 4: Send PDF to user
        with open(save_path, 'rb') as pdf_file:
            caption = (
                f"✅ เรียบร้อยครับ!\n\n"
                f"👤 ลูกค้า: {quotation_data.get('customer_name', 'N/A')}\n"
                f"💰 ยอดรวม: {quotation_data.get('total_price', 0):,} บาท"
            )
            bot.send_document(
                chat_id,
                pdf_file,
                caption=caption,
                reply_to_message_id=message.message_id
            )
        
        # Step 5: Clean up loading message
        bot.delete_message(chat_id, loading_msg.message_id)
        
    except Exception as e:
        error_msg = f"❌ เกิดข้อผิดพลาด: {str(e)}"
        print(f"❌ Error processing message from {chat_id}: {e}")
        bot.edit_message_text(error_msg, chat_id, loading_msg.message_id)


# ==========================================
# MAIN
# ==========================================

if __name__ == "__main__":
    try:
        bot.infinity_polling()
    except KeyboardInterrupt:
        print("\n👋 Bot stopped by user")
    except Exception as e:
        print(f"\n❌ Bot crashed: {e}")
