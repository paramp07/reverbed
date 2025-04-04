# Reverbed

![alt text](<resources/logo.png>)

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

```python
from reverbed import Reverbed

# Create a Reverbed instance
reverbed = Reverbed()

# Process a video using interactive mode
reverbed.process()

# Or configure programmatically
reverbed.audio_url = "https://www.youtube.com/watch?v=example"
reverbed.audio_speed = 0.8
reverbed.loop_video = "https://www.youtube.com/watch?v=example"
reverbed.start_time = "0:20"
reverbed.end_time = "0:30"
reverbed.final_video = "output_video"
reverbed.process()
```

## Configuration

Create a `config.json` file with your processing settings:

```json
{
    "examples": [
        {
            "name": "Example 1",
            "audio_url": "https://www.youtube.com/watch?v=example",
            "audio_speed": 0.8,
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

| Parameter | Type | Description | Range |
|-----------|------|-------------|--------|
| `name` | string | Name of the processing example | - |
| `audio_url` | string | YouTube URL for audio source | Valid YouTube URL |
| `audio_speed` | float | Speed multiplier for audio | 0.0 to 1.0 |
| `loop_video` | string | YouTube URL for video to loop | Valid YouTube URL |
| `start_time` | string | Start time for video loop | Seconds or "MM:SS" |
| `end_time` | string | End time for video loop | Seconds or "MM:SS" |
| `final_video` | string | Output video filename | - |
| `room_size` | float | Room size for reverb effect | 0.0 to 1.0 |
| `damping` | float | Damping for reverb effect | 0.0 to 1.0 |
| `wet_level` | float | Wet level for reverb effect | 0.0 to 1.0 |
| `dry_level` | float | Dry level for reverb effect | 0.0 to 1.0 |

## API Reference

### Core Module

#### `class Reverbed`

Main class for video processing.

Methods:
- `__init__()`: Initialize Reverbed instance
- `process()`: Process video with current settings
- `load_example(example)`: Load settings from example configuration
- `assign_values()`: Interactive configuration of settings

### Utility Functions

#### Audio Processing

```python
from reverbed import download_audio, slowed_reverb

# Download audio from YouTube
download_audio(video_url, output_path, audio_format='wav')

# Apply slowed and reverb effects
slowed_reverb(
    audio_file,
    output_file,
    speed=0.8,
    room_size=0.75,
    damping=0.5,
    wet_level=0.08,
    dry_level=0.2
)
```

#### Video Processing

```python
from reverbed import download_video, combine_audio_video

# Download and trim video
download_video(url, output_path, start_time, end_time)

# Combine audio and video
combine_audio_video(audio_file, video_file, output_name)
```

#### YouTube Search

```python
from reverbed import search_youtube, select_from_search

# Search YouTube
results = search_youtube(query, max_results=10)

# Interactive result selection
selected_url = select_from_search(results)
```

## Requirements

- Python 3.6 or higher
- FFmpeg (for audio/video processing)
- Required Python packages (automatically installed):
  - pytube
  - moviepy
  - yt-dlp
  - soundfile
  - pedalboard
  - numpy

## Development

### Setting up Development Environment

1. Clone the repository
2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
3. Install development dependencies:
```bash
pip install -e ".[dev]"
```

### Running Tests

```bash
python -m pytest tests/
```

### Building the Package

```bash
python -m build
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- FFmpeg for audio/video processing
- YouTube-DL for video downloading
- All contributors and users of this package

## Changelog

### 0.1.0 (Initial Release)
- Basic functionality for video processing
- YouTube video download support
- Audio speed and reverb effects
- Video looping capabilities
- Interactive YouTube search
