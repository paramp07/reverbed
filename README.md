# Reverbed

A Python-based tool for creating slowed and reverbed versions of videos by processing audio and video content from YouTube.

## Features

- Download and process audio from YouTube videos
- Adjust audio speed and optionally add reverb effects
- Loop video segments with custom start and end times
- Combine processed audio with looped video
- Support for multiple processing configurations

## Prerequisites

- Python 3.x
- FFmpeg (for audio/video processing)
- Required Python packages (see requirements.txt)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/reverbed.git
cd reverbed
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
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
            "final_video": "example1_output"
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
- `reverb_speed`: (Optional) Speed multiplier for the reverb effect. If not specified, no reverb will be applied.

## Configuration Examples

### Basic Configuration (No Reverb)
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
            "final_video": "example1_output"
        }
    ]
}
```

### Configuration with Reverb
```json
{
    "examples": [
        {
            "name": "Example 2",
            "audio_url": "https://www.youtube.com/watch?v=example",
            "audio_speed": 0.2,
            "reverb_speed": 0.5,
            "loop_video": "https://www.youtube.com/watch?v=example",
            "start_time": "20",
            "end_time": "30",
            "final_video": "example2_output"
        }
    ]
}
```

## Usage

1. Configure your settings in `config.json`
2. Run the main script:
```bash
python main.py
```

The script will:
1. Download the specified audio and video
2. Process the audio according to the speed settings
3. Extract and loop the specified video segment
4. Combine the processed audio with the looped video
5. Save the final output with the specified name

## Output

Processed videos will be saved in the output directory with the names specified in the configuration.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- FFmpeg for audio/video processing
- YouTube-DL for video downloading
- Other open-source libraries used in this project 