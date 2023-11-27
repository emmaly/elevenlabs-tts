import aiohttp
import logging
from homeassistant.components.tts import Provider
import homeassistant.helpers.config_validation as cv
import voluptuous as vol

_LOGGER = logging.getLogger(__name__)

# Configuration Schema
PLATFORM_SCHEMA = vol.Schema(
    {
        vol.Required("api_key"): cv.string,
        vol.Optional("model_id"): cv.string,
        vol.Optional("voice_id"): cv.string,
        vol.Optional("stability"): vol.All(cv.positive_float, vol.Range(min=0.0, max=1.0)),
        vol.Optional("similarity_boost"): vol.All(cv.positive_float, vol.Range(min=0.0, max=1.0)),
        vol.Optional("style"): vol.All(cv.positive_float, vol.Range(min=0.0, max=1.0)),
        vol.Optional("use_speaker_boost"): cv.boolean,
    }
)

class ElevenLabsTTSProvider(Provider):
    def __init__(self, hass, conf):
        self.api_key = conf.get('api_key')
        self.hass = hass

    async def async_get_tts_audio(self, message, language, options=None):
        default_voice_id = "piTKgcLEGmPE4e6mEKli"
        voice_id = options.get('voice_id', default_voice_id) if options else default_voice_id

        default_model_id = "eleven_multilingual_v1"
        model_id = options.get('model_id', default_model_id) if options else default_model_id

        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
        voice_settings = {k: v for k, v in (options or {}).items() if k in ['stability', 'similarity_boost', 'style', 'use_speaker_boost']}

        payload = {
            "text": message,
            "model_id": model_id,
            "voice_settings": voice_settings
        }
        headers = {
            "xi-api-key": self.api_key,
            "Content-Type": "application/json"
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload, headers=headers) as response:
                    if response.status == 200:
                        return "audio/mpeg", await response.read()
                    else:
                        _LOGGER.error(f"Error from ElevenLabs API: {response.status}")
                        return None, None
        except Exception as e:
            _LOGGER.error(f"Error communicating with ElevenLabs API: {e}")
            return None, None
