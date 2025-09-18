import streamlit as st
from pydub import AudioSegment
import math
import tempfile
import os

st.title("Upload Audio, Split into 5-Minute Chunks, Playback & Download")

uploaded_file = st.file_uploader("Upload WAV or MP3 audio file", type=["wav", "mp3"])

if uploaded_file is not None:
    # PyDub expects a file-like object; always use from_file for broad compatibility
    audio = AudioSegment.from_file(uploaded_file)
    st.audio(uploaded_file)  # Optionally play original file

    chunk_duration_ms = 5 * 60 * 1000  # 5 minutes in ms
    total_duration_ms = len(audio)
    num_chunks = math.ceil(total_duration_ms / chunk_duration_ms)
    st.write(f"Full audio duration: {total_duration_ms/60000:.2f} minutes")
    st.write(f"Number of 5-minute chunks: {num_chunks}")

    # For each chunk, prepare and display
    for i in range(num_chunks):
        start_ms = i * chunk_duration_ms
        end_ms = min((i + 1) * chunk_duration_ms, total_duration_ms)
        chunk = audio[start_ms:end_ms]
        chunk_label = f"Chunk {i+1} ({(end_ms-start_ms)/1000:.2f} seconds)"

        # Use a NamedTemporaryFile so the chunk is available for download and playback,
        # it will auto cleanup on close except on Windows, but we'll handle that.
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as chunk_tempfile:
            chunk.export(chunk_tempfile.name, format="wav")
            chunk_tempfile.seek(0)
            chunk_bytes = chunk_tempfile.read()

        st.write(chunk_label)
        st.audio(chunk_bytes, format="audio/wav")
        st.download_button(
            label=f"Download {chunk_label}",
            data=chunk_bytes,
            file_name=f"chunk_{i+1}.wav",
            mime="audio/wav"
        )

        # Clean up the temp file if still on disk (important for hosted environments)
        try:
            os.remove(chunk_tempfile.name)
        except Exception:
            pass
