# DadSaidSo v0.2 (GitHub Edition)

Automated Quotation Generator powered by AI (Gemini) for Bus Rental Businesses.
Supports operation via Console and Telegram Bot.

## 📋 Features
- Converts natural language text (e.g., "Going to Chiang Mai for 3 days, 2 buses") into a PDF quotation.
- Automatically extracts location data and customer addresses using AI.
- Calculates total price and converts numbers to Thai Baht text.
- Generates professional PDF files ready for sending.

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
   # Google Gemini API Key (Get for free at aistudio.google.com)
   GEMINI_API_KEY=your_gemini_api_key_here

   # Telegram Bot Token (If using Telegram)
   TELEGRAM_TOKEN=your_telegram_bot_token_here
   ```

   *Note: The code supports reading from system Environment Variables or using the `python-dotenv` library to read from a .env file (this example uses `os.getenv` which supports both).*

## 🚀 Usage

### 1. Console Usage (Testing)
Run `dad_app.py` to test PDF generation from text in the Terminal.
```bash
python dad_app.py
```

### 2. Telegram Bot Usage
Run `dad_telegram.py`
```bash
python dad_telegram.py
```
Then chat with your bot and type the job details.

## 📂 File Structure
- `dad_logic.py`: Core logic, connects to AI and processes text.
- `dad_printer.py`: Document manager, generates PDF files.
- `dad_app.py`: Main program for local execution.
- `dad_telegram.py`: Bot for Telegram.
- `fonts/`: Folder containing Thai fonts (TH Sarabun New).

## ⚠️ Caution
- Do not upload `.env` files or files containing API Keys to GitHub.
- Check your Google Gemini API usage quota.

---
Developed by Title08
