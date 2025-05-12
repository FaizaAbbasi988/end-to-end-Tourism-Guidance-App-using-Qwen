from funasr import AutoModel


class SpeechRecognitionModel:
    def __init__(self):
        self.model = None
        self.load_model()
    
    def load_model(self):
        """Initialize the ASR model with specified configurations"""
        self.model = AutoModel(
            model=r"D:\Backend_Algorithm_travel_assistance\downloaded_models\paraformer-zh", 
            model_revision="v2.0.4",
            vad_model=r"D:\Backend_Algorithm_travel_assistance\downloaded_models\fsmn-vad", 
            vad_model_revision="v2.0.4",
            punc_model=r"D:\Backend_Algorithm_travel_assistance\downloaded_models\ct-punc", 
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
    