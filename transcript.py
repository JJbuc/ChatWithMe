from youtube_transcript_api import YouTubeTranscriptApi
import yt_dlp
from datetime import datetime


def video_content(video_id: str) -> str:
    """Fetch transcript using YouTubeTranscriptApi"""
    try:
        ytt_api = YouTubeTranscriptApi()
        transcript = ytt_api.fetch(video_id)
        full_transcript = " ".join([entry.text for entry in transcript])
        return full_transcript
    except Exception as e:
        return f"Error fetching transcript: {str(e)}"


def get_video_id(url: str) -> str:
    """Extract the video ID from a YouTube URL"""
    if "youtu.be" in url:
        return url.split("/")[-1].split("?")[0]
    if "youtube.com" in url:
        if "v=" in url:
            return url.split("v=")[1].split("&")[0]
        elif "embed/" in url:
            return url.split("embed/")[1].split("/")[0]
    print(f"The youtube link is not parsable, the link received is {url}")
    return None


def get_video_content(url: str):
    """
    Takes a YouTube video URL and returns:
    transcript, url, title, upload_date, description
    (uses only ONE yt_dlp call)
    """
    video_id = get_video_id(url)
    if not video_id:
        return "Invalid YouTube URL", url, None, None, None

    ydl_opts = {'quiet': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

    title = info.get('title', 'Unknown Title')
    upload_date = info.get('upload_date')
    if upload_date:
        upload_date = datetime.strptime(upload_date, "%Y%m%d").strftime("%Y-%m-%d")
    else:
        upload_date = "Unknown Date"

    description = info.get('description', 'No description available').strip()

    transcript = video_content(video_id)
    return transcript, url, title, upload_date, description


if __name__ == "__main__":
    video_url = "https://www.youtube.com/watch?v=Psp3YarOKVw"
    transcript, url, title, upload_date, description = get_video_content(video_url)
    print(url, title, upload_date, description)
