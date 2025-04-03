"""
Reverbed - A Python package for creating slowed and reverbed versions of videos
"""

__version__ = "0.1.0"

from .core import Reverbed
from .utils import remove_illegal_characters, is_valid_youtube_url
from .audio import download_audio, slowed_reverb
from .video import download_video, combine_audio_video
from .search import search_youtube, select_from_search

__all__ = [
    'Reverbed',
    'remove_illegal_characters',
    'is_valid_youtube_url',
    'download_audio',
    'slowed_reverb',
    'download_video',
    'combine_audio_video',
    'search_youtube',
    'select_from_search'
] 