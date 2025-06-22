"""
Fire TV Group Preference System 

- The code give below simulates how our movie Matrix gets updated according to the user watching the movie 

Purpose:
Enhances recommendation accuracy by replacing uniform 0.5 matrix initialization with
genre-aware weights, integrating context into preference modeling. Analyzes 20 users 
across 4 modalities: time (timezone blocks), behavior (MediaSession API), voice 
(Alexa sentiment), and facial (CV emotion recognition).

"""

import numpy as np
from collections import Counter
from enum import Enum

# Define all attribute categories
class TimeBlock(Enum):
    SUNRISE_BOOST = "morning_energizer"
    FOCUS_FLOW = "midday_focus"
    CHILL_ZONE = "afternoon_unwind"
    PRIME_TIME_MAGIC = "evening_prime"
    COZY_CORNER = "night_relaxer"
    NIGHT_OWL_TERRITORY = "late_night"

class BehaviorPattern(Enum):
    HIGH_ENGAGE = "high_engagement"
    QUICK_BROWSER = "quick_browser"
    BINGE = "binge_watcher"
    ACCESS = "accessibility_user"
    SWITCH = "content_switcher"
    SOCIAL = "social_viewer"

class FacialExpression(Enum):
    HAPPY = "happy"
    SAD = "sad"
    ANGRY = "angry"
    FEARFUL = "fearful"
    NEUTRAL = "neutral"
    BACKGROUND = "background"

class VoiceAttribute(Enum):
    HAPPY = "happy"
    SAD = "sad"
    ANGRY = "angry"
    FEARFUL = "fearful"
    NEUTRAL = "neutral"
    CALM = "calm"

class FireTVGroupPreferenceSystem:
    def __init__(self):
        # Initialize standard normalized 6x4 matrix (all entries = 0.5)
        self.initial_matrix = np.full((6, 4), 0.5)
        
        # Define attribute lists for easy indexing
        self.time_attributes = [tb.value for tb in TimeBlock]
        self.behavior_attributes = [bp.value for bp in BehaviorPattern]
        self.facial_attributes = [fe.value for fe in FacialExpression]
        self.voice_attributes = [va.value for va in VoiceAttribute]
        
        # Define modalities
        self.modalities = ["Time", "Behavior", "Voice", "Facial"]
        
        # Hardcoded user preferences for realistic scenarios
        self.user_preferences = self._define_hardcoded_preferences()
        
        # Genre-specific initial matrices
        self.genre_initial_matrices = self._define_genre_initial_matrices()

    def _define_hardcoded_preferences(self):
        movie1_preferences = {
            "time": {
                "morning_energizer": ["User_03", "User_17"],  # 2 users
                "midday_focus": ["User_08", "User_12", "User_19"],  # 3 users
                "afternoon_unwind": ["User_05", "User_14", "User_16"],  # 3 users
                "evening_prime": ["User_01", "User_02", "User_06", "User_09", "User_11", "User_13", "User_20"],  # 7 users
                "night_relaxer": ["User_04", "User_07", "User_10"],  # 3 users
                "late_night": ["User_15", "User_18"]  # 2 users
            },
            "behavior": {
                "high_engagement": ["User_01", "User_02", "User_04", "User_06", "User_09", "User_11", "User_13", "User_15"],  # 8 users
                "quick_browser": ["User_08", "User_17"],  # 2 users
                "binge_watcher": ["User_05", "User_07", "User_10", "User_14", "User_18"],  # 5 users
                "accessibility_user": ["User_12", "User_19"],  # 2 users
                "content_switcher": ["User_03", "User_16"],  # 2 users
                "social_viewer": ["User_20"]  # 1 user
            },
            "voice": {
                "happy": ["User_03", "User_12"],  # 2 users
                "sad": ["User_08", "User_17"],  # 2 users
                "angry": ["User_01", "User_04", "User_06", "User_13", "User_15"],  # 5 users
                "fearful": ["User_02", "User_07", "User_09", "User_10", "User_18"],  # 5 users
                "neutral": ["User_05", "User_11", "User_14", "User_16", "User_19"],  # 5 users
                "calm": ["User_20"]  # 1 user
            },
            "facial": {
                "happy": ["User_03", "User_12", "User_20"],  # 3 users
                "sad": ["User_08", "User_17"],  # 2 users
                "angry": ["User_01", "User_04", "User_06", "User_13"],  # 4 users
                "fearful": ["User_02", "User_07", "User_09", "User_10", "User_15", "User_18"],  # 6 users
                "neutral": ["User_05", "User_11", "User_14", "User_16", "User_19"],  # 5 users
                "background": []  # 0 users
            }
        }
        '''movie2_preferences = {
            "time": {
                "morning_energizer": ["User_01", "User_02", "User_05", "User_08", "User_11", "User_14"],  # 6 users
                "midday_focus": ["User_03", "User_06", "User_09", "User_12"],  # 4 users
                "afternoon_unwind": ["User_04", "User_07", "User_10", "User_13", "User_15", "User_16"],  # 6 users
                "evening_prime": ["User_17", "User_18", "User_19"],  # 3 users
                "night_relaxer": ["User_20"],  # 1 user
                "late_night": []  # 0 users
            },
            "behavior": {
                "high_engagement": ["User_02", "User_06", "User_09"],  # 3 users
                "quick_browser": ["User_17", "User_18"],  # 2 users
                "binge_watcher": ["User_04", "User_07", "User_10"],  # 3 users
                "accessibility_user": ["User_03", "User_12", "User_15", "User_19"],  # 4 users
                "content_switcher": ["User_13", "User_16"],  # 2 users
                "social_viewer": ["User_01", "User_05", "User_08", "User_11", "User_14", "User_20"]  # 6 users
            },
            "voice": {
                "happy": ["User_01", "User_02", "User_05", "User_08", "User_11", "User_14", "User_17", "User_20"],  # 8 users
                "sad": ["User_04", "User_07", "User_10"],  # 3 users
                "angry": ["User_13"],  # 1 user
                "fearful": ["User_16"],  # 1 user
                "neutral": ["User_03", "User_06", "User_09", "User_12", "User_15", "User_18", "User_19"],  # 7 users
                "calm": []  # 0 users
            },
            "facial": {
                "happy": ["User_01", "User_02", "User_05", "User_08", "User_11", "User_14", "User_17", "User_20"],  # 8 users
                "sad": ["User_04", "User_07", "User_10"],  # 3 users
                "angry": ["User_13"],  # 1 user
                "fearful": ["User_16"],  # 1 user
                "neutral": ["User_03", "User_06", "User_09", "User_12", "User_15", "User_18", "User_19"],  # 7 users
                "background": []  # 0 users
            }
        }'''
        return {
            "The Dark Knight": movie1_preferences
        }
    
    def _define_genre_initial_matrices(self):
        """
        Define genre-specific initial matrices that better reflect content context
        rather than using uniform 0.5 initialization
        """
        # Action/Thriller genre (The Dark Knight)
        action_thriller_matrix = np.array([
            # Time,   Behavior, Voice,   Facial
            [0.40,    0.45,     0.40,    0.40],  # Morning
            [0.50,    0.60,     0.45,    0.45],  # Midday
            [0.45,    0.50,     0.40,    0.40],  # Afternoon
            [0.75,    0.65,     0.60,    0.60],  # Evening Prime
            [0.55,    0.50,     0.50,    0.50],  # Night
            [0.70,    0.65,     0.60,    0.60],  # Late Night
        ])
        
        # Animation/Family genre (Inside Out)
        '''animation_family_matrix = np.array([
            # Time,   Behavior, Voice,   Facial
            [0.70,    0.60,     0.65,    0.65],  # Morning
            [0.65,    0.55,     0.60,    0.60],  # Midday
            [0.75,    0.65,     0.70,    0.70],  # Afternoon
            [0.60,    0.50,     0.55,    0.55],  # Evening Prime
            [0.50,    0.45,     0.45,    0.45],  # Night
            [0.30,    0.35,     0.30,    0.30],  # Late Night
        ])'''

        
        return {
            "The Dark Knight": action_thriller_matrix
        }

    def calculate_updated_matrix(self, movie_name, initial_matrix):
        """
        Calculate updated matrix based on user preferences, starting from the provided initial matrix
        """
        prefs = self.user_preferences[movie_name]
        updated_matrix = initial_matrix.copy()
        
        attr_mappings = {
            "time": self.time_attributes,
            "behavior": self.behavior_attributes,
            "voice": self.voice_attributes,
            "facial": self.facial_attributes
        }
        
        modality_names = ["time", "behavior", "voice", "facial"]
        
        for mod_idx, modality in enumerate(modality_names):
            attr_list = attr_mappings[modality]
            for attr_idx, attribute in enumerate(attr_list):
                user_count = len(prefs[modality].get(attribute, []))
                # Calculate influence factor (0.0 to 0.5 scale)
                influence = user_count / 20.0 * 0.5
                # Apply influence to initial value
                base_value = initial_matrix[attr_idx, mod_idx]
                updated_matrix[attr_idx, mod_idx] = base_value + influence
                
        # Normalize to ensure values stay in 0-1 range
        updated_matrix = np.clip(updated_matrix, 0.0, 1.0)
        return updated_matrix

    def print_movie_analysis(self, movie_name):
        print(f"\n{'='*80}")
        print(f"MOVIE: {movie_name}")
        print(f"{'='*80}")
        
        prefs = self.user_preferences[movie_name]
        
        print("\nUSER PREFERENCE DISTRIBUTION:")
        print("-" * 50)
        
        # Time Analysis (sorted, single line)
        time_counts = [(attr, len(prefs["time"].get(attr, []))) for attr in self.time_attributes]
        time_counts.sort(key=lambda x: x[1], reverse=True)
        print("Time Analysis: " + " | ".join(f"{attr.replace('_',' ').title()} ({count})" for attr, count in time_counts))
        
        # Behavior Analysis (sorted, single line)
        behavior_counts = [(attr, len(prefs["behavior"].get(attr, []))) for attr in self.behavior_attributes]
        behavior_counts.sort(key=lambda x: x[1], reverse=True)
        print("Behavior Analysis: " + " | ".join(f"{attr.replace('_',' ').title()} ({count})" for attr, count in behavior_counts))
        
        # Voice Analysis (sorted, single line)
        voice_counts = [(attr, len(prefs["voice"].get(attr, []))) for attr in self.voice_attributes]
        voice_counts.sort(key=lambda x: x[1], reverse=True)
        print("Voice Analysis: " + " | ".join(f"{attr.title()} ({count})" for attr, count in voice_counts))
        
        # Facial Analysis (sorted, single line)
        facial_counts = [(attr, len(prefs["facial"].get(attr, []))) for attr in self.facial_attributes]
        facial_counts.sort(key=lambda x: x[1], reverse=True)
        print("Facial Analysis: " + " | ".join(f"{attr.title()} ({count})" for attr, count in facial_counts))
        
        # Calculate updated matrices from both initial matrices
        standard_updated_matrix = self.calculate_updated_matrix(movie_name, self.initial_matrix)
        genre_initial_matrix = self.genre_initial_matrices[movie_name]
        genre_updated_matrix = self.calculate_updated_matrix(movie_name, genre_initial_matrix)
        
        # Print standard matrix comparison
        #print("\n" + "STANDARD MATRIX COMPARISON".center(125))
        #print("-" * 100)
       # self._print_matrix_comparison_formatted(self.initial_matrix, standard_updated_matrix)
        
        # Print genre-aware matrix comparison
        print("\n" + "GENRE-AWARE MATRIX COMPARISON".center(125))
        print("-" * 100)
        self._print_matrix_comparison_formatted(genre_initial_matrix, genre_updated_matrix)
        
        self.print_majority_preferences(movie_name, prefs)
        
        # Print matrix impact analysis
        self._print_matrix_impact_analysis(standard_updated_matrix, genre_updated_matrix)

    def _print_matrix_comparison_formatted(self, initial_matrix, updated_matrix):
        """Helper method to print formatted matrix comparison"""
        header1 = "Initial Matrix".ljust(60)
        header2 = "Updated User-Driven Matrix"
        print(f"{header1} | {header2}")
        print("-" * 100)
        
        # Attribute labels (fully spelled out)
        attr_labels = [
            "Morning Energizer", "Midday Focus", "Afternoon Unwind",
            "Evening Prime", "Night Relaxer", "Late Night"
        ]
        
        col_headers = ["Time", "Behv", "Voic", "Face"]
        col_header1 = "Attr".ljust(20) + "".join(f"{h:>10}" for h in col_headers)
        col_header2 = "Attr".ljust(20) + "".join(f"{h:>10}" for h in col_headers)
        print(f"{col_header1:48} | {col_header2}")
        print("-" * 100)
        
        for i in range(6):
            row1 = f"{attr_labels[i]:20}" + "".join(f"{initial_matrix[i,j]:10.2f}" for j in range(4))
            row2 = f"{attr_labels[i]:20}" + "".join(f"{updated_matrix[i,j]:10.2f}" for j in range(4))
            print(f"{row1:48} | {row2}")

    def print_majority_preferences(self, movie_name, prefs):
        # Find majority preferences for each modality
        modalities = ["time", "behavior", "voice", "facial"]
        majority_prefs = {}
        
        for modality in modalities:
            max_users = 0
            most_popular = None
            for attr, users in prefs[modality].items():
                if len(users) > max_users:
                    max_users = len(users)
                    most_popular = attr
            majority_prefs[modality] = (most_popular, max_users)
        
        time_pref, time_count = majority_prefs["time"]
        behavior_pref, behavior_count = majority_prefs["behavior"]
        voice_pref, voice_count = majority_prefs["voice"]
        facial_pref, facial_count = majority_prefs["facial"]
        
        # Print all on a single line
        print(f"\nMajority Preference: Group suggests '{movie_name}' is best watched during {time_pref.replace('_', ' ').title()} ({time_count} users), "
              f"with {behavior_pref.replace('_', ' ').title()} ({behavior_count}), "
              f"expecting {voice_pref.title()} voice ({voice_count}) and {facial_pref.title()} facial ({facial_count}) responses.")

    def _print_matrix_impact_analysis(self, standard_matrix, genre_matrix):
        """
        Print analysis of how genre-aware initialization impacts final recommendations
        """
        
        
        # Calculate differences between matrices
        diff_matrix = genre_matrix - standard_matrix
        
        # Find largest positive and negative differences
        max_diff_idx = np.unravel_index(np.argmax(diff_matrix), diff_matrix.shape)
        min_diff_idx = np.unravel_index(np.argmin(diff_matrix), diff_matrix.shape)
        
        # Get attribute and modality names for differences
        attr_labels = [
            "Morning Energizer", "Midday Focus", "Afternoon Unwind",
            "Evening Prime", "Night Relaxer", "Late Night"
        ]
        
        mod_labels = ["Time", "Behavior", "Voice", "Facial"]
        
        max_attr = attr_labels[max_diff_idx[0]]
        max_mod = mod_labels[max_diff_idx[1]]
        min_attr = attr_labels[min_diff_idx[0]]
        min_mod = mod_labels[min_diff_idx[1]]
        
        # Calculate overall impact metrics
        mean_abs_diff = np.mean(np.abs(diff_matrix))
        max_diff = np.max(diff_matrix)
        min_diff = np.min(diff_matrix)
        
        
        # Calculate diagonal elements (specific alignment scores)
        standard_diag = np.diag(np.dot(standard_matrix.T, standard_matrix))
        genre_diag = np.diag(np.dot(genre_matrix.T, genre_matrix))
        
        # Apply modality weights
        weights = np.array([0.3, 0.25, 0.25, 0.2])  # Time, Behavior, Voice, Facial
        standard_score = np.dot(standard_diag, weights)
        genre_score = np.dot(genre_diag, weights)
        '''
        if genre_score > standard_score:
            print("Conclusion: Genre-aware initialization provides more accurate recommendations")
        else:
            print("Conclusion: Standard initialization may be sufficient for this content")'''

    def run_complete_analysis(self):
        #print("FIRE TV GROUP PREFERENCE ANALYSIS SYSTEM")
        #print("=" * 80)
        print("Analyzing 20 user preferences across 4 modalities for 1 movie")
        #print("Matrix Structure: 6x4 (attributes × modalities)")
        #print("Comparing standard 0.5 initialization vs. genre-aware initialization")
        
        movies = ["The Dark Knight"]
        for movie in movies:
            self.print_movie_analysis(movie)
        '''
        print("ANALYSIS COMPLETE")
        print("=" * 80)
        print("System Features:")
        print("✓ Standard uniform matrix (6x4)")
        print("✓ Genre-aware contextual matrix")
        print("✓ Dynamic matrix updates based on user choices")
        print("✓ Impact analysis of genre-aware initialization")
        print("✓ Ready for Fire TV integration")'''

def main():
    system = FireTVGroupPreferenceSystem()
    system.run_complete_analysis()

if __name__ == "__main__":
    main()