def update_user_insights(user_insights, analysis):
    """
    Update user insights dictionary with data from the latest input analysis.

    Params:
        :user_insights: A dictionary tracking emotional patterns, entities, and themes.
        :analysis: NLP output containing emotion, context, and entity details.
    Returns:
        :None: Modifies user_insights in-place.
    """
    # Log emotion, confidence, and context over time
    user_insights['emotional_patterns'].append({
        'emotion': analysis['emotion']['primary_emotion'],
        'confidence': analysis['emotion']['primary_confidence'],
        'context': analysis['context']['primary_context'],
        'timestamp': analysis['timestamp']
    })

    # Increment theme frequency
    theme = analysis['context']['primary_context']
    user_insights['recurring_themes'][theme] = user_insights['recurring_themes'].get(theme, 0) + 1

    # Track all named entities mentioned
    user_insights['entities_mentioned'].extend(analysis['entities'])


def get_conversation_insights(user_insights, conversation_history):
    """
    Generate a summary of key insights from the conversation session.

    Params:
        :user_insights: Accumulated insights from all previous exchanges.
        :conversation_history: List of user inputs and analysis history.
    Returns:
        :Dict: Summary with total exchanges, themes, emotions, and entity stats.
    """
    if not conversation_history:
        return {"message": "No conversation data yet."}

    # Get the most frequent topic if one exists
    most_common_theme = max(
        user_insights['recurring_themes'].items(),
        key=lambda x: x[1]
    ) if user_insights['recurring_themes'] else None

    # Show last 5 emotional tones
    recent_emotions = [e['emotion'] for e in user_insights['emotional_patterns'][-5:]]

    # Count unique entities across the conversation
    unique_entities = len(set(e['word'] for e in user_insights['entities_mentioned']))

    return {
        "total_exchanges": len(conversation_history),
        "most_discussed_theme": most_common_theme,
        "recent_emotional_pattern": recent_emotions,
        "unique_entities_mentioned": unique_entities,
        "conversation_themes": user_insights['recurring_themes']
    }