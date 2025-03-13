import requests
import base64
from PIL import Image
import io

class TextRequest:
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
        self.base_url = "IyS0wq21YTSsRnzqq1bri70rmDqTKeIG"

    def send(self, text: str, model: str) -> dict:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "text": text,
            "model": model
        }
        try:
            response = requests.post(self.base_url, headers=headers, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return {"error": "Failed to send request"}

class ImageRequest:
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
        self.base_url = "IyS0wq21YTSsRnzqq1bri70rmDqTKeIG"

    def send(self, text: str, image_path: str, model: str) -> dict:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        try:
            with open(image_path, "rb") as image_file:
                image = Image.open(image_file)
                buffered = io.BytesIO()
                image.save(buffered, format="JPEG")
                image_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')

            data = {
                "text": text,
                "image": image_base64,
                "model": model
            }

            response = requests.post(self.base_url, headers=headers, json=data)
            response.raise_for_status()
            return response.json()

        except Exception as e:
            print(f"An error occurred: {e}")
            return {"error": "Failed to send request"}

class ChatFacade:
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
        self.text_request = TextRequest(api_key)
        self.image_request = ImageRequest(api_key)
        self.models = {
            1: ["text-model-1", "text-model-2"],
            2: ["image-model-1", "image-model-2"]
        }
        self.history = []

    def select_mode(self) -> int:
        print("Select request type: 1 – Text, 2 – Image")
        return int(input("Enter choice: "))

    def select_model(self, mode: int) -> str:
        if mode not in self.models:
            raise ValueError("Invalid mode selected.")

        print(f"Available models for mode {mode}: {', '.join(self.models[mode])}")
        model = input("Enter model name: ")

        if model not in self.models[mode]:
            raise ValueError("Invalid model selected.")

        return model

    def load_image(self, image_path: str) -> str:
        try:
            with open(image_path, "rb") as image_file:
                image = Image.open(image_file)
                buffered = io.BytesIO()
                image.save(buffered, format="JPEG")
                return base64.b64encode(buffered.getvalue()).decode('utf-8')
        except Exception as e:
            print(f"Error loading image: {e}")
            return ""

    def ask_question(self, text: str, model: str, image_path: str = None) -> dict:
        if image_path:
            response = self.image_request.send(text, image_path, model)
        else:
            response = self.text_request.send(text, model)

        self.history.append((text, response))
        return response

    def get_history(self) -> list:
        return self.history

    def clear_history(self) -> None:
        self.history.clear()


