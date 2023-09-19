import os
import subprocess
import logging
import time  

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
            
            # Assuming the output is named by combining the input names
            # (Replace with actual naming convention)
            output_filename = predict_output_name(image_path, video_path)
            output_filepath = os.path.join("G:/My Drive/5GS/batch_180924_ryan_z115_yn1", output_filename)
            print("Checking for: ", output_filepath)

            # Check if the output file already exists and skip if it does
            if os.path.exists(output_filepath):
                logging.info(f"Skipping {output_filepath} as it already exists.")
                continue

            # Record the start time for this specific combination
            combination_start_time = time.time()

            logging.info(f"Processing combination {combination_index}/{total_combinations}: image {image_path} and video {video_path}")

            # Construct the command
            cmd = [
                "python", "inference.py",
                "--config", "configs/inference.yaml",
                "--video_source", video_path,
                "--image_source", image_path,
                "--output_dir", "G:/My Drive/5GS/batch_180924_ryan_z115_yn1",
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

def predict_output_name(image_path, video_path):
    # Extract base names without extension
    image_name = os.path.splitext(os.path.basename(image_path))[0]
    video_name = os.path.splitext(os.path.basename(video_path))[0]

    # Combine them to produce the output name
    return f"{video_name}_{image_name}.mp4"

if __name__ == "__main__":
    image_folder = "batch_180923_resized_solo"
    video_folder = "videos"
    run_inference_on_combinations(image_folder, video_folder)
