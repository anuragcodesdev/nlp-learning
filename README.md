# NLP Audio Transcription

This notebook provides a practical workflow for **speech-to-text transcription** and basic **NLP processing**. It’s built in Jupyter Notebook to focus on real-world tasks like audio preprocessing, transcription, and data management.

## Overview

The notebook processes `.m4a` audio files by:

- Converting them to `.wav` using `pydub` (since `.m4a` from MacOS voice memos is not compatible with Google’s Speech Recognition API)
- Transcribing the converted audio using Google’s Speech Recognition API
- Organising outputs in date-based directories for efficient data tracking
- Removing original `.m4a` files after conversion to maintain a clean workspace

This workflow covers typical data handling steps:

- **Data ingestion**: Handling raw audio inputs
- **Preprocessing**: Converting audio formats for downstream tasks
- **Inference**: Extracting text from audio recordings
- **Output management**: Saving and organising results for traceability
- **Data hygiene**: Keeping only what’s necessary for reproducibility and clarity

It’s a practical way to work with audio data in an NLP context and lays the groundwork for further exploration of sentiment analysis and conversational systems.

## Setup

Install Python dependencies:

```bash
pip install -r requirements.txt
