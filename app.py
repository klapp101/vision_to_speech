from openai import OpenAI
import cv2
import time
import base64
import requests

client = OpenAI(api_key='API_KEY_HERE')

class CameraApp:
    def __init__(self, camera_index, api_key):
        self.camera_index = camera_index
        self.api_key = api_key

    def initialize_camera(self):
        self.cap = cv2.VideoCapture(self.camera_index)
        if not self.cap.isOpened():
            print("Cannot open camera")
            return False
        return True

    def capture_image(self, filename='capture.jpg'):
        if not self.initialize_camera():
            return False
        # Give the camera some warm-up time
        time.sleep(2)
        # Capture a few dummy frames to allow the camera's autoexposure to adjust
        for _ in range(10):
            self.cap.read()
        # Now capture the actual frame
        ret, frame = self.cap.read()
        if ret:
            cv2.imwrite(filename, frame)
            print("Image captured successfully")
        else:
            print("Failed to capture image")
        # When everything done, release the capture
        self.cap.release()
        cv2.destroyAllWindows()
        return ret

    def encode_image(self, image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def send_request(self, image_data):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        payload = {
            "model": "gpt-4-vision-preview",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Tell me about this image. Limit your response to 100 words."
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_data}"
                            }
                        }
                    ]
                }
            ],
            "max_tokens": 300
        }
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        return response.json()

    def save_response_as_audio(self, response_data):
        response = client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=response_data['choices'][0]['message']['content'],
        )
        response.stream_to_file("output.mp3")

    def openai_api_calculate_cost(self, usage, model="gpt-4-1106-vision-preview"):
      pricing = {
          'gpt-3.5-turbo-1106': {
              'prompt': 0.001,
              'completion': 0.002,
          },
          'gpt-4-8k': {
              'prompt': 0.03,
              'completion': 0.06,
          },
          'gpt-4-32k': {
              'prompt': 0.06,
              'completion': 0.12,
          },
          'gpt-4-1106-vision-preview': {
              'prompt': 0.01,
              'completion': 0.03,
          }
      }

      try:
          model_pricing = pricing[model]
      except KeyError:
          raise ValueError("Invalid model specified")
      
      prompt_cost = usage['prompt_tokens'] * model_pricing['prompt'] / 1000
      completion_cost = usage['completion_tokens'] * model_pricing['completion'] / 1000

      total_cost = prompt_cost + completion_cost
      print(f"\nTokens used:  {usage['prompt_tokens']:,} prompt + {usage['completion_tokens']:,} completion = {usage['total_tokens']:,} tokens")
      print(f"Total cost for {model}: ${total_cost:.4f}\n")

      return total_cost

# Main execution
camera_app = CameraApp(camera_index=1, api_key=client.api_key)
if camera_app.capture_image():
    encoded_image = camera_app.encode_image('capture.jpg')
    response_data = camera_app.send_request(encoded_image)
    total_cost = camera_app.openai_api_calculate_cost(response_data['usage'])
    camera_app.save_response_as_audio(response_data)
