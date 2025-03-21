import time
import os

def read_ascii_frames(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()

    params = {}
    frames = []
    current_frame = []

    for line in lines:
        if line.startswith("#"):
            key, value = line.strip()[2:].split(": ")
            params[key] = value
        elif line.strip() == "Delimiter":
            if current_frame:
                frames.append(current_frame)
                current_frame = []
        else:
            current_frame.append(line.rstrip())

    if current_frame:
        frames.append(current_frame)

    return params, frames

def display_frames(frames, fps):
    frame_duration = 1 / fps
    for frame in frames:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n".join(frame))
        time.sleep(frame_duration)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python player.py <ascii_txt>")
        sys.exit(1)

    file_path = sys.argv[1]
    params, frames = read_ascii_frames(file_path)

    width = int(params.get('Width', 0))
    height = int(params.get('Height', 0))
    fps = int(params.get('FPS', 10))

    while(True):
        display_frames(frames, fps)
