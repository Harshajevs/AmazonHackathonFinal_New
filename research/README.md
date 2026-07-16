# Research — Original Hackathon Prototypes

These are the untouched Amazon HackOn Season 5 prototypes, kept as provenance for the algorithms now productionized in `backend/app/services/`:

| Prototype | Productionized as |
|---|---|
| `statement-1/Personalised_AI_Recommendations/Personalised_recommendations.py` | `services/recommendations/personal.py` |
| `statement-1/.../preprocessing_with_history.py` (also statement-3 copy) | `services/recommendations/history.py` |
| `statement-1/.../dynamic_ratios.py` | `services/recommendations/weights.py` |
| `statement-2/Room_Recommendations/updated_6X6_group_suggestions.py` | `services/recommendations/group.py` |
| `statement-3/Processing_Movie_Matrix/updated_changing_matrix.py` | `services/recommendations/evolution.py` |
| `statement-1/.../Behaviour_Detection/Behaviour_classifier.py` (dup in statement-2) | `services/analysis/behavior.py` |
| `statement-1/.../Time_Detection/FireTVTimeDisplay.py` (dup in statement-2) | `services/analysis/time_blocks.py` |
| `statement-2/Analysis/Reactions_Analysis/emoji_emotion.py` | `services/analysis/emoji.py` |
| `statement-1/.../Mood_Detection(YOLO)/` (`best.onnx`, dup in statement-2) | `services/analysis/mood/onnx_facial.py` (optional provider) |
| `statement-2/Custom_Room_Simulator/` (file-based CLI room state machine) | `services/rooms/` (WebSocket realtime + same role model) |
| Voice mood / BERT chat / VR filter notebooks | future providers behind the same interfaces |

Nothing here is imported by the application; run these only for reference.
