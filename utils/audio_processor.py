import yt_dlp
import os
import ffmpeg

DOWNLOAD_DIR = 'downloades'
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


def download_youtube_audio(url: str) -> str:
    output_path = os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s")
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_path,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "wav",
                "preferredquality": "192",
            }
        ],
        "quiet": True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info).replace(".webm", ".wav").replace(".m4a", ".wav")
    return filename


def _get_audio_duration(path: str) -> float:
    probe = ffmpeg.probe(path)
    return float(probe["format"]["duration"])


def convert_to_wav(input_path: str) -> str:
    """Convert any audio/video file to WAV format using ffmpeg."""
    output_path = os.path.splitext(input_path)[0] + "_converted.wav"
    (
        ffmpeg.input(input_path)
        .output(output_path, ac=1, ar=16000, format="wav")
        .overwrite_output()
        .run(quiet=True)
    )
    return output_path


def chunk_audio(wav_path: str, chunk_minutes: int = 10) -> list:
    duration = _get_audio_duration(wav_path)
    chunk_seconds = chunk_minutes * 60

    chunks = []
    start = 0

    while start < duration:
        chunk_path = f"{wav_path}_chunk_{len(chunks)}.wav"
        (
            ffmpeg.input(wav_path, ss=start, t=chunk_seconds)
            .output(chunk_path, ac=1, ar=16000, format="wav")
            .overwrite_output()
            .run(quiet=True)
        )
        chunks.append(chunk_path)
        start += chunk_seconds

    return chunks

def process_input(source: str) -> list:
    if source.startswith("http://") or source.startswith("https://"):
        print("Detected YouTube URL. Downloading audio...")
        wav_path = download_youtube_audio(source)
    else:
        print("Detected local file. Converting to WAV...")
        wav_path = convert_to_wav(source)

    print("Chunking audio...")
    chunks = chunk_audio(wav_path)
    print(f"Audio ready — {len(chunks)} chunk(s) created.")
    return chunks


