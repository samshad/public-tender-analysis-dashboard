import nltk
import os
import sys

# Define the directory where NLTK data will be downloaded
# This uses the NLTK_DATA environment variable set in the Dockerfile,
# or defaults to /usr/local/nltk_data if the variable is not set.
nltk_data_dir = os.environ.get('NLTK_DATA', '/usr/local/nltk_data')

# Create the directory if it doesn't exist
os.makedirs(nltk_data_dir, exist_ok=True)

# List of NLTK packages to download
# Make sure this list includes all packages your application needs.
packages = ['punkt', 'punkt_tab', 'stopwords']

print(f"Downloading NLTK data to {nltk_data_dir}...")

# Download each package
for package in packages:
    print(f"Attempting to download {package}...")
    try:
        # Use quiet=True to avoid interactive prompts during download.
        # Specify the download_dir to ensure data goes to the correct location.
        success = nltk.download(package, download_dir=nltk_data_dir, quiet=True)
        if success:
            print(f"Successfully downloaded {package}")
        else:
            # If download fails, print an error and exit the script.
            # This will cause the Docker build step to fail, indicating an issue.
            print(f"Error downloading {package}. Please check your network connection or try again later.")
            sys.exit(1) # Exit with a non-zero status to indicate failure
    except Exception as e:
        # Catch any other exceptions during download and exit.
        print(f"An error occurred while downloading {package}: {e}")
        sys.exit(1) # Exit with a non-zero status

print("All specified NLTK data packages downloaded successfully.")
