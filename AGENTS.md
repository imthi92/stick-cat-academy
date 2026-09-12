# Stick Cat Academy — Memory

## Overview
- **Repo:** imthi92/stick-cat-academy
- **Channel:** @StickCatAcademy
- **Schedule:** Daily shorts (Mon-Fri 2PM UTC) + Weekly long video (Thursday 2PM UTC)

## Key Files
- `automation/generate_short.py` — Shorts generator (vertical 1080x1920)
- `automation/generate_episode.py` — Long episode generator
- `automation/youtube_upload.py` — YouTube upload with OAuth2
- `automation/youtube_token.pickle` — **NEVER commit** (in .gitignore)
- `automation/client_secret.json` — **NEVER commit** (in .gitignore)

## Important Notes
- Token pickle must be regenerated if corrupted (`EOFError: Ran out of input`)
- YouTube upload uses `google.oauth2.credentials` with refresh token
- `.gitignore` must include: `youtube_token.pickle`, `client_secret.json`, `__pycache__/`, `output/`
- If push blocked by secret scanning: `git reset --soft HEAD~1`, unstage secrets

## YouTube Schedule
- Shorts: Mon-Fri 2PM UTC (vertical 1080x1920)
- Long-form: Thursday 2PM UTC (horizontal 1920x1080)
