'''
Preprocess the user input based on watch history.

This part of the code modifies the user input according to their watch history.
Each movie is assigned a weight based on its position in the watch history.

The processed user input from this step will be passed to the final recommendation phase.

Optimization:
- Multiply the existing previous history matrix by exp(-0.5)
- Add the recent transposed movie matrix (multiplied by 0.3935)
'''



import numpy as np
import random
import datetime
from collections import deque

# Define constants
MODALITIES = ["Time", "Behavior", "Voice", "Facial"]
ATTRIBUTES = ["Primary", "Secondary", "Tertiary", "Quaternary", "Quinary", "Senary"]

# Base movie database
BASE_MOVIES = [
    {
        "title": "Avengers: Endgame",
        "year": 2019,
        "genre": "Action/Adventure",
        "compat": np.array([
            [0.30, 1.00, 0.40, 0.40],
            [0.80, 0.50, 0.60, 0.90],
            [0.50, 0.80, 0.50, 0.50],
            [1.00, 0.80, 0.80, 0.90],
            [0.60, 0.60, 0.70, 0.80],
            [0.80, 0.90, 0.80, 0.80]
        ]),
    },
    {
        "title": "Inside Out",
        "year": 2015,
        "genre": "Animation/Family",
        "compat": np.array([
            [0.90, 0.80, 0.95, 0.85],
            [0.95, 0.75, 0.80, 0.90],
            [0.80, 0.90, 0.90, 0.80],
            [0.85, 0.85, 0.90, 0.95],
            [0.75, 0.80, 0.85, 0.80],
            [0.80, 0.85, 0.80, 0.85]
        ]),
    },
    {
        "title": "Inception",
        "year": 2010,
        "genre": "Sci-Fi/Thriller",
        "compat": np.array([
            [0.70, 0.90, 0.60, 1.00],
            [0.80, 0.60, 0.80, 0.90],
            [0.60, 0.80, 0.70, 0.80],
            [0.90, 0.80, 0.80, 0.90],
            [0.70, 0.70, 0.80, 0.80],
            [0.80, 0.80, 0.90, 0.80]
        ]),
    },
    {
        "title": "The Dark Knight",
        "year": 2008,
        "genre": "Action/Crime",
        "compat": np.array([
            [0.60, 0.95, 0.70, 0.85],
            [0.90, 0.65, 0.85, 0.90],
            [0.75, 0.85, 0.80, 0.75],
            [0.95, 0.90, 0.85, 0.90],
            [0.80, 0.75, 0.85, 0.80],
            [0.85, 0.90, 0.80, 0.85]
        ]),
    },
    {
        "title": "Parasite",
        "year": 2019,
        "genre": "Thriller/Drama",
        "compat": np.array([
            [0.50, 0.80, 0.60, 0.70],
            [0.85, 0.55, 0.75, 0.95],
            [0.65, 0.85, 0.65, 0.65],
            [0.95, 0.85, 0.85, 0.95],
            [0.75, 0.70, 0.80, 0.85],
            [0.85, 0.90, 0.85, 0.85]
        ]),
    }
]

def calculate_exponential_decay_weights(num_movies, alpha=1.0, beta=0.5):
    """
    Calculate exponential decay weights for movie history.
    Most recent movie gets highest weight, and weights decrease exponentially.
    Total weights sum to 1.
    """
    weights = np.array([alpha * np.exp(-beta * i) for i in range(num_movies)])
    # Normalize weights to sum to 1
    return weights / np.sum(weights)

def simulate_user_matrix():
    """Simulate a 4x6 user preference matrix (modalities x attributes)."""
    user_matrix = np.zeros((4, 6))
    user_matrix[0, :] = np.random.dirichlet([2, 3, 4, 5, 3, 2])  # Time
    user_matrix[1, :] = np.random.dirichlet([3, 2, 4, 2, 2, 3])  # Behavior
    user_matrix[2, :] = np.random.dirichlet([3, 2, 3, 4, 3, 2])  # Voice
    user_matrix[3, :] = np.random.dirichlet([3, 3, 2, 3, 3, 2])  # Facial
    return np.round(user_matrix, 3)

def print_matrix(matrix, row_labels, col_labels, title):
    """Print a matrix with row and column labels."""
    print(f"\n{title}")
    print("=" * 80)
    
    # Print column headers
    print(f"{'':12}", end="")
    for col in col_labels:
        print(f"{col:12}", end="")
    print()
    
    # Print separator
    print("-" * 80)
    
    # Print rows
    for i, row_label in enumerate(row_labels):
        print(f"{row_label:12}", end="")
        for j in range(matrix.shape[1]):
            print(f"{matrix[i, j]:12.3f}", end="")
        print()

def generate_movie_history(num_movies=20):
    """Generate a movie history with slightly modified compatibility matrices."""
    np.random.seed(42)
    history = deque(maxlen=num_movies)
    
    for i in range(num_movies):
        # Select a random base movie
        base_movie = random.choice(BASE_MOVIES).copy()
        
        # Create a slightly modified version
        noise = 0.1 * (2 * np.random.random((6, 4)) - 1)  # ±10% variation
        modified_compat = np.clip(base_movie["compat"] + noise, 0, 1)
        
        # Add to history with a new title
        base_movie["compat"] = np.round(modified_compat, 3)
        base_movie["view_time"] = datetime.datetime.now() - datetime.timedelta(days=random.randint(0, 30))
        history.appendleft(base_movie)  # Most recent first
    
    return list(history)

def main():
    """Main function to run the Fire TV History-Aware Recommendation Engine."""
    print("=" * 80)
    print("FIRE TV HISTORY-AWARE RECOMMENDATION ENGINE - MULTI-MODAL MATRIX PROTOTYPE")
    print("=" * 80)
    now = datetime.datetime.now()
    print(f"Analysis at {now.strftime('%Y-%m-%d %I:%M:%S %p')}\n")
    
    # Generate movie history (20 most recent movies)
    movie_history = generate_movie_history(20)
    
    # Calculate exponential decay weights for the movies
    weights = calculate_exponential_decay_weights(len(movie_history))
    
    # Display weights
    print("\nExponential Decay Weights for Movie History (Most Recent First):")
    print("-" * 60)
    for i, (movie, weight) in enumerate(zip(movie_history, weights)):
        print(f"{i+1:2}. {movie['title']:20} ({movie['genre']:20}) Weight: {weight:.4f}")
    
    # Calculate the weighted sum of movie compatibility matrices
    history_matrix = np.zeros((6, 4))
    for i, movie in enumerate(movie_history):
        history_matrix += weights[i] * movie["compat"]
    history_matrix = np.round(history_matrix, 3)
    
    # Transpose the history matrix to get a 4x6 matrix
    history_matrix_transposed = np.round(history_matrix.T, 3)
    
    # Generate the user input matrix (4x6)
    user_input_matrix = simulate_user_matrix()
    
    # Combine user input (80%) with history (20%)
    processed_user_matrix = np.round(0.8 * user_input_matrix + 0.2 * history_matrix_transposed, 3)
    
    # Print all matrices
    
    print_matrix(history_matrix_transposed, MODALITIES, ATTRIBUTES, "TRANSPOSED HISTORY MATRIX (4x6)")
    print_matrix(user_input_matrix, MODALITIES, ATTRIBUTES, "USER INPUT MATRIX (4x6)")
    print_matrix(processed_user_matrix, MODALITIES, ATTRIBUTES, "PROCESSED USER MATRIX (4x6) - 80% User Input + 20% History")
    

if __name__ == "__main__":
    main()
