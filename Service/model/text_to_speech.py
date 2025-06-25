import pyttsx3
import os
import base64
import uuid


class TTS():
    def __init__(self):
        self.engine = pyttsx3.init()
        self.audio_dir = r'D:\toursim\updated\Backend_Algorithm_tourism_App\saved_audio'

    def text_to_speech_and_show_bytes(self, text: str, mode: str = 'ZH'):
        """Convert text to speech, save it with unique name, return base64 audio and file path"""
        try:
            if mode == 'ZH':
                input_voice, input_language = 'Chinese', 'ZH'
            else:
                input_voice, input_language = 'English', 'EN'

            # Initialize the engine
            self.engine = pyttsx3.init()
            
            # Try to set voice
            voices = self.engine.getProperty('voices')
            for voice in voices:
                if input_voice in voice.name or input_language in voice.languages:
                    self.engine.setProperty('voice', voice.id)
                    break
            
            # Generate unique filename and full path
            unique_id = uuid.uuid4().hex
            filename = f"audio_{unique_id}.mp3"
            full_path = os.path.join(self.audio_dir, filename)
            
            # Save to file
            self.engine.save_to_file(text, full_path)
            self.engine.runAndWait()
            
            # Read the file back as bytes
            with open(full_path, 'rb') as f:
                audio_bytes = f.read()
            audio_bytes_64 = base64.b64encode(audio_bytes).decode('utf-8')

            return audio_bytes_64, full_path
            
        except Exception as e:
            print(f"Error: {e}")
            return None, None
