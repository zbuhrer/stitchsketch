import cv2
import os
from typing import List


def extract_frames(video_path: str, output_dir: str, fps: float = 1.0) -> List[str]:
    """
    Extract frames from a video at a specified frame rate.

    Args:
        video_path: Path to the input video file.
        output_dir: Directory to save the extracted frames.
        fps: Frames per second to extract.  Defaults to 1.0.

    Returns:
        A list of paths to the extracted frames.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    video = cv2.VideoCapture(video_path)
    frame_rate = video.get(cv2.CAP_PROP_FPS)
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

    if not video.isOpened():
        raise ValueError(f"Could not open video: {video_path}")

    frame_interval = frame_rate / fps
    frame_count = 0
    extracted_frames: List[str] = []
    success = True

    while success:
        frame_id = int(round(frame_count * frame_interval))
        video.set(cv2.CAP_PROP_POS_FRAMES, frame_id)
        success, frame = video.read()

        if success:
            frame_name = f"frame_{frame_id:06d}.jpg"
            frame_path = os.path.join(output_dir, frame_name)
            cv2.imwrite(frame_path, frame)
            extracted_frames.append(frame_path)

        frame_count += 1

        if frame_id >= total_frames - 1:
            break

    video.release()
    return extracted_frames
