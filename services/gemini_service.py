import os
from typing import List, Dict, Any
from google import genai
from google.genai import types
from google.genai.errors import APIError
from prompts.system_prompt import SYSTEM_PROMPT

class GeminiService:
    def __init__(self):
        # The client automatically picks up GEMINI_API_KEY from environment variables.
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.client = None
        self.model_name = "gemini-2.5-flash"
        
        # Check if API key is present and doesn't match the known leaked key (for local debugging)
        if self.api_key and not self.api_key.startswith("AIzaSyC5tYMiND"):
            try:
                self.client = genai.Client(api_key=self.api_key)
            except Exception as e:
                print(f"Error initializing Gemini client: {e}")
        else:
            print("Warning: Missing or placeholder/leaked API key. Using rule-based conversation engine.")

    def get_rule_based_response(self, user_msg: str) -> str:
        """
        Provides rich, conversational fallback responses for eye wellness queries
        when the Gemini API is inaccessible or blocked.
        """
        msg = user_msg.lower().strip()
        
        # Dry eyes
        if any(w in msg for w in ["dry", "blink", "gritty", "scratchy", "watery", "burning"]):
            return (
                "It sounds like your eyes might be feeling dry or irritated. When we stare at screens, "
                "our blinking rate decreases by about 50%, which causes the tear film on our eyes to dry up.\n\n"
                "I recommend trying a **Slow Blinking Exercise**: close your eyes slowly, squeeze gently for "
                "a second, and open. Repeat this 10 times. Also, remember to take a quick sip of water to stay hydrated!"
            )
            
        # Eye strain
        elif any(w in msg for w in ["strain", "tired", "burn", "ache", "sore", "hurt", "pressure", "blur"]):
            return (
                "I'm sorry to hear that your eyes are feeling strained. Focus strain happens when your ciliary "
                "muscles stay contracted to look at a close screen for too long.\n\n"
                "I highly recommend doing the **20-20-20 Rule**: look away from your screen for 20 seconds "
                "at something 20 feet (6 meters) away. This allows your focusing muscles to relax completely. "
                "You can also rub your palms together to warm them up and cup them over your closed eyes (Palming) for a few minutes."
            )
            
        # Focus/games
        elif any(w in msg for w in ["focus", "concentrat", "distract", "game", "reflex", "attention"]):
            return (
                "If you are finding it hard to focus, your eyes and mind might be experiencing screen-induced fatigue. "
                "A brief shift in attention can help reset your concentration.\n\n"
                "I recommend trying a quick tracking or matching game, such as our **Nainataara Matcher** or "
                "**Eye Tracker**. These games stimulate visual reflexes and restore short-term concentration!"
            )
            
        # Screen fatigue/break
        elif any(w in msg for w in ["fatigue", "screen", "break", "posture", "neck", "shoulder"]):
            return (
                "Working on screens for long hours can fatigue your eyes and your body. Let's do a quick **Posture Reset**:\n\n"
                "1. Sit back and keep your feet flat on the floor.\n"
                "2. Roll your shoulders back and relax your neck.\n"
                "3. Adjust your screen so it is about arm's length away, with the top of the monitor at eye level.\n\n"
                "Taking a 5-minute physical stretch break will help restore blood circulation and relieve eye fatigue."
            )
            
        # Greetings
        elif any(w in msg for w in ["hello", "hi", "hey", "naina", "greetings"]):
            return (
                "Hello! I am Naina, your conversational eye wellness companion.\n\n"
                "I'm here to help you manage screen fatigue, guide you through eye relaxation exercises, "
                "and recommend focus games. How are your eyes feeling right now?"
            )
            
        # Identity
        elif any(w in msg for w in ["name", "who are you", "what are you"]):
            return (
                "I am Naina, your eye wellness assistant from Nainataara. "
                "I help you build healthy screen habits, reduce digital eye strain, and suggest focus-building exercises. "
                "I am not a medical system, but I'm a friendly companion for your daily digital routine!"
            )
            
        # Medical queries safety check
        elif any(w in msg for w in ["disease", "cure", "medicine", "doctor", "drops", "glasses", "prescription", "infection"]):
            return (
                "Just a reminder that I am an eye wellness assistant and cannot prescribe medicines, diagnose "
                "diseases, or suggest medical treatments.\n\n"
                "If you are experiencing persistent irritation, pain, or vision changes, please consult an "
                "ophthalmologist or eye specialist for a proper examination."
            )
            
        # Default
        else:
            return (
                "I'm here to support your eye wellness! Staring at screens for long periods can cause eye strain, "
                "dryness, or low focus.\n\n"
                "Tell me if you are feeling any strain or tiredness, or if you'd like a quick eye relaxation exercise "
                "or focus game recommendation."
            )

    def generate_chat_response(self, conversation_history: List[Dict[str, str]]) -> str:
        """
        Sends conversation history to Gemini and returns the model response.
        Falls back to rule-based logic if API is blocked or unconfigured.
        """
        user_message = conversation_history[-1]["content"] if conversation_history else ""
        
        # If API client isn't initialized, use rule-based fallback
        if not self.client:
            # Attempt to re-initialize client in case API key was updated
            self.api_key = os.getenv("GEMINI_API_KEY")
            if self.api_key and not self.api_key.startswith("AIzaSyC5tYMiND"):
                try:
                    self.client = genai.Client(api_key=self.api_key)
                except Exception:
                    pass
            
            if not self.client:
                return self.get_rule_based_response(user_message)

        try:
            # Map history to the format expected by google-genai
            contents = []
            for msg in conversation_history:
                role = "model" if msg["role"] in ["model", "assistant"] else "user"
                contents.append(
                    types.Content(
                        role=role,
                        parts=[types.Part.from_text(text=msg["content"])]
                    )
                )

            # Generate content
            config = types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                temperature=0.7,
            )
            
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=contents,
                config=config
            )
            return response.text
        except APIError as e:
            print(f"Gemini API Error (falling back to rule-based): {e}")
            return self.get_rule_based_response(user_message)
        except Exception as e:
            print(f"Unexpected error in GeminiService (falling back to rule-based): {e}")
            return self.get_rule_based_response(user_message)

    def generate_structured_recommendations(self, prompt: str) -> str:
        """
        Generates a structured recommendation response from Gemini.
        """
        if not self.client:
            return ""
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.2,
                )
            )
            return response.text
        except Exception as e:
            print(f"Error generating recommendations: {e}")
            return ""
