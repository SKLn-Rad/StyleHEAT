import os
import shutil
import imghdr

def ensure_dir_exists(directory):
    """Utility function to make sure a directory exists."""
    if not os.path.exists(directory):
        os.makedirs(directory)

# Set the directory path
dir_path = "batch_180923_resized"
base_destination_path = "batch_180923_resized_solo"

# Create the base images_solo directory if it doesn't exist
ensure_dir_exists(base_destination_path)

# This set will store the names we have already processed
processed_names = set()  

# Use os.walk() to iterate over all sub-directories and files
for current_dir, dirs, files in os.walk(dir_path):
    for filename in files:
        # Determine if it's an image
        if imghdr.what(os.path.join(current_dir, filename)):
            # Split the filename by spaces (ignoring the file extension)
            parts = filename.rsplit('.', 1)[0].split(' ')

            print("Got parts:", parts)

            # Check if there are enough parts
            if len(parts) > 1:
                name = parts[1].lower()
                
                if name not in processed_names:
                    # Create the same folder structure in the destination
                    rel_dir = os.path.relpath(current_dir, dir_path)
                    destination_dir = os.path.join(base_destination_path, rel_dir)
                    ensure_dir_exists(destination_dir)
                    
                    # Set the full path for source and destination
                    src = os.path.join(current_dir, filename)
                    dest = os.path.join(destination_dir, filename)
                    
                    # Move the file
                    print("Copying from", src, "to", dest)
                    shutil.copy2(src, dest)
                    
                    processed_names.add(name)

print("Files moved successfully!")
