from app.models.receipt_content import Word, Phrase
from app.utils.image_processing import img_pre_process, img_pre_process_PIL
import pytesseract
from pytesseract import Output
from collections import defaultdict

# OCR data extraction
def ocr_words(image_path: str, psm: int) -> list[Word]:
    img = img_pre_process(image_path)
    
    cfg = f"--oem 3 --psm {psm}"
    data = pytesseract.image_to_data(img, output_type=Output.DICT, config=cfg)

    words: list[Word] = []
    n = len(data["text"])
    for i in range(n):
        txt = (data["text"][i] or "").strip()
        # removes blanks
        if not txt:
            continue
        conf = float(data.get("conf", [0]*n)[i])
        #if conf < 0:  # Tesseract uses -1 for non-words
        #    continue
        w = Word(
            text=txt,
            left=int(data["left"][i]),
            top=int(data["top"][i]),
            width=int(data["width"][i]),
            height=int(data["height"][i]),
            conf=conf,
            ids=(
                int(data.get("page_num")[i]),
                int(data.get("block_num")[i]),
                int(data.get("par_num")[i]),
                int(data.get("line_num")[i]),
            ),
        )
        words.append(w)
    return words

def ocr_words_PIL(image_pil, psm: int) -> list[Word]:
    img = img_pre_process_PIL(image_pil)
    
    cfg = f"--oem 3 --psm {psm}"
    data = pytesseract.image_to_data(img, output_type=Output.DICT, config=cfg)

    words: list[Word] = []
    n = len(data["text"])
    for i in range(n):
        txt = (data["text"][i] or "").strip()
        # removes blanks
        if not txt:
            continue
        conf = float(data.get("conf", [0]*n)[i])
        #if conf < 0:  # Tesseract uses -1 for non-words
        #    continue
        w = Word(
            text=txt,
            left=int(data["left"][i]),
            top=int(data["top"][i]),
            width=int(data["width"][i]),
            height=int(data["height"][i]),
            conf=conf,
            ids=(
                int(data.get("page_num")[i]),
                int(data.get("block_num")[i]),
                int(data.get("par_num")[i]),
                int(data.get("line_num")[i]),
            ),
        )
        words.append(w)
    return words


#
def line_key(w: Word): return w.ids

def split_into_phrases(words: list[Word]) -> list[Phrase]:
    # Group words by line
    lines = defaultdict(list)
    for w in words:
        lines[line_key(w)].append(w)

    phrases = []
    for ids, wlist in lines.items():

        wlist.sort(key=lambda w: w.left)

        # Dynamic gap threshold: median word height * factor
        heights = sorted([w.height for w in wlist])
        med_h = heights[len(heights)//2] if heights else 16
        gap_thresh = 1.2 * med_h  # adjust 1.0–1.6 if needed

        current = []
        for i, w in enumerate(wlist):
            if not current:
                current = [w]
                continue
            # Logic for dynamic gap
            prev = current[-1]
            gap = w.left - prev.right
            if gap > gap_thresh:    
                # finalize current phrase
                phrases.append(words_to_phrase(current))
                current = [w]
            else:
                current.append(w)

        if current:
            phrases.append(words_to_phrase(current))

    # Sort phrases top-to-bottom, left-to-right for readability
    phrases.sort(key=lambda p: (p.bbox[1], p.bbox[0]))
    return phrases

def words_to_phrase(words: list[Word]) -> Phrase:
    text = ""
    x1 = float("inf")
    y1 = float("inf")
    x2 = -float("inf")
    y2 = -float("inf")
    for w in words:
        if text == "":
            text = w.text
        else:
            text = text + " "  + w.text
        x1 = min(x1, w.left)
        y1 = min(y1, w.top)
        x2 = max(x2, w.right)
        y2 = max(y2, w.bottom)
    return Phrase(text=text, bbox=(x1, y1, x2, y2))