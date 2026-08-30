#!/usr/bin/env python3
"""
Stick Cat Academy - YouTube Upload
Reuses the same OAuth token from cat-podcast-voice-gen
"""

import os
import sys
import pickle

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

try:
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload
    HAS_YT_API = True
except ImportError:
    HAS_YT_API = False

SCOPES = ["https://www.googleapis.com/auth/youtube"]
CLIENT_SECRETS_FILE = os.path.join(SCRIPT_DIR, "client_secret.json")
TOKEN_FILE = os.path.join(SCRIPT_DIR, "youtube_token.pickle")

DEFAULT_CONFIG = {
    "category_id": "24",
    "privacy_status": "private",
    "default_language": "en",
    "embeddable": True,
    "public_stats_viewable": True,
}

DEFAULT_TAGS = [
    "stick cat", "cat animation", "stick figure cat",
    "professor cat", "cat comedy", "funny cats",
    "cat vs owner", "cat logic", "life hacks",
    "stick cat academy", "cat education", "cat funny",
]

def get_youtube_service():
    if not HAS_YT_API:
        print("ERROR: YouTube API libraries not installed")
        return None

    credentials = None
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'rb') as token:
            credentials = pickle.load(token)

    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            if not os.path.exists(CLIENT_SECRETS_FILE):
                print(f"ERROR: {CLIENT_SECRETS_FILE} not found!")
                return None
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
            credentials = flow.run_local_server(port=0)

        with open(TOKEN_FILE, 'wb') as token:
            pickle.dump(credentials, token)

    return build('youtube', 'v3', credentials=credentials)

def upload_video(video_path, title, description, tags=None, category_id=None, privacy_status=None):
    youtube = get_youtube_service()
    if not youtube:
        return {"success": False, "error": "YouTube service not available"}

    if not os.path.exists(video_path):
        return {"success": False, "error": f"Video not found: {video_path}"}

    body = {
        "snippet": {
            "title": title[:100],
            "description": description[:5000],
            "tags": (tags or DEFAULT_TAGS)[:30],
            "categoryId": category_id or DEFAULT_CONFIG["category_id"],
        },
        "status": {
            "privacyStatus": privacy_status or DEFAULT_CONFIG["privacy_status"],
            "embeddable": DEFAULT_CONFIG["embeddable"],
            "publicStatsViewable": DEFAULT_CONFIG["public_stats_viewable"],
        }
    }

    media = MediaFileUpload(video_path, mimetype="video/mp4", resumable=True)

    try:
        request = youtube.videos().insert(
            part="snippet,status",
            body=body,
            media_body=media
        )
        response = request.execute()
        video_id = response["id"]
        url = f"https://youtube.com/watch?v={video_id}"
        print(f"  [UPLOAD] {url}")
        return {"success": True, "video_id": video_id, "url": url}
    except Exception as e:
        print(f"  [ERROR] Upload failed: {e}")
        return {"success": False, "error": str(e)}

def create_thumbnail(video_id, thumbnail_path):
    youtube = get_youtube_service()
    if not youtube:
        return False

    if not os.path.exists(thumbnail_path):
        return False

    try:
        youtube.thumbnails().set(
            videoId=video_id,
            media_body=MediaFileUpload(thumbnail_path, mimetype="image/jpeg")
        ).execute()
        print(f"  [THUMBNAIL] Set for {video_id}")
        return True
    except Exception as e:
        print(f"  [ERROR] Thumbnail failed: {e}")
        return False

if __name__ == "__main__":
    print("YouTube Upload module ready")
