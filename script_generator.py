import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

def initialize_gemini():
    """Initialize Gemini API with the provided API key"""
    api_key = os.getenv('GOOGLE_GEMINI_API_KEY')
    if not api_key:
        raise ValueError("Gemini API key not found in environment variables")
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-pro')

def generate_script(text, tone):
    """
    Generate a podcast script using Gemini AI
    """
    try:
        model = initialize_gemini()

        # Create prompt for Gemini
        prompt = f"""
        Create an engaging podcast script for 'To Put It Simply' with hosts Krish and Zaara.
        The tone should be {tone}.

        Guidelines for the conversation:
        - Zaara wrote the article and provides expert insights
        - Krish asks engaging questions and facilitates discussion
        - Include natural filler words like "uh", "um", and word repetitions
        - Use short, speech-synthesis-friendly sentences
        - Show genuine excitement and emotion in the conversation
        - Create a natural back-and-forth dialogue
        - Format each line with the speaker's name

        Format the output exactly like this:
        Krish: [dialogue]
        Zaara: [dialogue]

        Source text to discuss:
        {text[:8000]}  # Using more text for longer conversations

        Make it engaging and conversational, with natural back-and-forth.
        The conversation should thoroughly explore the topic with authentic reactions and follow-up questions.
        DO NOT include any background music or sound effect descriptions.
        """

        # Generate script using Gemini
        response = model.generate_content(prompt)

        if not response.text:
            raise ValueError("Failed to generate script content")

        return response.text

    except Exception as e:
        raise Exception(f"Error generating script: {str(e)}")

def format_dialogue(text):
    """Format the dialogue to separate speakers"""
    lines = text.split('\n')
    krish_lines = []
    zaara_lines = []

    for line in lines:
        if line.startswith('Krish:'):
            krish_lines.append(line.replace('Krish:', '').strip())
        elif line.startswith('Zaara:'):
            zaara_lines.append(line.replace('Zaara:', '').strip())

    return {
        'krish': krish_lines,
        'zaara': zaara_lines
    }

def get_tone_intro(tone):
    """Generate tone-specific introduction"""
    intros = {
        "Professional": "Welcome to this informative podcast where we'll explore an important topic.",
        "Insightful": "Get ready for a deep dive into a fascinating subject.",
        "Funny": "Hey folks! Ready for a not-so-serious take on this topic?",
        "Brainrot": "Yo what's up everyone! Let's get absolutely unhinged with this content!"
    }
    return intros.get(tone, "Welcome to this podcast.")

def get_tone_outro(tone):
    """Generate tone-specific conclusion"""
    outros = {
        "Professional": "Thank you for listening to this informative session.",
        "Insightful": "I hope these insights have expanded your understanding of the topic.",
        "Funny": "Well, that's all folks! Hope you had as much fun as I did!",
        "Brainrot": "Aight, that's all the chaos for today! Peace out!"
    }
    return outros.get(tone, "Thanks for listening.")