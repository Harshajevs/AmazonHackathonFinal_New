"""
Fire TV Group Recommendation System (6×6 Matrix)

Purpose: This system analyzes group preferences across 6 modalities (time, behavior, facial, voice, emoji, text)
using a 6×6 matrix structure. It performs matrix multiplication and diagonal extraction to generate personalized
movie recommendations optimized for social viewing experiences.

Key Features:
- Processes group preferences as a 6×6 matrix (modalities × attributes)
- Uses matrix multiplication and diagonal extraction for precise alignment scoring
- Incorporates popularity and group suitability factors
- Generates detailed movie-specific emotion matrices
- Provides comprehensive group consensus metrics

Real-World Integration:
- Would connect to Fire TV's MediaSession API for behavior tracking
- Could integrate with Amazon Alexa for voice analysis
- Would use YOLO11 for real-time facial emotion detection
- Could leverage AWS Kinesis for data streaming and processing
"""

import numpy as np
import random
from enum import Enum
from dataclasses import dataclass
from typing import List, Dict, Tuple

# --- Enumerations for Modalities and Attributes ---
class TimeBlock(Enum):
    SUNRISE_BOOST = "morning_energizer"
    FOCUS_FLOW = "midday_focus"
    CHILL_ZONE = "afternoon_unwind"
    PRIME_TIME_MAGIC = "evening_prime"
    COZY_CORNER = "night_relaxer"
    NIGHT_OWL_TERRITORY = "late_night"

class Behavior(Enum):
    HIGH_ENGAGE = "high_engagement"
    QUICK_BROWSER = "quick_browser"
    BINGE = "binge_watcher"
    ACCESS = "accessibility_user"
    SWITCH = "content_switcher"
    SOCIAL = "social_viewer"

class Emotion(Enum):
    ANGRY = "angry"
    DISGUST = "disgust"
    FEAR = "fear"
    HAPPY = "happy"
    NEUTRAL = "neutral"
    SAD = "sad"

class AnalysisType(Enum):
    TIME = "time_block"
    BEHAVIOR = "behavior"
    FACIAL = "facial"
    VOICE = "voice"
    EMOJI = "emoji"
    TEXT = "text"

# --- Data Structures ---
@dataclass
class Movie:
    title: str
    year: int
    genre: str
    emotion_compatibility: Dict[str, Dict[str, float]]
    popularity_score: float
    group_suitability: float

@dataclass
class GroupRecommendation:
    movie: Movie
    consensus_score: float
    std_deviation: float
    selectability: float
    explanation: str
    movie_matrix: np.ndarray

# --- Sample Movie Database ---
MOVIES = [
    Movie("Avengers: Endgame", 2019, "Action/Adventure",
          {"angry": {"time_block": 0.7, "behavior": 0.8, "facial": 0.8, "voice": 0.7, "emoji": 0.6, "text": 0.7},
           "disgust": {"time_block": 0.3, "behavior": 0.4, "facial": 0.3, "voice": 0.2, "emoji": 0.3, "text": 0.4},
           "fear": {"time_block": 0.6, "behavior": 0.7, "facial": 0.7, "voice": 0.6, "emoji": 0.5, "text": 0.6},
           "happy": {"time_block": 0.8, "behavior": 0.9, "facial": 0.9, "voice": 0.8, "emoji": 0.7, "text": 0.8},
           "neutral": {"time_block": 0.5, "behavior": 0.6, "facial": 0.6, "voice": 0.5, "emoji": 0.4, "text": 0.5},
           "sad": {"time_block": 0.4, "behavior": 0.5, "facial": 0.4, "voice": 0.3, "emoji": 0.2, "text": 0.3}},
          9.2, 9.5),
    
    Movie("Inside Out", 2015, "Animation/Family",
          {"angry": {"time_block": 0.3, "behavior": 0.4, "facial": 0.4, "voice": 0.3, "emoji": 0.2, "text": 0.3},
           "disgust": {"time_block": 0.2, "behavior": 0.3, "facial": 0.3, "voice": 0.2, "emoji": 0.1, "text": 0.2},
           "fear": {"time_block": 0.4, "behavior": 0.5, "facial": 0.5, "voice": 0.4, "emoji": 0.3, "text": 0.4},
           "happy": {"time_block": 0.9, "behavior": 0.8, "facial": 0.9, "voice": 0.9, "emoji": 0.8, "text": 0.9},
           "neutral": {"time_block": 0.6, "behavior": 0.7, "facial": 0.7, "voice": 0.6, "emoji": 0.5, "text": 0.6},
           "sad": {"time_block": 0.8, "behavior": 0.7, "facial": 0.8, "voice": 0.8, "emoji": 0.7, "text": 0.8}},
          8.2, 9.0),
    
    Movie("Inception", 2010, "Sci-Fi/Thriller",
          {"angry": {"time_block": 0.4, "behavior": 0.5, "facial": 0.5, "voice": 0.4, "emoji": 0.3, "text": 0.4},
           "disgust": {"time_block": 0.2, "behavior": 0.3, "facial": 0.3, "voice": 0.2, "emoji": 0.1, "text": 0.2},
           "fear": {"time_block": 0.8, "behavior": 0.9, "facial": 0.9, "voice": 0.8, "emoji": 0.7, "text": 0.8},
           "happy": {"time_block": 0.5, "behavior": 0.6, "facial": 0.6, "voice": 0.5, "emoji": 0.4, "text": 0.5},
           "neutral": {"time_block": 0.9, "behavior": 0.8, "facial": 0.9, "voice": 0.9, "emoji": 0.8, "text": 0.9},
           "sad": {"time_block": 0.3, "behavior": 0.2, "facial": 0.3, "voice": 0.3, "emoji": 0.2, "text": 0.3}},
          8.8, 8.5),
    
    Movie("The Dark Knight", 2008, "Action/Crime",
          {"angry": {"time_block": 0.8, "behavior": 0.9, "facial": 0.9, "voice": 0.8, "emoji": 0.7, "text": 0.8},
           "disgust": {"time_block": 0.4, "behavior": 0.5, "facial": 0.5, "voice": 0.4, "emoji": 0.3, "text": 0.4},
           "fear": {"time_block": 0.9, "behavior": 0.8, "facial": 0.8, "voice": 0.9, "emoji": 0.8, "text": 0.9},
           "happy": {"time_block": 0.3, "behavior": 0.4, "facial": 0.4, "voice": 0.3, "emoji": 0.2, "text": 0.3},
           "neutral": {"time_block": 0.6, "behavior": 0.7, "facial": 0.7, "voice": 0.6, "emoji": 0.5, "text": 0.6},
           "sad": {"time_block": 0.5, "behavior": 0.4, "facial": 0.5, "voice": 0.6, "emoji": 0.5, "text": 0.4}},
          9.0, 8.0),
    
    Movie("Parasite", 2019, "Thriller/Drama",
          {"angry": {"time_block": 0.6, "behavior": 0.7, "facial": 0.7, "voice": 0.6, "emoji": 0.5, "text": 0.6},
           "disgust": {"time_block": 0.7, "behavior": 0.6, "facial": 0.6, "voice": 0.7, "emoji": 0.6, "text": 0.7},
           "fear": {"time_block": 0.8, "behavior": 0.7, "facial": 0.8, "voice": 0.8, "emoji": 0.7, "text": 0.8},
           "happy": {"time_block": 0.2, "behavior": 0.3, "facial": 0.3, "voice": 0.2, "emoji": 0.1, "text": 0.2},
           "neutral": {"time_block": 0.7, "behavior": 0.8, "facial": 0.8, "voice": 0.7, "emoji": 0.6, "text": 0.7},
           "sad": {"time_block": 0.5, "behavior": 0.6, "facial": 0.6, "voice": 0.5, "emoji": 0.4, "text": 0.5}},
          8.6, 7.0)
]

# --- Recommendation Engine ---
class GroupRecommender:
    def __init__(self, movies: List[Movie]):
        self.movies = movies
        self.modality_weights = np.array([0.15, 0.15, 0.25, 0.20, 0.15, 0.10])
        
    def generate_group_matrix(self, group_size: int = 10) -> np.ndarray:
        """Generate a realistic 6×6 group preference matrix"""
        matrix = np.zeros((6, 6))
        
        # Create base profile with realistic distributions
        base_profile = {
            "angry": [0.3, 0.2, 0.4, 0.5, 0.3, 0.4],
            "disgust": [0.1, 0.1, 0.2, 0.3, 0.2, 0.2],
            "fear": [0.4, 0.3, 0.5, 0.6, 0.4, 0.5],
            "happy": [0.8, 0.9, 0.7, 0.8, 0.9, 0.8],
            "neutral": [0.6, 0.7, 0.6, 0.5, 0.7, 0.6],
            "sad": [0.2, 0.3, 0.2, 0.1, 0.3, 0.2]
        }
        
        # Apply group variations
        for emotion_idx, emotion in enumerate(Emotion):
            for modality_idx in range(6):
                values = []
                for _ in range(group_size):
                    variation = np.random.uniform(0.8, 1.2)
                    values.append(base_profile[emotion.value][modality_idx] * variation)
                
                # Use robust aggregation (70% median, 30% mean)
                median_val = np.median(values)
                mean_val = np.mean(values)
                matrix[emotion_idx, modality_idx] = 0.7 * median_val + 0.3 * mean_val
        
        # Normalize to [0,1] range
        return np.clip(matrix, 0, 1)
    
    def calculate_match_matrix(self, group_matrix: np.ndarray, movie: Movie) -> np.ndarray:
        """Compute movie-specific match matrix through element-wise multiplication"""
        match_matrix = np.zeros((6, 6))
        
        for emotion_idx, emotion in enumerate(Emotion):
            for modality_idx, modality in enumerate(AnalysisType):
                if emotion.value in movie.emotion_compatibility:
                    if modality.value in movie.emotion_compatibility[emotion.value]:
                        match_matrix[emotion_idx, modality_idx] = (
                            group_matrix[emotion_idx, modality_idx] * 
                            movie.emotion_compatibility[emotion.value][modality.value]
                        )
        
        # Normalize to 0-1 range
        max_val = match_matrix.max()
        if max_val > 0:
            match_matrix /= max_val
            
        return match_matrix
    
    def calculate_consensus_score(self, match_matrix: np.ndarray, movie: Movie) -> float:
        """Calculate consensus score using diagonal extraction and weighting"""
        # Extract diagonal elements representing specific alignments
        diagonal = np.diag(match_matrix)
        
        # Apply modality weights to diagonal scores
        raw_score = np.dot(diagonal, self.modality_weights)
        
        # Include popularity and suitability factors
        pop_factor = movie.popularity_score / 10.0
        suit_factor = movie.group_suitability / 10.0
        
        # Final consensus score (60% match, 20% popularity, 20% suitability)
        return 0.6 * raw_score + 0.2 * pop_factor + 0.2 * suit_factor
    
    def calculate_group_metrics(self, scores: List[float]) -> Tuple[float, float]:
        """Calculate standard deviation and selectability"""
        std_dev = float(np.std(scores))
        selectability = float((np.array(scores) > 0.7).mean() * 100)
        return std_dev, selectability
    
    def generate_explanation(self, consensus_score: float, std_dev: float, selectability: float) -> str:
        """Generate human-readable explanation based on metrics"""
        if consensus_score > 0.9 and std_dev < 0.1 and selectability > 95:
            return "Exceptional group harmony: 100% of users highly aligned."
        elif consensus_score > 0.8 and std_dev < 0.15 and selectability > 85:
            return "Strong consensus with high user satisfaction."
        elif consensus_score > 0.7 and selectability > 75:
            return "Broad appeal despite some variance."
        else:
            return "Mixed group sentiment with unique alignment."
    
    def generate_recommendations(self, group_matrix: np.ndarray) -> List[GroupRecommendation]:
        """Generate top 5 group recommendations"""
        recommendations = []
        all_scores = []
        
        for movie in self.movies:
            # Compute match matrix and consensus score
            match_matrix = self.calculate_match_matrix(group_matrix, movie)
            consensus_score = self.calculate_consensus_score(match_matrix, movie)
            all_scores.append(consensus_score)
            
            # Generate explanation
            std_dev, selectability = self.calculate_group_metrics([consensus_score])
            explanation = self.generate_explanation(consensus_score, std_dev, selectability)
            
            recommendations.append(GroupRecommendation(
                movie=movie,
                consensus_score=consensus_score,
                std_deviation=std_dev,
                selectability=selectability,
                explanation=explanation,
                movie_matrix=match_matrix
            ))
        
        # Sort by consensus score and return top 5
        recommendations.sort(key=lambda x: x.consensus_score, reverse=True)
        return recommendations[:5]
    
    def display_recommendations(self, recommendations: List[GroupRecommendation], group_matrix: np.ndarray):
        """Display recommendations in the specified format"""
        print("TOP 5 GROUP MOVIE RECOMMENDATIONS")
        print("=" * 50)
        
        for i, rec in enumerate(recommendations, 1):
            movie = rec.movie
            print(f"{i}. {movie.title} ({movie.year}) - {movie.genre}")
            print(f"   Group Consensus Score: {rec.consensus_score:.3f}/1.000")
            print(f"   Explanation: {rec.explanation}")
            print(f"   Individual Appeal: Popularity {movie.popularity_score}/10.0, Group Suitability {movie.group_suitability}/10.0")
            '''print("\n   Movie-Specific Emotion Matrix:")
            print("   " + "      ".join(f"{mod.value[:6]}" for mod in AnalysisType))
            print("   " + "-" * 60)
            
            for emotion_idx, emotion in enumerate(Emotion):
                row = rec.movie_matrix[emotion_idx]
                print(f"   {emotion.value:<8} " + " ".join(f"{val:.3f}".ljust(8) for val in row))
            print()'''
        
        # Display aggregated group matrix
        print("AGGREGATED GROUP EMOTION MATRIX")
        print("=" * 80)
        print("Normalized emotion intensities across all modalities:")
        print("   " + "      ".join(f"{mod.value[:6]}" for mod in AnalysisType))
        print("   " + "-" * 60)
        
        for emotion_idx, emotion in enumerate(Emotion):
            row = group_matrix[emotion_idx]
            print(f"   {emotion.value:<8} " + " ".join(f"{val:.3f}".ljust(8) for val in row))
        print()
        
        # Display modality correlation
        '''print("MODALITY CORRELATION MATRIX")
        print("=" * 50)
        print("Correlation between different analysis modalities:")
        print("   " + "      ".join(f"{mod.value[:6]}" for mod in AnalysisType))
        print("   " + "-" * 60)
        
        # Compute correlation matrix
        corr_matrix = np.corrcoef(group_matrix, rowvar=False)
        for i in range(6):
            row = corr_matrix[i]
            print(f"   {list(AnalysisType)[i].value[:6]:<8} " + " ".join(f"{val:.3f}".ljust(8) for val in row))
'''
# --- Main Execution ---
def main():
    print("=" * 80)
    print("FIRE TV GROUP RECOMMENDATION SYSTEM - 6×6 MATRIX ANALYSIS")
    print("=" * 80)
    print("Processing group preferences across 6 modalities and 6 emotions...")
    
    # Initialize recommender and generate group matrix
    recommender = GroupRecommender(MOVIES)
    group_matrix = recommender.generate_group_matrix()
    
    # Generate recommendations
    recommendations = recommender.generate_recommendations(group_matrix)
    
    # Display results
    recommender.display_recommendations(recommendations, group_matrix)
    
    print("=" * 80)
    print("Recommendation process completed successfully")
    

if __name__ == "__main__":
    # Set random seed for reproducible results
    np.random.seed(42)
    random.seed(42)
    main()