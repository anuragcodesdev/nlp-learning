import os
from datetime import datetime
import edge_tts

async def speak_response(text: str, voice: str = "en-US-JennyNeural", output_folder: str = "reflection_outputs") -> None:
    """
    Convert text to speech and save the audio output using Microsoft Edge TTS.

    Params:
        :text: The string content to be spoken aloud.
        :voice: The voice model used for synthesis (default is Jenny, US accent).
        :output_folder: Folder where the audio file will be saved.
    Returns:
        :None: Saves MP3 file locally and prints path.
    """
    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Format timestamped filename
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_file = os.path.join(output_folder, f"reflection_{timestamp}.mp3")

    # Generate and save speech
    await edge_tts.Communicate(text, voice).save(output_file)

    print(f"Audio response saved: {output_file}")