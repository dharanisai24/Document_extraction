import re

def extract_invoice_fields(text):
    data = {}

    invoice_no = extract_invoice_number(text)
    date = extract_invoice_date(text)
    vendor = extract_vendor_name(text)
    items = extract_line_items(text)

    data["Document Type"] = "Invoice"
    data["Vendor Name"] = vendor
    data["Invoice Number"] = invoice_no
    data["Invoice Date"] = date
    data["Line Items"] = items if items else ["No items found"]

    return data


# ✅ ULTRA ROBUST Invoice Number Detection
def extract_invoice_number(text):

    patterns = [

        # 1️⃣ Invoice No label variations
        r"invoice\s*n[o0]\.?\s*[:\-]?\s*([A-Z0-9\/\-]+)",

        # 2️⃣ Bill No
        r"bill\s*n[o0]\.?\s*[:\-]?\s*([A-Z0-9\/\-]+)",

        # 3️⃣ Ref No / Reference No
        r"ref(erence)?\s*n[o0]\.?\s*[:\-]?\s*([A-Z0-9\/\-]+)",

        # 4️⃣ Doc No
        r"doc(ument)?\s*n[o0]\.?\s*[:\-]?\s*([A-Z0-9\/\-]+)",

        # 5️⃣ Generic INV pattern
        r"\bINV[\/\-]?\d+\b",

        # 6️⃣ Generic Alphanumeric/Slash Pattern
        r"\b[A-Z]{2,5}[\/\-]\d{2,5}[\/\-]?\d*\b"
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            if match.groups():
                return match.group(match.lastindex)
            return match.group(0)

    return "Not Found"


# ✅ Invoice Date
def extract_invoice_date(text):
    date = re.search(
        r"(invoice\s*date|date)\s*[:\-]?\s*([0-9]{4}[-/][0-9]{2}[-/][0-9]{2})",
        text,
        re.IGNORECASE
    )

    return date.group(2) if date else "Not Found"


# ✅ Vendor Name
def extract_vendor_name(text):
    lines = text.split("\n")

    for line in lines[:10]:
        clean = line.strip()

        if clean:
            if not re.search(r"invoice|gst|tax|date", clean, re.IGNORECASE):
                if len(clean.split()) <= 7:
                    return clean

    return "Not Found"


# ✅ Line Items (Names Only)
def extract_line_items(text):
    lines = text.split("\n")
    items = []

    for line in lines:
        clean = line.strip()

        if not clean:
            continue

        if re.search(r"total|gst|tax|invoice|date|hsn|qty|rate|amount", clean, re.IGNORECASE):
            continue

        if re.search(r"charges|charge|handling|seal|documentation|scanning|weighment|edi|lift|customs", clean, re.IGNORECASE):
            items.append(clean_item_name(clean))

    return items


def clean_item_name(line):
    cleaned = re.split(r"\s+\d", line)[0]
    return cleaned.strip()