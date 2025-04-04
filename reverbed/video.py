"""
Video processing functions for the Reverbed package
"""

import moviepy.editor as mp
from yt_dlp import YoutubeDL
import shutil
from subprocess import run

def download_video(url, output_path, start_time, end_time):
    """Download and trim a video from YouTube"""
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
            '-preset', 'ultrafast',
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
        from os import remove
        remove(output_path)
        shutil.move(temp_output, output_path)
        
        print(f'Video downloaded and trimmed to {output_path}')
    except Exception as e:
        print(f"Error downloading video: {e}")
        raise

def combine_audio_video(audio, clip, output_name):
    """Combine audio and video into a single file"""
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