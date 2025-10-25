from transcript import get_video_content
from get_video_url import get_all_videos

creator_link = "https://www.youtube.com/@MrBeast/videos"
urls = get_all_videos(creator_link)
print(urls)
# for video_url in urls:
#     print(video_url)
#     transcript, url, title, upload_date, description = get_video_content(video_url)
#     print(url, title, upload_date)