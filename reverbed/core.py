import json
from os import makedirs, remove
from .utils import remove_illegal_characters, is_valid_youtube_url
from .audio import download_audio, slowed_reverb
from .video import download_video, combine_audio_video
from pytube import YouTube


class Reverbed:
    def __init__(self):
        # Create necessary directories
        makedirs("./Songs", exist_ok=True)
        makedirs("./Finished Product", exist_ok=True)

        # Initialize instance variables
        self.audio_url = None
        self.loop_video = None
        self.audio_speed = 1.0
        self.room_size = 0.75
        self.damping = 0.5
        self.wet_level = 0.08
        self.dry_level = 0.2
        self.start_time = "00:00"
        self.end_time = None
        self.final_video = None
        self.audio_title = None
        self.video_title = None
        self.audio_output_path = None

    def get_video_title(self, url):
        """Safely get video title from YouTube URL"""
        try:
            if not is_valid_youtube_url(url):
                raise ValueError("Invalid YouTube URL")
            yt = YouTube(url)
            return yt.title
        except Exception as e:
            print(f"Error getting video title: {e}")
            return "video"

    def process_noninteractive(self):
        """Non-interactive processing method for API integration"""
        try:
            if not self.audio_url or not self.loop_video:
                raise ValueError("Both audio_url and loop_video must be provided")

            # Get video titles
            self.audio_title = remove_illegal_characters(self.get_video_title(self.audio_url))
            self.video_title = remove_illegal_characters(self.get_video_title(self.loop_video))

            # Download audio
            self.audio_output_path = f'{self.audio_title}.wav'
            download_audio(self.audio_url, self.audio_output_path)

            # Apply slowed + reverb effect
            reverb_output = f'reverb - {self.audio_title}.wav'
            slowed_reverb(
                self.audio_output_path,
                reverb_output,
                self.audio_speed,
                self.room_size,
                self.damping,
                self.wet_level,
                self.dry_level
            )
            remove(self.audio_output_path)

            # Download loop video
            loop_output = f'{self.video_title}.mp4'
            download_video(self.loop_video, loop_output, self.start_time, self.end_time)

            # Combine reverb audio + loop video
            combine_audio_video(reverb_output, loop_output, self.final_video)

            # Clean up
            remove(loop_output)
            remove(reverb_output)

        except Exception as e:
            print(f"Error in non-interactive process: {e}")
            raise
