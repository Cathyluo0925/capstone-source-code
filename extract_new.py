import sys
from pathlib import Path
import cv2  # Assuming you're using OpenCV for frame extraction
import os

# Get the absolute path of the current file and resolve any symbolic links
FILE = Path(__file__).resolve()

# Get the parent directory of the current file, which is the root folder of the project
BASE_ROOT = FILE.parents[0]

# Check if the root folder is already in the system path, and add it if it's not
if str(BASE_ROOT) not in sys.path:
    sys.path.append(str(BASE_ROOT))

# Get the relative path from the root folder to the current working directory
ROOT = Path(Path.relative_to(BASE_ROOT, Path.cwd()))


#############################
### Edit these settings ###
#############################
# Video directory
VIDEO_DIRPATH = ROOT / 'Nov29'  # Directory containing the videos

# Frame settings
REQUIRED_FRAME_RATE = 0.25  # Seconds between frames
START_FROM_SECOND = 0  # Start frame extraction after this time in seconds
REQUIRED_IMAGE_FORMAT = 'jpg'  # Image format
REQUIRED_IMAGE_WIDTH = 1080  # Width of extracted frames
REQUIRED_IMAGE_HEIGHT = 1080  # Height of extracted frames

# Output frames directory
OUTDIR = BASE_ROOT / 'Nov29_outcome'  # Output directory for frames

### END EDIT ###

def extract_frames(video_path, out_dir, frame_rate, start_time, image_format, width, height):
    """
    Extract frames from a video and save them to the specified output directory.
    Each video's frames are saved in a separate folder named after the video file (without extension).
    """
    video_name = video_path.stem  # Get video name without extension
    video_output_dir = out_dir / video_name
    video_output_dir.mkdir(parents=True, exist_ok=True)  # Create directory for this video's frames

    cap = cv2.VideoCapture(str(video_path))
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_interval = int(fps * frame_rate)
    start_frame = int(fps * start_time)
    
    current_frame = 0
    frame_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        if current_frame >= start_frame and (current_frame - start_frame) % frame_interval == 0:
            frame = cv2.resize(frame, (width, height))  # Resize frame
            frame_filename = video_output_dir / f"{frame_count + 1}.{image_format}"
            cv2.imwrite(str(frame_filename), frame)  # Save frame
            frame_count += 1

        current_frame += 1

    cap.release()
    print(f"Frames extracted for {video_name}: {frame_count}")


def main():
    OUTDIR.mkdir(parents=True, exist_ok=True)  # Ensure output directory exists

    video_files = list(VIDEO_DIRPATH.glob("*.mp4"))  # Adjust the file pattern if needed
    if not video_files:
        print("No video files found in the specified directory.")
        return

    for video_file in video_files:
        extract_frames(
            video_path=video_file,
            out_dir=OUTDIR,
            frame_rate=REQUIRED_FRAME_RATE,
            start_time=START_FROM_SECOND,
            image_format=REQUIRED_IMAGE_FORMAT,
            width=REQUIRED_IMAGE_WIDTH,
            height=REQUIRED_IMAGE_HEIGHT
        )


if __name__ == "__main__":
    main()
