#!/usr/bin/env python3
"""
Stick Cat Academy - Script Generator
Generates episode scripts for three content types:
1. Stick Cat vs Owner - daily relatable battles
2. Cat Logic - why cats do weird things
3. Master Cat Life Hacks - Professor Whiskers teaches
"""

import json
import os
import random
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(SCRIPT_DIR, "templates")
PROCESSED_FILE = os.path.join(SCRIPT_DIR, "processed_episodes.json")

CHARACTERS = {
    "professor": {
        "name": "Professor Whiskers",
        "short": "Professor",
        "voice": "en-US-GuyNeural",
        "personality": "wise, slightly dramatic, loves teaching"
    },
    "luna": {
        "name": "Luna",
        "short": "Luna",
        "voice": "en-US-JennyNeural",
        "personality": "curious, enthusiastic, eager to learn"
    },
    "mochi": {
        "name": "Mochi",
        "short": "Mochi",
        "voice": "en-US-ChristopherNeural",
        "personality": "lazy, sleepy, always distracted, lovable"
    },
    "owner": {
        "name": "Owner",
        "short": "Owner",
        "voice": "en-US-AriaNeural",
        "personality": "confused, trying their best"
    }
}

def load_templates(content_type):
    path = os.path.join(TEMPLATES_DIR, f"{content_type}.json")
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return []

def load_processed():
    if os.path.exists(PROCESSED_FILE):
        with open(PROCESSED_FILE, "r") as f:
            return json.load(f)
    return {"vs_owner": [], "cat_logic": [], "life_hacks": []}

def save_processed(data):
    with open(PROCESSED_FILE, "w") as f:
        json.dump(data, f, indent=2)

def get_next_episode_number(content_type, processed):
    return len(processed.get(content_type, [])) + 1

def generate_vs_owner_script(template=None):
    if not template:
        templates = load_templates("vs_owner")
        template = random.choice(templates) if templates else {
            "title": "When you're eating and cat stares",
            "scene": "owner eating, cat staring",
            "dialogue": [
                {"character": "owner", "text": "Just trying to eat my lunch in peace..."},
                {"character": "luna", "text": "What are you eating? Is that for me?"},
                {"character": "owner", "text": "No, this is my food."},
                {"character": "luna", "text": "But I'm staring at you. That means it's mine now."},
                {"character": "mochi", "text": "Zzz... wake me when there's tuna..."},
                {"character": "luna", "text": "*pushes plate closer to edge*"},
                {"character": "owner", "text": "Don't you dare!"},
                {"character": "luna", "text": "*knocks plate off table* Too late."},
            ]
        }

    script_lines = []
    for line in template["dialogue"]:
        char = CHARACTERS.get(line["character"], CHARACTERS["luna"])
        script_lines.append({
            "character": line["character"],
            "character_name": char["short"],
            "voice": char["voice"],
            "text": line["text"]
        })

    return {
        "type": "vs_owner",
        "title": template["title"],
        "scene": template.get("scene", ""),
        "lines": script_lines,
        "duration_estimate": len(script_lines) * 4
    }

def generate_cat_logic_script(template=None):
    if not template:
        templates = load_templates("cat_logic")
        template = random.choice(templates) if templates else {
            "title": "Why cats knead with their paws",
            "fact": "Kitten behavior from nursing, shows comfort and contentment",
            "dialogue": [
                {"character": "luna", "text": "Professor, why do I keep pressing my paws on everything?"},
                {"character": "professor", "text": "Ah, excellent question, Luna! That's called kneading."},
                {"character": "professor", "text": "When you were a kitten, you pressed your mother's belly to get milk."},
                {"character": "luna", "text": "So I'm doing it because... I'm happy?"},
                {"character": "professor", "text": "Precisely! It's a comfort behavior from kittenhood."},
                {"character": "mochi", "text": "*kneading the desk* I'm kneading too!"},
                {"character": "professor", "text": "Mochi, you're kneading your homework. That's not the same thing."},
                {"character": "mochi", "text": "It feels nice though..."},
            ]
        }

    script_lines = []
    for line in template["dialogue"]:
        char = CHARACTERS.get(line["character"], CHARACTERS["luna"])
        script_lines.append({
            "character": line["character"],
            "character_name": char["short"],
            "voice": char["voice"],
            "text": line["text"]
        })

    return {
        "type": "cat_logic",
        "title": template["title"],
        "fact": template.get("fact", ""),
        "lines": script_lines,
        "duration_estimate": len(script_lines) * 4
    }

def generate_life_hack_script(template=None):
    if not template:
        templates = load_templates("life_hacks")
        template = random.choice(templates) if templates else {
            "title": "How to sleep in 10 minutes",
            "topic": "sleep efficiency",
            "dialogue": [
                {"character": "professor", "text": "Good morning, class! Today's lesson: How to sleep in just 10 minutes."},
                {"character": "luna", "text": "Is that even possible, Professor?"},
                {"character": "professor", "text": "Of course! Cats sleep 16 hours a day. We are the experts."},
                {"character": "professor", "text": "Step one: Find the warmest spot in the room."},
                {"character": "mochi", "text": "*already asleep on a sunbeam*"},
                {"character": "professor", "text": "Step two: Curl into a tight ball. Reduce surface area."},
                {"character": "luna", "text": "Like this? *curls up*"},
                {"character": "professor", "text": "Perfect! Step three: Close your eyes and think of tuna."},
                {"character": "mochi", "text": "I'm already dreaming of tuna... zzz..."},
                {"character": "professor", "text": "And that's how you sleep in 10 minutes. Class dismissed!"},
            ]
        }

    script_lines = []
    for line in template["dialogue"]:
        char = CHARACTERS.get(line["character"], CHARACTERS["luna"])
        script_lines.append({
            "character": line["character"],
            "character_name": char["short"],
            "voice": char["voice"],
            "text": line["text"]
        })

    return {
        "type": "life_hacks",
        "title": template["title"],
        "topic": template.get("topic", ""),
        "lines": script_lines,
        "duration_estimate": len(script_lines) * 4
    }

def generate_episode(content_type=None):
    processed = load_processed()

    if not content_type:
        types = ["vs_owner", "cat_logic", "life_hacks"]
        weights = [0.4, 0.3, 0.3]
        content_type = random.choices(types, weights=weights, k=1)[0]

    ep_num = get_next_episode_number(content_type, processed)

    if content_type == "vs_owner":
        script = generate_vs_owner_script()
    elif content_type == "cat_logic":
        script = generate_cat_logic_script()
    else:
        script = generate_life_hack_script()

    script["episode_number"] = ep_num
    script["timestamp"] = datetime.now().isoformat()

    output_dir = os.path.join(SCRIPT_DIR, "..", "scripts")
    os.makedirs(output_dir, exist_ok=True)

    script_path = os.path.join(output_dir, f"{content_type}_{ep_num:03d}.json")
    with open(script_path, "w") as f:
        json.dump(script, f, indent=2)

    processed[content_type].append(ep_num)
    save_processed(processed)

    print(f"Generated: {script['title']}")
    print(f"Type: {content_type} | Episode: {ep_num}")
    print(f"Lines: {len(script['lines'])} | Est. duration: {script['duration_estimate']}s")
    print(f"Saved: {script_path}")

    return script_path, script

if __name__ == "__main__":
    import sys
    content_type = sys.argv[1] if len(sys.argv) > 1 else None
    generate_episode(content_type)
