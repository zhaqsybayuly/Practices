"""
Practice 5 — 2.2: Receipt Parser
Parses raw.txt pharmacy receipt using Python re module.
"""

import re
import json

# ── Load receipt text ──────────────────────────────────────────────────────
with open("raw.txt", encoding="utf-8") as f:
    text = f.read()


def parse_price(price_str: str) -> float:
    """Convert price string like '1 200,00' → 1200.0"""
    return float(price_str.replace(" ", "").replace(",", "."))


# ── 1. Extract all prices ──────────────────────────────────────────────────
# Format: digits (optional space thousands) comma two decimals, e.g. '1 200,00' or '308,00'
price_pattern = r"\b\d[\d\s]*,\d{2}\b"
all_price_strings = re.findall(price_pattern, text)
all_prices = [parse_price(p) for p in all_price_strings]

print("=" * 55)
print("1. ALL PRICES FOUND IN RECEIPT")
print("=" * 55)
for p_str, p_val in zip(all_price_strings, all_prices):
    print(f"  {p_str.strip():>15}  →  {p_val:>10.2f}")


# ── 2. Find all product names ──────────────────────────────────────────────
# Items are numbered: "1.\n<product name>\n<qty x price>"
# We grab the line(s) immediately after an item number line
item_block_pattern = r"^\d+\.\s*\n(.*?)\n[\d,\s]+x\s*[\d\s,]+"
items_raw = re.findall(item_block_pattern, text, re.MULTILINE)

print("\n" + "=" * 55)
print("2. PRODUCT NAMES")
print("=" * 55)
products = []
for i, name in enumerate(items_raw, 1):
    # Strip [RX] prefixes and extra spaces
    clean_name = re.sub(r"^\[RX\]-", "", name.strip())
    products.append(clean_name)
    print(f"  {i:>2}. {clean_name}")


# ── 3. Calculate total amount ──────────────────────────────────────────────
# Look for "ИТОГО:\n<amount>" or "ИТОГО:\s*<amount>"
total_match = re.search(r"ИТОГО:\s*\n?([\d\s]+,\d{2})", text)
total = parse_price(total_match.group(1)) if total_match else 0.0

print("\n" + "=" * 55)
print("3. TOTAL AMOUNT")
print("=" * 55)
print(f"  ИТОГО: {total:,.2f} KZT")


# ── 4. Extract date and time ───────────────────────────────────────────────
datetime_match = re.search(
    r"Время:\s*(\d{2}\.\d{2}\.\d{4})\s+(\d{2}:\d{2}:\d{2})", text
)
date_str = datetime_match.group(1) if datetime_match else "N/A"
time_str = datetime_match.group(2) if datetime_match else "N/A"

print("\n" + "=" * 55)
print("4. DATE AND TIME")
print("=" * 55)
print(f"  Date: {date_str}")
print(f"  Time: {time_str}")


# ── 5. Find payment method ─────────────────────────────────────────────────
payment_match = re.search(
    r"(Банковская карта|Наличные|Kaspi Pay|QR-код)[:\s]*([\d\s]+,\d{2})?", text
)
payment_method = payment_match.group(1) if payment_match else "Unknown"
payment_amount_str = payment_match.group(2).strip() if payment_match and payment_match.group(2) else None
payment_amount = parse_price(payment_amount_str) if payment_amount_str else total

print("\n" + "=" * 55)
print("5. PAYMENT METHOD")
print("=" * 55)
print(f"  Method: {payment_method}")
print(f"  Amount: {payment_amount:,.2f} KZT")


# ── 6. Structured JSON output ──────────────────────────────────────────────
# Also extract per-item quantity and unit price
item_detail_pattern = (
    r"^\d+\.\s*\n(.*?)\n([\d,]+)\s*x\s*([\d\s,]+)\n([\d\s,]+)"
)
item_details = re.findall(item_detail_pattern, text, re.MULTILINE)

structured_items = []
for name, qty_str, unit_str, cost_str in item_details:
    clean_name = re.sub(r"^\[RX\]-", "", name.strip())
    structured_items.append({
        "name": clean_name,
        "quantity": parse_price(qty_str),
        "unit_price": parse_price(unit_str.strip()),
        "cost": parse_price(cost_str.strip()),
    })

# Extract company info
bin_match = re.search(r"БИН\s*(\d+)", text)
cashier_match = re.search(r"Кассир\s+(.+)", text)
check_match = re.search(r"Чек №(\d+)", text)

receipt_json = {
    "company": "Филиал ТОО EUROPHARMA Астана",
    "BIN": bin_match.group(1) if bin_match else "N/A",
    "check_number": check_match.group(1) if check_match else "N/A",
    "cashier": cashier_match.group(1).strip() if cashier_match else "N/A",
    "date": date_str,
    "time": time_str,
    "payment_method": payment_method,
    "items": structured_items,
    "total_KZT": total,
}

print("\n" + "=" * 55)
print("6. STRUCTURED OUTPUT (JSON)")
print("=" * 55)
print(json.dumps(receipt_json, ensure_ascii=False, indent=2))

# Save to file
with open("receipt_parsed.json", "w", encoding="utf-8") as out:
    json.dump(receipt_json, out, ensure_ascii=False, indent=2)
print("\n  Saved to receipt_parsed.json")
