import random
from datetime import datetime
from typing import Dict, Any

from analysis import (
    analyse_sentiment,
    analyse_emotions,
    analyse_context,
    analyse_entities
)
from insights import update_user_insights, get_conversation_insights
from question_templates import load_question_templates

class ReflectionHelper:
    """
    Core class to manage NLP-based reflection logic.
    Processes user input, tracks conversation history,
    and generates reflective outputs.
    """

    def __init__(self):
        """
        Initialise question templates, user insights, and conversation history.
        """
        self.question_templates = load_question_templates()
        self.conversation_history = []
        self.user_insights = {
            'recurring_themes': {},
            'emotional_patterns': [],
            'entities_mentioned': []
        }

    def get_full_analysis(self, text: str) -> Dict[str, Any]:
        """
        Run all analysis pipelines on user input text.

        Params:
            :text: The raw user input string.
        Returns:
            :Dict[str, Any]: Full analysis including sentiment, emotion, context, entities, and timestamp.
        """
        return {
            "text": text,
            "sentiment": analyse_sentiment(text),
            "emotion": analyse_emotions(text),
            "context": analyse_context(text),
            "entities": analyse_entities(text),
            "timestamp": datetime.now().isoformat()
        }

    def process_user_input(self, user_input: str) -> str:
        """
        Handle user input end-to-end: analyse, update history, and generate response.

        Params:
            :user_input: Raw string input from user.
        Returns:
            :str: Composed reflection and action response.
        """
        analysis = self.get_full_analysis(user_input)
        update_user_insights(self.user_insights, analysis)

        # Add to conversation history
        self.conversation_history.append({
            'user_input': user_input,
            'analysis': analysis,
            'timestamp': datetime.now().isoformat()
        })

        reflection = self.generate_personalised_response(analysis)
        action = self.generate_action_point(analysis)
        return f"{reflection}\n\n{action}"

    def generate_personalised_response(self, analysis: Dict[str, Any]) -> str:
        """
        Create reflection based on emotion, sentiment, and named entities.

        Params:
            :analysis: Full NLP analysis of the input.
        Returns:
            :str: Reflective question and acknowledgment.
        """
        emotion = analysis['emotion']['primary_emotion']
        sentiment = analysis['sentiment']['sentiment'].lower()
        entities = analysis['entities']

        # Acknowledgment phrase based on emotion
        acknowledgments = self.question_templates.get('acknowledgments', {})
        acknowledgment = random.choice(acknowledgments.get(emotion, ["I hear what you're sharing."]))

        # Add entity-specific context if available
        entity_acknowledgment = ""
        if entities:
            people = [e for e in entities if e['entity_type'] == 'PER']
            places = [e for e in entities if e['entity_type'] == 'LOC']
            if people:
                entity_acknowledgment = f" It sounds like {people[0]['word']} plays an important role in this."
            elif places:
                entity_acknowledgment = f" And this connection to {places[0]['word']} seems significant."

        question = self.select_reflection_question(analysis)
        return f"{acknowledgment}{entity_acknowledgment}\n\n{question}"

    def generate_action_point(self, analysis: Dict[str, Any]) -> str:
        """
        Suggest a simple next step based on primary emotion and sentiment.

        Params:
            :analysis: Full NLP analysis of the input.
        Returns:
            :str: Action suggestion and emotional summary.
        """
        emotion = analysis['emotion']['primary_emotion']
        sentiment = analysis['sentiment']['sentiment'].lower()
        action_templates = self.question_templates.get('actions', {})

        # Pick an action suggestion or fallback
        action = random.choice(action_templates.get(emotion, [
            "Reflect on what this moment is revealing about your deeper values.",
            "Note down any insights that emerged from this experience.",
            "Ask yourself: what part of me most needed this moment to happen?"
        ]))

        reference = f"There’s a clear feeling of {emotion} in what you expressed, and a kind of {sentiment} tone that lingers as you share."
        return f"{reference}\n\nOne gentle step forward might be: {action} \n\n------------------------------------------------"

    def select_reflection_question(self, analysis: Dict[str, Any]) -> str:
        """
        Choose a reflection question based on emotion or contextual confidence.

        Params:
            :analysis: Full NLP analysis of the input.
        Returns:
            :str: A single reflection question.
        """
        emotion = analysis['emotion']['primary_emotion']
        context = analysis['context']['primary_context']

        # Priority to high-confidence emotion, fallback to context, then generic
        if analysis['emotion']['primary_confidence'] > 0.8 and emotion in self.question_templates:
            questions = self.question_templates[emotion]
        elif analysis['context']['confidence'] > 0.6:
            questions = self.question_templates.get(context, self.question_templates.get('self_reflection', []))
        else:
            questions = self.question_templates.get('self_reflection', [])

        return random.choice(questions) if questions else ""


async def start_reflection_session():
    """
    Starts CLI-based reflection loop.
    Accepts input, returns insights or response until user exits.
    """
    helper = ReflectionHelper()
    print("Welcome to your Reflection Assistant!")
    print("Type **'insights'** for patterns, or 'quit' to end.\n")

    while True:
        try:
            user_input = input("\nWhat is something you'd like to reflect on today? ").strip()

            # End session if user wants to exit
            if user_input.lower() in ['quit', 'exit', 'bye', 'cya']:
                print("\nThanks for the chat. Take care!")
                break

            # Print summary insights so far
            if user_input.lower() == 'insights':
                insights = get_conversation_insights(helper.user_insights, helper.conversation_history)
                for k, v in insights.items():
                    print(f"  {k}: {v}")
                continue

            # Skip if input is empty
            if not user_input:
                print("\n-----------------------------------------------------------------------------\n")
                print("I'm here when you're ready.")
                continue

            # Process user input and generate response
            response = helper.process_user_input(user_input)
            print(f"\n{response}")

        # Handle CTRL+C gracefully
        except KeyboardInterrupt:
            print("\n\nThanks for the chat. Take care!")
            break

        # Catch unexpected errors but keep session going
        except Exception as e:
            print(f"Error: {e}. Let's keep going.")
