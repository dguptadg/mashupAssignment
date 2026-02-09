import os
import yt_dlp
from pydub import AudioSegment
import zipfile
import smtplib
from email.message import EmailMessage




def create_dirs(base="temp"):
    os.makedirs(f"{base}/videos", exist_ok=True)
    os.makedirs(f"{base}/audios", exist_ok=True)
    os.makedirs(f"{base}/trimmed", exist_ok=True)
    os.makedirs(f"{base}/output", exist_ok=True)
    



def generate_mashup(singer, num_videos, duration):
    # Detect Streamlit Cloud
    if os.getenv("STREAMLIT_SERVER_RUNNING"):
        raise Exception(
            "YouTube download is disabled on Streamlit Cloud. "
            "Please run the mashup locally for full functionality."
        )
    base = "temp"
    create_dirs(base)

    # DOWNLOAD VIDEOS 
    if not os.listdir(f"{base}/videos"):
        ydl_opts = {
            "format": "best",
            "outtmpl": f"{base}/videos/%(title)s.%(ext)s",
            "noplaylist": True
        }

        search_query = f"ytsearch{num_videos}:{singer} songs"

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([search_query])

    # VIDEO → AUDIO
    if not os.listdir(f"{base}/audios"):
        for file in os.listdir(f"{base}/videos"):
            path = os.path.join(f"{base}/videos", file)
            audio = AudioSegment.from_file(path)
            out = os.path.splitext(file)[0] + ".mp3"
            audio.export(f"{base}/audios/{out}", format="mp3")

    #  TRIM AUDIO
    trim_ms = duration * 1000

    if not os.listdir(f"{base}/trimmed"):
        for file in os.listdir(f"{base}/audios"):
            audio = AudioSegment.from_mp3(f"{base}/audios/{file}")
            trimmed = audio[:trim_ms]
            trimmed.export(f"{base}/trimmed/{file}", format="mp3")

    # MERGE 
    combined = AudioSegment.empty()
    for file in sorted(os.listdir(f"{base}/trimmed")):
        audio = AudioSegment.from_mp3(f"{base}/trimmed/{file}")
        combined += audio

    output_path = f"{base}/output/final_mashup.mp3"
    combined.export(output_path, format="mp3")

    zip_path = zip_output_file(output_path)
    return zip_path



def zip_output_file(mp3_path):
    zip_path = os.path.join("temp", "output", "mashup_result.zip")

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(
            mp3_path,
            arcname=os.path.basename(mp3_path)
        )

    return zip_path




def send_email(receiver_email, zip_path):
    sender_email = os.getenv("SENDER_EMAIL")
    app_password = os.getenv("APP_PASSWORD")

    if not sender_email or not app_password:
        raise Exception("Email credentials not configured")

    msg = EmailMessage()
    msg["Subject"] = "Your Mashup File"
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg.set_content(
        "Hello,\n\nYour mashup has been generated successfully.\n"
        "Please find the attached ZIP file.\n\nRegards"
    )

    with open(zip_path, "rb") as f:
        msg.add_attachment(
            f.read(),
            maintype="application",
            subtype="zip",
            filename="mashup_result.zip"
        )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, app_password)
        server.send_message(msg)



