# CameraApp

CameraApp is a Python application that integrates OpenAI's GPT-4 Vision API and Audio API to capture an image using a laptop camera, interpret the image using AI, and provide an audio output of the AI's description.

## Features

- Capture images from a specified camera index.
- Encode the image to a base64 string.
- Send the encoded image to OpenAI's API for interpretation.
- Convert the API's text response to audio.
- Calculate the cost of API usage based on token count.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.10.7+
- OpenAI Python library
- OpenCV-Python library
- A valid OpenAI API key

## Installation

Clone the repository to your local machine:

```sh
git clone https://github.com/klapp101/camera-app.git
```

Navigate to the project directory:

```sh
cd camera-app
```

Install the required Python packages:

```sh
pip install openai opencv-python requests
```

## Usage

To use CameraApp, follow these steps:

1. Replace `'API_KEY_HERE'` with your actual OpenAI API key.

```python
client = OpenAI(api_key='YOUR_API_KEY')
```

2. Initialize the CameraApp with the appropriate camera index and your OpenAI API key.

```python
camera_app = CameraApp(camera_index=0, api_key='YOUR_API_KEY')
```

3. Call the `capture_image` method to take a picture with the camera.

4. The image will be processed, and the AI's interpretation will be output as an audio file named `output.mp3`.

## Contributing

To contribute to CameraApp, follow these steps:

1. Fork this repository.
2. Create a branch: `git checkout -b <branch_name>`.
3. Make your changes and commit them: `git commit -m '<commit_message>'`
4. Push to the original branch: `git push origin <project_name>/<location>`
5. Create the pull request.

Alternatively, see the GitHub documentation on [creating a pull request](https://help.github.com/articles/creating-a-pull-request/).

## Contact

If you want to contact me you can reach me at `ryan.klapper.ma@gmail.com`.
