import os
import sys
import time
import cv2
from google import genai
from google.genai.errors import APIError
from gtts import gTTS
from IPython.display import Audio, display
from tqdm import tqdm

# --- Configuration ---
MODEL_NAME = "gemini-2.5-flash"
MAX_WAIT_SECONDS = 120 # Maximum time to wait for the video to process

def extract_key_frames(video_path):
    """
    Checks if the video is valid and displays a check message. 
    In a real-time app, this would also detect the face, but we simplify it here.
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Could not open video file {video_path}")
        return False
    
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.release()
    
    if frame_count > 10:
        print(f"\n[STEP 1/3] Video verified with {frame_count} frames. Ready for analysis.")
        return True
    else:
        print("Video is too short or invalid. Please ensure a clear video is provided.")
        return False

def visual_speech_recognition(video_path, api_key):
    """
    VSR: Uses the Gemini SDK to upload, process, and analyze the video for transcription.
    """
    print("\n[STEP 2/3] Performing Lip Reading (VSR) - Analyzing video content...")

    video_file = None # Initialize to None for cleanup in case of error
    
    try:
        client = genai.Client(api_key=api_key)
        
        # 1. Upload the file to the Gemini service
        print("   - Uploading video file...")
        video_file = client.files.upload(file=video_path)

        # 2. CRITICAL: Wait for the file to become ACTIVE
        print("   - Waiting for server to finish processing video...")
        start_time = time.time()
        
        while time.time() - start_time < MAX_WAIT_SECONDS:
            status = client.files.get(name=video_file.name).state.name
            
            if status == "ACTIVE":
                print(f"   - File is ready. Status: {status}")
                break
            
            print(f"   - Current status: {status}. Waiting 5 seconds...")
            time.sleep(5)
        
        if status != "ACTIVE":
             print("Error: Video processing timed out.", file=sys.stderr)
             client.files.delete(name=video_file.name)
             return "API ERROR: Video processing timed out."

        # 3. Define the VSR prompt
        prompt = (
            "You are a specialized Visual Speech Recognition (VSR) model. "
            "Analyze the silent video file provided. Focus exclusively on the speaker's "
            "lip and mouth movements to transcribe exactly what they are saying. "
            "Output ONLY the transcribed sentence, with no other commentary."
        )

        # 4. Generate content (Lip Reading)
        print("   - Requesting transcription from model...")
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=[prompt, video_file],
        )

        # 5. Clean up the uploaded file
        client.files.delete(name=video_file.name)
        print("   - Uploaded video file deleted from service.")

        return response.text.strip()

    except APIError as e:
        # Ensure cleanup on API error
        if video_file:
            try: client.files.delete(name=video_file.name)
            except: pass
        print(f"API Error: {e}", file=sys.stderr)
        return "API ERROR: Check API key validity or permissions."
    except Exception as e:
        if video_file:
            try: client.files.delete(name=video_file.name)
            except: pass
        print(f"General Error: {e}", file=sys.stderr)
        return "API ERROR: An unexpected error occurred."


def reconstruct_voice(predicted_text, output_filename='reconstructed_audio.mp3'):
    """
    TTS: Synthesizes the predicted text back into speech audio using gTTS.
    """
    print(f"\n[STEP 3/3] Reconstructing voice from text...")
    
    try:
        # Use gTTS (Text-to-Speech) to generate the audio
        tts = gTTS(text=predicted_text, lang='en')
        tts.save(output_filename)
        
        print(f"   - Voice reconstruction complete. Audio saved as '{output_filename}'")
        print("\nNOTE: You must play the reconstructed audio file manually.")
        
    except Exception as e:
        print(f"Error during voice reconstruction: {e}")


def main():
    """Main execution function for the project."""
    
    print("="*60)
    print("  SIMPLE REAL-TIME LIP READING & VOICE RECONSTRUCTION  ")
    print("="*60)
    
    # Get inputs from the user
    api_key = input("Enter your Gemini API Key (Required): ").strip()
    video_path = input("Enter the path to your silent video file: ").strip()

    if not api_key:
        print("API Key is required. Exiting.")
        return
    if not os.path.exists(video_path):
        print(f"Error: File not found at path: {video_path}")
        return

    # 1. Check video viability
    if not extract_key_frames(video_path):
        return

    # 2. Perform Lip Reading (VSR)
    predicted_text = visual_speech_recognition(video_path, api_key)
    
    # 3. Final Output and Voice Reconstruction (TTS)
    print("\n" + "#"*60)
    print("                  FINAL RESULT                  ")
    print("#"*60)
    
    if predicted_text.startswith("API ERROR"):
        print(f"Status: FAILED")
        print(f"Error Details: {predicted_text}")
    else:
        print(f"Status: SUCCESS")
        print(f"Transcription (VSR Output): '{predicted_text}'")
        
        # Reconstruct the voice
        reconstruct_voice(predicted_text)
        
        print("\n\n--- IMPORTANT: VSR Accuracy Note ---")
        print("Lip reading is highly challenging. For best results, use very short phrases")
        print("and record with a clear, frontal view, speaking slowly and deliberately.")

    print("\n--- Project Execution Complete ---")

if __name__ == '__main__':
    main()