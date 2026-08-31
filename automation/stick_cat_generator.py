#!/usr/bin/env python3
"""
Stick Cat Academy - Stick Cat Image Generator
Generates stick cat character images using Pollinations AI
"""

import os
import requests
import time
import hashlib

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CHARACTERS_DIR = os.path.join(SCRIPT_DIR, "..", "assets", "characters")
CACHE_DIR = os.path.join(SCRIPT_DIR, ".image_cache")

STYLES = {
    "professor": {
        "prompt": "cute minimal stick figure cat wearing glasses and bow tie, standing next to a chalkboard, holding a pointer stick, professor outfit, simple black lines on white background, cartoon style, clean vector art",
        "suffix": "stick figure cat professor with chalkboard, minimal style"
    },
    "luna": {
        "prompt": "cute minimal stick figure female cat with eyelashes, holding a notebook and pen, curious expression, simple black lines on white background, cartoon style, clean vector art",
        "suffix": "stick figure female cat student, minimal style"
    },
    "mochi": {
        "prompt": "cute minimal stick figure cat sleeping on desk, drooling, lazy expression, zzz symbols, simple black lines on white background, cartoon style, clean vector art",
        "suffix": "stick figure lazy sleeping cat, minimal style"
    },
    "vs_owner_scene": {
        "prompt": "cute minimal stick figure cat knocking things off a table, human stick figure looking shocked, simple black lines on white background, cartoon comic strip style, clean vector art",
        "suffix": "stick figure cat vs owner comedy scene, minimal style"
    },
    "cat_logic_scene": {
        "prompt": "cute minimal stick figure cat doing weird cat behavior, with question marks around, educational feel, simple black lines on white background, cartoon style, clean vector art",
        "suffix": "stick figure cat mystery explained, minimal style"
    },
    "lifehack_scene": {
        "prompt": "cute minimal stick figure cat at chalkboard teaching a lesson, with simple diagrams, educational comedy, simple black lines on white background, cartoon style, clean vector art",
        "suffix": "stick figure cat teaching life hack, minimal style"
    },
    "title_card": {
        "prompt": "cute minimal stick figure cats in a classroom, Professor Whiskers at front, Luna and Mochi at desks, chalkboard says Academy, simple black lines on white background, cartoon style, logo design, clean vector art",
        "suffix": "Stick Cat Academy logo, minimal style"
    },
    "flashback_professor": {
        "prompt": "beautiful Studio Ghibli anime style, wise old cat professor with glasses in a magical warm glowing library, soft watercolor background, cherry blossoms, golden light, detailed anime illustration, Miyazaki style, pastel colors, dreamy atmosphere",
        "suffix": "Ghibli style wise cat professor in magical library"
    },
    "flashback_luna": {
        "prompt": "beautiful Studio Ghibli anime style, cute young female cat character with big eyes, sitting in a field of flowers, soft watercolor background, warm sunset light, detailed anime illustration, Miyazaki style, pastel colors, nostalgic atmosphere",
        "suffix": "Ghibli style young cat in flower field"
    },
    "flashback_mochi": {
        "prompt": "beautiful Studio Ghibli anime style, chubby lazy cat sleeping on a fluffy cloud, dreamy sky background, soft pastel colors, floating stars, detailed anime illustration, Miyazaki style, peaceful atmosphere",
        "suffix": "Ghibli style sleeping cat on cloud"
    },
    "flashback_scene": {
        "prompt": "beautiful Studio Ghibli anime style, magical forest with glowing fireflies, small cats walking on a path, soft watercolor painting, warm golden light, detailed anime landscape, Miyazaki style, dreamy nostalgic atmosphere",
        "suffix": "Ghibli style magical forest scene"
    }
}

def ensure_dirs():
    os.makedirs(CHARACTERS_DIR, exist_ok=True)
    os.makedirs(CACHE_DIR, exist_ok=True)

def get_cache_key(prompt, width, height):
    return hashlib.md5(f"{prompt}_{width}_{height}".encode()).hexdigest()

def generate_image(prompt, width=512, height=512, output_path=None):
    ensure_dirs()

    cache_key = get_cache_key(prompt, width, height)
    cache_path = os.path.join(CACHE_DIR, f"{cache_key}.png")

    if os.path.exists(cache_path) and output_path:
        import shutil
        shutil.copy2(cache_path, output_path)
        return output_path

    encoded_prompt = requests.utils.quote(prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={width}&height={height}&nologo=true&seed={int(time.time())}"

    print(f"  [AI] Generating image: {prompt[:60]}...")

    try:
        response = requests.get(url, timeout=60)
        if response.status_code == 200:
            with open(cache_path, "wb") as f:
                f.write(response.content)

            if output_path:
                import shutil
                shutil.copy2(cache_path, output_path)
                return output_path
            return cache_path
        else:
            print(f"  [ERROR] Pollinations returned {response.status_code}")
            return None
    except Exception as e:
        print(f"  [ERROR] {e}")
        return None

def generate_character_image(character_key, output_path=None):
    if character_key not in STYLES:
        print(f"  [ERROR] Unknown character: {character_key}")
        return None

    style = STYLES[character_key]
    prompt = style["prompt"]

    if not output_path:
        output_path = os.path.join(CHARACTERS_DIR, f"{character_key}.png")

    return generate_image(prompt, 512, 512, output_path)

def generate_scene_image(scene_type, custom_prompt=None, output_path=None):
    if custom_prompt:
        prompt = f"cute minimal stick figure cat scene: {custom_prompt}, simple black lines on white background, cartoon style, clean vector art"
    elif scene_type in STYLES:
        prompt = STYLES[scene_type]["prompt"]
    else:
        prompt = f"cute minimal stick figure cat scene: {scene_type}, simple black lines on white background, cartoon style"

    if not output_path:
        output_path = os.path.join(CHARACTERS_DIR, f"scene_{int(time.time())}.png")

    return generate_image(prompt, 768, 432, output_path)

def generate_episode_frames(script, output_dir):
    ensure_dirs()
    os.makedirs(output_dir, exist_ok=True)

    frames = []
    content_type = script.get("type", "vs_owner")

    frame_count = min(len(script.get("lines", [])), 8)

    for i in range(frame_count):
        line = script["lines"][i]
        character = line["character"]

        if character in ["professor"]:
            scene_type = "lifehack_scene" if content_type == "life_hacks" else "cat_logic_scene"
        elif content_type == "vs_owner":
            scene_type = "vs_owner_scene"
        elif content_type == "cat_logic":
            scene_type = "cat_logic_scene"
        else:
            scene_type = "lifehack_scene"

        frame_path = os.path.join(output_dir, f"frame_{i:02d}.png")

        if character in STYLES:
            result = generate_character_image(character, frame_path)
        else:
            result = generate_scene_image(scene_type, output_path=frame_path)

        if result:
            frames.append({
                "path": result,
                "character": character,
                "text": line["text"],
                "line_index": i
            })
            print(f"  [OK] Frame {i+1}/{frame_count}: {character}")

        time.sleep(1)

    return frames

def generate_all_characters():
    ensure_dirs()
    print("Generating character images...")
    for key in ["professor", "luna", "mochi"]:
        path = os.path.join(CHARACTERS_DIR, f"{key}.png")
        if not os.path.exists(path):
            generate_character_image(key, path)
            print(f"  [OK] {key}")
        else:
            print(f"  [SKIP] {key} exists")
    print("Done!")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "characters":
        generate_all_characters()
    else:
        print("Usage: python stick_cat_generator.py characters")
