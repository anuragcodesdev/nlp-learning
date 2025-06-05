# NLP Audio Transcription Pipeline

This project presents a structured pipeline for processing and transcribing English-language audiobooks sourced from the LibriVox API. The workflow encompasses data acquisition, audio conversion, chunk-based transcription, and organised storage of outputs, facilitating experimentation in natural language processing tasks.

## Overview

The pipeline automates the following steps:

1. **Data Acquisition**: Fetches metadata for a set of audiobooks using the LibriVox API.
2. **Random Selection**: Randomly selects an audiobook from the fetched list.
3. **Audio Retrieval**: Obtains the audio URL for the first chapter of the selected audiobook.
4. **Format Conversion**: Downloads the MP3 audio and converts it to WAV format using `pydub`.
5. **Chunk-Based Transcription**: Processes the WAV file in defined segments (excluding the first chunk) and transcribes each using Google's Speech Recognition API.
6. **Output Management**: Organises the converted audio and transcription text into date-stamped directories for streamlined data management.

## Directory Structure

The outputs are organised as follows:

```
├── processed_audio/
│   └── YYYY-MM-DD/
│       └── [book_title].wav
├── transcriptions/
│   └── YYYY-MM-DD/
│       └── [book_title].txt
├── SpeechToText.ipynb
└── requirements.txt
```

* `processed_audio/`: Contains the converted `.wav` files, organised by processing date.
* `transcriptions/`: Holds the corresponding transcription text files, also organised by date.
* `SpeechToText.ipynb`: Jupyter Notebook implementing the audio processing and transcription workflow.
* `requirements.txt`: Lists the Python dependencies required to run the pipeline.

## Setup Instructions

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/anuragcodesdev/nlp-learning.git
   cd nlp-audio-transcription
   ```

2. **Create a Virtual Environment** (optional but recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Install `ffmpeg`**:

   `pydub` requires `ffmpeg` for audio conversion. Ensure `ffmpeg` is installed and accessible in your system's PATH.

   * **macOS**: `brew install ffmpeg`
   * **Ubuntu**: `sudo apt-get install ffmpeg`
   * **Windows**: Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH.

## Usage

Open the `SpeechToText.ipynb` notebook and execute the cells sequentially to initiate the transcription pipeline.

The notebook will:

* Retrieve metadata for 10 audiobooks from the LibriVox API.
* Randomly select one audiobook and obtain the audio URL for its first chapter.
* Download the MP3 audio and convert it to WAV format.
* Transcribe the WAV file in 20-second chunks, skipping the first chunk.
* Save the converted audio and transcription text into date-stamped directories.

## Notes

* The pipeline is configured to process and transcribe the second to fourth 20-second chunks of the audio file, skipping the first chunk to avoid potential non-speech segments.
* All audio sources are from LibriVox, which provides public domain audiobooks, ensuring compliance with usage rights.
* This setup is intended for educational and experimental purposes, facilitating exploration in speech-to-text transcription and subsequent NLP tasks.
