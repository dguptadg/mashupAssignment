import sys
import os
import yt_dlp
from pydub import AudioSegment

# USAGE 

def print_usage():
    print("Usage:")
    print('python 102303877.py "<SingerName>" <NumberOfVideos> <AudioDuration> <OutputFileName>')
    print('Example:')
    print('python 102303877.py "Sharry Maan" 20 21 output.mp3')


# SETUP 

def create_directories():
    os.makedirs("videos", exist_ok=True)
    os.makedirs("audios", exist_ok=True)
    os.makedirs("trimmed", exist_ok=True)
    os.makedirs("output", exist_ok=True)


def validate_arguments():
    if len(sys.argv) != 5:
        print("Error: Incorrect number of arguments.")
        print_usage()
        sys.exit(1)

    singer = sys.argv[1]

    try:
        num_videos = int(sys.argv[2])
        duration = int(sys.argv[3])
    except ValueError:
        print("Error: NumberOfVideos and AudioDuration must be integers.")
        sys.exit(1)

    output_file = sys.argv[4]

    if num_videos <= 10:
        print("Error: NumberOfVideos must be greater than 10.")
        sys.exit(1)

    if duration <= 20:
        print("Error: AudioDuration must be greater than 20 seconds.")
        sys.exit(1)

    if not output_file.lower().endswith(".mp3"):
        print("Error: OutputFileName must end with .mp3")
        sys.exit(1)

    return singer, num_videos, duration, output_file


# DOWNLOAD 

def download_videos(singer, num_videos):
    if os.listdir("videos"):
        print("Videos already exist. Skipping download.")
        return

    print(f"\nDownloading {num_videos} videos for singer: {singer}")

    ydl_opts = {
        "format": "best",
        "outtmpl": "videos/%(title)s.%(ext)s",
        "noplaylist": True
    }

    search_query = f"ytsearch{num_videos}:{singer} songs"

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([search_query])

    print("Video download completed.")


#  VIDEO → AUDIO 

def convert_videos_to_audio():
    if os.listdir("audios"):
        print("Audios already exist. Skipping conversion.")
        return

    print("\nConverting videos to audio...")

    for file in os.listdir("videos"):
        video_path = os.path.join("videos", file)

        if not os.path.isfile(video_path):
            continue

        try:
            audio = AudioSegment.from_file(video_path)
            audio_name = os.path.splitext(file)[0] + ".mp3"
            audio_path = os.path.join("audios", audio_name)
            audio.export(audio_path, format="mp3")
            print(f"Converted: {file}")
        except Exception as e:
            print(f"Skipping {file}: {e}")

    print("Audio conversion completed.")


# TRIMMING 

def trim_audio_files(duration):
    if os.listdir("trimmed"):
        print("Trimmed audios already exist. Skipping trimming.")
        return

    print(f"\nTrimming first {duration} seconds from each audio...")
    trim_ms = duration * 1000

    for file in os.listdir("audios"):
        audio_path = os.path.join("audios", file)

        if not audio_path.lower().endswith(".mp3"):
            continue

        try:
            audio = AudioSegment.from_mp3(audio_path)

            if len(audio) < trim_ms:
                print(f"Skipping {file}: shorter than {duration} seconds")
                continue

            trimmed_audio = audio[:trim_ms]
            trimmed_path = os.path.join("trimmed", file)
            trimmed_audio.export(trimmed_path, format="mp3")
            print(f"Trimmed: {file}")
        except Exception as e:
            print(f"Error trimming {file}: {e}")

    print("Audio trimming completed.")


#  MERGING 

def merge_audio_files(output_file):
    print("\nMerging trimmed audio files...")

    combined = AudioSegment.empty()
    files = sorted(os.listdir("trimmed"))

    if not files:
        print("Error: No trimmed audio files found.")
        sys.exit(1)

    for file in files:
        if file.lower().endswith(".mp3"):
            audio = AudioSegment.from_mp3(os.path.join("trimmed", file))
            combined += audio
            print(f"Added: {file}")

    output_path = os.path.join("output", output_file)
    combined.export(output_path, format="mp3")

    print(f"\nFinal merged file created: {output_path}")


# MAIN 

def main():
    singer, num_videos, duration, output_file = validate_arguments()
    create_directories()
    download_videos(singer, num_videos)
    convert_videos_to_audio()
    trim_audio_files(duration)
    merge_audio_files(output_file)


if __name__ == "__main__":
    main()
