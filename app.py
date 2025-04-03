from re import sub
from pytube import YouTube, Search
from os import remove, makedirs, system, name
from subprocess import run
import moviepy.editor as mp
from random import random
from yt_dlp import YoutubeDL
import soundfile as sf
from pedalboard import Pedalboard, Reverb
from math import trunc
import json
import re
import shutil
import msvcrt  # For Windows keyboard input

class Reverbed:
    def __init__(self):
        # Create necessary directories
        makedirs("./Songs", exist_ok=True)
        makedirs("./Finished Product", exist_ok=True)
        
        # Initialize instance variables
        self.audio_url = None
        self.audio_speed = None
        self.loop_video = None
        self.start_time = None
        self.end_time = None
        self.final_video = None
        self.video_title = None
        self.audio_title = None
        self.audio_output_path = None
        self.reverb_speed = None  # New instance variable for reverb speed
        
        # Load configuration
        try:
            with open('config.json', 'r') as f:
                self.config = json.load(f)
        except FileNotFoundError:
            print("Warning: config.json not found. Creating default config...")
            self.config = {
                "examples": [
                    {
                        "name": "Example 1",
                        "audio_url": "https://www.youtube.com/watch?v=H8E0WIy_vFc",
                        "audio_speed": 0.5,
                        "loop_video": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                        "start_time": "0:00",
                        "end_time": "0:30",
                        "final_video": "example1_output"
                    }
                ]
            }
            with open('config.json', 'w') as f:
                json.dump(self.config, f, indent=4)

    @staticmethod
    def remove_illegal_characters(string):
        return sub(r'[^a-zA-Z0-9 ]', '', string)

    @staticmethod
    def is_valid_youtube_url(url):
        """Check if the URL is a valid YouTube URL"""
        youtube_regex = r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/(watch\?v=|embed/|v/|.+\?v=)?([^"&?/s]{11})'
        return bool(re.match(youtube_regex, url))

    def get_video_title(self, url):
        """Safely get video title from YouTube URL"""
        try:
            if not self.is_valid_youtube_url(url):
                raise ValueError("Invalid YouTube URL")
            
            yt = YouTube(url)
            return yt.title
        except Exception as e:
            print(f"Error getting video title: {e}")
            # Return a default title if we can't get the actual one
            return "video"

    def load_example(self, example):
        """Load values from an example configuration"""
        try:
            self.audio_url = example['audio_url']
            self.audio_speed = example['audio_speed']
            self.loop_video = example['loop_video']
            self.start_time = example['start_time']
            self.end_time = example['end_time']
            self.final_video = example['final_video']
            self.reverb_speed = example.get('reverb_speed')  # Optional reverb speed
            
            # Get titles safely
            self.video_title = self.remove_illegal_characters(self.get_video_title(self.loop_video))
            self.audio_title = self.remove_illegal_characters(self.get_video_title(self.audio_url))
            self.audio_output_path = f'{self.audio_title}.wav'
        except Exception as e:
            print(f"Error loading example: {e}")
            raise

    @staticmethod
    def clear_console():
        """Clear the console screen"""
        # Windows
        if name == 'nt':
            system('cls')
        # macOS/Linux
        else:
            system('clear')

    def assign_values(self):
        try:
            self.clear_console()
            print("\nChoose an option:")
            print("1. Use example configuration")
            print("2. Input custom values")
            print("3. Exit")
            
            choice = input("Enter your choice (1-3): ")
            
            if choice == "1":
                self.clear_console()
                print("\nAvailable examples:")
                for i, example in enumerate(self.config['examples'], 1):
                    print(f"{i}. {example['name']}")
                
                example_choice = int(input("\nSelect an example (enter number): ")) - 1
                if 0 <= example_choice < len(self.config['examples']):
                    self.load_example(self.config['examples'][example_choice])
                    return "yes"
                else:
                    print("Invalid example number")
                    return "none"
                    
            elif choice == "2":
                # Handle audio URL input
                while True:
                    self.clear_console()
                    print("\nEnter YouTube URL or search query for audio:")
                    query = input("> ")
                    if self.is_valid_youtube_url(query):
                        self.audio_url = query
                        break
                    else:
                        print("Searching YouTube...")
                        results = self.search_youtube(query)
                        if results:
                            selected_url = self.select_from_search(results)
                            if selected_url:
                                self.audio_url = selected_url
                                break
                        print("No valid selection made. Please try again.")
                
                # Handle audio speed
                while True:
                    self.clear_console()
                    try:
                        self.audio_speed = float(input("How slow would you like it: "))
                        if 0 < self.audio_speed <= 1:
                            break
                        print("Speed must be between 0 and 1")
                    except ValueError:
                        print("Please enter a valid number")
                
                # Handle loop video input
                while True:
                    self.clear_console()
                    print("\nEnter YouTube URL or search query for loop video:")
                    query = input("> ")
                    if self.is_valid_youtube_url(query):
                        self.loop_video = query
                        break
                    else:
                        print("Searching YouTube...")
                        results = self.search_youtube(query)
                        if results:
                            selected_url = self.select_from_search(results)
                            if selected_url:
                                self.loop_video = selected_url
                                break
                        print("No valid selection made. Please try again.")
                
                self.clear_console()
                self.start_time = input('When would you like the video to start?: ')
                self.end_time = input('When would you like the video to end?: ')
                self.final_video = input("what do you want the end product to be called?: ")
                
                # Get titles safely
                self.video_title = self.remove_illegal_characters(self.get_video_title(self.loop_video))
                self.audio_title = self.remove_illegal_characters(self.get_video_title(self.audio_url))
                self.audio_output_path = f'{self.audio_title}.wav'
                return "yes"
            else:
                print("Ok bye")
                return "none"
        except Exception as e:
            print(f"Error in assign_values: {e}")
            return "none"

    def download_video(self, url, output_path, start_time, end_time):
        try:    
            # Ensure output path has .mp4 extension
            if not output_path.endswith('.mp4'):
                output_path += '.mp4'
                
            # First download the video with more compatible settings
            ydl_opts = {
                'format': 'bestvideo[ext=mp4][height=1080]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                'outtmpl': output_path,
                'merge_output_format': 'mp4',
                'postprocessors': [{
                    'key': 'FFmpegVideoConvertor',
                    'preferedformat': 'mp4',
                }],
            }
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            # Then trim the video using FFmpeg with more compatible settings
            temp_output = output_path.replace('.mp4', '_temp.mp4')
            ffmpeg_cmd = [
                'ffmpeg',
                '-y',  # Overwrite output file if it exists
                '-ss', start_time,
                '-to', end_time,
                '-i', output_path,
                '-c:v', 'libx264',
                '-preset', 'medium',
                '-crf', '23',
                '-c:a', 'aac',
                '-b:a', '192k',
                '-movflags', '+faststart',  # Enable fast start for web playback
                temp_output
            ]
            
            # Run FFmpeg command and capture output
            result = run(ffmpeg_cmd, capture_output=True, text=True)
            if result.returncode != 0:
                print(f"FFmpeg error: {result.stderr}")
                raise Exception("FFmpeg command failed")
            
            # Replace original with trimmed version using Python's file operations
            remove(output_path)
            shutil.move(temp_output, output_path)
            
            print(f'Video downloaded and trimmed to {output_path}')
        except Exception as e:
            print(f"Error downloading video: {e}")
            raise

    def download_audio(self, video_url, output_path, audio_format='wav'):
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

    def slowed_reverb(self, audio, output, speed=0.4):
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
            if self.reverb_speed is not None:
                print('Adding reverb...')
                board = Pedalboard([Reverb(
                    room_size=.75,
                    damping=0.5,
                    wet_level=0.08,
                    dry_level=0.2
                )])
                effected = board(audio_data, sample_rate)
            else:
                print('No reverb specified, skipping reverb effect...')
                effected = audio_data

            print('Exporting audio...')
            sf.write(output, effected, sample_rate)
            print(f'Audio exported to {output}')
        except Exception as e:
            print(f"Error in slowed_reverb: {e}")
            raise

    def combine_audio_video(self, audio, clip, output_name):
        try:
            print(clip)
            # Load the video and audio
            video_clip = mp.VideoFileClip(clip)
            audio_clip = mp.AudioFileClip(audio)
            
            # Calculate the number of times to loop the video
            video_duration = video_clip.duration
            audio_duration = audio_clip.duration
            loops = int(audio_duration // video_duration) + 1  # Ensure it covers full audio length
            
            # Repeat the video clip to match the audio duration
            repeated_video = mp.concatenate_videoclips([video_clip] * loops)
            final_video = repeated_video.subclip(0, audio_duration)  # Trim to match exact audio length
            
            # Set the audio to the video
            final_video = final_video.set_audio(audio_clip)
            
            # Export the final video
            final_video.write_videofile(
                f"{output_name}.mp4",
                fps=24,
                codec='libx264',
                audio_codec='aac',
                preset='ultrafast',
                threads=4
            )
            
            # Clean up
            final_video.close()
            repeated_video.close()
            video_clip.close()
            audio_clip.close()
            
        except Exception as e:
            print(f"Error combining audio and video: {e}")
            raise

    def process(self):
        try:
            answer = self.assign_values()
            if answer == "yes":
                # DOWNLOAD AUDIO
                self.download_audio(self.audio_url, self.audio_output_path)

                # ADD EFFECTS TO AUDIO
                reverb_output_name = f'reverb - {self.audio_title}.wav'
                self.slowed_reverb(self.audio_output_path, reverb_output_name, self.audio_speed)
                remove(self.audio_output_path)

                # DOWNLOAD LOOP VIDEO
                loop_output_name = f'{self.video_title}.mp4'
                print("Downloading video...")
                self.download_video(self.loop_video, loop_output_name, self.start_time, self.end_time)

                # COMBINE TO MP4
                self.combine_audio_video(reverb_output_name, loop_output_name, self.final_video)
                remove(loop_output_name)
                remove(reverb_output_name)  # Clean up the reverb audio file
            else:
                print("ok bye")
        except Exception as e:
            print(f"Error in process: {e}")

    def search_youtube(self, query, max_results=5):
        """Search YouTube and return a list of video results"""
        try:
            search = Search(query)
            results = []
            for video in search.results[:max_results]:
                results.append({
                    'title': video.title,
                    'url': f"https://www.youtube.com/watch?v={video.video_id}"
                })
            return results
        except Exception as e:
            print(f"Error searching YouTube: {e}")
            return []

    def select_from_search(self, results):
        """Display search results and let user select one using arrow keys"""
        if not results:
            print("No results found.")
            return None

        current_index = 0
        while True:
            # Clear screen and show results
            print("\n" * 50)  # Clear screen
            print("Use ↑/↓ or W/S to navigate, Enter to select:")
            print("\nSearch Results:")
            for i, result in enumerate(results):
                prefix = "➡️    " if i == current_index else "  "
                print(f"{prefix}{i+1}. {result['title']}")
            
            # Get keyboard input
            key = msvcrt.getch()
            
            # Handle arrow keys and WASD
            if key in [b'\xe0', b'\x00']:  # Arrow key prefix
                key = msvcrt.getch()
                if key == b'H':  # Up arrow
                    current_index = max(0, current_index - 1)
                elif key == b'P':  # Down arrow
                    current_index = min(len(results) - 1, current_index + 1)
            elif key.lower() in [b'w', b's']:  # WASD
                if key.lower() == b'w':
                    current_index = max(0, current_index - 1)
                else:
                    current_index = min(len(results) - 1, current_index + 1)
            elif key == b'\r':  # Enter key
                return results[current_index]['url']
            elif key == b'\x1b':  # Escape key
                return None

def main():
    reverbed = Reverbed()
    reverbed.process()

if __name__ == "__main__":
    main()


