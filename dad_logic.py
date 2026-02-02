"""
DadSaidSo - AI Logic Module
Handles text extraction and data processing using Groq Cloud API
"""

import os
import json
import re
from datetime import datetime
from dotenv import load_dotenv
from groq import Groq


# ==========================================
# CONFIGURATION
# ==========================================

# Load environment variables
load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")
# Model with web search and better reasoning capabilities
# llama-3.3-70b-versatile: Best for calculations and reasoning
# llama-3.1-405b-reasoning: Experimental, strongest reasoning
GROQ_MODEL = "llama-3.3-70b-versatile"


# ==========================================
# HELPER FUNCTIONS
# ==========================================

def get_current_date_context():
    """Get current date in Thai Buddhist Era format"""
    now = datetime.now()
    year_th = now.year + 543
    return f"วันนี้คือวันที่: {now.day}/{now.month}/{year_th} (พ.ศ.)"


def clean_json_response(response_text):
    """Remove markdown code blocks from JSON response"""
    if not response_text:
        return None
    return re.sub(r'```json|```', '', response_text).strip()


def build_prompt(user_input):
    """Build the AI prompt for quotation extraction"""
    return f"""
You are an expert secretary for a Thai bus rental business with access to accurate information.
{get_current_date_context()}

Task: Extract data from user input. You have access to search for official addresses and location information.

**CRITICAL CALCULATION RULES:**
- READ the numbers CAREFULLY from user input
- Extract EXACT numbers: quantity and unit_price
- DO NOT perform multiplication (system will calculate total_price)
- quantity = number of vehicles
- unit_price = price per vehicle
- Example: "8 คัน คันละ 9000" → quantity: 8, unit_price: 9000

**DATA EXTRACTION RULES:**
1. **Customer:** - Convert nickname to OFFICIAL name
   - Examples: "รร.รัตนาทิเบต" → "ผู้อำนวยการ โรงเรียนรัตนาธิเบศร์"
   - Search for official address if you know the organization
   
2. **Destination:** - Convert to OFFICIAL name with location
   - Examples: "ค่ายหัตวุฒิ" → "ค่ายหัตวุฒิ จังหวัดกาญจนบุรี"
   - Include district and province information
   
3. **Date:** Convert informal date to "D Month YYYY" (Thai Buddhist Era)
   - "69" = 2569 BE, "26" = 2526 BE, etc.
   - Current year: {datetime.now().year + 543} BE
   
4. **Project Name:** Create formal project title
   - "ม 2" → "โครงการทัศนศึกษา มัธยมศึกษาปีที่ 2"
   - "ม 6" → "โครงการศึกษาดูงาน มัธยมศึกษาปีที่ 6"
   
5. **Filename:** Safe filename (alphanumeric only)
   - Format: "Quotation_CustomerName_Date.pdf"
   - Remove special characters

**IMPORTANT - NUMBER EXTRACTION:**
User Input: "{user_input}"

Find these numbers EXACTLY as written:
- How many vehicles? (จำนวนคัน)
- Price per vehicle? (ราคาต่อคัน / คันละ)

**JSON Schema (Return ONLY this, NO markdown):**
{{
  "customer_name": "string - official name",
  "customer_address": "string - full address with district/province",
  "project_name": "string - formal project name",
  "destination": "string - official destination name",
  "destination_address": "string - location with district/province",
  "date_start": "string - D Month YYYY (Thai)",
  "date_end": "string - D Month YYYY (Thai)",
  "item_description": "string - default: ค่าจ้างเหมารถบัส พร้อมน้ำมันเชื้อเพลิง",
  "quantity": integer - EXACT number from input,
  "unit_price": integer/float - EXACT price from input,
  "total_price": 0 - leave as 0, system will calculate,
  "remark": "string - default: ราคานี้ไม่รวมค่าทางด่วน",
  "suggested_filename": "string - safe filename.pdf"
}}
"""


def validate_extracted_data(data):
    """
    Validate extracted data for completeness and correctness
    
    Returns:
        tuple: (is_valid, error_messages)
    """
    errors = []
    
    # Required fields
    required_fields = ['customer_name', 'quantity', 'unit_price']
    for field in required_fields:
        if not data.get(field):
            errors.append(f"Missing required field: {field}")
    
    # Validate numbers
    try:
        qty = int(data.get('quantity', 0))
        if qty <= 0:
            errors.append(f"Invalid quantity: {qty} (must be positive)")
    except (ValueError, TypeError):
        errors.append(f"Quantity is not a valid number: {data.get('quantity')}")
    
    try:
        price = float(data.get('unit_price', 0))
        if price <= 0:
            errors.append(f"Invalid unit_price: {price} (must be positive)")
    except (ValueError, TypeError):
        errors.append(f"Unit price is not a valid number: {data.get('unit_price')}")
    
    return (len(errors) == 0, errors)


def calculate_total_price(data):
    """
    Calculate total price using hard logic
    Override AI calculations to ensure 100% accuracy
    Performs validation and calculation
    """
    try:
        # Extract and validate numbers
        qty = int(data.get('quantity', 1))
        price = float(data.get('unit_price', 0))
        
        # Validation checks
        if qty <= 0:
            print(f"⚠️  Invalid quantity: {qty}")
            return False
        
        if price <= 0:
            print(f"⚠️  Invalid unit price: {price}")
            return False
        
        # Calculate total (HARD LOGIC - 100% accurate)
        total_price = qty * price
        
        # Update data with validated and calculated values
        data['quantity'] = qty
        data['unit_price'] = price
        data['total_price'] = total_price
        
        # Detailed logging for verification
        print(f"✅ Hard Logic Calculation:")
        print(f"   Quantity: {qty:,} คัน")
        print(f"   Unit Price: {price:,.2f} บาท/คัน")
        print(f"   Total: {qty} × {price:,.2f} = {total_price:,.2f} บาท")
        
        return True
        
    except ValueError as e:
        print(f"⚠️  Number conversion error: {e}")
        print(f"   quantity: {data.get('quantity')} (type: {type(data.get('quantity'))})")
        print(f"   unit_price: {data.get('unit_price')} (type: {type(data.get('unit_price'))})")
        return False
        
    except Exception as e:
        print(f"⚠️  Calculation Error: {e}")
        return False


# ==========================================
# MAIN FUNCTION
# ==========================================

def extract_data_from_text(user_input):
    """
    Extract quotation data from natural language text using AI
    
    Args:
        user_input (str): Natural language description of the quotation
        
    Returns:
        dict: Extracted quotation data or None if failed
    """
    # Validate API Key
    if not API_KEY or "YOUR_GROQ_API_KEY" in API_KEY:
        print("❌ Error: GROQ_API_KEY not found or invalid in .env file")
        return None

    print("   🤖 Sending to Groq AI (Llama)...")
    
    try:
        # Initialize Groq client
        client = Groq(api_key=API_KEY)
        
        # Build prompt
        prompt = build_prompt(user_input)
        
        # Call Groq API
        try:
            response = client.chat.completions.create(
                model=GROQ_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are an expert Thai secretary specializing in bus rental quotations. "
                            "Your primary task is to EXTRACT EXACT NUMBERS from user input. "
                            "DO NOT calculate totals. DO NOT modify numbers. "
                            "Return ONLY valid JSON without any markdown formatting. "
                            "Use your knowledge to find official addresses and locations."
                        )
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.1,  # Lower temperature for more accurate number extraction
                max_tokens=2500,
                top_p=0.9
            )
            response_text = response.choices[0].message.content
            
        except Exception as api_error:
            print(f"❌ Groq API Error: {api_error}")
            return None
        
        # Parse JSON response
        if not response_text:
            print("❌ AI returned empty response")
            return None
        
        clean_text = clean_json_response(response_text)
        data = json.loads(clean_text)
        
        # Validate extracted data
        is_valid, errors = validate_extracted_data(data)
        if not is_valid:
            print("⚠️  Data validation warnings:")
            for error in errors:
                print(f"   - {error}")
        
        # Apply hard logic for price calculation (CRITICAL)
        calculation_success = calculate_total_price(data)
        
        if not calculation_success:
            print("❌ Failed to calculate total price")
            return None
        
        return data
        
    except json.JSONDecodeError as e:
        print(f"❌ JSON Parsing Error: {e}")
        print(f"   Response: {response_text[:200]}...")
        return None
        
    except Exception as e:
        print(f"❌ System Error: {e}")
        return None
