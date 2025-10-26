import csv
from transcript import get_video_content
from get_video_url import get_all_videos

# Channel to scrape
creator_link = "https://www.youtube.com/@mkbhd"
urls = get_all_videos(creator_link)
print('here')
# Name of CSV output file
output_file = "mkbhd_videos.csv"

# Create and open the CSV file
with open(output_file, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    # Write header row
    writer.writerow(["date", "title", "url", "transcript", "description"])

    # Loop through each video and write data
    for video_url in urls[:25]:
        print(video_url)
        try:
            transcript, url, title, upload_date, description = get_video_content(video_url)
            writer.writerow([upload_date, title, url, transcript, description])
            print(f"✅ Saved: {title}")
        except Exception as e:
            print(f"❌ Error with {video_url}: {e}")

print(f"\nAll data saved to {output_file}")
