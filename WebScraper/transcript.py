# pip install youtube-transcript-api
from youtube_transcript_api import YouTubeTranscriptApi
### Give the video id and get the transcript, only import the 
### Import the get_video_content function only
import yt_dlp
from datetime import datetime


def video_content(video_id: str) -> str:
    """ Take a video id from youtube and fetch the transcript
    Args:
        The input video id (not the video url)
    Output:
        The output transcript as a string 
    """
    try:
        # Fetch transcript
        # transcript = YouTubeTranscriptApi.get_transcript(video_id)
        ytt_api = YouTubeTranscriptApi()
        transcript = ytt_api.fetch(video_id)
        # Combine all text snippets into a single string
        full_transcript = " ".join([entry.text for entry in transcript])
        
        return full_transcript
    
    except Exception as e:
        return f"Error fetching transcript: {str(e)}"

def get_video_id(url: str) -> str:
    """ Extract the video id from a youtube url
    Args:
        The input video url
    output:
        The output video id
    """
    if "youtu.be" in url:
        return url.split("/")[-1].split("?")[0]
    
    # Handle youtube.com URLs
    if "youtube.com" in url:
        if "v=" in url:
            return url.split("v=")[1].split("&")[0]
        elif "embed/" in url:
            return url.split("embed/")[1].split("/")[0]
        
    print("The youtube link is not parsable, the link received is {0}".format(url))
    return None

def get_video_upload_date(video_url: str) -> str:
    """
    Returns the upload date (YYYY-MM-DD) of a given YouTube video URL.
    """
    ydl_opts = {'quiet': True}

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=False)
        upload_date = info.get('upload_date')  # e.g., "20230115"
    
    if upload_date:
        # Convert from YYYYMMDD to YYYY-MM-DD
        return datetime.strptime(upload_date, "%Y%m%d").strftime("%Y-%m-%d")
    else:
        return "Unknown Date"
    
def get_video_title(video_url: str) -> str:
    """
    Returns the title of a given YouTube video URL.
    """
    ydl_opts = {'quiet': True}

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=False)
        title = info.get('title', 'Unknown Title')
    return title

def get_video_description(video_url: str) -> str:
    """
    Returns the full text description of a given YouTube video URL.
    """
    ydl_opts = {'quiet': True}

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=False)
        description = info.get('description', 'No description available')
    
    return description.strip()

def get_video_content(url: str) -> str:
    """ Take a video url from youtube and fetch the transcript
    Args:
        The input video url
    Output:
        The output transcript as a string
    """
    video_id = get_video_id(url)
    title = get_video_title(url)
    upload_date = get_video_upload_date(url)
    description = get_video_description(url)
    if video_id:
        return video_content(video_id),url,title,upload_date, description
    return "Invalid YouTube URL", url, None, None, description



if __name__ == "__main__":
    video_url = "https://www.youtube.com/watch?v=Psp3YarOKVw"
    transcript, url, title, upload_date, description = get_video_content(video_url)
    print(url, title, upload_date, description)
