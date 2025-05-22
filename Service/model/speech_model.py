from funasr import AutoModel
import os

class SpeechRecognitionModel:
    def __init__(self):
        self.model = None
        self.load_model()
    
    def load_model(self):
        """Initialize the ASR model with specified configurations using relative paths"""
        base_dir = os.path.dirname(os.path.abspath(__file__))
        models_dir = os.path.abspath(os.path.join(base_dir, '..', '..', 'downloaded_models'))

        self.model = AutoModel(
            model=os.path.join(models_dir, 'paraformer-zh'), 
            model_revision="v2.0.4",
            vad_model=os.path.join(models_dir, 'fsmn-vad'), 
            vad_model_revision="v2.0.4",
            punc_model=os.path.join(models_dir, 'ct-punc'), 
            punc_model_revision="v2.0.4"
        )

    def transcribe(self, audio_data):
        """Transcribe audio data to text"""
        res = self.model.generate(
            input=audio_data,
            cache={},
            language="zn",
            use_itn=True,
            batch_size_s=60,
            merge_vad=True,
            merge_length_s=15,
        )
        return res[0]["text"] if res else ""
    