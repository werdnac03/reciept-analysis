from flask import Flask, request, jsonify
from app.models.receipt_content import Word, Phrase
from app.utils.ocr_data_extraction import ocr_words_PIL, split_into_phrases
from app.utils.llm import parse_items_with_openai
from app.utils.annotate import draw_all_bbox_with_label
import json
import base64
from io import BytesIO
from PIL import Image



def pipeline(image, psm: int = 6, model: str = "gpt-4o-mini") -> dict[str, any]:

    words = ocr_words_PIL(image, psm=psm)
    phrases = split_into_phrases(words)
    #return phrases
    result = parse_items_with_openai(phrases, model=model)
    return result



# Create an instance of the Flask class.
# __name__ is a convenient shortcut that helps Flask locate resources.
app = Flask(__name__)

# Define a route for the root URL ("/").
# The @app.route decorator associates the URL with the function below it.

def decode_image_base64(base64_data: str):
    image_data = base64.b64decode(base64_data)
    image = Image.open(BytesIO(image_data))
    return image

@app.route("/")
def index():
    return "<h1>Server is running.</h1><hr />Some information"

@app.route("/analysis", methods=["POST"])
def process_receipt():
    data = request.get_json()
    if not data or "image_base64" not in data:
        return jsonify({"error": "No image data provided"}), 400
    try:
        image = decode_image_base64(data["image_base64"])
    except Exception as e:
        return jsonify({"error": "Base64 encoding is wrong"}), 400
    
    psm = data.get("psm", 6)
    model = data.get("model", "gpt-4o-mini")
    result = pipeline(image, psm=psm, model=model)
    return jsonify({
        "result": result,
        "error": None
    })

# This block ensures the application runs only when the script is executed directly.
if __name__ == "__main__":
    # Run the Flask application in debug mode for development.
    # debug=True allows for automatic reloading on code changes and provides a debugger.
    app.run("0.0.0.0", port=8085, debug=True)