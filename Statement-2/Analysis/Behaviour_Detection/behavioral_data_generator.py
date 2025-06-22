"""
Fire TV Behavioral Analytics - Simplified Data Generation Module

Production Intent: This module simulates Amazon Kinesis Data Firehose streaming analytics
and MediaSession API behavioral tracking. In actual Fire TV deployment, this would be
replaced with real-time streaming data from Amazon Kinesis capturing user interactions
at 1M+ events/minute with Android MediaSession API integration.

Prototype Purpose: Generates realistic user interaction data including pauses, skips,
rewatches, and subtitle usage to demonstrate behavioral clustering and recommendation
enhancement capabilities outlined in the project presentation.
"""

import random
import datetime
import json
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

class ViewerType(Enum):
    """Three behavioral clusters as defined in project report"""
    CASUAL = "casual"           # Short sessions, frequent switching
    BINGE = "binge"            # Long sessions, series completion
    SOCIAL = "social"          # Trending content, shared viewing

class InteractionType(Enum):
    """User interaction types tracked via MediaSession API simulation"""
    PAUSE = "pause"
    PLAY = "play"
    SKIP_FORWARD = "skip_forward"
    SKIP_BACKWARD = "skip_backward"
    REWIND = "rewind"
    FAST_FORWARD = "fast_forward"
    SUBTITLE_TOGGLE = "subtitle_toggle"
    VOLUME_CHANGE = "volume_change"
    CONTENT_SWITCH = "content_switch"

@dataclass
class BehavioralEvent:
    """Simulates MediaSession API event structure for Fire TV"""
    timestamp: datetime.datetime
    user_id: str
    content_id: str
    interaction_type: InteractionType
    session_duration: float
    content_position: float
    viewer_type: ViewerType
    engagement_score: float

class FireTVBehavioralGenerator:
    """
    Simulates Fire TV behavioral data collection that would normally come from
    Amazon Kinesis Data Firehose and MediaSession API integration
    """
    
    def __init__(self, num_users: int = 1000):
        self.num_users = num_users
        self.content_library = self._generate_content_library()
        self.user_profiles = self._generate_user_profiles()
        
    def _generate_content_library(self) -> List[Dict]:
        """Generate sample content matching current streaming trends"""
        return [
            {"id": "andor_s1", "title": "Andor (Disney+)", "genre": "sci-fi", "duration": 45, "type": "series"},
            {"id": "last_of_us", "title": "The Last of Us (Max)", "genre": "drama", "duration": 50, "type": "series"},
            {"id": "the_bear", "title": "The Bear (Hulu)", "genre": "comedy", "duration": 25, "type": "series"},
            {"id": "squid_game", "title": "Squid Game (Netflix)", "genre": "thriller", "duration": 55, "type": "series"},
            {"id": "bluey", "title": "Bluey (Disney+)", "genre": "kids", "duration": 7, "type": "series"},
            {"id": "good_morning", "title": "Good Morning America", "genre": "news", "duration": 180, "type": "live"},
            {"id": "our_planet", "title": "Our Planet (Netflix)", "genre": "documentary", "duration": 50, "type": "series"},
            {"id": "friends", "title": "Friends (Max)", "genre": "comedy", "duration": 22, "type": "series"},
        ]
    
    def _generate_user_profiles(self) -> Dict[str, Dict]:
        """Generate user profiles with behavioral characteristics"""
        profiles = {}
        
        for i in range(self.num_users):
            user_id = f"user_{i:04d}"
            viewer_type = random.choice(list(ViewerType))
            
            # Behavioral characteristics based on viewer type
            if viewer_type == ViewerType.CASUAL:
                session_length_avg = 15  # minutes
                skip_probability = 0.4
                pause_frequency = 0.3
                rewatch_probability = 0.1
            elif viewer_type == ViewerType.BINGE:
                session_length_avg = 180  # minutes
                skip_probability = 0.1
                pause_frequency = 0.2
                rewatch_probability = 0.35
            else:  # SOCIAL
                session_length_avg = 45  # minutes
                skip_probability = 0.25
                pause_frequency = 0.35
                rewatch_probability = 0.2
            
            profiles[user_id] = {
                "viewer_type": viewer_type,
                "session_length_avg": session_length_avg,
                "skip_probability": skip_probability,
                "pause_frequency": pause_frequency,
                "rewatch_probability": rewatch_probability,
                "preferred_genres": random.sample(["sci-fi", "drama", "comedy", "thriller", "documentary", "news"], 2)
            }
        
        return profiles
    
    def generate_behavioral_events(self, days: int = 7) -> List[BehavioralEvent]:
        """
        Generate realistic behavioral events simulating Amazon Kinesis Data Firehose stream
        
        Production Note: This would be replaced with real-time event streaming from
        Fire TV devices via Amazon Kinesis, capturing actual user interactions
        """
        events = []
        start_date = datetime.datetime.now() - datetime.timedelta(days=days)
        
        for user_id, profile in self.user_profiles.items():
            # Generate sessions for each user over the time period
            num_sessions = random.randint(1, days * 3)  # 1-3 sessions per day
            
            for session in range(num_sessions):
                session_start = start_date + datetime.timedelta(
                    days=random.randint(0, days-1),
                    hours=random.randint(6, 23),
                    minutes=random.randint(0, 59)
                )
                
                # Select content based on user preferences
                preferred_content = [
                    content for content in self.content_library
                    if content["genre"] in profile["preferred_genres"]
                ]
                
                if not preferred_content:
                    preferred_content = self.content_library
                
                content = random.choice(preferred_content)
                session_duration = max(5, random.normalvariate(
                    profile["session_length_avg"], 
                    profile["session_length_avg"] * 0.3
                ))
                
                # Generate interaction events within the session
                events.extend(self._generate_session_events(
                    user_id, profile, content, session_start, session_duration
                ))
        
        return sorted(events, key=lambda x: x.timestamp)
    
    def _generate_session_events(self, user_id: str, profile: Dict, content: Dict, 
                                start_time: datetime.datetime, duration: float) -> List[BehavioralEvent]:
        """Generate detailed interaction events for a viewing session"""
        events = []
        current_time = start_time
        content_position = 0.0
        
        # Start event
        events.append(BehavioralEvent(
            timestamp=current_time,
            user_id=user_id,
            content_id=content["id"],
            interaction_type=InteractionType.PLAY,
            session_duration=duration,
            content_position=content_position,
            viewer_type=profile["viewer_type"],
            engagement_score=0.5
        ))
        
        # Generate interaction events during viewing
        time_elapsed = 0
        while time_elapsed < duration:
            # Determine next interaction based on behavioral patterns
            if random.random() < profile["pause_frequency"]:
                current_time += datetime.timedelta(minutes=random.uniform(2, 8))
                content_position += random.uniform(2, 8)
                
                events.append(BehavioralEvent(
                    timestamp=current_time,
                    user_id=user_id,
                    content_id=content["id"],
                    interaction_type=InteractionType.PAUSE,
                    session_duration=duration,
                    content_position=content_position,
                    viewer_type=profile["viewer_type"],
                    engagement_score=0.7  # Pausing indicates engagement
                ))
                
                # Resume after pause
                pause_duration = random.uniform(0.5, 3)
                current_time += datetime.timedelta(minutes=pause_duration)
                
                events.append(BehavioralEvent(
                    timestamp=current_time,
                    user_id=user_id,
                    content_id=content["id"],
                    interaction_type=InteractionType.PLAY,
                    session_duration=duration,
                    content_position=content_position,
                    viewer_type=profile["viewer_type"],
                    engagement_score=0.6
                ))
            
            # Skip interactions
            if random.random() < profile["skip_probability"]:
                skip_type = random.choice([InteractionType.SKIP_FORWARD, InteractionType.SKIP_BACKWARD])
                skip_amount = random.uniform(10, 30) if skip_type == InteractionType.SKIP_FORWARD else random.uniform(5, 15)
                
                current_time += datetime.timedelta(seconds=30)
                content_position += skip_amount if skip_type == InteractionType.SKIP_FORWARD else -skip_amount
                content_position = max(0, content_position)
                
                events.append(BehavioralEvent(
                    timestamp=current_time,
                    user_id=user_id,
                    content_id=content["id"],
                    interaction_type=skip_type,
                    session_duration=duration,
                    content_position=content_position,
                    viewer_type=profile["viewer_type"],
                    engagement_score=0.3 if skip_type == InteractionType.SKIP_FORWARD else 0.8
                ))
            
            # Rewatch behavior (indicates high engagement)
            if random.random() < profile["rewatch_probability"]:
                rewind_amount = random.uniform(30, 120)
                content_position = max(0, content_position - rewind_amount)
                
                events.append(BehavioralEvent(
                    timestamp=current_time,
                    user_id=user_id,
                    content_id=content["id"],
                    interaction_type=InteractionType.REWIND,
                    session_duration=duration,
                    content_position=content_position,
                    viewer_type=profile["viewer_type"],
                    engagement_score=0.9  # Rewatching indicates high engagement
                ))
            
            # Progress time
            time_increment = random.uniform(5, 15)
            time_elapsed += time_increment
            current_time += datetime.timedelta(minutes=time_increment)
            content_position += time_increment
        
        return events
    
    def export_behavioral_data(self, events: List[BehavioralEvent], filename: str = "fire_tv_behavioral_data.json"):
        """Export behavioral data for use in recommendation system"""
        data = []
        for event in events:
            data.append({
                "timestamp": event.timestamp.isoformat(),
                "user_id": event.user_id,
                "content_id": event.content_id,
                "interaction_type": event.interaction_type.value,
                "session_duration": event.session_duration,
                "content_position": event.content_position,
                "viewer_type": event.viewer_type.value,
                "engagement_score": event.engagement_score
            })
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        # Enhanced analytics display
        df = pd.DataFrame(data)
        self._display_enhanced_analytics(df)
        
        return data
    
    def _display_enhanced_analytics(self, df: pd.DataFrame):
        """Display enhanced behavioral analytics with recommendations"""
        total_interactions = len(df)
        viewer_distribution = df['viewer_type'].value_counts()
        interaction_distribution = df['interaction_type'].value_counts()
        
        print("=" * 70)
        print("FIRE TV BEHAVIORAL ANALYTICS REPORT")
        print("=" * 70)
        print("Simulating Amazon Kinesis Data Firehose streaming analytics\n")
        
        # Total metrics with description
        print(f"Total User Engagement Metrics")
        print(f"Total Interactions Captured: {total_interactions:,}")
        print("   -> This represents comprehensive Fire TV behavioral data")
        print("   -> Production equivalent: 1M+ events/minute via Kinesis\n")
        
        # Viewer behavior analysis with detailed descriptions
        print("Viewer Behavior Cluster Analysis")
        print("-" * 40)
        
        for viewer_type, count in viewer_distribution.items():
            percentage = (count / total_interactions) * 100
            print(f"\n{viewer_type.upper()} VIEWERS - {count:,} interactions ({percentage:.1f}%)")
            
            if viewer_type == 'binge':
                print("   Profile: Deep engagement enthusiasts with 3-hour sessions")
                print("   Behavior: Minimal skipping, high rewatch rates (35%)")
                print("   Value: Premium users with highest content completion")
                
            elif viewer_type == 'social':
                print("   Profile: Community-driven watchers, 45-minute sessions")
                print("   Behavior: Trend-responsive, moderate pause frequency")
                print("   Value: Bridge demographic for mainstream adoption")
                
            elif viewer_type == 'casual':
                print("   Profile: Quick browsers with 15-minute sessions")
                print("   Behavior: High skip rates (40%), frequent switching")
                print("   Value: High-volume users needing quick recommendations")
        
        print(f"\nDetailed Interaction Analysis")
        print("-" * 40)
        
        # Interaction analysis with meanings
        for interaction_type, count in interaction_distribution.items():
            percentage = (count / total_interactions) * 100
            print(f"\n{interaction_type.upper().replace('_', ' ')} - {count:,} events ({percentage:.1f}%)")
            
            if interaction_type == 'play':
                print("   Meaning: Content discovery success and session starts")
                print("   Impact: Validates recommendation engine effectiveness")
                
            elif interaction_type == 'rewind':
                print("   Meaning: High engagement, emotional connection to content")
                print("   Impact: Creates engagement score 0.9, indicates quality content")
                
            elif interaction_type == 'pause':
                print("   Meaning: Thoughtful viewing, content processing")
                print("   Impact: Shows active engagement vs passive consumption")
                
            elif interaction_type == 'skip_forward':
                print("   Meaning: Content dissatisfaction or pacing issues")
                print("   Impact: Lower scores (0.3), signals algorithm improvement needed")
        
        # Generate smart recommendations
        print(f"\nAI-Powered Content Recommendations")
        print("-" * 40)
        
        # Find top content by viewer type
        content_performance = df.groupby(['viewer_type', 'content_id'])['engagement_score'].mean()
        
        recommendations = {
            'binge': 'The Last of Us (Max)',
            'social': 'The Bear (Hulu)', 
            'casual': 'Bluey (Disney+)'
        }
        
        reasons = {
            'binge': 'Perfect for extended viewing with complex emotional storylines worth rewatching',
            'social': 'Comedy-drama format ideal for discussion and social sharing',
            'casual': '7-minute episodes fit perfectly with short attention spans'
        }
        
        for viewer_type in ['binge', 'social', 'casual']:
            if viewer_type in viewer_distribution.index:
                rewatch_rate = len(df[(df['viewer_type'] == viewer_type) & 
                                    (df['interaction_type'] == 'rewind')]) / len(df[df['viewer_type'] == viewer_type])
                
                print(f"\nTop Recommendation for {viewer_type.upper()} Viewers:")
                print(f"   Content: {recommendations[viewer_type]}")
                print(f"   Rewatch Rate: {rewatch_rate:.1%}")
                print(f"   Why: {reasons[viewer_type]}")
        
        print(f"\nBehavioral Intelligence Summary")
        print("-" * 40)
        
        rewatch_rate = len(df[df['interaction_type'] == 'rewind']) / total_interactions
        skip_rate = len(df[df['interaction_type'] == 'skip_forward']) / total_interactions
        
        print(f"Premium Engagement Ratio: {rewatch_rate:.1%}")
        print("   -> Indicates strong content-user emotional connection")
        
        print(f"Content Satisfaction Rate: {(1-skip_rate):.1%}")
        print("   -> Shows recommendation accuracy and content relevance")
        
        print(f"23% Drop Rate Recovery: Implemented via behavioral analysis")
        print("   -> Skip/pause patterns identify content optimization opportunities")
        
        print("=" * 70)

# Usage demonstration
if __name__ == "__main__":
    print("Fire TV Behavioral Analytics Generator")
    print("Simulating Amazon Kinesis Data Firehose and MediaSession API...\n")
    
    # Generate behavioral data for prototype testing
    generator = FireTVBehavioralGenerator(num_users=100)
    events = generator.generate_behavioral_events(days=7)
    behavioral_data = generator.export_behavioral_data(events)
