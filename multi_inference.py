import os
import subprocess
import logging
import time  # Import the time module

def get_files_from_directory(directory, extensions):
    """Return a list of files with the specified extensions from a directory (recursively)."""
    return [os.path.join(dirpath, filename) 
            for dirpath, dirnames, filenames in os.walk(directory) 
            for filename in filenames 
            if filename.lower().endswith(extensions)]

def run_inference_on_combinations(image_folder, video_folder):
    # Define the extensions for images and videos you want to consider
    image_extensions = ('.png', '.jpg', '.jpeg')
    video_extensions = ('.mp4', '.avi', '.mov')
    
    # Get all the image and video files
    image_files = get_files_from_directory(image_folder, image_extensions)
    video_files = get_files_from_directory(video_folder, video_extensions)
    
    logging.basicConfig(level=logging.INFO)
    total_combinations = len(image_files) * len(video_files)
    
    # Counter to keep track of the combination being processed
    combination_index = 1

    # Record the start time for the entire process
    total_start_time = time.time()

    # Loop through each combination of image and video
    for image_path in image_files:
        for video_path in video_files:
            # Record the start time for this specific combination
            combination_start_time = time.time()

            logging.info(f"Processing combination {combination_index}/{total_combinations}: image {image_path} and video {video_path}")

            # Construct the command
            cmd = [
                "python", "inference.py",
                "--config", "configs/inference.yaml",
                "--video_source", video_path,
                "--image_source", image_path,
                "--output_dir", "G:/My Drive/5GS/140923-205111",
                "--cross_id",
                "--if_extract",
                "--if_align",
            ]

            # Run the command and stream the output
            with subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) as process:
                for line in process.stdout:
                    print(line, end='')
                for line in process.stderr:
                    print(line, end='')

            # Calculate and print the time taken for this specific combination
            combination_end_time = time.time()
            combination_duration = combination_end_time - combination_start_time
            print(f"Time taken for combination {combination_index}: {combination_duration:.2f} seconds")

            combination_index += 1

    # Calculate and print the total time taken for all combinations
    total_end_time = time.time()
    total_duration = total_end_time - total_start_time
    print(f"Total time taken for all combinations: {total_duration:.2f} seconds")

if __name__ == "__main__":
    image_folder = "images_resized"
    video_folder = "videos"
    run_inference_on_combinations(image_folder, video_folder)
