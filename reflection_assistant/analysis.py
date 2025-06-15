from transformers import pipeline

# Pipelines to extract sentiment, emotion, contextual themes, and named entities
sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert/distilbert-base-uncased-finetuned-sst-2-english")
emotion_pipeline = pipeline("text-classification", model="hamzawaheed/emotion-classification-model")
zero_shot_pipeline = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
ner_pipeline = pipeline("ner", model="dslim/distilbert-NER", aggregation_strategy="simple")

# Maps emotion model labels to readable emotions
LABEL_MAP = {
    "LABEL_0": "sadness",
    "LABEL_1": "joy",
    "LABEL_2": "love",
    "LABEL_3": "anger",
    "LABEL_4": "fear",
    "LABEL_5": "surprise"
}

# Candidate topics for context classification
CANDIDATE_LABELS = [
    "relationships", "work stress", "self-reflection", "family",
    "health", "change transition", "daily life", "personal growth",
    "anxiety", "depression", "motivation", "goals", "past experiences"
]

def analyse_sentiment(text):
    """
    Analyse sentiment of input text using sentiment analysis pipeline.

    Params:
        :text: User input string.
    Returns:
        :dict: Sentiment label and confidence score.
    """
    result = sentiment_pipeline(text)[0]
    return {"sentiment": result["label"], "confidence": result["score"]}

def analyse_emotions(text):
    """
    Analyse emotional tone of input text using emotion classification model.

    Params:
        :text: User input string.
    Returns:
        :dict: Primary emotion, confidence, and list of all detected emotions.
    """
    emotions = emotion_pipeline(text)
    top = max(emotions, key=lambda x: x["score"])
    return {
        "primary_emotion": LABEL_MAP.get(top["label"], top["label"]),
        "primary_confidence": top["score"],
        "all_emotions": [(LABEL_MAP.get(e["label"], e["label"]), e["score"]) for e in emotions]
    }

def analyse_context(text):
    """
    Determine likely context or topic using zero-shot classification.

    Params:
        :text: User input string.
    Returns:
        :dict: Primary context label, confidence, and all label scores.
    """
    result = zero_shot_pipeline(text, candidate_labels=CANDIDATE_LABELS)
    return {
        "primary_context": result["labels"][0],
        "confidence": result["scores"][0],
        "all_contexts": list(zip(result["labels"], result["scores"]))
    }

def analyse_entities(text):
    """
    Extract named entities from input using NER pipeline.

    Params:
        :text: User input string.
    Returns:
        :list: Extracted entities with type, word, and confidence.
    """
    results = ner_pipeline(text)
    return [{"entity_type": r["entity_group"], "word": r["word"], "confidence": r["score"]} for r in results]
