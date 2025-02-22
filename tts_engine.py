import io
from gtts import gTTS
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env.

class TTSEngine:
    def __init__(self):
        # Initialize voice settings for different speakers
        self.voice_settings = {
            "krish": {
                "lang": "en",
                "tld": "co.in"
            },  # Male voice - Indian English
            "zaara": {
                "lang": "en",
                "tld": "us"
            },  # Female voice - US English
        }

        # Tone modifications
        self.tone_settings = {
            "Professional": {
                "slow": False
            },
            "Insightful": {
                "slow": False
            },
            "Funny": {
                "slow": False
            },
            "Brainrot": {
                "slow": False
            }
        }

    def generate_speech(self, text, speaker, tone="Professional"):
        """Generate speech from text using gTTS"""
        try:
            # Get settings for the specified speaker
            settings = self.voice_settings.get(speaker.lower(),
                                               self.voice_settings["krish"])
            tone_setting = self.tone_settings.get(tone, {"slow": False})

            # Create gTTS instance
            tts = gTTS(text=text,
                       lang=settings["lang"],
                       tld=settings["tld"],
                       slow=tone_setting["slow"])

            # Save to a temporary file
            temp_file = f"temp_{speaker}_{hash(text)}.mp3"  # Unique filename
            tts.save(temp_file)
            return temp_file

        except Exception as e:
            raise Exception(f"Error generating speech: {str(e)}")


def text_to_speech(text, tone):
    """
    Convert script to speech using Google Text-to-Speech
    Returns the audio data as bytes
    """
    try:
        from script_generator import format_dialogue

        # Split the script into separate lines for each speaker
        dialogue = format_dialogue(text)

        engine = TTSEngine()
        audio_files = []  # Store paths to temporary audio files

        # Generate audio for each line
        max_lines = max(len(dialogue['krish']), len(dialogue['zaara']))

        for i in range(max_lines):
            if i < len(dialogue['krish']):
                audio_file = engine.generate_speech(dialogue['krish'][i], "krish", tone)
                audio_files.append(audio_file)

            if i < len(dialogue['zaara']):
                audio_file = engine.generate_speech(dialogue['zaara'][i], "zaara", tone)
                audio_files.append(audio_file)

        # Combine audio files into a single file
        final_audio_path = "final_podcast.mp3"
        with open(final_audio_path, "wb") as final_audio:
            for audio_file in audio_files:
                with open(audio_file, "rb") as f:
                    final_audio.write(f.read())  # Append audio data
                os.remove(audio_file)  # Delete temporary file

        # Read the final audio file as bytes
        with open(final_audio_path, "rb") as f:
            audio_data = f.read()

        # Delete the final audio file after reading its data
        os.remove(final_audio_path)

        return audio_data  # Return audio data as bytes

    except Exception as e:
        raise Exception(f"Error generating audio: {str(e)}")