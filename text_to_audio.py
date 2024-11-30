import whisper
import os
from pydub import AudioSegment
from tqdm import tqdm
import torch
import sys
import logging

torch.set_printoptions(profile="none")
logging.getLogger("torch").setLevel(logging.ERROR) 
logging.getLogger("whisper").setLevel(logging.ERROR) 
logging.getLogger("openai").setLevel(logging.ERROR)
logging.getLogger("httpx").setLevel(logging.ERROR)

def split_audio(file_path, chunk_duration_ms=30000):
    """Split audio into chunks of chunk_duration_ms milliseconds."""
    audio = AudioSegment.from_file(file_path)
    chunks = []
    for i in range(0, len(audio), chunk_duration_ms):
        chunks.append(audio[i:i + chunk_duration_ms])
    return chunks

def transcribe_audio_with_progress(file_path, output_file, model_name="base", chunk_duration_ms=30000):
    """Transcribe audio with progress tracking and save transcription incrementally."""
    model = whisper.load_model(model_name)
    audio_chunks = split_audio(file_path, chunk_duration_ms)
    total_chunks = len(audio_chunks)
 
    # Open output file in write mode
    with open(output_file, "w", encoding="utf-8") as f:
        with tqdm(total=total_chunks, desc="Transcribing", unit="chunk") as pbar:
            for i, chunk in enumerate(audio_chunks):
                # Save the chunk to a temporary file
                chunk_path = f"temp_chunk_{i}.wav"
                chunk.export(chunk_path, format="wav")

                # Transcribe the chunk
                result = model.transcribe(chunk_path)
                chunk_transcription = result["text"]

                # Write transcription to the file
                f.write(chunk_transcription + "\n")
                f.flush()  # Ensure it writes immediately to disk

                # Cleanup temporary chunk file
                os.remove(chunk_path)

                # Update progress bar
                pbar.update(1)

def run_trasncription():
    audio_path = "downloads/audio.mp3"
    absolute_path = os.path.abspath(audio_path)
    output_file_path = "transcription.txt"

    transcribe_audio_with_progress(absolute_path, output_file_path)

    print(f"Transcription saved to {output_file_path}")
