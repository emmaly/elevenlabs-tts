import requests
from homeassistant.components.tts import HomeAssistantTTSProvider

class ElevenLabsTTSProvider(HomeAssistantTTSProvider):
    def __init__(self, hass, conf):
        self.api_key = conf.get('api_key')

    def get_tts_audio(self, message, language, options=None):
        default_voice_id = "piTKgcLEGmPE4e6mEKli"
        voice_id = options.get('voice_id', default_voice_id) if options else default_voice_id

        default_model_id = "eleven_multilingual_v1"
        model_id = options.get('model_id', default_model_id) if options else default_model_id

        # API URL with the voice ID
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

        # Initialize voice settings only with provided options
        voice_settings = {k: v for k, v in (options or {}).items() if k in ['similarity_boost', 'stability', 'style', 'use_speaker_boost']}

        payload = {
            "text": message,
            "model_id": model_id,
            "voice_settings": voice_settings
        }
        headers = {
            "xi-api-key": self.api_key,
            "Content-Type": "application/json"
        }

        response = requests.request("POST", url, json=payload, headers=headers)

        if response.status_code == 200:
            return "audio/mpeg", response.content
        else:
            return None, None
