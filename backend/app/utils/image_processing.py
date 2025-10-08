from PIL import Image
from io import BytesIO
import re
import base64

def img_pre_process_PIL(img):
    from io import BytesIO
    # If image is small, upscale—helps Tesseract on tiny fonts
    # img size doesn't matter since Tesseract ran locally
    max_dim = max(img.size)
    if max_dim < 1200:
        scale = 1200 / max_dim
        new_size = (int(img.width * scale), int(img.height * scale))
        img = img.resize(new_size)
    return img

def decode_image_base64(base64_data: str):

    if base64_data.startswith("data:"):
        base64_data = re.sub("^data:image/[^;]+;base64,", "", base64_data)

    image_data = base64.b64decode(base64_data)
    image = Image.open(BytesIO(image_data))
    return image