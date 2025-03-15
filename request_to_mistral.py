MISTAL_API_KEY = "x"

from mistralai import Mistral
import base64

class TextRequest:
    """
    Класс отвечает за отправку текстовых запросов
    """
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
        self.client = Mistral(api_key=self.api_key)
        
    def send(self, text: str, model: str = "mistral-large-latest") -> dict:
        """
        Основной метод отправки текстового запроса к API Mistral
        """
        response = self.client.chat.complete(
            model=model,
            messages=[
                {
                    "role":"user",
                    "content": text
                }
            ]
        )
        #Формируем ответ в виде словаря для работы с историей чата 
        result = {
            "role": "assistant",
            "content": response.choices[0].message.content
        }

        return result
    
class ImageRequest:
    """
    Класс отвечает за отправку запросов, включающих изображение.
    """
    def __init__(self, api_key: str) ->None:
        self.api_key = api_key
        self.client = Mistral(api_key=self.api_key)

    def __encode_image(self, image_path: str) -> str:
        """Переводит изображение в формат base64"""
        try:
            with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode('utf-8')
        except FileNotFoundError:
            print(f"Error: the file {image_path} was not found.")
            return ""
        except Exception as e:
            print(f"Error: {e}")
            return ""
    
    def send(self, text: str, image_path: str, model: str = "pixtral-12b-2409") -> dict:
        """
        Основной метод отравки мультимодального  запроса
        """
        # Получаем изображение в формате base64
        base64_image = self.__encode_image(image_path)
        # Формируем сообщение для чата
        messages = [
            {
                "role" : "user",
                "content" : [
                    {
                        "type" : "text",
                        "text" : text
                    },
                    {
                        "type" : "image_url",
                        "image_url" : f"data:image/jpeg;base64,{base64_image}"
                    }
                ]
            }
        ]

        chat_response = self.client.chat.complete(
            model=model,
            messages=messages
        )

        # Формируем ответ в виде словаря для работы с историей чата
        result = {
            "role" : "assistant", 
            "content" : chat_response.choices[0].message.content
        }

        return result
    
# # text_request = TextRequest(api_key=MISTAL_API_KEY)
# image_request = ImageRequest(api_key=MISTAL_API_KEY)
# # text_response = text_request.send("Бонжур", model="mistral-large-latest")
# # print(text_response)
# image_response = image_request.send("что изображено на картинке", r"C:\Users\User-X\Desktop\Python\Request_to_Mistral\357d7153677451.593d686ecec5f.png", model= "pixtral-12b-2409")
# print(image_response)
