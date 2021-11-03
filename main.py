import soundfile as sf
import torch
import uvicorn
from fastapi import FastAPI, UploadFile, File
from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC

# Initialise FastAPI app
app = FastAPI()
# Including defined routes
model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base-100h")
processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-base-100h")


@app.post("/transcribe")
def transcribe(file: UploadFile = File(...)):
    audio, sampling_rate = sf.read(file.file)
    with torch.no_grad():
        input_features = processor(audio, return_tensors="pt").input_values
        logits = model(input_features).logits
        prediction = torch.argmax(logits, dim=-1)
        transcription = processor.batch_decode(prediction)[0]
        return transcription


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
