#!/usr/bin/env python3
"""
Stick Cat Academy - Video Assembler
Combines stick cat images + voiceover into final video using FFmpeg
"""

import os
import subprocess
import json

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def get_audio_duration(audio_path):
    cmd = [
        "ffprobe", "-v", "quiet", "-print_format", "json",
        "-show_format", audio_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        data = json.loads(result.stdout)
        return float(data.get("format", {}).get("duration", 5.0))
    return 5.0

def create_video_from_frames_and_audio(frames, audio_files, output_path, bg_color="white"):
    if not frames or not audio_files:
        print("  [ERROR] No frames or audio files provided")
        return None

    temp_dir = os.path.join(os.path.dirname(output_path), "temp")
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
            "-vf", "scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2:color=white",
            "-pix_fmt", "yuv420p",
            "-shortest",
            "-t", str(duration + 0.5),
            segment_path
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            segments.append(segment_path)
            print(f"  [OK] Segment {i+1}: {duration:.1f}s")
        else:
            print(f"  [ERROR] Segment {i+1}: {result.stderr[:200]}")

    if not segments:
        print("  [ERROR] No segments created")
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
        print(f"  [OK] Video: {output_path}")
        return output_path
    else:
        print(f"  [ERROR] Concat failed: {result.stderr[:200]}")
        return None

def create_video_from_images(image_paths, audio_path, output_path, fps=1):
    if not image_paths:
        return None

    duration_per_image = get_audio_duration(audio_path) / max(len(image_paths), 1)

    input_args = []
    for img in image_paths:
        input_args.extend(["-loop", "1", "-t", str(duration_per_image), "-i", img])

    filter_parts = []
    n = len(image_paths)
    for i in range(n):
        filter_parts.append(f"[{i}:v]scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2:color=white[v{i}]")

    concat_inputs = "".join(f"[v{i}]" for i in range(n))
    filter_parts.append(f"{concat_inputs}concat=n={n}:v=1:a=0[outv]")

    filter_complex = ";".join(filter_parts)

    cmd = [
        "ffmpeg", "-y",
    ] + input_args + [
        "-i", audio_path,
        "-filter_complex", filter_complex,
        "-map", "[outv]", "-map", f"{n}:a",
        "-c:v", "libx264", "-c:a", "aac",
        "-shortest",
        "-movflags", "+faststart",
        output_path
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"  [OK] Video created: {output_path}")
        return output_path
    else:
        print(f"  [ERROR] {result.stderr[:300]}")
        return None

def assemble_episode(frames, audio_files, output_dir, episode_title="episode"):
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"{episode_title}.mp4")

    print(f"\n[VIDEO] Assembling {len(frames)} frames + {len(audio_files)} audio files...")

    result = create_video_from_frames_and_audio(frames, audio_files, output_path)

    if result:
        size_mb = os.path.getsize(result) / (1024 * 1024)
        print(f"  [DONE] {result} ({size_mb:.1f} MB)")

    return result

if __name__ == "__main__":
    print("Stick Cat Academy - Video Assembler")
    print("Run via generate_video.py for full pipeline")
