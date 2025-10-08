import os
import pdfplumber
from google import genai

# ==============================================================================
# PART 1: PDF TEXT EXTRACTION (using pdfplumber)
# ==============================================================================

# Set your API key here
API_KEY = "YAIzaSyBdVbl_k-eNRfqmNdziCAvwLBETrg4ZtiM" 


def extract_text_from_pdf(pdf_path):
    full_text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    full_text += text + "\n---\n"
        return full_text.strip()
    except Exception as e:
        print(f"Error: Could not open or process PDF file at '{pdf_path}'. Details: {e}")
        return None

# ==============================================================================
# PART 2: GEMINI KEY-VALUE EXTRACTION (using google-genai)
# ==============================================================================

def extract_invoice_key_values(invoice_text: str, model_name: str = 'gemini-2.5-flash') -> str:
    client = genai.Client(api_key=API_KEY)

    system_instruction = (
        "You are an expert financial assistant. Your task is to extract the most critical "
        "key-value fields from the provided invoice text and present them as a short, "
        "easy-to-read summary. The key fields to extract are: **Invoice Number**, "
        "**Invoice Date**, **Vendor/Supplier Name**, **Total Amount Due**, and **Currency**. "
        "Present the final output as a clear, formatted list or short paragraph of text."
    )

    user_prompt = f"Extract the key details from this invoice text: \n\n--- INVOICE TEXT ---\n{invoice_text}\n\n--- SUMMARY OUTPUT ---"
    
    contents = [user_prompt]

    try:
        response = client.models.generate_content(
            model=model_name,
            contents=contents,
            config=genai.types.GenerateContentConfig(
                system_instruction=system_instruction
            )
        )
        
        return response.text.strip()
        
    except Exception as e:
        return f"Error occurred during the Gemini API call: {e}"

# ==============================================================================
# PART 3: UNIFIED WORKFLOW FUNCTION
# ==============================================================================

def summarize_invoice_from_pdf(pdf_path: str) -> str:
    """
    Unified function to extract text from a PDF and summarize key fields using Gemini.

    Args:
        pdf_path: The file path to the PDF invoice document.

    Returns:
        A string containing the extracted key-value summary, or an error message.
    """
    print(f"Starting extraction for: {pdf_path}")
    extracted_text = extract_text_from_pdf(pdf_path)
    if not extracted_text:
        return "Extraction failed: No text could be retrieved from the PDF."
    summary = extract_invoice_key_values(extracted_text)
    return summary

# ==============================================================================
# --- FINAL USAGE EXAMPLE ---
# ==============================================================================

PDF_FILE_PATH = "C:/Users/thang/Downloads/PremiumpaymentReceipt_21403652_.pdf" 
print(summarize_invoice_from_pdf(pdf_path=PDF_FILE_PATH))
