"""
YouTube search functionality for the Reverbed package
"""

import msvcrt  # For Windows keyboard input
from pytube import Search

def search_youtube(query, max_results=10):
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

def select_from_search(results):
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
            print(f"{prefix}{i+1}. {result['title']} ")
        
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