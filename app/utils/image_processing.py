from PIL import Image

def img_pre_process(image_path: str):
    img = Image.open(image_path).convert("RGB")
    # If image is small, upscale—helps Tesseract on tiny fonts
    # img size doesn't matter since Tesseract ran locally
    max_dim = max(img.size)
    if max_dim < 1200:
        scale = 1200 / max_dim
        new_size = (int(img.width * scale), int(img.height * scale))
        img = img.resize(new_size)
    return img

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