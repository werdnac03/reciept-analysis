import requests
import base64
import json
import os
import pytest

test_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(test_dir, "data")

def encode_image(img_path: str):
    with open(img_path, "rb") as image_file:
        image_data = base64.b64encode(image_file.read()).decode('utf-8')
    return image_data

@pytest.mark.smoke
def test_simple_request():
    url = "http://localhost:8085/analysis"
    # headers = {"Content-Type": "application/json"}
    img_path = os.path.join(data_dir, "receipt1.PNG")
    image_encoding = encode_image(img_path)
    data = {
        "image_base64": image_encoding,
    }
    response = requests.post(url, json=data)
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    response_data = response.json()
    print("Response data:", response_data)


if __name__ ==  "__main__":
    test_simple_request()
