#!/usr/bin/env python3
"""
Stick Cat Academy - Main Video Generator
Full pipeline: Script → Images → Voiceover → Video → Upload
"""

import os
import sys
import json
import time
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from script_generator import generate_episode, CHARACTERS
from stick_cat_generator import generate_episode_frames
from voiceover import generate_full_voiceover
from video_assembler import assemble_episode
from youtube_upload import upload_video

OUTPUT_DIR = os.path.join(SCRIPT_DIR, "..", "output")

def generate_thumbnail(script, output_dir):
    try:
        from PIL import Image, ImageDraw, ImageFont
        img = Image.new("RGB", (1280, 720), color=(255, 255, 255))
        draw = ImageDraw.Draw(img)

        draw.rectangle([(0, 0), (1280, 100)], fill=(13, 115, 119))

        try:
            font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 36)
            font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
        except:
            font_large = ImageFont.load_default()
            font_small = ImageFont.load_default()

        draw.text((640, 50), "STICK CAT ACADEMY", fill="white", font=font_large, anchor="mm")

        title = script.get("title", "Episode")
        draw.text((640, 400), title[:60], fill="black", font=font_small, anchor="mm")

        content_type = script.get("type", "vs_owner")
        type_labels = {
            "vs_owner": "Stick Cat vs Owner",
            "cat_logic": "Cat Logic",
            "life_hacks": "Master Cat Life Hack"
        }
        draw.text((640, 450), type_labels.get(content_type, ""), fill=(13, 115, 119), font=font_small, anchor="mm")

        thumb_path = os.path.join(output_dir, "thumbnail.jpg")
        img.save(thumb_path, "JPEG", quality=90)
        print(f"  [THUMBNAIL] {thumb_path}")
        return thumb_path
    except Exception as e:
        print(f"  [ERROR] Thumbnail: {e}")
        return None

def generate_video(content_type=None, upload=False):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    print("=" * 60)
    print("STICK CAT ACADEMY - Video Generator")
    print("=" * 60)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    print("[1/5] Generating script...")
    script_path, script = generate_episode(content_type)
    print(f"  Title: {script['title']}")
    print(f"  Type: {script['type']} | Episode: {script['episode_number']}")
    print(f"  Lines: {len(script['lines'])}")
    print()

    episode_dir = os.path.join(OUTPUT_DIR, f"episode_{script['episode_number']:03d}_{script['type']}")
    frames_dir = os.path.join(episode_dir, "frames")
    audio_dir = os.path.join(episode_dir, "audio")
    os.makedirs(episode_dir, exist_ok=True)

    print("[2/5] Generating stick cat images...")
    frames = generate_episode_frames(script, frames_dir)
    print(f"  Generated {len(frames)} frames")
    print()

    print("[3/5] Generating voiceover...")
    audio_files = generate_full_voiceover(script, audio_dir)
    print(f"  Generated {len(audio_files)} audio lines")
    print()

    print("[4/5] Creating video...")
    video_path = assemble_episode(frames, audio_files, episode_dir, f"episode_{script['episode_number']:03d}")
    print()

    print("[5/5] Creating thumbnail...")
    thumbnail_path = generate_thumbnail(script, episode_dir)
    print()

    upload_result = None
    if upload and video_path:
        print("[UPLOAD] Uploading to YouTube...")
        type_labels = {
            "vs_owner": "Stick Cat vs Owner",
            "cat_logic": "Cat Logic Explained",
            "life_hacks": "Master Cat Life Hack"
        }
        title = f"Stick Cat Academy #{script['episode_number']} - {script['title']}"
        description = f"""Professor Whiskers teaches life the way cats see it!

{type_labels.get(script['type'], '')}: {script['title']}

Subscribe for daily stick cat content!

#StickCat #CatComedy #ProfessorCat #StickFigure #FunnyCats"""
        upload_result = upload_video(video_path, title, description)
        print()

    metadata = {
        "title": script["title"],
        "type": script["type"],
        "episode_number": script["episode_number"],
        "script": script_path,
        "video": video_path,
        "thumbnail": thumbnail_path,
        "frames": len(frames),
        "audio_lines": len(audio_files),
        "upload": upload_result,
        "timestamp": timestamp,
    }

    meta_path = os.path.join(episode_dir, "metadata.json")
    with open(meta_path, "w") as f:
        json.dump(metadata, f, indent=2)

    print("=" * 60)
    print("COMPLETE!")
    print(f"  Title: {script['title']}")
    print(f"  Video: {video_path}")
    if upload_result and upload_result.get("success"):
        print(f"  YouTube: {upload_result['url']}")
    print("=" * 60)

    return metadata

if __name__ == "__main__":
    content_type = sys.argv[1] if len(sys.argv) > 1 else None
    do_upload = "--upload" in sys.argv
    generate_video(content_type, do_upload)
