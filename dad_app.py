import dad_logic
import dad_printer
import os

# --- ตั้งค่าโฟลเดอร์เก็บไฟล์ ---
OUTPUT_FOLDER = "Output_PDF"

def main():
    print("--- DadSaidSo : โปรแกรมสร้างใบเสนอราคาฉบับคุณพ่อ ---")
    
    # สร้างโฟลเดอร์ถ้ายังไม่มี
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)
        print(f"📂 สร้างโฟลเดอร์เก็บไฟล์: {OUTPUT_FOLDER}")

    # dad_input = input("กรุณาใส่ข้อความ: ")
    dad_input = "ม 2 รัตนาทิเบต ค่ายหัตวุฒิ 8 คัน คันละ 9000 28 - 29 มค 69"
    
    print(f"\n📩 ได้รับข้อความ: {dad_input}")

    # 1. ส่งให้ AI คิด
    quotation_data = dad_logic.extract_data_from_text(dad_input)
    
    if quotation_data:
        print("\n🧠 AI ประมวลผลเสร็จสิ้น")
        
        # 2. ดึงชื่อไฟล์ที่ AI ตั้งให้ (ถ้าไม่มี ให้ตั้งเองกันเหนียว)
        ai_filename = quotation_data.get('suggested_filename', 'Quotation_Unknown.pdf')
        
        # ล้างชื่อไฟล์ให้ปลอดภัย (เผื่อ AI ใส่ path ประหลาดมา)
        safe_filename = os.path.basename(ai_filename)
        
        # 3. รวมร่าง Path (โฟลเดอร์ + ชื่อไฟล์)
        full_output_path = os.path.join(OUTPUT_FOLDER, safe_filename)
        
        # 4. สั่งปริ้นท์
        dad_printer.create_pdf(quotation_data, full_output_path)
        
        print(f"\n✅ เสร็จเรียบร้อย!")
        print(f"   ไฟล์ถูกเก็บไว้ที่: {full_output_path}")
    else:
        print("\n❌ ไม่สามารถประมวลผลได้")

if __name__ == "__main__":
    main()