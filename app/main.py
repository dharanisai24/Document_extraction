from ocr import read_document
from classify import classify_document
from extract_invoice import extract_invoice_fields
from extract_packing import extract_packing_fields
from save_output import save_json


def process_document(file_path):
    print(f"📄 Processing: {file_path}")

    text = read_document(file_path)

    print("\n📝 Extracted Text Preview:")
    print(text)  # first 300 characters

    doc_type = classify_document(text)
    print(f"\n🧠 Detected Document Type: {doc_type}")

    if doc_type == "Invoice":
        data = extract_invoice_fields(text)
        save_json(data, "invoice_output.json")

    elif doc_type == "Packing List":
        data = extract_packing_fields(text)
        save_json(data, "packing_output.json")

    else:
        print("❌ Could not classify document")


if __name__ == "__main__":
    file_path = r"C:\Users\dhara\Downloads\document-extraction-template-repo-main\samples\invoices\invoice_8.pdf"  # Change if needed
    process_document(file_path)