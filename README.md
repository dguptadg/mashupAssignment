# Mashup Assignment

## Project Overview

The Music Mashup Creator is a comprehensive audio processing application that automatically downloads YouTube videos of a singer, extracts audio, trims segments, and merges them into a single cohesive mashup file. The project includes both a command-line tool and a web-based interface built with Streamlit.

## Website Link 

The link for the website created for the project is :
</br>
https://mashup-website-hedregmvji7xwcujgnww7u.streamlit.app/

## Methodology

### 1. **Video Download Phase**
- Uses `yt-dlp` library to search YouTube for music videos
- Downloads the best quality version available
- Searches with query pattern: `ytsearch{N}:{singer} songs`
- Stores downloaded videos in the `videos/` directory

### 2. **Audio Extraction Phase**
- Converts video files to MP3 format using `pydub` library
- Extracts audio stream from each video
- Stores converted audio files in the `audios/` directory

### 3. **Audio Trimming Phase**
- Trims each audio file to a user-specified duration (in seconds)
- Validates that audio files are at least as long as the requested duration
- Skips shorter audio files with appropriate warnings
- Stores trimmed segments in the `trimmed/` directory

### 4. **Audio Merging Phase**
- Combines all trimmed audio segments in sorted order
- Concatenates audio segments sequentially
- Exports the final merged mashup as an MP3 file
- Stores final output in the `output/` directory

### 5. **Email Delivery (Web Service Only)**
- Packages the final mashup into a ZIP file
- Sends the mashup file via email to user-specified email address
- Uses Gmail SMTP with app-specific passwords for authentication

## Features

### Command-Line Tool (102303877.py)

**Features:**
- Fully automated mashup generation from command line
- Input validation for all parameters
- Directory creation and management
- Skip existing files to resume interrupted processes
- Detailed console output for each processing step

**Usage:**
```bash
python 102303877.py "<SingerName>" <NumberOfVideos> <AudioDuration> <OutputFileName>
```

**Example:**
```bash
python 102303877.py "Sharry Maan" 20 21 output.mp3
```

**Parameters:**
- `SingerName`: Name of the artist (enclosed in quotes)
- `NumberOfVideos`: Minimum 11 videos to download
- `AudioDuration`: Minimum 21 seconds per segment
- `OutputFileName`: Must end with `.mp3` extension

**Validation:**
- NumberOfVideos must be > 10
- AudioDuration must be > 20 seconds
- OutputFileName must be a valid MP3 file
- All parameters are required

### Web Application (Streamlit)

**Features:**
- User-friendly web interface
- Real-time form validation
- Email notification system
- Progress spinner during processing
- Comprehensive error handling and user feedback

**Input Fields:**
- Singer Name (text input)
- Number of Videos (numeric input, minimum 1)
- Duration of Each Segment (in seconds, minimum 1)
- Email ID (for receiving the mashup file)

**Constraints:**
- Number of videos must be > 10
- Duration must be > 20 seconds
- Valid email format required
- YouTube download disabled on Streamlit Cloud (local execution only)

## Technical Stack

**Libraries Used:**
- `yt-dlp`: YouTube video downloading and searching
- `pydub`: Audio file processing and conversion
- `streamlit`: Web application framework
- `smtplib`: Email sending functionality
- `zipfile`: Output file compression

**Python Version:** 3.7+

**Dependencies:** See `requirements.txt`
```
streamlit
yt-dlp
pydub
```

## Results & Outputs

### Expected Output Files

1. **final_mashup.mp3** - The completed mashup file containing all audio segments merged together
2. **mashup_result.zip** - ZIP-compressed version of the mashup (web service only)

### Output Characteristics

- **Format**: MP3 (MPEG Audio Layer III)
- **Total Duration**: `(NumberOfVideos × AudioDuration) seconds`
- **Quality**: Best quality available from YouTube sources
- **File Size**: Varies based on video count and segment duration

### Example Output

For a mashup with 20 videos at 21 seconds each:
- Total Duration: ~420 seconds (7 minutes)
- File contains 20 concatenated audio segments
- Preserves original audio quality through the processing pipeline

## Setup & Installation

### Command-Line Setup

1. **Install Python Dependencies:**
   ```bash
   pip install streamlit yt-dlp pydub
   ```

2. **Install FFmpeg** (required by pydub):
   - Windows: Download from [ffmpeg.org](https://ffmpeg.org) or use `choco install ffmpeg`
   - macOS: `brew install ffmpeg`
   - Linux: `sudo apt-get install ffmpeg`

3. **Run the Script:**
   ```bash
   python 102303877.py "Artist Name" 15 21 mashup.mp3
   ```

### Web Application Setup

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Email (Optional):**
   Set environment variables for email functionality:
   ```bash
   export SENDER_EMAIL="your-email@gmail.com"
   export APP_PASSWORD="your-app-specific-password"
   ```

3. **Run the Web App:**
   ```bash
   streamlit run app.py
   ```

## Error Handling

### Common Errors & Solutions

| Error | Cause | Solution |
|-------|-------|----------|
| "NumberOfVideos must be > 10" | Insufficient video count | Increase parameter to >= 11 |
| "AudioDuration must be > 20 seconds" | Duration too short | Increase parameter to >= 21 |
| "OutputFileName must end with .mp3" | Invalid output format | Use `.mp3` extension |
| "YouTube download is disabled on Streamlit Cloud" | Cloud restriction | Run application locally |
| "No trimmed audio files found" | Audio extraction failed | Check internet connection and video availability |

### Graceful Degradation

- Skips videos/audios shorter than requested duration
- Resumes from last successful step if process is interrupted
- Validates input parameters before processing begins
- Provides detailed error messages for troubleshooting

## Limitations & Constraints

1. **YouTube Availability**: Videos must be publicly accessible and downloadable
2. **Audio Quality**: Limited to best quality available on YouTube (typically 128-256 kbps)
3. **Cloud Deployment**: yt-dlp limitations prevent execution on Streamlit Cloud
4. **Audio Length**: Cannot trim audio shorter than requested duration
5. **Email Service**: Requires Gmail account with app-specific password


