import streamlit as st
from pydub import AudioSegment
import math
import tempfile
import os

st.title("Upload Audio, Split into 5-Minute Chunks with Playback & Download")

uploaded_file = st.file_uploader("Upload WAV or MP3 audio file", type=["wav", "mp3"])

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
        if uploaded_file.type == "audio/wav":
            audio = AudioSegment.from_wav(uploaded_file)
        else:
            audio = AudioSegment.from_file(uploaded_file)
        audio.export(tmp_file.name, format="wav")
        audio_path = tmp_file.name

    st.audio(audio_path)  # Play the full uploaded audio

    chunk_duration_ms = 5 * 60 * 1000  # 5 minutes in ms
    total_duration_ms = len(audio)
    num_chunks = math.ceil(total_duration_ms / chunk_duration_ms)

    st.write(f"Full audio duration: {total_duration_ms/60000:.2f} minutes")
    st.write(f"Number of 5-minute chunks: {num_chunks}")

    chunk_files = []

    for i in range(num_chunks):
        start_ms = i * chunk_duration_ms
        end_ms = min((i + 1) * chunk_duration_ms, total_duration_ms)
        chunk = audio[start_ms:end_ms]
        
        chunk_filename = f"chunk_{i+1}.wav"
        chunk.export(chunk_filename, format="wav")
        chunk_files.append(chunk_filename)
        
        st.write(f"Chunk {i+1} duration: {(end_ms - start_ms)/1000:.2f} seconds")
        
        # Audio player for the chunk
        st.audio(chunk_filename)
        
        # Download button for the chunk
        with open(chunk_filename, "rb") as f:
            st.download_button(
                label=f"Download chunk {i+1}",
                data=f,
                file_name=chunk_filename,
                mime="audio/wav"
            )

    # Cleanup temp file
    os.remove(audio_path)
