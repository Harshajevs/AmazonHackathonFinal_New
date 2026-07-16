"""
Adaptive Movie Recommendation System (Final Verified Version)
Features: Face, Voice, Time, Behavior — initialized at 25% each.
Dynamically updates weights based on user feedback.
"""

import numpy as np
import matplotlib.pyplot as plt

# Feature order: Face, Voice, Time, Behavior
FEATURE_NAMES = ["Face", "Voice", "Time", "Behavior"]
weights = np.array([0.25, 0.25, 0.25, 0.25])
weight_evolution = [weights.copy()]

def update_weights(old_weights, user_feedback):
    momentum = 0.6
    new_weights = momentum * old_weights + (1 - momentum) * user_feedback
    return new_weights / np.sum(new_weights)

def calculate_score(movie_matrix, user_emotions, weights):
    product = np.dot(movie_matrix, user_emotions)
    feature_scores = np.diagonal(product)
    final_score = np.dot(feature_scores, weights)
    return final_score, feature_scores

def print_weight_analysis(iteration, prev_weights, new_weights, feedback):
    print(f"\n📊 WEIGHT ANALYSIS — ITERATION {iteration}")
    print("-" * 72)
    print(f"{'Feature':10} | {'Previous':>10} | {'Updated':>10} | {'Change':>10} | {'% Change':>10} | Dir")
    print("-" * 72)
    for i, feature in enumerate(FEATURE_NAMES):
        change = new_weights[i] - prev_weights[i]
        change_percent = (change / prev_weights[i]) * 100
        direction = "↑" if change > 0 else "↓" if change < 0 else "→"
        print(f"{feature:10} | {prev_weights[i]:10.3f} | {new_weights[i]:10.3f} | "
              f"{change:+10.3f} | {change_percent:+9.1f}% | {direction}")
    print("-" * 72)
    print(f"Feedback Used   : {feedback}")
    print(f"Sum of Weights  : {np.sum(new_weights):.3f}")

movie_feature_matrices = {
    "Action Movie": np.array([
        [0.8, 0.7, 0.9, 0.6, 0.7, 0.8],
        [0.6, 0.9, 0.7, 0.8, 0.5, 0.6],
        [0.7, 0.8, 0.6, 0.9, 0.7, 0.5],
        [0.9, 0.6, 0.8, 0.7, 0.6, 0.9]
    ]),
    "Romance Movie": np.array([
        [0.3, 0.4, 0.2, 0.5, 0.3, 0.4],
        [0.5, 0.3, 0.4, 0.2, 0.6, 0.3],
        [0.4, 0.5, 0.3, 0.4, 0.2, 0.5],
        [0.2, 0.6, 0.5, 0.3, 0.4, 0.2]
    ]),
    "Comedy Movie": np.full((4, 6), 0.5),
    "Horror Movie": np.array([
        [0.9, 0.8, 0.7, 0.9, 0.8, 0.7],
        [0.4, 0.5, 0.6, 0.3, 0.4, 0.5],
        [0.8, 0.7, 0.9, 0.8, 0.7, 0.6],
        [0.3, 0.4, 0.3, 0.4, 0.5, 0.4]
    ])
}

user_emotions = np.array([
    [0.8, 0.2, 0.5, 0.6],
    [0.3, 0.7, 0.4, 0.9],
    [0.6, 0.4, 0.8, 0.3],
    [0.5, 0.5, 0.5, 0.5],
    [0.7, 0.3, 0.6, 0.4],
    [0.4, 0.6, 0.7, 0.8]
])

feedback_scenarios = [
    np.array([0.8, 0.7, 0.9, 0.6]),
    np.array([0.2, 0.8, 0.3, 0.7]),
    np.array([0.9, 0.4, 0.6, 0.5]),
    np.array([0.6, 0.9, 0.7, 0.3]),
    np.array([0.3, 0.4, 0.4, 0.9])
]

def main():
    global weights
    #print("=" * 72)
    #print("🎯 ADAPTIVE MOVIE RECOMMENDATION SYSTEM — FINAL VERSION")
    #print("=" * 72)
    #print(f"Initial Weights: {dict(zip(FEATURE_NAMES, np.round(weights, 3)))}")

    for i in range(1, 6):
        #print(f"\n🎬 ITERATION {i}")
        #print("-" * 72)
        ##print(f"{'Movie':20} | {'Score':>8} | {'Feature Scores'}")
        #print("-" * 72)

        scores = {}
        for name, matrix in movie_feature_matrices.items():
            score, feature_scores = calculate_score(matrix, user_emotions, weights)
            scores[name] = score
            feature_scores_str = ', '.join(f"{v:.2f}" for v in feature_scores)
           # print(f"{name:20} | {score:8.3f} | [{feature_scores_str}]")

        top_movie = max(scores, key=scores.get)
        #print(f"\n🏆 RECOMMENDED MOVIE: {top_movie} — Score: {scores[top_movie]:.3f}")

        user_feedback = feedback_scenarios[i - 1]
        prev_weights = weights.copy()
        weights = update_weights(weights, user_feedback)
        weight_evolution.append(weights.copy())

        #print_weight_analysis(i, prev_weights, weights, user_feedback)

    print("\n" + "=" * 72)
    print("📈 FINAL WEIGHT EVOLUTION SUMMARY")
    print("=" * 72)
    print(f"{'Iteration':12} | " + ' | '.join(f"{f:>8}" for f in FEATURE_NAMES))
    print("-" * 72)
    for idx, w in enumerate(weight_evolution):
        label = "Initial" if idx == 0 else f"Iter {idx}"
        values = ' | '.join(f"{v:8.3f}" for v in w)
        print(f"{label:12} | {values}")

    initial = weight_evolution[0]
    final = weight_evolution[-1]
    total_change = final - initial

    #print("\nNet Change per Feature:")
    #print("-" * 72)
    #print(f"{'Feature':10} | {'Initial':>8} | {'Final':>8} | {'Change':>8} | {'% Change':>9} | Dir")
    #print("-" * 72)
    for i, feature in enumerate(FEATURE_NAMES):
        change = total_change[i]
        change_percent = (change / initial[i]) * 100
        trend = "↑" if change > 0 else "↓" if change < 0 else "→"
        #print(f"{feature:10} | {initial[i]:8.3f} | {final[i]:8.3f} | "
            #  f"{change:+8.3f} | {change_percent:+8.1f}% | {trend}")

    #print(f"\nFinal Weights Sum Check: {np.sum(final):.6f}")

    evolution_array = np.array(weight_evolution)
    plt.figure(figsize=(10, 6))
    for idx, feature in enumerate(FEATURE_NAMES):
        plt.plot(evolution_array[:, idx], marker='o', label=feature)
    plt.title("Feature Weight Evolution")
    plt.xlabel("Iteration")
    plt.ylabel("Weight Value")
    plt.xticks(range(len(weight_evolution)), ["Initial"] + [f"Iter {i}" for i in range(1, len(weight_evolution))])
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    #plt.show()

if __name__ == "__main__":
    main()
