
import io
import soundfile as sf
import numpy as np
import librosa 

from fastapi import APIRouter
from pydantic import BaseModel
from fastapi import FastAPI, UploadFile, Form, HTTPException
# from Service.model.non_login import NonLogin
# from Service.common.http.transcription_request import TranscriptionRequest
# from Service.common.http.transcription_response import TranscriptionResponse
# from Service.model.speech_model import SpeechRecognitionModel
# from Service.common.http.chatbot_request import ChatbotRequest
# from Service.common.http.chatbot_response import ChatbotResponse
# from Service.model.non_login_speech_answer import NonLoginSpeechAnswer
# # from Service.model_service.non_login_chatbot import non_login_chatbot
# # from Service.model_service.non_login_chatbot import non_audio_chatbot

# # non_login_model = NonLogin()
# speech_model = SpeechRecognitionModel()
# non_login_speech_answer = NonLoginSpeechAnswer()

router = APIRouter(
    prefix = "/non-login",
    tags = ["non-login"]
)
# @router.post("/chatbot", response_model = ChatbotResponse)
# async def non_login(parameters: ChatbotRequest):
    

#     place = parameters.place
#     info  = parameters.info
#     # chatbot_answer = non_login_chatbot(place, info)
#     r = 'None'
#     a = 'None'
#     return ChatbotResponse(answer = r, audio_response = a ,success = True)     
# @router.post("/audio_chatbot", response_model=TranscriptionResponse)
# async def audio_chatbot(
#     file: UploadFile,
# ):
#     try:
#         content = await file.read()
#         r = 'None'
#         a = 'None'
#         # result = non_audio_chatbot(content)
#         return TranscriptionResponse(
#             question = r,
#             answer = a,
#             success = True
#         )
#     except Exception as e:
#         raise HTTPException(
#             status_code=500, 
#             detail=f"Error processing input: {str(e)}"
#         )