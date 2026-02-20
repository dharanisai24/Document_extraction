def classify_document(text):
    text_lower = text.lower()

    if "invoice" in text_lower:
        return "Invoice"
    elif "packing list" in text_lower or "ship to" in text_lower:
        return "Packing List"
    else:
        return "Unknown"