# Reverbed API

A FastAPI server that provides an API for the Reverbed library, allowing you to apply slowed + reverb effects to audio from YouTube videos.

## Features

- Process YouTube videos with slowed + reverb effects
- Customize reverb parameters (room size, damping, wet level, dry level)
- Optionally combine processed audio with a loop video
- Return processed audio as WAV or combined video as MP4

## Installation

1. Make sure you have Python 3.8+ installed
2. Install the required dependencies:

```bash
pip install fastapi uvicorn yt-dlp reverbed
```

## Usage

1. Start the server:

```bash
python reverbed_api.py
```

2. The server will run at `http://localhost:8000`

3. Send POST requests to `/process-audio` with the following JSON body:

```json
{
  "youtube_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
  "audio_speed": 0.8,
  "room_size": 0.8,
  "wet_level": 0.5,
  "damping": 0.3,
  "dry_level": 0.5,
  "start_time": "00:00",
  "end_time": "00:10",
  "loop_video": "https://www.youtube.com/watch?v=example"
}
```

4. You can also test the API with a sample request by visiting `/test` in your browser

## API Parameters

- `youtube_url` (required): YouTube URL of the audio to process
- `audio_speed` (required): Speed factor (0-1, where lower is slower)
- `room_size` (optional, default 0.75): Size of the reverb room (0-1)
- `wet_level` (optional, default 0.08): Level of reverb effect (0-1)
- `damping` (optional, default 0.5): Damping factor for reverb (0-1)
- `dry_level` (optional, default 0.2): Level of original signal (0-1)
- `start_time` (optional, default "00:00"): Start time for loop video (MM:SS)
- `end_time` (optional): End time for loop video (MM:SS)
- `loop_video` (optional): YouTube URL of video to loop with the processed audio

## Response

The API returns the processed audio file (WAV) or video file (MP4) as a downloadable attachment.
