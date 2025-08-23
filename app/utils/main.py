from app.models.receipt_content import Word, Phrase
from app.utils.ocr_data_extraction import ocr_words, split_into_phrases
from app.utils.llm import parse_items_with_openai


def pipeline(image_path: str, psm: int = 6, model: str = "gpt-4o-mini") -> dict[str, any]:
    words = ocr_words(image_path, psm=psm)
    phrases = split_into_phrases(words)
    #return phrases
    result = parse_items_with_openai(phrases, model=model)
    return result
    


if __name__ == "__main__":
    img_path = '/home/andrewcheng/reciept-analysis/src/reciept1.PNG'
    img_path = '/home/andrewcheng/reciept-analysis/src/receipt2.png'
    psm = 6

    print(pipeline(img_path, psm))