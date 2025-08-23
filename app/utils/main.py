from app.models.receipt_content import Word, Phrase
from app.utils.ocr_data_extraction import ocr_words, split_into_phrases
from app.utils.llm import parse_items_with_openai
from app.utils.annotate import draw_all_bbox_with_label
import json


def pipeline(image_path: str, psm: int = 6, model: str = "gpt-4o-mini") -> dict[str, any]:
    words = ocr_words(image_path, psm=psm)
    phrases = split_into_phrases(words)
    #return phrases
    result = parse_items_with_openai(phrases, model=model)
    return result
    


if __name__ == "__main__":
    #config
    psm = 6
    img_suffix = "receipt1"
    f_type = ".PNG"
    prompt = "2.0-best"
    annotate = True

    #----------------
    
    
    img_path = '/home/andrewcheng/reciept-analysis/src/' + img_suffix + f_type
    json_path = "/home/andrewcheng/reciept-analysis/json-outs/" + img_suffix + "-" + prompt
    out_dir = "/home/andrewcheng/reciept-analysis/annotated_labels/" + img_suffix + "-" + prompt
    
    if annotate:
        draw_all_bbox_with_label(json_path, img_path, out_dir)
    
    else:
        result = pipeline(img_path, psm)
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
