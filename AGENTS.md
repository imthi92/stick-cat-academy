# Stick Cat Academy - AGENTS.md

## What
YouTube channel producing stick-figure cat animated content. Professor, Luna, Mochi characters teach cat logic and life hacks.

## Tech Stack
- Python 3.11+
- edge-tts (voice generation)
- moviepy (video assembly)
- Pillow (frame rendering)
- YouTube Data API v3 (upload via OAuth2)

## Key Files
- automation/generate_short.py - Shorts generator (1080x1920 vertical, 4 lines)
- automation/generate_episode.py - Long episode generator (1920x1080 horizontal)
- automation/youtube_upload.py - YouTube OAuth2 upload
- automation/youtube_token.pickle - NEVER COMMIT (in .gitignore)
- automation/client_secret.json - NEVER COMMIT (in .gitignore)
- automation/script_generator.py - Script generation
- automation/voiceover.py - TTS voice generation
- automation/video_assembler.py - FFmpeg video assembly

## How to Deploy
1. Push to main branch
2. GitHub Actions triggers daily_shorts.yml (Mon-Fri 2PM UTC) or weekly_long.yml (Thursday 2PM UTC)
3. Workflow runs generate_short.py or generate_episode.py
4. Video uploaded to YouTube as private, then published

## How to Run Locally
```
cd automation
pip install edge-tts moviepy Pillow google-api-python-client google-auth-oauthlib
python generate_short.py
```

## Known Issues
1. youtube_token.pickle EOFError: File gets corrupted. Fix: regenerate with authenticate_youtube.py or from cat-podcast-voice-gen repo
2. Secret scanning blocks push if pickle/client_secret.json accidentally committed: git reset --soft HEAD~1, unstage, recommit
3. If voice sounds robotic: check edge-tts version >= 7.2.0

## Environment
- GROQ_API_KEY: Not used in this repo (cat-podcast-voice-gen uses it)
- YouTube OAuth: client_secret.json + youtube_token.pickle in automation/

## YouTube Schedule
- Shorts: Mon-Fri 2PM UTC (vertical 1080x1920, 4 topics per day)
- Long-form: Thursday 2PM UTC (horizontal 1920x1080)

## .gitignore
automation/youtube_token.pickle
automation/client_secret.json
automation/__pycache__/
output/
