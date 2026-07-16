#!/usr/bin/env python3
"""

- 6 core emotions: angry, disgust, fear, happy, neutral, sad
- 12 emojis mapped to those emotions
- 5 users, each with friendly names
- Each user: inputs 20–25 emojis, with one dominant emoji (7–12 times), rest random
- Output: user input emojis, dominant mood with metrics, and rationale
"""

import numpy as np
import random
from collections import Counter

# 1. Define 6 core emotions and their representative emojis
EMOTIONS = [
    ("Angry", "😡"),
    ("Disgust", "🤢"),
    ("Fear", "😱"),
    ("Happy", "😀"),
    ("Neutral", "😐"),
    ("Sad", "😢")
]

# 2. 12 emojis, each mapped to a 6-dim emotion vector
EMOJI_RATINGS = {
    "😀": [1,1,1,10,3,1],   # Happy
    "😂": [1,1,1,9,2,1],    # Happy
    "😢": [1,1,2,1,2,10],   # Sad
    "😡": [10,2,2,1,2,2],   # Angry
    "😱": [2,1,10,1,2,2],   # Fear
    "😐": [1,1,1,2,10,2],   # Neutral
    "🤢": [1,10,2,1,2,2],   # Disgust
    "😞": [1,1,2,1,2,9],    # Sad
    "😏": [3,2,1,6,3,1],    # Happy/Neutral
    "😤": [9,2,2,2,2,2],    # Angry
    "😋": [1,1,1,9,2,1],    # Happy
    "😬": [2,2,3,2,4,2]     # Neutral
}

emoji_list = list(EMOJI_RATINGS.keys())
ratings_mat = np.array([EMOJI_RATINGS[e] for e in emoji_list])

# 3. User names and related mood groups (to guide non-contradictory emoji assignment)
NAMES_AND_MOODGROUPS = [
    ("Alice", ["Happy", "Neutral", "Sad"]),
    ("Bob", ["Happy", "Neutral", "Fear"]),
    ("Carol", ["Angry", "Happy", "Sad"]),
    ("Dave", ["Happy", "Neutral", "Angry"]),
    ("Eva", ["Fear", "Sad", "Happy"])
]

EMOTION_TO_EMOJIS = {
    "Angry":   ["😡", "😤"],
    "Disgust": ["🤢"],
    "Fear":    ["😱"],
    "Happy":   ["😀", "😂", "😋", "😏"],
    "Neutral": ["😐", "😬"],
    "Sad":     ["😢", "😞"]
}

# 4. Generate user emoji inputs with dominant emoji
random.seed(2025)
USER_INPUTS = {}
USER_DOMINANT = {}

for name, mood_group in NAMES_AND_MOODGROUPS:
    # Pick dominant emoji from allowed mood group
    possible_emojis = []
    for mood in mood_group:
        possible_emojis.extend(EMOTION_TO_EMOJIS[mood])
    possible_emojis = [e for e in possible_emojis if e in emoji_list]
    dominant_emoji = random.choice(possible_emojis)
    USER_DOMINANT[name] = dominant_emoji
    n_total = random.randint(18,30)
    n_dom = random.randint(6, 12)
    n_rest = n_total - n_dom
    emojis = [dominant_emoji] * n_dom
    # For rest, avoid over-favoring the dominant
    other_emojis = [e for e in emoji_list if e != dominant_emoji]
    emojis += random.choices(other_emojis, k=n_rest)
    random.shuffle(emojis)
    USER_INPUTS[name] = emojis

def normalize(vec):
    total = vec.sum()
    return vec / total if total > 0 else vec

def emoji_confidence_pct(idx):
    vec = normalize(ratings_mat[idx])
    top2 = np.partition(vec, -2)[-2:]
    return float(np.mean(top2) * 100)

def usage_probability(count, total, unique_k):
    return (count + 1) / (total + unique_k) * 100

def dominant_emotion_from_input(emojis):
    cnt = Counter(emojis)
    total = len(emojis)
    top_emoji, top_count = cnt.most_common(1)[0]
    idx = emoji_list.index(top_emoji)
    conf = emoji_confidence_pct(idx)
    prob = usage_probability(top_count, total, len(cnt))
    emo, score = EMOTIONS[np.argmax(ratings_mat[idx])][0], ratings_mat[idx][np.argmax(ratings_mat[idx])]
    return top_emoji, emo, score, conf, prob, top_count, total

# 5. Output results in new format
for name in USER_INPUTS:
    emojis = USER_INPUTS[name]
    top_emoji, emo, score, conf, prob, top_count, total = dominant_emotion_from_input(emojis)
    print(f"{name}'s Input Emojis: {' '.join(emojis)}")
    print(f"Dominant Mood: {emo} ")
    print(f"Reason: The emoji {top_emoji} appears {top_count} times out of {total}, strongly indicating {emo.lower()} as the predominant mood.\n")
