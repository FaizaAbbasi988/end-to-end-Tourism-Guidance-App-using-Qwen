"""Shared audio preprocessing for the speech-related endpoints.

Convert uploaded WAV/decodable audio into mono 16-kHz WAV bytes for FunASR.
This module has no model initialization side effects.
"""
import io

import librosa
import numpy as np
import soundfile as sf


def preprocess_audio(audio_bytes: bytes) -> bytes:
    buffer = io.BytesIO(audio_bytes)
    audio, sr = sf.read(buffer)
    if audio.ndim == 2:
        audio = np.mean(audio, axis=1)
    if sr != 16000:
        audio = librosa.resample(audio, orig_sr=sr, target_sr=16000)
        sr = 16000
    output = io.BytesIO()
    sf.write(output, audio, sr, format="WAV")
    return output.getvalue()
