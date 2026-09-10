#!/usr/bin/env python3
"""
Stick Cat Academy - Shorts Generator
Generates short vertical videos (1080x1920, 15-60 seconds)
"""

import os
import sys
import json
import subprocess
import random
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from stick_cat_generator import generate_episode_frames
from voiceover import generate_full_voiceover
from youtube_upload import upload_video

OUTPUT_DIR = os.path.join(SCRIPT_DIR, "..", "output")

SHORT_TOPICS = [
    {"type": "vs_owner", "title": "Cat vs Alarm Clock", "lines": [
        ("professor", "Today's lesson: The art of ignoring alarms."),
        ("luna", "Professor, how do you sleep through everything?"),
        ("professor", "Step 1: Hear the alarm. Step 2: Close eyes harder."),
        ("mochi", "I've been practicing this my whole life."),
    ]},
    {"type": "cat_logic", "title": "Why Cats Sit in Boxes", "lines": [
        ("professor", "Question: Why do cats sit in boxes?"),
        ("luna", "Is it because they feel safe?"),
        ("professor", "No. It's because the box didn't run away."),
        ("mochi", "Yet."),
    ]},
    {"type": "life_hacks", "title": "How to Open Any Door", "lines": [
        ("professor", "Life hack: How to open any door."),
        ("luna", "Use the handle?"),
        ("professor", "No. Sit in front of it and meow until a human opens it."),
        ("mochi", "Works 100% of the time."),
    ]},
    {"type": "vs_owner", "title": "The 3 AM Zoomies", "lines": [
        ("professor", "Class, explain the 3 AM zoomies."),
        ("luna", "Sudden burst of energy at night?"),
        ("professor", "Correct. It's called 'Circuit Training for Cats'."),
        ("mochi", "I prefer 'Terrorize the Household Cardio'."),
    ]},
    {"type": "cat_logic", "title": "If I Fits I Sits", "lines": [
        ("professor", "The law of If I Fits I Sits."),
        ("luna", "If a cat can fit in it, the cat must sit in it?"),
        ("professor", "Exactly. Even if it's a teacup."),
        ("mochi", "Especially if it's a teacup."),
    ]},
    {"type": "life_hacks", "title": "Professional Napper", "lines": [
        ("professor", "Career tip: Become a professional napper."),
        ("luna", "Is that a real job?"),
        ("professor", "Cats have been doing it for 10,000 years."),
        ("mochi", "I'm overqualified."),
    ]},
    {"type": "vs_owner", "title": "Keyboard Cat", "lines": [
        ("professor", "Today: How to help your owner work from home."),
        ("luna", "Sit on the keyboard?"),
        ("professor", "Correct. Maximum disruption, minimum effort."),
        ("mochi", "I also like to chew the mouse cable."),
    ]},
    {"type": "cat_logic", "title": "The Red Dot Mystery", "lines": [
        ("professor", "The red dot. The eternal mystery."),
        ("luna", "What IS it?"),
        ("professor", "Nobody knows. But we must catch it."),
        ("mochi", "I caught it once. It disappeared."),
    ]},
]

def get_audio_duration(audio_path):
    cmd = [
        "ffprobe", "-v", "quiet", "-print_format", "json",
        "-show_format", audio_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        data = json.loads(result.stdout)
        return float(data.get("format", {}).get("duration", 3.0))
    return 3.0

def assemble_shorts(frames, audio_files, output_dir, title="short"):
    """Assemble vertical shorts video (1080x1920)."""
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"{title}.mp4")
    temp_dir = os.path.join(output_dir, "temp")
    os.makedirs(temp_dir, exist_ok=True)

    segments = []
    for i, (frame, audio) in enumerate(zip(frames, audio_files)):
        duration = get_audio_duration(audio["path"])
        segment_path = os.path.join(temp_dir, f"segment_{i:02d}.mp4")

        cmd = [
            "ffmpeg", "-y",
            "-loop", "1", "-i", frame["path"],
            "-i", audio["path"],
            "-c:v", "libx264", "-tune", "stillimage",
            "-c:a", "aac", "-b:a", "192k",
            "-vf", "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:color=white",
            "-pix_fmt", "yuv420p",
            "-shortest",
            "-t", str(duration + 0.3),
            segment_path
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            segments.append(segment_path)
            print(f"  [OK] Segment {i+1}: {duration:.1f}s")

    if not segments:
        return None

    concat_file = os.path.join(temp_dir, "concat.txt")
    with open(concat_file, "w") as f:
        for seg in segments:
            f.write(f"file '{seg}'\n")

    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", concat_file,
        "-c:v", "libx264",
        "-c:a", "aac",
        "-movflags", "+faststart",
        output_path
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    for seg in segments:
        try:
            os.remove(seg)
        except:
            pass
    try:
        os.remove(concat_file)
        os.rmdir(temp_dir)
    except:
        pass

    if result.returncode == 0:
        return output_path
    return None

def generate_short():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    print("=" * 60)
    print("STICK CAT ACADEMY - Shorts Generator")
    print("=" * 60)

    topic = random.choice(SHORT_TOPICS)
    script = {
        "title": topic["title"],
        "type": topic["type"],
        "episode_number": int(timestamp[-4:]),
        "lines": [{"character": c, "text": t} for c, t in topic["lines"]],
    }

    print(f"Topic: {script['title']}")
    print(f"Type: {script['type']}")
    print(f"Lines: {len(script['lines'])}")

    short_dir = os.path.join(OUTPUT_DIR, f"short_{timestamp}")
    frames_dir = os.path.join(short_dir, "frames")
    audio_dir = os.path.join(short_dir, "audio")
    os.makedirs(short_dir, exist_ok=True)

    print("\n[1/4] Generating frames...")
    frames = generate_episode_frames(script, frames_dir)
    print(f"  {len(frames)} frames generated")

    print("\n[2/4] Generating voiceover...")
    audio_files = generate_full_voiceover(script, audio_dir)
    print(f"  {len(audio_files)} audio lines generated")

    print("\n[3/4] Assembling vertical video...")
    video_path = assemble_shorts(frames, audio_files, short_dir, f"short_{timestamp}")
    if not video_path:
        print("  [ERROR] Video assembly failed")
        return None

    print(f"  Video: {video_path}")

    print("\n[4/4] Uploading to YouTube...")
    title = f"Stick Cat Academy Shorts - {script['title']}"
    description = f"""{script['title']}

Professor Whiskers teaches life the way cats see it!

#StickCat #Shorts #CatComedy #ProfessorCat #FunnyCats"""

    upload_result = upload_video(video_path, title, description)

    metadata = {
        "title": script["title"],
        "type": script["type"],
        "video": video_path,
        "upload": upload_result,
        "timestamp": timestamp,
        "format": "shorts_vertical_1080x1920",
    }

    meta_path = os.path.join(short_dir, "metadata.json")
    with open(meta_path, "w") as f:
        json.dump(metadata, f, indent=2)

    print("\n" + "=" * 60)
    print("SHORTS COMPLETE!")
    print(f"  Title: {script['title']}")
    print(f"  Video: {video_path}")
    if upload_result and upload_result.get("success"):
        print(f"  YouTube: {upload_result['url']}")
    print("=" * 60)

    return metadata

if __name__ == "__main__":
    generate_short()
