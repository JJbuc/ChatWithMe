### Get the link to the youtubers channel and get the link to all videos
## returns a list of video urls
import warnings

# Ignore all warnings
warnings.filterwarnings("ignore")
import yt_dlp

def get_all_videos(channel_url: str):
    """
    Returns a list of all video URLs from a YouTube channel.
    Works for /@username, /channel/ID, or /c/handle URLs.
    """
    if not channel_url.rstrip("/").endswith("videos"):
        channel_url = channel_url.rstrip("/") + "/videos"
    ydl_opts = {
        'extract_flat': True,   # Don't download, just extract metadata
        'quiet': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(channel_url, download=False)
    
    video_urls = []
    if 'entries' in info:
        for entry in info['entries']:
            if entry and 'url' in entry:
                video_urls.append(entry['url'])
                # video_urls.append(f"https://www.youtube.com/watch?v={entry['url']}")
    return video_urls


# # # Example usage:
if __name__ == "__main__":
    channel = "https://www.youtube.com/@MrBeast/videos"
    urls = get_all_videos(channel)
    print(f"Found {len(urls)} videos:")
    for u in urls[:10]:  # preview first 10
        print(u)

