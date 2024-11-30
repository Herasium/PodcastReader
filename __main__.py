from download import download_and_rename
from split import split_text_file
from pydub import AudioSegment
import math
import pyperclip
from text_to_audio import run_trasncription

logo = """
   ___          _               _                        _           
  / _ \___   __| | ___ __ _ ___| |_   _ __ ___  __ _  __| | ___ _ __ 
 / /_)/ _ \ / _` |/ __/ _` / __| __| | '__/ _ \/ _` |/ _` |/ _ \ '__|
/ ___/ (_) | (_| | (_| (_| \__ \ |_  | | |  __/ (_| | (_| |  __/ |   
\/    \___/ \__,_|\___\__,_|___/\__| |_|  \___|\__,_|\__,_|\___|_|   
                                                                     
"""
file_path = 'downloads/audio.mp3'

def seconds_to_hms(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"

def run_main():

    print(logo)
    url = input("Podcast CDN URL: ")
    download_and_rename(url,"downloads")
    audio = AudioSegment.from_file(file_path)
    duration_seconds = len(audio) / 1000  
    print(f"The audio length is {seconds_to_hms(duration_seconds)} seconds. Estimated time: {seconds_to_hms(math.floor(duration_seconds/30*6))} ({math.ceil(duration_seconds/30)} chunks)")
    print("Running Transcription")
    run_trasncription()
    chunks = split_text_file("transcription.txt")
    responses = []
    count = 1
    for i in chunks:
        pyperclip.copy(i)
        print(f"Copied chunk {count}/{len(chunks)} to clipboard. Please paste it in a new ChatGPT conversation and come back wiht the response.")
        input("Enter to continue.")
        response = pyperclip.paste()
        responses.append(response)
        count += 1

    with open("result.txt", "w", encoding="utf-8") as file:
        for string in responses:
            file.write(string + "\n")

    print("Result saved in result.txt")
if __name__ == "__main__":
    run_main()