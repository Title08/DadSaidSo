# DadSaidSo v0.3 (Groq Edition)

Automated Quotation Generator powered by AI (Groq Cloud) for Bus Rental Businesses.
Supports operation via Console and Telegram Bot.

## 📋 Features
- Converts natural language text (e.g., "Going to Chiang Mai for 3 days, 2 buses") into a PDF quotation.
- Automatically extracts location data and customer addresses using AI.
- Calculates total price and converts numbers to Thai Baht text.
- Generates professional PDF files ready for sending.
- Powered by Groq Cloud API with Llama models for fast inference.

## 🛠️ Installation

1. **Clone the project**
   ```bash
   git clone https://github.com/Title08/DadSaidSo.git
   cd DadSaidSo
   ```

2. **Install required libraries**
   ```bash
   pip install -r requirements.txt
   ```

3. **Setup Environment Variables**
   Create a `.env` file in the project folder and add the following keys:

   ```env
   # Groq Cloud API Key (Get for free at https://console.groq.com/keys)
   GROQ_API_KEY=your_groq_api_key_here

   # Telegram Bot Token (If using Telegram)
   TELEGRAM_TOKEN=your_telegram_bot_token_here
   
   # Telegram Bot Password (Set your own password for security)
   BOT_PASSWORD=dad2026
   ```

   **How to get a Groq API Key:**
   - Visit [https://console.groq.com](https://console.groq.com)
   - Sign up for a free account
   - Navigate to API Keys section
   - Create a new API key and copy it to your `.env` file

   *Note: The code supports reading from system Environment Variables or using the `python-dotenv` library to read from a .env file (this example uses `os.getenv` which supports both).*

## 🚀 Usage

### 1. Console Usage (Testing)
Run `dad_app.py` to test PDF generation from text in the Terminal.
```bash
python dad_app.py
```

### 2. Telegram Bot Usage

#### 📱 Setting Up Your Telegram Bot

**Step 1: Create a Telegram Bot**
1. Open Telegram and search for `@BotFather`
2. Start a chat and send `/newbot`
3. Follow the instructions:
   - Choose a name for your bot (e.g., "DadSaidSo Quotation Bot")
   - Choose a username ending in "bot" (e.g., "dadsaidso_quote_bot")
4. BotFather will give you a **Token** (looks like: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)
5. Copy this token to your `.env` file:
   ```env
   TELEGRAM_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
   ```

**Step 2: Run the Bot**
```bash
python dad_telegram.py
```
You should see: `🚀 DadSaidSo Telegram Bot เริ่มทำงานแล้ว...`

**Step 3: Start Chatting**
1. Search for your bot username in Telegram (e.g., @dadsaidso_quote_bot)
2. Click **Start** or send `/start`
3. Bot will ask you to login with password

**Step 4: Login with Password 🔐**
For security, the bot requires authentication before use:
```
/login dad2026
```
(Or use your custom password from `.env` file)

After successful login, you can:
- Generate quotations by typing job details
- Use `/logout` to sign out
- Use `/help` for instructions

**Step 5: Generate Quotations**
Simply type your job details in natural language, for example:
```
ม 2 รัตนาทิเบต ค่ายหัตวุฒิ 8 คัน คันละ 9000 28-29 มค 69
```

The bot will:
1. Show "⏳ กำลังประมวลผล..." (Processing)
2. Send the text to Groq AI for analysis
3. Generate a professional PDF quotation
4. Send the PDF file back to you with a summary

**Example Messages You Can Send:**
- `รร.วัดราชโอรส เชียงใหม่ 3 วัน 2 คัน คันละ 15000`
- `บริษัท ABC จ.ระยอง 5 คัน คันละ 8500 15-16 ก.พ. 69`
- `ม.6 โรงเรียนสตรีวิทยา ทัศนศึกษา กาญจนบุรี 10 คัน 12000/คัน`

#### 🎯 How It Works
```
User opens bot
    ↓
Bot asks for login
    ↓
User sends: /login password
    ↓
✅ Authentication successful
    ↓
User sends message (job details)
    ↓
Bot receives & shows "Processing..."
    ↓
Groq AI analyzes text & extracts:
  - Customer name & address
  - Project name
  - Destination
  - Dates
  - Vehicle quantity & price
    ↓
System calculates total
    ↓
PDF generator creates quotation
    ↓
Bot sends PDF file back to user
    ↓
Done! ✅
```

#### 🔐 Security Commands
- `/login [password]` - Login to use the bot
- `/logout` - Logout from the bot
- `/start` or `/help` - Show instructions

#### 💡 Tips
- **Change the default password** in your `.env` file for security
- The AI understands Thai abbreviations (ม.2, รร., จ., ก.พ., etc.)
- It automatically finds full addresses for schools/companies
- Buddhist Era (BE) year format: "69" = 2569 BE = 2026 AD
- The bot works 24/7 as long as the script is running
- Only logged-in users can generate quotations

## 📂 File Structure
- `dad_logic.py`: Core logic, connects to AI and processes text.
- `dad_printer.py`: Document manager, generates PDF files.
- `dad_app.py`: Main program for local execution.
- `dad_telegram.py`: Bot for Telegram.
- `fonts/`: Folder containing Thai fonts (TH Sarabun New).

## ⚠️ Caution
- Do not upload `.env` files or files containing API Keys to GitHub.
- Groq offers free API access with generous rate limits.
- Check your Groq API usage at [https://console.groq.com](https://console.groq.com)

---
Developed by Title08
