"""
Utility functions for the Reverbed package
"""

import re

def remove_illegal_characters(string):
    """Remove illegal characters from a string"""
    return re.sub(r'[^a-zA-Z0-9 ]', '', string)

def is_valid_youtube_url(url):
    """Check if the URL is a valid YouTube URL"""
    youtube_regex = r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/(watch\?v=|embed/|v/|.+\?v=)?([^"&?/s]{11})'
    return bool(re.match(youtube_regex, url)) 