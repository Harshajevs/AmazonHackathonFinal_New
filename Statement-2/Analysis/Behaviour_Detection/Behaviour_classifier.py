# fire_tv_ci_classifier.py

from collections import Counter, defaultdict
import numpy as np
import pandas as pd

# --- Predefined clusters ---
CLUSTERS = [
    "high_engagement",
    "quick_browser",
    "binge_watcher",
    "accessibility_user",
    "content_switcher",
    "social_viewer"
]

# --- Heuristic rule-based classifier ---
def classify(events):
    c = Counter(events)
    n = sum(c.values())
    skip_rate = (c['skip_forward'] + c['skip_backward']) / n
    switch_rate = c['content_switch'] / n
    subtitle_rate = c['subtitle_toggle'] / n
    rewind_rate = c['rewind'] / n

    if subtitle_rate > 0.4:
        return "accessibility_user"
    if switch_rate > 0.6:
        return "content_switcher"
    if skip_rate > 0.5 and n < 15:
        return "quick_browser"
    if rewind_rate > 0.25 and n > 20:
        return "high_engagement"
    if n > 30 and switch_rate < 0.2:
        return "binge_watcher"
    return "social_viewer"

# --- Bootstrap for robust prediction (support not shown) ---
def cluster_with_support(events, B=1000):
    boot_preds = [
        classify(np.random.choice(events, len(events), replace=True))
        for _ in range(B)
    ]
    counts = Counter(boot_preds)
    top_cluster, _ = counts.most_common(1)[0]
    return top_cluster

# --- Example user logs  ---
logs = {
    "user_01": ["play"] + ["subtitle_toggle"] * 12 + ["pause"] * 3 + ["play"] * 2,
    "user_02": ["play"] + ["skip_forward"] * 7 + ["content_switch"] * 6 + ["play"] * 2,
    "user_03": ["play"] + ["rewind"] * 9 + ["pause"] * 5 + ["play"] * 10,
    "user_04": ["play"] + ["rewind"] * 30 + ["pause"] * 5,
    "user_05": ["play"] * 5 + ["content_switch"] * 20 + ["pause"] * 5,
}

# --- Classify and prepare output ---
results = defaultdict(list)

for uid, events in logs.items():
    cluster = cluster_with_support(events)
    counts = Counter(events)
    interaction_summary = ", ".join(f"{k}: {v}" for k, v in sorted(counts.items()))
    results["User ID"].append(uid)
    results["Interactions"].append(interaction_summary)
    results["Predicted Cluster"].append(cluster)

# --- Create DataFrame and print as neat table ---
df = pd.DataFrame(results)

print("\n=== Fire TV Viewer Behaviour Classifier ===\n")
print(df.to_string(index=False))
