from PIL import Image, ImageDraw, ImageFont
import json, os
from app.utils.image_processing import img_pre_process


def draw_bbox_with_label(
    image_path: str,
    bbox: list[int],   # [x1, y1, x2, y2]
    label: str,
    out_path: str = "output.jpg"):
    """
    Draws a bounding box and label on an image.

    Args:
        image_path: path to the input JPG image.
        bbox: list [x1, y1, x2, y2] for the bounding box.
        label: text label to display above the bounding box.
        out_path: path to save the output image.
    """
    # Load image
    img = img_pre_process(image_path)
    draw = ImageDraw.Draw(img)

    x1, y1, x2, y2 = bbox

    # Draw bounding box
    draw.rectangle([x1, y1, x2, y2], outline="red", width=3)
    font = ImageFont.load_default()
    bbox_text = font.getbbox(label)
    text_w, text_h = bbox_text[2] - bbox_text[0], bbox_text[3] - bbox_text[1]

    # Draw filled rectangle behind text
    draw.rectangle([x1, y1 - text_h - 4, x1 + text_w + 4, y1], fill="red")
    
    # Draw text
    draw.text((x1 + 2, y1 - text_h - 2), label, fill="white", font=font)

    # Save output
    img.save(out_path)
    print(f"Saved output to {out_path}")


def read_json(path: str) -> dict:
    """
    Reads a JSON file from the given path and returns it as a dictionary.
    """
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

def draw_all_bbox_with_label(json_path: str, img_path: str, out_dir: str):
    try:
        os.mkdir(out_dir)     # try to make the folder
    except FileExistsError:
        # already exists → do nothing
        pass

    data = read_json(json_path)
    for key in data:
        img_name = key
        img_name = img_name.replace(" ", "_").replace(".", "")
        out_path = out_dir + "/" + f"{img_name}" + ".jpg"
        bbox = data[key][0]
        draw_bbox_with_label(img_path, bbox, key, out_path)


if __name__ == "__main__":

    #json_path = "/home/andrewcheng/reciept-analysis/json-outs/r1-single-6"
    #json_path = "/home/andrewcheng/reciept-analysis/json-outs/r2-single-4"
    json_path = "/home/andrewcheng/reciept-analysis/json-outs/r2-2"
    #img_path = "/home/andrewcheng/reciept-analysis/src/receipt1.PNG"
    img_path = "/home/andrewcheng/reciept-analysis/src/receipt2.png"
    out_dir = "/home/andrewcheng/reciept-analysis/annotated_labels"
    data = read_json(json_path)
    for key in data:
        img_name = key
        img_name = img_name.replace(" ", "_").replace(".", "_")
        out_path = out_dir + "/" + f"{img_name}" + ".jpg"
        bbox = data[key][0]
        draw_bbox_with_label(img_path, bbox, key, out_path)
    
