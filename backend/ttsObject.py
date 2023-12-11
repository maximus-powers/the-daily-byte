import os
from google.cloud import texttospeech
from dotenv import load_dotenv

load_dotenv()
class TTSObject:
    def __init__(self):
        self.client = texttospeech.TextToSpeechClient() # inits client

    def script_to_audio(self, script):
        synthesis_input = texttospeech.SynthesisInput(text=script) # set the script to be synthesized

        # voice vars
        voice = texttospeech.VoiceSelectionParams(
            language_code="en-US",
            name="en-US-Studio-M",
            ssml_gender=texttospeech.SsmlVoiceGender.MALE
        )

        # we want an mp3
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )

        # send request
        response = self.client.synthesize_speech(
            input=synthesis_input,
            voice=voice,
            audio_config=audio_config
        )

        return_dict = {}
        return_dict['audio'] = response.audio_content # this is already binary
        return_dict['script'] = script
        # print("Script synthesized")
        
        return return_dict

# tts_object = TTSObject()
# mp3_file = tts_object.script_to_audio("Hello and welcome to the daily byte")