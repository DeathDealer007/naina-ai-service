from typing import List, Dict, Any

# Static registry of exercises
EXERCISES = [
    {
        "id": "ex_20_20_20",
        "title": "The 20-20-20 Rule",
        "category": "EYE_STRAIN",
        "description": "Every 20 minutes, look at an object at least 20 feet away for at least 20 seconds. This helps reset the focusing muscles in your eyes.",
        "duration": "20 seconds",
        "steps": [
            "Set a timer for 20 minutes.",
            "When it rings, look away from your screen.",
            "Focus on an object about 20 feet (6 meters) away.",
            "Keep looking at it for a full 20 seconds."
        ],
        "tags": ["strain", "fatigue", "break", "screen"]
    },
    {
        "id": "ex_blinking",
        "title": "Slow Blinking Exercise",
        "category": "DRY_EYES",
        "description": "Intentionally blink slowly to restore the tear film over your cornea, preventing dry, irritated eyes.",
        "duration": "1 minute",
        "steps": [
            "Close your eyes slowly and keep them closed for 2 seconds.",
            "Squeeze them gently for 1 additional second.",
            "Open your eyes and relax for 2 seconds.",
            "Repeat this cycle 10 times."
        ],
        "tags": ["dry", "irritation", "burning", "blink"]
    },
    {
        "id": "ex_palming",
        "title": "Eye Palming",
        "category": "EYE_STRAIN",
        "description": "Use the warmth of your hands to soothe your ocular muscles and block out light to give your retinas a break.",
        "duration": "2 minutes",
        "steps": [
            "Rub your palms together vigorously until they feel warm.",
            "Gently cup your palms over your closed eyes (don't press on the eyeballs).",
            "Fingers should rest on your forehead, heel of hand on cheekbones.",
            "Breathe deeply in the darkness for 2 minutes."
        ],
        "tags": ["strain", "fatigue", "pain", "darkness"]
    },
    {
        "id": "ex_eye_rolling",
        "title": "Ocular Muscle Stretch (Eye Rolling)",
        "category": "SCREEN_FATIGUE",
        "description": "Strengthen and stretch your extraocular muscles to relieve tension in and around your eyes.",
        "duration": "1 minute",
        "steps": [
            "Sit up straight and look ahead.",
            "Without moving your head, look up, then slowly roll your eyes clockwise.",
            "Complete 5 slow circles clockwise.",
            "Reverse the direction and complete 5 slow circles counter-clockwise.",
            "Close your eyes and rest."
        ],
        "tags": ["fatigue", "tension", "stiffness", "stretch"]
    },
    {
        "id": "ex_focus_shift",
        "title": "Near-Far Focus Shifting",
        "category": "LOW_FOCUS",
        "description": "Train your ciliary muscles to switch focus dynamically, improving visual agility and concentration.",
        "duration": "1.5 minutes",
        "steps": [
            "Hold your thumb about 10 inches in front of your face.",
            "Focus on your thumb for 5 seconds.",
            "Shift your gaze to a distant object (15+ feet away) for 5 seconds.",
            "Shift back to your thumb.",
            "Repeat this process 10 times."
        ],
        "tags": ["focus", "blurry", "concentration", "exercise"]
    },
    {
        "id": "ex_posture",
        "title": "Ergonomic & Posture Reset",
        "category": "SCREEN_FATIGUE",
        "description": "Correct your sitting posture to reduce strain on your neck and spine, which directly impacts eye pressure and fatigue.",
        "duration": "1 minute",
        "steps": [
            "Sit back in your chair, feet flat on the floor.",
            "Roll your shoulders back and down.",
            "Align your neck so your ears are directly above your shoulders.",
            "Ensure the top of your screen is at or slightly below eye level."
        ],
        "tags": ["posture", "neck", "headache", "fatigue"]
    }
]

# Static registry of games
GAMES = [
    {
        "id": "game_tracker",
        "title": "Eye Tracker",
        "category": "LOW_FOCUS",
        "description": "Follow a moving star as it darts across the screen. Promotes eye tracking and quick concentration adjustments.",
        "type": "reflex",
        "difficulty": "Easy",
        "tags": ["focus", "reflex", "tracking", "attention"]
    },
    {
        "id": "game_reflex",
        "title": "Reflex Runner",
        "category": "LOW_FOCUS",
        "description": "A high-speed click/tap game where objects appear rapidly. Exercises response time and visual reflexes.",
        "type": "speed",
        "difficulty": "Medium",
        "tags": ["reflex", "speed", "hand-eye", "quick"]
    },
    {
        "id": "game_memory",
        "title": "Nainataara Matcher",
        "category": "LOW_FOCUS",
        "description": "Flip and match cards showing eye wellness symbols. Builds concentration, visual memory, and short-term focus.",
        "type": "memory",
        "difficulty": "Medium",
        "tags": ["memory", "focus", "concentration", "brain"]
    },
    {
        "id": "game_peripheral",
        "title": "Bubble Pop",
        "category": "LOW_FOCUS",
        "description": "Pop bubbles that appear in your peripheral vision without looking away from the center target. Expands visual awareness.",
        "type": "visual",
        "difficulty": "Hard",
        "tags": ["peripheral", "awareness", "focus", "tracking"]
    }
]

class RecommendationService:
    def get_all_exercises(self) -> List[Dict[str, Any]]:
        return EXERCISES

    def get_all_games(self) -> List[Dict[str, Any]]:
        return GAMES

    def recommend(self, tags_or_symptoms: List[str]) -> Dict[str, List[Dict[str, Any]]]:
        """
        Recommends exercises and games based on input symptoms/tags.
        """
        recommended_exercises = []
        recommended_games = []
        
        # Lowercase everything for matching
        search_terms = [term.lower().strip() for term in tags_or_symptoms]
        
        # Category-based fallback check
        matched_categories = set()
        for term in search_terms:
            if "strain" in term or "burn" in term or "tired" in term:
                matched_categories.add("EYE_STRAIN")
            if "dry" in term or "scratchy" in term or "blink" in term or "irritat" in term:
                matched_categories.add("DRY_EYES")
            if "focus" in term or "concentrat" in term or "reflex" in term or "attention" in term or "distract" in term:
                matched_categories.add("LOW_FOCUS")
            if "fatigue" in term or "neck" in term or "posture" in term or "headache" in term or "screen" in term:
                matched_categories.add("SCREEN_FATIGUE")
        
        # Filter exercises
        for ex in EXERCISES:
            # Match by category
            if ex["category"] in matched_categories:
                recommended_exercises.append(ex)
                continue
            # Match by tags
            if any(tag in search_terms for tag in ex["tags"]):
                recommended_exercises.append(ex)
                continue
            # Direct text search match
            if any(term in ex["title"].lower() or term in ex["description"].lower() for term in search_terms):
                recommended_exercises.append(ex)

        # Filter games
        for gm in GAMES:
            # Match by category
            if gm["category"] in matched_categories:
                recommended_games.append(gm)
                continue
            # Match by tags
            if any(tag in search_terms for tag in gm["tags"]):
                recommended_games.append(gm)
                continue
            # Direct text search match
            if any(term in gm["title"].lower() or term in gm["description"].lower() for term in search_terms):
                recommended_games.append(gm)

        # Remove duplicates
        unique_exercises = {ex["id"]: ex for ex in recommended_exercises}.values()
        unique_games = {gm["id"]: gm for gm in recommended_games}.values()

        # If nothing matches, provide default/general recommendations
        if not unique_exercises:
            # Default to 20-20-20 rule and Palming
            unique_exercises = [ex for ex in EXERCISES if ex["id"] in ["ex_20_20_20", "ex_palming"]]
        if not unique_games:
            # Default to Nainataara Matcher
            unique_games = [gm for gm in GAMES if gm["id"] in ["game_memory", "game_tracker"]]

        return {
            "exercises": list(unique_exercises),
            "games": list(unique_games)
        }

recommendation_engine = RecommendationService()
