"""
Command-line interface for the Reverbed package
"""

from .core import Reverbed

def main():
    """Main entry point for the CLI"""
    try:
        reverbed = Reverbed()
        reverbed.process()
    except KeyboardInterrupt:
        print("\nProcess interrupted by user. Exiting...")
    except Exception as e:
        print(f"Error: {e}")
        
if __name__ == "__main__":
    main()
