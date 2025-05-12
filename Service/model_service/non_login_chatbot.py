from Service.model.non_login import NonLogin
from Service.model.text_to_speech import TextToAudio
from pydantic import BaseModel
from typing import Optional
import numpy as np
import io
from scipy.io.wavfile import write
import base64

class NonLoginChatBotResponse(BaseModel):
    response: str
    audio: Optional[str] = None


non_login_model = NonLogin()
text_to_speech = TextToAudio()

def non_login_chatbot(place: str, info: str):
    if info not in ['文化介绍','特色美食']:
        answer = non_login_model.invoke(place, info)
        return NonLoginChatBotResponse(response = answer)
    else:
        answer = non_login_model.invoke(place, info)
        speech_answer = text_to_speech.generate(answer)
        buffer = io.BytesIO()
        write(buffer, 24000, speech_answer.astype(np.float32))  # Bark uses 24kHz
        audio_bytes = buffer.getvalue()
        audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
        return NonLoginChatBotResponse(response = answer, audio = audio_base64)

