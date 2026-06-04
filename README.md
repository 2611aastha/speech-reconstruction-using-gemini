# Speech Reconstruction Using Visual Speech Recognition

## Overview

Speech Reconstruction Using Visual Speech Recognition is a Python-based project that reconstructs speech from a silent video. The system analyzes lip movements in a video, predicts the spoken text using Google's Gemini AI model, and then converts the predicted text back into speech using Text-to-Speech (TTS) technology.

This project demonstrates the integration of Computer Vision, Generative AI, and Speech Synthesis to create an end-to-end speech reconstruction pipeline.

---

## Features

* Upload and analyze silent video recordings
* Verify video validity before processing
* Perform lip-reading using Google's Gemini AI model
* Generate text transcription from visual speech cues
* Convert predicted text into audible speech
* Save reconstructed speech as an MP3 audio file
* Simple command-line interface

---

## Technologies Used

* Python
* Google Gemini API
* OpenCV
* gTTS (Google Text-to-Speech)
* tqdm
* IPython

---

## Project Workflow

1. User provides a Gemini API Key.
2. User provides the path to a silent video.
3. OpenCV verifies the video and checks frame availability.
4. The video is uploaded to Gemini AI.
5. Gemini analyzes the speaker's lip movements and generates a transcription.
6. The predicted text is returned to the application.
7. gTTS converts the transcription into speech.
8. The reconstructed audio is saved as an MP3 file.

---

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd Speech-Reconstruction-Project
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate the environment:

#### Windows

```bash
venv\Scripts\activate
```

#### Linux / Mac

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Running the Project

Run the application:

```bash
python main.py
```

The program will ask for:

1. Gemini API Key
2. Path to the silent video file

Example:

```text
Enter your Gemini API Key (Required):
Enter the path to your silent video file:
```

After successful processing, an audio file named:

```text
reconstructed_audio.mp3
```

will be generated in the project directory.

---

## Sample Output

```text
Status: SUCCESS
Transcription (VSR Output): "Hello everyone"
Voice reconstruction complete.
Audio saved as 'reconstructed_audio.mp3'
```

---

## Limitations

* Lip-reading accuracy depends heavily on video quality.
* Best results are achieved with a frontal face view.
* Short and clearly spoken phrases provide better predictions.
* Gemini is used for visual speech analysis and may not always produce perfect transcriptions.

---

## Future Improvements

* Real-time webcam support
* Advanced face and lip tracking
* Dedicated Visual Speech Recognition models
* Speaker voice cloning
* Web-based user interface
* Multi-language support

---

## Author

**Aastha Deep**

B.Tech Computer Engineering Student

Passionate about Artificial Intelligence, Computer Vision, Data Analytics, and Software Development.
