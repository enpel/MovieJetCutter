
# jetcut

This project provides a tool for processing video files, extracting audio tracks, detecting silence, and generating clips with transcriptions. The user interface allows for easy file selection and processing.

## Features

- Extracts audio tracks from video files
- Detects silence with buffer zones
- Transcribes audio to text using Google Speech Recognition
- Generates video clips based on detected audio segments
- Outputs processed video clips and a CSV file with timestamps and transcriptions

## Requirements

- Python 3.6 or higher
- FFmpeg
- Required Python libraries

## Setup

### 1. Clone the Repository

```sh
git clone https://github.com/enpel/MovieJetCutter.git
cd MoviewJetCutter
```

### 2. Create and Activate a Virtual Environment

#### Windows

```sh
python -m venv venv
venv\Scripts\activate
```

#### MacOS/Linux

```sh
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Required Libraries

```sh
pip install -r requirements.txt
```

If `requirements.txt` does not exist, manually install the necessary libraries:

```sh
pip install moviepy pydub speechrecognition tkinter
```

### 4. Install FFmpeg

#### Windows

1. Download FFmpeg from the [official website](https://ffmpeg.org/download.html).
2. Extract the downloaded archive.
3. Add the `bin` directory to your system's PATH environment variable.

#### MacOS

```sh
brew install ffmpeg
```

#### Linux (Debian-based)

```sh
sudo apt-get install ffmpeg
```

## Usage

1. Ensure your virtual environment is activated:

   ```sh
   # Windows
   venv\Scripts\activate

   # MacOS/Linux
   source venv/bin/activate
   ```

2. Run the script:

   ```sh
   python jetcut.py
   ```

3. Use the GUI to select a video file and process it.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


## Acknowledgments

- [MoviePy](https://zulko.github.io/moviepy/)
- [pydub](https://github.com/jiaaro/pydub)
- [SpeechRecognition](https://github.com/Uberi/speech_recognition)
- [FFmpeg](https://ffmpeg.org/)

