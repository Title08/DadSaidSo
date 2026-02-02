"""
DadSaidSo - Automated Quotation Generator (Console Version)
Powered by Groq Cloud API (Llama models)
"""

import os
import dad_logic
import dad_printer


# ==========================================
# CONFIGURATION
# ==========================================

OUTPUT_FOLDER = "Output_PDF"


# ==========================================
# HELPER FUNCTIONS
# ==========================================

def sanitize_filename(filename):
    """Extract and clean filename to prevent path traversal"""
    safe_name = os.path.basename(filename)
    if not safe_name.endswith('.pdf'):
        safe_name += '.pdf'
    return safe_name


def get_user_input():
    """Get input from user or use default test data"""
    # For testing: uncomment the line below to enable user input
    # return input("กรุณาใส่ข้อความ: ")
    
    # Default test data
    return "ม 2 รัตนาทิเบต ค่ายหัตวุฒิ 8 คัน คันละ 9000 28 - 29 มค 69"


# ==========================================
# MAIN FUNCTION
# ==========================================

def main():
    """Main application entry point"""
    print("=" * 60)
    print("DadSaidSo : โปรแกรมสร้างใบเสนอราคาฉบับคุณพ่อ")
    print("=" * 60)
    
    # Create output folder if it doesn't exist
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    print(f"📂 Output folder: {OUTPUT_FOLDER}\n")

    # Get input
    dad_input = get_user_input()
    print(f"📩 ได้รับข้อความ: {dad_input}\n")

    # Step 1: Send to AI for processing
    print("🧠 กำลังส่งข้อมูลให้ AI ประมวลผล...")
    quotation_data = dad_logic.extract_data_from_text(dad_input)
    
    if not quotation_data:
        print("\n❌ ไม่สามารถประมวลผลได้")
        print("   กรุณาตรวจสอบข้อมูลหรือการตั้งค่า API Key")
        return 1
    
    print("✅ AI ประมวลผลเสร็จสิ้น\n")
    
    # Step 2: Generate filename
    ai_filename = quotation_data.get('suggested_filename', 'Quotation_Unknown.pdf')
    safe_filename = sanitize_filename(ai_filename)
    full_output_path = os.path.join(OUTPUT_FOLDER, safe_filename)
    
    # Step 3: Create PDF
    print("📄 กำลังสร้างไฟล์ PDF...")
    dad_printer.create_pdf(quotation_data, full_output_path)
    
    # Step 4: Success message
    print("\n" + "=" * 60)
    print("✅ เสร็จเรียบร้อย!")
    print("=" * 60)
    print(f"📁 ไฟล์ถูกเก็บไว้ที่: {full_output_path}")
    print(f"👤 ลูกค้า: {quotation_data.get('customer_name', 'N/A')}")
    print(f"💰 ยอดรวม: {quotation_data.get('total_price', 0):,} บาท")
    print("=" * 60)
    
    return 0


# ==========================================
# ENTRY POINT
# ==========================================

if __name__ == "__main__":
    try:
        exit_code = main()
        exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n👋 โปรแกรมถูกยกเลิกโดยผู้ใช้")
        exit(0)
    except Exception as e:
        print(f"\n❌ เกิดข้อผิดพลาด: {e}")
        exit(1)