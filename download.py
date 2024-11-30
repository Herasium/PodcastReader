
import os
import requests

def download_and_rename(url, folder):
    try:
        os.makedirs(folder, exist_ok=True)

        file_path = os.path.join(folder, "audio.mp3")
        print("Downloading...")
        response = requests.get(url, stream=True)
        response.raise_for_status()

        with open(file_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        print(f"File downloaded and saved as: {file_path}")

    except requests.exceptions.RequestException as e:
        print(f"Error during download: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

