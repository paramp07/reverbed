# Reverbed

A Python package for creating slowed and reverbed versions of videos by processing audio and video content from YouTube.

## Features

- Download and process audio from YouTube videos
- Adjust audio speed and add custom reverb effects
- Loop video segments with custom start and end times
- Combine processed audio with looped video
- Support for multiple processing configurations
- Interactive YouTube search with keyboard navigation

## Installation

### From PyPI (Recommended)

```bash
pip install reverbed
```

### From Source

1. Clone the repository:
```bash
git clone https://github.com/paramp07/reverbed.git
cd reverbed
```

2. Install the package:
```bash
pip install -e .
```

## Usage

### Command Line Interface

After installation, you can use the package from the command line:

```bash
reverbed
```

This will start the interactive interface where you can:
1. Choose to use an example configuration or create a new one
2. Input YouTube URLs or search for videos
3. Customize audio speed and reverb effects
4. Set video loop times
5. Process and combine the final video

### Python API

You can also use the package programmatically:

```python
from reverbed import Reverbed

# Create a Reverbed instance
reverbed = Reverbed()

# Process a video
reverbed.process()
```

## Configuration

Create a `config.json` file with your processing settings. Example configuration:

```json
{
    "examples": [
        {
            "name": "Example 1",
            "audio_url": "https://www.youtube.com/watch?v=example",
            "audio_speed": 0.2,
            "loop_video": "https://www.youtube.com/watch?v=example",
            "start_time": "20",
            "end_time": "30",
            "final_video": "example1_output",
            "room_size": 0.75,
            "damping": 0.5,
            "wet_level": 0.08,
            "dry_level": 0.2
        }
    ]
}
```

### Configuration Parameters

- `name`: Name of the processing example
- `audio_url`: YouTube URL for the audio source
- `audio_speed`: Speed multiplier for the audio (0.0 to 1.0)
- `loop_video`: YouTube URL for the video to loop
- `start_time`: Start time for video loop (in seconds or MM:SS format)
- `end_time`: End time for video loop (in seconds or MM:SS format)
- `final_video`: Name for the output video file
- `room_size`: Room size for reverb effect (0.0 to 1.0)
- `damping`: Damping for reverb effect (0.0 to 1.0)
- `wet_level`: Wet level for reverb effect (0.0 to 1.0)
- `dry_level`: Dry level for reverb effect (0.0 to 1.0)

## Requirements

- Python 3.6 or higher
- FFmpeg (for audio/video processing)
- Required Python packages (automatically installed with pip):
  - pytube
  - moviepy
  - yt-dlp
  - soundfile
  - pedalboard
  - numpy

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- FFmpeg for audio/video processing
- YouTube-DL for video downloading
- Other open-source libraries used in this project 