import os
import json
import random
import asyncio
import edge_tts
from typing import Dict, List, Any
from transformers import pipeline
from datetime import datetime

class ReflectionHelper:
    """
    A chatbot that uses NLP analysis to ask thoughtful reflection questions
    based on user sentiment, emotions, and content analysis.
    """
    
    def __init__(self):
        """
        Initialise all the NLP pipelines and question templates.
        """
        self.setup_pipelines()
        self.setup_question_templates()
        self.conversation_history = []
        self.user_insights = {
            'recurring_themes': {},
            'emotional_patterns': [],
            'entities_mentioned': []
        }
    
    def setup_pipelines(self):
        """
        Load all NLP pipelines.
        """
        print("Loading NLP models...")
        
        self.sentiment_pipeline = pipeline(
            "sentiment-analysis", 
            model="distilbert/distilbert-base-uncased-finetuned-sst-2-english"
        )
        
        self.emotion_pipeline = pipeline(
            "text-classification", 
            model="hamzawaheed/emotion-classification-model"
        )
        
        self.zero_shot_pipeline = pipeline(
            "zero-shot-classification", 
            model="facebook/bart-large-mnli"
        )
        
        self.ner_pipeline = pipeline(
            "ner", 
            model="dslim/distilbert-NER", 
            aggregation_strategy="simple"
        )
        
        print("All models loaded successfully.")
    
    def setup_question_templates(self):
        """
        Define templates for reflective questions.
        """
        self.question_templates = {}
        self.deepening_questions = []

    def analyse_sentiment(self, text: str) -> Dict[str, Any]:
        """
        Return sentiment label and confidence.
        """
        result = self.sentiment_pipeline(text)[0]
        return {
            "sentiment": result["label"],
            "confidence": result["score"]
        }
    
    def analyse_emotions(self, text: str) -> Dict[str, Any]:
        """
        Return primary emotion, its score, and full emotion breakdown.
        """
        emotions = self.emotion_pipeline(text)
        label_map = {
            "LABEL_0": "sadness",
            "LABEL_1": "joy", 
            "LABEL_2": "love",
            "LABEL_3": "anger",
            "LABEL_4": "fear",
            "LABEL_5": "surprise"
        }
        top = max(emotions, key=lambda x: x["score"])
        return {
            "primary_emotion": label_map.get(top["label"], top["label"]),
            "primary_confidence": top["score"],
            "all_emotions": [(label_map.get(e["label"], e["label"]), e["score"]) for e in emotions]
        }
    
    def analyse_context(self, text: str) -> Dict[str, Any]:
        """
        Return the most likely context from a predefined list.
        """
        labels = [
            "relationships", "work stress", "self-reflection", "family", 
            "health", "change transition", "daily life", "personal growth",
            "anxiety", "depression", "motivation", "goals", "past experiences"
        ]
        result = self.zero_shot_pipeline(text, candidate_labels=labels)
        return {
            "primary_context": result["labels"][0],
            "confidence": result["scores"][0],
            "all_contexts": list(zip(result["labels"], result["scores"]))
        }
    
    def analyse_entities(self, text: str) -> List[Dict[str, Any]]:
        """
        Extract named entities from the text.
        """
        results = self.ner_pipeline(text)
        return [{
            "entity_type": r["entity_group"],
            "word": r["word"],
            "confidence": r["score"]
        } for r in results]
    
    def get_full_analysis(self, text: str) -> Dict[str, Any]:
        """
        Run full analysis and return structured result.
        """
        return {
            "text": text,
            "sentiment": self.analyse_sentiment(text),
            "emotion": self.analyse_emotions(text),
            "context": self.analyse_context(text),
            "entities": self.analyse_entities(text),
            "timestamp": datetime.now().isoformat()
        }

    def update_user_insights(self, analysis: Dict[str, Any]):
        """
        Append emotion, context, and entities to user insights.
        """
        self.user_insights['emotional_patterns'].append({
            'emotion': analysis['emotion']['primary_emotion'],
            'confidence': analysis['emotion']['primary_confidence'],
            'context': analysis['context']['primary_context'],
            'timestamp': analysis['timestamp']
        })

        theme = analysis['context']['primary_context']
        self.user_insights['recurring_themes'][theme] = self.user_insights['recurring_themes'].get(theme, 0) + 1

        self.user_insights['entities_mentioned'].extend(analysis['entities'])

    def select_reflection_question(self, analysis: Dict[str, Any]) -> str:
        """
        Pick a question based on confidence and emotion/context.
        """
        emotion = analysis['emotion']['primary_emotion']
        context = analysis['context']['primary_context']

        if analysis['emotion']['primary_confidence'] > 0.8 and emotion in self.question_templates:
            questions = self.question_templates[emotion]
        elif analysis['context']['confidence'] > 0.6:
            questions = self.question_templates.get(context, self.question_templates.get('self_reflection', []))
        else:
            questions = self.question_templates.get('self_reflection', [])

        return random.choice(questions) if questions else ""

    def generate_personalised_response(self, analysis: Dict[str, Any]) -> str:
        """
        Return a reflective message with emotional acknowledgment and question.
        """
        emotion = analysis['emotion']['primary_emotion']
        sentiment = analysis['sentiment']['sentiment'].lower()
        entities = analysis['entities']

        acknowledgments = {
            'joy': [
                "I can hear the happiness in what you're sharing.",
                "It sounds like this brings you real joy.",
                "That seems like a genuinely uplifting experience for you.",
                "Your words have a bright, joyful tone to them."
            ],
            'love': [
                "There's such warmth in how you describe this.",
                "I can sense the deep connection you're feeling.",
                "That connection sounds meaningful and sincere.",
                "The way you talk about this shows a lot of care and affection."
            ],
            'sadness': [
                "I hear the heaviness in what you're going through.",
                "It sounds like you're carrying something difficult right now.",
                "This feels like a tender moment—thank you for sharing it.",
                "Your words hold a quiet depth—like something important is beneath them."
            ],
            'anger': [
                "I can feel the intensity of your frustration.",
                "It sounds like something really important to you has been affected.",
                "There’s a strong energy behind what you're expressing.",
                "You’re clearly standing up for something that matters."
            ],
            'fear': [
                "I hear the uncertainty you're experiencing.",
                "It sounds like you're facing something that feels overwhelming.",
                "That sounds like a situation that would make most people pause.",
                "It's clear you're being honest about what feels unsettling."
            ],
            'surprise': [
                "What an unexpected turn of events.",
                "It sounds like this really caught you off guard.",
                "That shift seems like it really came out of nowhere.",
                "You sound like you're still processing the surprise."
            ]
        }

        acknowledgment = random.choice(acknowledgments.get(emotion, ["I hear what you're sharing."]))

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
        Return a practical follow-up action idea.
        """
        emotion = analysis['emotion']['primary_emotion']
        sentiment = analysis['sentiment']['sentiment'].lower()
        action_templates = {
            'joy': [
                "Take a moment to appreciate what brought you this joy—maybe even share it with someone.",
                "Write down why this moment made you feel good, so you can revisit it later.",
                "Plan a way to relive or expand this joy in your week ahead.",
                "Celebrate it—small wins matter too."
            ],
            'love': [
                "Reach out to the person you're thinking of and let them know.",
                "Reflect on how this feeling of love impacts your daily decisions.",
                "Notice what helps you feel connected—and seek more of it.",
                "Think of a simple way to show this love through action."
            ],
            'sadness': [
                "Let yourself sit with the sadness without trying to fix it.",
                "Do something gentle: rest, walk, or write about what you're feeling.",
                "Talk to someone who listens well, even if you just need quiet company.",
                "Reflect on what this sadness is asking you to pay attention to."
            ],
            'anger': [
                "Name exactly what triggered the anger, without judgement.",
                "Write a letter you won't send—just to let it out.",
                "Move your body to release that built-up energy.",
                "Notice what your anger might be protecting or standing up for."
            ],
            'fear': [
                "Write out the fear in detail—sometimes clarity helps soften it.",
                "List one or two things you *can* do in this situation.",
                "Try grounding yourself with breath, then re-read what scared you.",
                "Ask yourself: what would you do if you trusted yourself more?"
            ],
            'surprise': [
                "Note what exactly caught you off guard and why.",
                "Think about whether this opened a new opportunity.",
                "Reflect on how you typically handle the unexpected.",
                "Share the story with someone—it might bring new perspective."
            ]
        }

        action = random.choice(action_templates.get(emotion, [
            "Reflect on what this moment is revealing about your deeper values.",
            "Note down any insights that emerged from this experience.",
            "Ask yourself: what part of me most needed this moment to happen?"
        ]))

        reference = f"You shared something that felt like it carried a sense of {emotion} and came across with a generally {sentiment} tone."
        return f"{reference} One gentle step forward might be: {action}"

    def process_user_input(self, user_input: str) -> str:
        """
        Return full response: reflection + action.
        """
        analysis = self.get_full_analysis(user_input)
        self.update_user_insights(analysis)
        self.conversation_history.append({
            'user_input': user_input,
            'analysis': analysis,
            'timestamp': datetime.now().isoformat()
        })
        reflection = self.generate_personalised_response(analysis)
        action = self.generate_action_point(analysis)
        return f"{reflection}\n\n{action}"

    
async def speak_response(self, text: str, voice: str = "en-US-JennyNeural", output_folder: str = "reflection_outputs") -> None:
    """
    Convert the response to audio using edge-tts.
    """
    os.makedirs(output_folder, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_file = os.path.join(output_folder, f"reflection_{timestamp}.mp3")
    await edge_tts.Communicate(text, voice).save(output_file)
    print(f"Audio response saved: {output_file}")


def get_conversation_insights(self) -> Dict[str, Any]:
    """
    Return summary stats and patterns.
    """
    if not self.conversation_history:
        return {"message": "No conversation data yet."}

    most_common_theme = max(
        self.user_insights['recurring_themes'].items(),
        key=lambda x: x[1]
    ) if self.user_insights['recurring_themes'] else None

    recent_emotions = [e['emotion'] for e in self.user_insights['emotional_patterns'][-5:]]
    unique_entities = len(set(e['word'] for e in self.user_insights['entities_mentioned']))

    return {
        "total_exchanges": len(self.conversation_history),
        "most_discussed_theme": most_common_theme,
        "recent_emotional_pattern": recent_emotions,
        "unique_entities_mentioned": unique_entities,
        "conversation_themes": self.user_insights['recurring_themes']
    }


async def start_reflection_session():
    """Launch a reflection session in terminal."""
    helper = ReflectionHelper()
    print("Welcome to your Reflection Assistant!")
    print("Type 'insights' for patterns, or 'quit' to end.\n")
    
    while True:
        try:
            user_input = input("\nWhat is something you'd like to reflect on today? ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye', 'cya']:
                print("\nThanks for the chat. Take care!")
                break
            
            if user_input.lower() == 'insights':
                insights = helper.get_conversation_insights()
                for k, v in insights.items():
                    print(f"  {k}: {v}")
                continue
            
            if not user_input:
                print("I'm here when you're ready.")
                continue
            
            response = helper.process_user_input(user_input)
            print(f"\n{response}")
            
        except KeyboardInterrupt:
            print("\n\nThanks for the chat. Take care!")
            break
        except Exception as e:
            print(f"Error: {e}. Let's keep going.")

if __name__ == "__main__":
    asyncio.run(start_reflection_session())
