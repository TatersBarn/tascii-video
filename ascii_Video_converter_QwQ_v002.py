import cv2
import numpy as np
import subprocess
import os
import sys

def resize_image(image, desired_width=150):
    original_height, original_width = image.shape[:2]
    aspect_ratio = original_height / original_width
    new_height = int(desired_width * aspect_ratio)
    resized = cv2.resize(image, (desired_width, new_height))
    return resized

def detect_edges(image):
    return cv2.Canny(image, 100, 200)

def image_to_ascii(image, edges, ascii_chars=' .,:;-~=+x*#%H@'):
    rows, cols = image.shape
    ascii_art = []
    for row in range(rows):
        line = ''
        for col in range(cols):
            brightness = image[row][col]
            index = int(brightness / 25.5)  # 255 / len(ascii_chars)
            line += ascii_chars[index]
        ascii_art.append(line)

    # Optionally, enhance edges
    for row in range(rows):
        for col in range(cols):
            if edges[row][col] == 255:
                ascii_art[row] = ascii_art[row][:col] + '*' + ascii_art[row][col+1:]

    return ascii_art

def main():
    if len(sys.argv) != 3:
        print("Usage: python script.py <video_file> <output_txt>")
        return

    video_file = sys.argv[1]
    output_txt = sys.argv[2]

    # Use ffmpeg to extract frames at desired FPS
    temp_frame_dir = "temp_frames"
    os.makedirs(temp_frame_dir, exist_ok=True)

    desired_fps = 10
    subprocess.call([
        'ffmpeg',
        '-i', video_file,
        '-r', str(desired_fps),
        f'{temp_frame_dir}/frame%04d.png'
    ])

    frame_files = sorted([f for f in os.listdir(temp_frame_dir) if f.endswith('.png')])

    with open(output_txt, 'w') as f:
        for frame_file in frame_files:
            frame_path = os.path.join(temp_frame_dir, frame_file)
            image = cv2.imread(frame_path, cv2.IMREAD_GRAYSCALE)
            resized = resize_image(image)
            edges = detect_edges(resized)
            ascii_art = image_to_ascii(resized, edges)

            if frame_file == frame_files[0]:
                # Write parameters at the beginning
                width = len(ascii_art[0])
                height = len(ascii_art)
                f.write(f"# Width: {width}\n")
                f.write(f"# Height: {height}\n")
                f.write(f"# FPS: {desired_fps}\n")

            for line in ascii_art:
                f.write(line + '\n')
            f.write("Delimiter\n")  # Use a unique delimiter to separate frames

    # Clean up temporary files
    for frame_file in frame_files:
        os.remove(os.path.join(temp_frame_dir, frame_file))
    os.rmdir(temp_frame_dir)

    print(f"Processed and saved ASCII frames to {output_txt}")

if __name__ == "__main__":
    main()
