# ElevenLabs TTS for Home Assistant

This component is a custom integration to allow [Home Assistant](https://www.home-assistant.io/) to use [ElevenLabs TTS](https://elevenlabs.io/docs/api-reference/text-to-speech).


## Install

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=emmaly&repository=elevenlabs-tts&category=integration)


## Default Config

```yaml
# configuration.yaml
tts:
  - platform: elevenlabs_tts
    api_key: YOUR_API_KEY
    model_id: eleven_multilingual_v1
    voice_id: piTKgcLEGmPE4e6mEKli # Nicole (prefers model eleven_multilingual_v1)
```


#### Example configuration options:
```yaml
tts:
  - platform: elevenlabs_tts
    api_key: YOUR_API_KEY
    model_id: eleven_multilingual_v2
    voice_id: 21m00Tcm4TlvDq8ikWAM # Rachel (voice has no model preference)
    stability: 0.5          # 0.00 to 1.00, default 0.50
    similarity_boost: 0.75  # 0.00 to 1.00, default 0.75
    style: 0                # 0.00 to 1.00, default 0.00
    use_speaker_boost: true # default true
```

```yaml
tts:
  - platform: elevenlabs_tts
    api_key: YOUR_API_KEY
    model_id: eleven_multilingual_v1
    voice_id: jsCqWAovK2LkecY7zXl4 # Freya (prefers model eleven_multilingual_v1)
    stability: 0.5          # 0.00 to 1.00, default 0.50
    similarity_boost: 0.75  # 0.00 to 1.00, default 0.75
    style: 0                # 0.00 to 1.00, default 0.00
    use_speaker_boost: true # default true
```
