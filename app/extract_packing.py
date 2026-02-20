import re

def extract_packing_fields(text):
    data = {}

    # ✅ ORDER NUMBER (Flexible + Fallback)
    order_no = re.search(
        r"(ORDER\s*#?|ORDER#|0RDER#)\s*[:\-]?\s*(ORD[-\d]+)",
        text,
        re.IGNORECASE
    )

    # 🔁 Fallback if above fails
    if not order_no:
        order_no = re.search(r"ORD[-\d]+", text, re.IGNORECASE)

    # ✅ SHIP TO (Multi-line Block)
    ship_to = extract_ship_to_block(text)

    # ✅ LINE ITEMS
    items = extract_line_items(text)

    data["Document Type"] = "Packing List"
    data["Order Number"] = order_no.group(2) if order_no and len(order_no.groups()) >= 2 else (
        order_no.group(0) if order_no else "Not Found"
    )
    data["Ship To"] = ship_to
    data["Line Items"] = items

    return data


# ✅ Extract Ship To Block
def extract_ship_to_block(text):
    lines = text.split("\n")
    capture = False
    address_lines = []

    for line in lines:
        clean = line.strip()

        if "SHIP TO" in clean.upper():
            capture = True
            continue

        if capture:
            # ✅ Stop if numbered item rows start
            if re.match(r"\d+\s+\w+", clean):
                break

            # ✅ Stop at TOTAL line
            if "TOTAL" in clean.upper():
                break

            if clean:
                address_lines.append(clean)

    return " ".join(address_lines) if address_lines else "Not Found"


# ✅ Extract Line Items (Only ITM rows)
def extract_line_items(text):
    lines = text.split("\n")
    items = []

    for line in lines:
        clean = line.strip()

        # ✅ Match numbered rows
        if re.match(r"\d+\s+\w+", clean):
            items.append(clean)

    return items if items else ["No items found"]