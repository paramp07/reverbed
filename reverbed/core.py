"""
Core functionality for the Reverbed package
"""

import json
from os import makedirs
from .utils import remove_illegal_characters, is_valid_youtube_url
from .audio import download_audio, slowed_reverb
from .video import download_video, combine_audio_video
from .search import search_youtube, select_from_search

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
        self.reverb_speed = None
        
        # Reverb parameters with default values
        self.room_size = 0.75
        self.damping = 0.5
        self.wet_level = 0.08
        self.dry_level = 0.2
        
        # Load configuration
        self._load_config()

    def _load_config(self):
        """Load configuration from config.json"""
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

    def load_example(self, example):
        """Load values from an example configuration"""
        try:
            self.audio_url = example['audio_url']
            self.audio_speed = example['audio_speed']
            self.loop_video = example['loop_video']
            self.start_time = example['start_time']
            self.end_time = example['end_time']
            self.final_video = example['final_video']
            self.reverb_speed = example.get('reverb_speed')
            
            # Load reverb parameters if they exist in the config
            self.room_size = example.get('room_size', 0.75)
            self.damping = example.get('damping', 0.5)
            self.wet_level = example.get('wet_level', 0.08)
            self.dry_level = example.get('dry_level', 0.2)
            
            # Get titles safely
            self.video_title = remove_illegal_characters(self.get_video_title(self.loop_video))
            self.audio_title = remove_illegal_characters(self.get_video_title(self.audio_url))
            self.audio_output_path = f'{self.audio_title}.wav'
        except Exception as e:
            print(f"Error loading example: {e}")
            raise

    def get_video_title(self, url):
        """Safely get video title from YouTube URL"""
        try:
            if not is_valid_youtube_url(url):
                raise ValueError("Invalid YouTube URL")
            
            from pytube import YouTube
            yt = YouTube(url)
            return yt.title
        except Exception as e:
            print(f"Error getting video title: {e}")
            return "video"

    def process(self):
        """Main processing function"""
        try:
            answer = self.assign_values()
            if answer == "yes":
                # DOWNLOAD AUDIO
                download_audio(self.audio_url, self.audio_output_path)

                # ADD EFFECTS TO AUDIO
                reverb_output_name = f'reverb - {self.audio_title}.wav'
                slowed_reverb(
                    self.audio_output_path, 
                    reverb_output_name, 
                    self.audio_speed,
                    self.room_size,
                    self.damping,
                    self.wet_level,
                    self.dry_level
                )
                from os import remove
                remove(self.audio_output_path)

                # DOWNLOAD LOOP VIDEO
                loop_output_name = f'{self.video_title}.mp4'
                print("Downloading video...")
                download_video(self.loop_video, loop_output_name, self.start_time, self.end_time)

                # COMBINE TO MP4
                combine_audio_video(reverb_output_name, loop_output_name, self.final_video)
                remove(loop_output_name)
                remove(reverb_output_name)  # Clean up the reverb audio file
            else:
                print("ok bye")
        except Exception as e:
            print(f"Error in process: {e}")

    def assign_values(self):
        """Assign values for processing"""
        try:
            from os import system, name
            def clear_console():
                system('cls' if name == 'nt' else 'clear')

            clear_console()
            print("Welcome to Reverbed!")
            print("1. Use example")
            print("2. Create new")
            choice = input("> ")

            if choice == "1":
                # Display available examples
                print("\nAvailable examples:")
                for i, example in enumerate(self.config['examples'], 1):
                    print(f"{i}. {example['name']}")
                
                # Get user selection
                while True:
                    try:
                        selection = int(input("\nSelect an example (number): "))
                        if 1 <= selection <= len(self.config['examples']):
                            self.load_example(self.config['examples'][selection-1])
                            return "yes"
                        print("Invalid selection. Please try again.")
                    except ValueError:
                        print("Please enter a valid number.")
                    
            elif choice == "2":
                # Handle audio URL input
                while True:
                    clear_console()
                    print("\nEnter YouTube URL or search query for audio:")
                    query = input("> ")
                    if is_valid_youtube_url(query):
                        self.audio_url = query
                        break
                    else:
                        print("Searching YouTube...")
                        results = search_youtube(query)
                        if results:
                            selected_url = select_from_search(results)
                            if selected_url:
                                self.audio_url = selected_url
                                break
                        print("No valid selection made. Please try again.")
                
                # Handle audio speed
                while True:
                    clear_console()
                    try:
                        self.audio_speed = float(input("How slow would you like it: "))
                        if 0 < self.audio_speed <= 1:
                            break
                        print("Speed must be between 0 and 1")
                    except ValueError:
                        print("Please enter a valid number")
                
                # Handle loop video input
                while True:
                    clear_console()
                    print("\nEnter YouTube URL or search query for loop video:")
                    query = input("> ")
                    if is_valid_youtube_url(query):
                        self.loop_video = query
                        break
                    else:
                        print("Searching YouTube...")
                        results = search_youtube(query)
                        if results:
                            selected_url = select_from_search(results)
                            if selected_url:
                                self.loop_video = selected_url
                                break
                        print("No valid selection made. Please try again.")
                
                clear_console()
                self.start_time = input('When would you like the video to start?: ')
                self.end_time = input('When would you like the video to end?: ')
                self.final_video = input("what do you want the end product to be called?: ")
                
                # Ask if user wants to add reverb
                clear_console()
                add_reverb = input("Would you like to add reverb? (y/n): ").lower()
                if add_reverb == 'y':
                    self.reverb_speed = 1.0  # Default reverb speed
                    
                    # Ask for custom reverb parameters
                    clear_console()
                    print("Enter reverb parameters (press Enter to use defaults):")
                    
                    try:
                        room_size_input = input(f"Room size (default: {self.room_size}): ")
                        if room_size_input.strip():
                            self.room_size = float(room_size_input)
                            
                        damping_input = input(f"Damping (default: {self.damping}): ")
                        if damping_input.strip():
                            self.damping = float(damping_input)
                            
                        wet_level_input = input(f"Wet level (default: {self.wet_level}): ")
                        if wet_level_input.strip():
                            self.wet_level = float(wet_level_input)
                            
                        dry_level_input = input(f"Dry level (default: {self.dry_level}): ")
                        if dry_level_input.strip():
                            self.dry_level = float(dry_level_input)
                    except ValueError:
                        print("Invalid input. Using default values.")
                else:
                    self.reverb_speed = None
                
                # Get titles safely
                self.video_title = remove_illegal_characters(self.get_video_title(self.loop_video))
                self.audio_title = remove_illegal_characters(self.get_video_title(self.audio_url))
                self.audio_output_path = f'{self.audio_title}.wav'
                return "yes"
            else:
                print("Ok bye")
                return "none"
        except Exception as e:
            print(f"Error in assign_values: {e}")
            return "none" 