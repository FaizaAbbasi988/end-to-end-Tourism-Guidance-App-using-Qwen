from transformers import BarkModel
from transformers import AutoProcessor
import numpy as np
import torch
import os

class TextToAudio():
    def __init__(self):
        self.load_all_models()
        # self.voice_preset = r"D:\Backend_Algorithm_travel_assistance\downloaded_models\zh_speaker_7.npz"
    
    def load_all_models(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.downloaded_models = os.path.abspath(os.path.join(self.base_dir, '..', '..', 'downloaded_models'))
        self.voice_preset = os.path.join(self.downloaded_models, 'zh_speaker_7.npz')
        self.model_path = os.path.join(self.downloaded_models, 'barksmall')
        # model_path = r'D:\Backend_Algorithm_travel_assistance\downloaded_models\barksmall'
        self.model = BarkModel.from_pretrained(self.model_path).to("cuda")
        self.processor = AutoProcessor.from_pretrained(self.model_path, padding=True, truncation=True)
    
    def generate(self, text):
        chunks = self.split_text(text)
        audio_segments = []

        for chunk in chunks:
            inputs = self.processor(chunk, voice_preset=self.voice_preset).to("cuda")
            inputs = {k: v.to("cuda") for k, v in inputs.items()}
            output = self.model.generate(**inputs)
            audio_array = output.cpu().numpy().squeeze()
            audio_segments.append(audio_array)
        
        final_audio = np.concatenate(audio_segments)
        return final_audio

    def split_text(self, text, max_len=30):
        """Splits the text into chunks based on a character limit, prioritizing sentence completion at full stops or commas."""
        if len(text) <= max_len:
            return [text]
        
        chunks = []
        start = 0
        text_length = len(text)
        
        while start < text_length:
            end = start + max_len
            window_end = min(end, text_length)
            
            # Find the last full stop in the current window
            last_full_stop = text.rfind('。', start, window_end)
            if last_full_stop != -1:
                # Include the full stop by setting end to last_full_stop + 1
                end = last_full_stop + 1
            else:
                # No full stop found, look for the last comma
                last_comma = text.rfind('，', start, window_end)
                if last_comma != -1:
                    # Include the comma by setting end to last_comma + 1
                    end = last_comma + 1
                else:
                    # No punctuation found, split at max_len or remaining text
                    end = window_end
            
            # Ensure we don't exceed the text length
            end = min(end, text_length)
            chunk = text[start:end].strip()
            if chunk:  # Avoid adding empty chunks
                chunks.append(chunk)
            start = end  # Move to the next part
        
        return chunks