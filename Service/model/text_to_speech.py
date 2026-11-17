import multiprocessing
import pyttsx3
import base64
import uuid
import os
from pathlib import Path


class TTS:
    def __init__(self):
        # Set TOURISM_AUDIO_DIR to choose another output directory.
        default_dir = Path(__file__).resolve().parents[2] / "generated_audio"
        self.audio_dir = os.environ.get("TOURISM_AUDIO_DIR", str(default_dir))
        os.makedirs(self.audio_dir, exist_ok=True)

    def _run_tts(self, text, mode, file_path):
        try:
            engine = pyttsx3.init()
            voices = engine.getProperty("voices")

            mode = mode.upper()
            selected_voice = None

            for voice in voices:
                voice_name = voice.name.lower()
                voice_id = voice.id.lower()

                languages = []
                for lang in voice.languages:
                    if isinstance(lang, bytes):
                        lang = lang.decode("utf-8", errors="ignore")
                    languages.append(str(lang).lower())

                language_info = " ".join(languages)

                if mode == "ZH":
                    if (
                        "chinese" in voice_name
                        or "mandarin" in voice_name
                        or "zh" in voice_id
                        or "zh" in language_info
                    ):
                        selected_voice = voice.id
                        break

                elif mode == "EN":
                    if (
                        "english" in voice_name
                        or "en-" in voice_id
                        or "en_" in voice_id
                        or "en-" in language_info
                        or "en_" in language_info
                    ):
                        selected_voice = voice.id
                        break

            if selected_voice:
                engine.setProperty("voice", selected_voice)
            else:
                print(f"No {mode} voice found. Using default voice.")

            engine.save_to_file(text, file_path)
            engine.runAndWait()
            engine.stop()

        except Exception as e:
            print(f"TTS generation error: {e}")

    def text_to_speech_and_show_bytes(self, text, mode="ZH"):
        try:
            mode = mode.upper()

            if mode not in ("ZH", "EN"):
                print(f"Unsupported language mode: {mode}")
                return None, None

            filename = f"{uuid.uuid4().hex}.mp3"
            file_path = os.path.join(self.audio_dir, filename)

            process = multiprocessing.Process(
                target=self._run_tts,
                args=(text, mode, file_path)
            )

            process.start()
            process.join()

            if process.exitcode != 0:
                print(f"TTS process failed with exit code: {process.exitcode}")
                return None, None

            if not os.path.exists(file_path):
                print(f"Audio file not generated: {file_path}")
                return None, None

            if os.path.getsize(file_path) == 0:
                print(f"Generated audio file is empty: {file_path}")
                return None, None

            with open(file_path, "rb") as audio_file:
                audio_bytes = audio_file.read()

            audio_base64 = base64.b64encode(
                audio_bytes
            ).decode("utf-8")

            return audio_base64, file_path

        except Exception as e:
            print(f"Text-to-speech error: {e}")
            return None, None
