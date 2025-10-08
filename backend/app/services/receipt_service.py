from app.utils.image_processing import decode_image_base64
from app.utils.ocr_data_extraction import ocr_words_PIL, split_into_phrases
from app.utils.llm import parse_items_with_openai
from app.extensions import db
from app.models.models import Receipt, Item

def process_receipt_image_pil(receipt_id, image_b64):
    """
    Full OCR→Parse→DB pipeline for a given user and PIL image.
    """

    img = decode_image_base64(image_b64)
    words = ocr_words_PIL(img, psm=6)  # PSM 6 works well for receipts
    phrases = split_into_phrases(words)
    parsed_data = parse_items_with_openai(phrases)
    
    
    receipt = Receipt.query.get(receipt_id)
    for name, (bbox, qty, price) in parsed_data.items():
        item = Item(
            receipt_id=receipt.receipt_id,
            item_name=name,
            quantity=qty,
            price=price,
        )
        db.session.add(item)

    db.session.commit()
    return receipt, parsed_data
