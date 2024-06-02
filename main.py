import os
import shutil
import logging
from pytube import YouTube
import ffmpeg

# constants and variables
CURRENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
LOG_FILE_PATH = os.path.join(CURRENT_DIRECTORY, 'logs', 'video_processing.log')
VIDEO_URL = "https://youtu.be/WBJzp-y4BHA?si=mqaU7s_Qo0G-ZKHo" # Replace it with your video link
FRAME_RATE = 60 #Select the number of frames per second you want
OUTPUT_FOLDERS = [
    os.path.join(CURRENT_DIRECTORY, "folder1"),
    os.path.join(CURRENT_DIRECTORY, "folder2"),
    os.path.join(CURRENT_DIRECTORY, "folder3"),
    os.path.join(CURRENT_DIRECTORY, "folder4")
]

def setup_logging():
    """Setup logging configuration and define log file."""
    os.makedirs(os.path.dirname(LOG_FILE_PATH), exist_ok=True)
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        handlers=[logging.FileHandler(LOG_FILE_PATH)])

def download_video(video_url):
    """Download video from YouTube and return the filename.

    Args:
        video_url (str): URL of the YouTube video to download.

    Returns:
        str: The filename of the downloaded video.
    """
    try:
        yt = YouTube(video_url)
        stream = yt.streams.get_highest_resolution()
        filename = stream.download(output_path=CURRENT_DIRECTORY)
        logging.info(f"Downloaded video: {filename}")
        return filename
    except Exception as e:
        logging.error(f"Error downloading video: {e}")
        return None

def extract_video_info(video_path):
    """Extract video information using ffmpeg.

    Args:
        video_path (str): Path to the video file.

    Returns:
        dict: Information about the video.
    """
    try:
        probe = ffmpeg.probe(video_path)
        video_info = next(stream for stream in probe['streams'] if stream['codec_type'] == 'video')
        logging.info(f"Extracted video info for {video_path}")
        return video_info
    except ffmpeg.Error as e:
        logging.error(f"Error extracting video info: {e}")
        return None

def create_folders(folders):
    """Create folders if they don't exist.

    Args:
        folders (list): List of folder paths to create.
    """
    for folder in folders:
        if os.path.exists(folder):
            shutil.rmtree(folder)
            logging.info(f"Deleted existing folder: {folder}")
        os.makedirs(folder, exist_ok=True)
        logging.info(f"Created folder: {folder}")

def extract_frames(video_path, output_folder, start_time, duration, frame_rate):
    """Extract frames from video and save to output folder.

    Args:
        video_path (str): Path to the video file.
        output_folder (str): Path to the folder where frames will be saved.
        start_time (float): Start time in seconds for frame extraction.
        duration (float): Duration in seconds for frame extraction.
        frame_rate (int): Frame rate for extracting frames.
    """
    try:
        (
            ffmpeg.input(video_path, ss=start_time, t=duration)
            .output(os.path.join(output_folder, "frame_%06d.png"), vf=f'fps={frame_rate}')
            .run()
        )
        logging.info(f"Extracted frames from {video_path} to {output_folder} (start time: {start_time}s, duration: {duration}s)")
    except ffmpeg.Error as e:
        logging.error(f"Error extracting frames: {e}")

def main():
    """Main function to coordinate video processing workflow."""
    # Setup logging
    setup_logging()
    logging.info(f"Starting processing for video URL: {VIDEO_URL}")

    # Download video
    video_path = download_video(VIDEO_URL)
    if not video_path:
        logging.error("Failed to download video, exiting.")
        return

    # Extract video information
    video_info = extract_video_info(video_path)
    if not video_info:
        logging.error("Failed to extract video info, exiting.")
        return

    video_duration_seconds = float(video_info['duration'])
    time_durations = [
        video_duration_seconds * 0.25, # It can be a percentage of the total or a fixed number of seconds
        video_duration_seconds * 0.25,
        video_duration_seconds * 0.25,
        video_duration_seconds * 0.25,
    ]

    # Create output folders
    create_folders(OUTPUT_FOLDERS)

    # Extract frames
    start_time = 0
    for i, folder in enumerate(OUTPUT_FOLDERS):
        duration = time_durations[i]
        extract_frames(video_path, folder, start_time, duration, FRAME_RATE)
        start_time += duration

    logging.info("Processing completed successfully.\n"+'-' * 150)

if __name__ == "__main__":
    main()
