"""
Audio processing functions for the Reverbed package
"""

import soundfile as sf
from pedalboard import Pedalboard, Reverb
from math import trunc
from yt_dlp import YoutubeDL

def download_audio(video_url, output_path, audio_format='wav'):
    """Download audio from a YouTube video"""
    try:
        # Remove any existing extension
        output_path = output_path.rsplit('.', 1)[0]
        
        URLS = [video_url]
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'wav',
            }],
            'outtmpl': output_path,
        }
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download(URLS)
        print(f'Audio downloaded to {output_path}.wav')
    except Exception as e:
        print(f"Error downloading audio: {e}")
        raise

def slowed_reverb(audio, output, speed=0.4, room_size=0.75, damping=0.5, wet_level=0.08, dry_level=0.2):
    """Apply reverb effect to audio"""
    try:
        if '.wav' not in audio:
            print('Audio needs to be .wav!')
            return

        print('Importing audio...')
        print(audio)
        audio_data, sample_rate = sf.read(audio)

        print('Slowing audio...')
        sample_rate -= trunc(sample_rate*speed)

        # Only add reverb if reverb_speed is specified
        print('Adding reverb...')
        board = Pedalboard([Reverb(
            room_size=room_size,
            damping=damping,
            wet_level=wet_level,
            dry_level=dry_level
        )])
        effected = board(audio_data, sample_rate)

        print('Exporting audio...')
        sf.write(output, effected, sample_rate)
        print(f'Audio exported to {output}')
    except Exception as e:
        print(f"Error in slowed_reverb: {e}")
        raise 