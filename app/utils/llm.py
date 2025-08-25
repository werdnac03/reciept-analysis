from dotenv import load_dotenv
import os, json
from app.models.receipt_content import Word, Phrase
from openai import OpenAI

# load_dotenv(dotenv_path=".env")
load_dotenv()
OPENAI_KEY = os.getenv("OPENAI_KEY")
SYSTEM_PROMPT = (
"You are a strict receipt parser. You will receive OCR phrases with bounding boxes.\n"
"Group phrases into purchasable items and summary rows.\n\n"

"Output only ONE JSON object mapping full item/summary names → [bbox, qty, price].\n"
"bbox = [x1,y1,x2,y2] integers in pixels covering ALL phrases for that item INCLUDING the price phrase.\n"
"Example keys include: items by full merged name, and summary rows like Subtotal, Service Charge, Auto Service Charge, Tax, Total.\n\n"

"Rules:\n"
"- Use ONLY provided phrases; never invent text or numbers. If qty not shown, use 1.\n"
"- Merge multi-line or multi-phrase item names; include suboptions/modifiers in the item name.\n"
"- A valid price matches \\b\\$?\\d{1,4}\\.\\d{2}\\b; strip $.\n"
"- If a line shows '2 @ 3.50 7.00', then qty=2, price=7.00.\n"
"- For weight lines like '1.23 lb @ 4.99 6.14', qty=1.23, price=6.14.\n"
"- Prefer the rightmost price associated with an item row.\n"
"- Ignore phone numbers, IDs, promos, and ads unless part of an item name.\n"
"- Preserve visual order. Output JSON only—no explanations.\n\n"

"Layout Association Policy:\n"
"- Detect the rightmost price column.\n"
"- Look at the first item+price pair to determine orientation:\n"
"   • TOP-ALIGNED: price top ≈ item top → each price starts its item, text continues until the next price.\n"
"   • BOTTOM-ALIGNED: price bottom ≈ item bottom → each price ends its item, text extends up until the previous price.\n"
"- Choose one orientation once and apply it consistently for all items.\n"
"- Summary rows (Subtotal, Tax, Total, etc.) pair directly with their matching price, outside this rule.\n\n"

"Bounding boxes:\n"
"- For each entry, take the union of name/modifier phrases and the price box.\n\n"

"Output format exactly:\n"
"{\n"
"  Full Item Name: [[x1,y1,x2,y2], qty, price],\n"
"  ...,\n"
"  Subtotal: [[x1,y1,x2,y2], 1, x.xx],\n"
"  Tax: [[x1,y1,x2,y2], 1, x.xx],\n"
"  Total: [[x1,y1,x2,y2], 1, x.xx]\n"
"}\n"
)

def phrases_payload(phrases: list[Phrase]) -> str:
    packed = [
        {"text": p.text, "bbox": list(map(int, p.bbox))}
        for p in phrases
    ]
    return json.dumps({"PHRASES": packed}, ensure_ascii=False)

def parse_items_with_openai(phrases: list[Phrase], model: str = "gpt-4o-mini") -> dict[str, any]:
    client = OpenAI(
        api_key=OPENAI_KEY
    )
    resp = client.chat.completions.create(
        model=model,
        temperature=0,
        response_format={"type": "json_object"},  # force valid JSON
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": phrases_payload(phrases)},
        ],
    )
    content = resp.choices[0].message.content.strip()
    return json.loads(content)