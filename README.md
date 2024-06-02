# Video Frame Extractor

## Description
The Video Frame Extractor is a Python project designed to automate the process of downloading a YouTube video, extracting detailed video information, and splitting the video into individual frames. Each frame is saved into separate folders at a specified frame rate. This project utilizes `pytube` for downloading videos and `ffmpeg` for processing and extracting frames.

## Features
- Download videos from YouTube
- Extract video metadata using `ffmpeg`
- Split video into frames at a specified frame rate
- Save frames into organized folders

## Requirements
- Python 3.x
- `pytube`
- `ffmpeg-python`
- `ffmpeg` installed on your system

## Setup

1. Clone the repository:
    ```bash
    git clone https://github.com/username/Video-Frame-Extractor.git
    ```

2. Navigate to the project directory:
    ```bash
    cd Video-Frame-Extractor
    ```

3. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate | venv\Scripts\activate 
    ```

4. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

5. Run the script:
    ```bash
    python main.py
    ```

## Logging
Logs are stored in `logs/video_processing.log`.

## Output
Extracted frames are saved in `folder1`, `folder2`, `folder3`, and `folder4`.

