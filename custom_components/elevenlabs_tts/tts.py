"""Support for the ElevenLabs TTS service."""
import os
import aiohttp
import logging
from homeassistant.components.tts import CONF_LANG, PLATFORM_SCHEMA, Provider, TtsAudioType
import homeassistant.helpers.config_validation as cv
import voluptuous as vol

_LOGGER = logging.getLogger(__name__)

DEFAULT_MODEL_ID            = "eleven_multilingual_v1"
DEFAULT_VOICE_ID            = "piTKgcLEGmPE4e6mEKli"
DEFAULT_STABILITY           = 0.50
DEFAULT_SIMILARITY_BOOST    = 0.75
DEFAULT_STYLE               = 0.00
DEFAULT_SPEAKER_BOOST       = True

CONF_API_KEY            = "api_key"
CONF_MODEL_ID           = "model_id"
CONF_VOICE_ID           = "voice_id"
CONF_STABILITY          = "stability"
CONF_SIMILARITY_BOOST   = "similarity_boost"
CONF_STYLE              = "style"
CONF_SPEAKER_BOOST      = "use_speaker_boost"

SUPPORTED_OPTIONS = [
    CONF_MODEL_ID,
    CONF_VOICE_ID,
    CONF_STABILITY,
    CONF_SIMILARITY_BOOST,
    CONF_STYLE,
    CONF_SPEAKER_BOOST,
]

API_KEY_SCHEMA          = cv.string
MODEL_ID_SCHEMA         = cv.string
VOICE_ID_SCHEMA         = cv.string
STABILITY_SCHEMA        = vol.All(vol.Coerce(float), vol.Clamp(min=0.0, max=1.0))
SIMILARITY_BOOST_SCHEMA = vol.All(vol.Coerce(float), vol.Clamp(min=0.0, max=1.0))
STYLE_SCHEMA            = vol.All(vol.Coerce(float), vol.Clamp(min=0.0, max=1.0))
SPEAKER_BOOST_SCHEMA    = cv.boolean

# Configuration Schema
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_API_KEY):                                             API_KEY_SCHEMA,
        vol.Optional(CONF_MODEL_ID,         default=DEFAULT_MODEL_ID):          MODEL_ID_SCHEMA,
        vol.Optional(CONF_VOICE_ID,         default=DEFAULT_VOICE_ID):          VOICE_ID_SCHEMA,
        vol.Optional(CONF_STABILITY,        default=DEFAULT_STABILITY):         STABILITY_SCHEMA,
        vol.Optional(CONF_SIMILARITY_BOOST, default=DEFAULT_SIMILARITY_BOOST):  SIMILARITY_BOOST_SCHEMA,
        vol.Optional(CONF_STYLE,            default=DEFAULT_STYLE):             STYLE_SCHEMA,
        vol.Optional(CONF_SPEAKER_BOOST,    default=DEFAULT_SPEAKER_BOOST):     SPEAKER_BOOST_SCHEMA,
    }
)

async def async_get_engine(hass, config, discovery_info=None):
    """Set up ElevenLabs TTS component."""
    return ElevenLabsTTSProvider(
        hass,
        config.get(CONF_API_KEY),
        config.get(CONF_MODEL_ID),
        config.get(CONF_VOICE_ID),
        config.get(CONF_STABILITY),
        config.get(CONF_SIMILARITY_BOOST),
        config.get(CONF_STYLE),
        config.get(CONF_SPEAKER_BOOST),
    )

class ElevenLabsTTSProvider(Provider):
    """The ElevenLabs TTS API provider."""

    def __init__(
            self,
            hass,
            api_key             = None,
            model_id            = DEFAULT_MODEL_ID,
            voice_id            = DEFAULT_VOICE_ID,
            stability           = DEFAULT_STABILITY,
            similarity_boost    = DEFAULT_SIMILARITY_BOOST,
            style               = DEFAULT_STYLE,
            use_speaker_boost   = DEFAULT_SPEAKER_BOOST,
        ):
        self.hass               = hass
        self._api_key           = api_key
        self._voice_id          = voice_id
        self._model_id          = model_id
        self._stability         = stability
        self._similarity_boost  = similarity_boost
        self._style             = style
        self._use_speaker_boost = use_speaker_boost

    @property
    def default_language(self):
        """Return the default language."""
        return self.hass.config.language # TODO: change if ElevenLabs actually uses this in the future

    @property
    def supported_languages(self):
        """Return the list of supported languages."""
        return [self.hass.config.language] # TODO: change if ElevenLabs actually uses this in the future

    @property
    def supported_options(self):
        """Return list of supported options."""
        return SUPPORTED_OPTIONS

    @property
    def default_options(self):
        """Return dict include default options."""
        return {
            CONF_MODEL_ID:          self._model_id,
            CONF_VOICE_ID:          self._voice_id,
            CONF_STABILITY:         self._stability,
            CONF_SIMILARITY_BOOST:  self._similarity_boost,
            CONF_STYLE:             self._style,
            CONF_SPEAKER_BOOST:     self._use_speaker_boost,
        }

    async def async_get_tts_audio(self, message, language, options=None) -> TtsAudioType:
        """Load TTS using ElevenLabs API."""

        options_schema = vol.Schema(
            {
                vol.Optional(CONF_MODEL_ID,         default=self._model_id):            MODEL_ID_SCHEMA,
                vol.Optional(CONF_VOICE_ID,         default=self._voice_id):            VOICE_ID_SCHEMA,
                vol.Optional(CONF_STABILITY,        default=self._stability):           STABILITY_SCHEMA,
                vol.Optional(CONF_SIMILARITY_BOOST, default=self._similarity_boost):    SIMILARITY_BOOST_SCHEMA,
                vol.Optional(CONF_STYLE,            default=self._style):               STYLE_SCHEMA,
                vol.Optional(CONF_SPEAKER_BOOST,    default=self._use_speaker_boost):   SPEAKER_BOOST_SCHEMA,
            }
        )
        options = options_schema(options or {})

        url = f"https://api.elevenlabs.io/v1/text-to-speech/{options[CONF_VOICE_ID]}"
        voice_settings = {k: v for k, v in (options or {}).items() if k in ['stability', 'similarity_boost', 'style', 'use_speaker_boost']}

        payload = {
            "text": message,
            "model_id": options[CONF_MODEL_ID],
            "voice_settings": voice_settings
        }
        headers = {
            "xi-api-key": self._api_key,
            "Content-Type": "application/json"
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload, headers=headers) as response:
                    if response.status == 200:
                        data = await response.read()
                        return "mp3", data
                    else:
                        _LOGGER.error(f"Error from ElevenLabs API: {response.status}")
                        return None, None
        except Exception as e:
            _LOGGER.error(f"Error communicating with ElevenLabs API: {e}")
            return None, None
