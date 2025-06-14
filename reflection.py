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
        Load all NLP pipelines for sentiment, emotion, context, and entity analysis.
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
        Define reflection question templates based on emotion and context.
        """
        self.question_templates = {
            # emotion and context mappings...
        }

        self.deepening_questions = [
            # follow-up prompts...
        ]
    
    def analyse_sentiment(self, text: str) -> Dict[str, Any]:
        """
        Analyse the sentiment of the input text.
        
        Params:
            :text: The text to analyse.
        
        Returns:
            A dictionary with sentiment label and confidence score.
        """
        result = self.sentiment_pipeline(text)[0]
        return {
            "sentiment": result["label"],
            "confidence": result["score"]
        }
    
    def analyse_emotions(self, text: str) -> Dict[str, Any]:
        """
        Analyse the emotions expressed in the input text.
        
        Params:
            :text: The text to analyse.
        
        Returns:
            A dictionary containing the primary emotion, confidence score, and all emotion predictions.
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
        top_emotion = max(emotions, key=lambda x: x["score"])
        return {
            "primary_emotion": label_map.get(top_emotion["label"], top_emotion["label"]),
            "primary_confidence": top_emotion["score"],
            "all_emotions": [(label_map.get(e["label"], e["label"]), e["score"]) for e in emotions]
        }
    
    def analyse_context(self, text: str) -> Dict[str, Any]:
        """
        Analyse the context or theme of the user's message.
        
        Params:
            :text: The text to analyse.
        
        Returns:
            A dictionary with the top context label, its score, and all label-score pairs.
        """
        context_labels = [
            "relationships", "work stress", "self-reflection", "family", 
            "health", "change transition", "daily life", "personal growth",
            "anxiety", "depression", "motivation", "goals", "past experiences"
        ]
        result = self.zero_shot_pipeline(text, candidate_labels=context_labels)
        return {
            "primary_context": result["labels"][0],
            "confidence": result["scores"][0],
            "all_contexts": list(zip(result["labels"], result["scores"]))
        }
    
    def analyse_entities(self, text: str) -> List[Dict[str, Any]]:
        """
        Extract named entities from the user's message.
        
        Params:
            :text: The text to analyse.
        
        Returns:
            A list of entity dictionaries with type, word, and confidence score.
        """
        results = self.ner_pipeline(text)
        cleaned_entities = []
        for item in results:
            entity_info = {
                "entity_type": item["entity_group"],
                "word": item["word"],
                "confidence": item["score"]
            }
            cleaned_entities.append(entity_info)
        return cleaned_entities
    
    def get_full_analysis(self, text: str) -> Dict[str, Any]:
        """
        Perform full NLP analysis on the input text.
        
        Params:
            :text: The user's message.
        
        Returns:
            A combined dictionary of sentiment, emotion, context, and entities with timestamp.
        """
        return {
            "text": text,
            "sentiment": self.analyse_sentiment(text),
            "emotion": self.analyse_emotions(text),
            "context": self.analyse_context(text),
            "entities": self.analyse_entities(text),
            "timestamp": datetime.now().isoformat()
        }