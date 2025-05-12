import streamlit as st
import pyaudio
import wave
import io
import requests
import threading
from datetime import datetime
import os
import base64

# Configuration
TRANSCRIPTION_API_URL = "http://localhost:8000/algorithm/api/non-login/audio_chatbot"
CHATBOT_API_URL = "http://localhost:8000/algorithm/api/non-login/chatbot"
AUDIO_DIR = "recordings"
os.makedirs(AUDIO_DIR, exist_ok=True)

# Audio settings
SAMPLE_RATE = 16000
CHUNK_SIZE = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1

# Initialize PyAudio
p = pyaudio.PyAudio()

def record_audio(stop_flag, audio_frames):
    stream = p.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=SAMPLE_RATE,
        input=True,
        frames_per_buffer=CHUNK_SIZE
    )
    while not stop_flag.is_set():
        data = stream.read(CHUNK_SIZE, exception_on_overflow=False)
        audio_frames.append(data)
    stream.stop_stream()
    stream.close()

def audio_frames_to_bytes(audio_frames):
    audio_data = b''.join(audio_frames)
    buffer = io.BytesIO()
    with wave.open(buffer, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(audio_data)
    buffer.seek(0)
    return buffer

def transcribe_audio(audio_data):
    try:
        files = {'file': ('audio.wav', audio_data, 'audio/wav')}
        response = requests.post(TRANSCRIPTION_API_URL, files=files)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {'error': f"Transcription failed: {str(e)}"}

def query_chatbot(place, info):
    try:
        payload = {"place": place, "info": info}
        response = requests.post(CHATBOT_API_URL, json=payload)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {'error': f"Chatbot query failed: {str(e)}"}

# Streamlit UI
st.title("🎤 Voice-Activated Chatbot")
st.markdown("Record your voice or write your query to interact with the chatbot.")

if "recording" not in st.session_state:
    st.session_state.recording = False
if "audio_frames" not in st.session_state:
    st.session_state.audio_frames = []
if "stop_flag" not in st.session_state:
    st.session_state.stop_flag = threading.Event()

# Start/Stop buttons
col1, col2 = st.columns(2)
with col1:
    if st.button("🎙️ Start Recording", disabled=st.session_state.recording):
        st.session_state.recording = True
        st.session_state.stop_flag.clear()
        st.session_state.audio_frames = []
        threading.Thread(
            target=record_audio,
            args=(st.session_state.stop_flag, st.session_state.audio_frames),
            daemon=True
        ).start()

with col2:
    if st.button("⏹️ Stop Recording", disabled=not st.session_state.recording):
        st.session_state.recording = False
        st.session_state.stop_flag.set()
        st.success("Recording stopped.")
        audio_data = audio_frames_to_bytes(st.session_state.audio_frames)
        transcription_result = transcribe_audio(audio_data)

        if "error" in transcription_result:
            st.error(transcription_result["error"])
        else:
            question = transcription_result.get("question", "")
            st.session_state.transcribed_question = question
            st.subheader("📝 Transcription")
            st.write(f"**Transcribed Question:** {question}")

        st.session_state.audio_frames = []

# Recording status
if st.session_state.recording:
    st.warning("🔴 Recording... Speak now.")
else:
    st.info("🟢 Ready to record.")

# Chatbot Input Section - Always Visible
st.markdown("---")
st.subheader("💬 Text-Based Chatbot Query")
with st.form("chatbot_form"):
    default_place = ""
    default_info = st.session_state.get("transcribed_question", "")
    place = st.text_input("Place", value=default_place)
    info = st.text_area("Info", value=default_info, height=100)
    submit = st.form_submit_button("Get Chatbot Answer")

    if submit and place and info:
        chatbot_result = query_chatbot(place, info)

        if "error" in chatbot_result:
            st.error(chatbot_result["error"])
        else:
            st.subheader("🤖 Chatbot Response")
            st.write(f"**Answer:** {chatbot_result.get('answer', 'No answer')}")

            # Audio Playback (if audio_response is base64 or bytes)
            audio_response = chatbot_result.get("audio_response")
            if audio_response:
                try:
                    # Decode if base64
                    if isinstance(audio_response, str):
                        audio_bytes = base64.b64decode(audio_response)
                    else:
                        audio_bytes = audio_response
                    st.audio(audio_bytes, format='audio/wav')
                except Exception as e:
                    st.warning(f"Audio could not be played: {e}")