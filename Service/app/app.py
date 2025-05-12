from fastapi import APIRouter
from pydantic import BaseModel
from fastapi import FastAPI, UploadFile, Form, HTTPException
from Service.model.non_login import NonLogin
from Service.common.http.transcription_request import TranscriptionRequest
from Service.common.http.transcription_response import TranscriptionResponse
from Service.model.speech_model import SpeechRecognitionModel
from Service.common.http.chatbot_request import ChatbotRequest
from Service.common.http.chatbot_response import ChatbotResponse
from Service.model.non_login_speech_answer import NonLoginSpeechAnswer
from Service.model_service.non_login_chatbot import non_login_chatbot

# non_login_model = NonLogin()
speech_model = SpeechRecognitionModel()
non_login_speech_answer = NonLoginSpeechAnswer()

router = APIRouter(
    prefix = "/non-login",
    tags = ["non-login"]
)


@router.post("/chatbot", response_model = ChatbotResponse)
async def non_login(parameters: ChatbotRequest):
    

    place = parameters.place
    info  = parameters.info
    chatbot_answer = non_login_chatbot(place, info)
    # print(f"chatbot Answer is: {chatbot_answer.response} and Chatbot audio is {len(chatbot_answer.audio)}")
    return ChatbotResponse(answer = chatbot_answer.response, audio_response = chatbot_answer.audio ,success = True)     


@router.post("/audio_chatbot", response_model=TranscriptionResponse)
async def audio_chatbot(
    file: UploadFile,
):
    try:
        content = await file.read()
        print(f"Content: {len(content)}")
        question = speech_model.transcribe(content)
        print(f"Received audio input, transcribed to: {question}")
        
        answer = non_login_speech_answer.invoke(question)
        print("Answer", answer)
        
        return TranscriptionResponse(
            question=question,
            answer=answer,
            success=True
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error processing input: {str(e)}"
        )
    