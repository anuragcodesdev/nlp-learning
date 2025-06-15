def load_question_templates():
    """
    Utilised to obtain different types of responses to specific emotions, and setiments.
    Provides acknowledgements and actions for reflections to be utilised as a templte.
    """
    return {
        'joy': [
            "What part of this experience meant the most to you?",
            "How did this joy impact the rest of your day?",
            "What can you do to create more moments like this?"
        ],
        'love': [
            "What makes this connection meaningful to you?",
            "How do you express love when words aren't enough?",
            "What have you learned about yourself through this bond?"
        ],
        'sadness': [
            "What is this sadness pointing to underneath?",
            "Is there something you're grieving or letting go of?",
            "What might this sadness be trying to teach you?"
        ],
        'anger': [
            "What value do you feel was violated here?",
            "What would justice look like to you in this moment?",
            "Where is this anger rooted—in fear, hurt, or something else?"
        ],
        'fear': [
            "What might help you feel a little safer right now?",
            "Is this fear tied to past experience or imagined future?",
            "What small step could build your confidence here?"
        ],
        'surprise': [
            "What made this so unexpected for you?",
            "Did this surprise bring anything new into perspective?",
            "How are you feeling now that the initial shock has passed?"
        ],
        'self_reflection': [
            "What does this tell you about who you’re becoming?",
            "What deeper pattern are you noticing in yourself?",
            "How has your perspective changed over time?"
        ],
        'acknowledgments': {
            'joy': [
                "I can hear the happiness in what you're sharing.",
                "It sounds like this brings you real joy.",
                "Your words have a bright, joyful tone to them.",
                "That seems like a genuinely uplifting experience for you."
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
        },
        'actions': {
            'joy': [
                "Write down why this made you feel good.",
                "Take a moment to appreciate what brought you this joy—maybe even share it with someone.",
                "Plan a way to relive or expand this joy in your week ahead.",
                "Celebrate it—small wins matter too."
            ],
            'love': [
                "Reach out to the person and let them know.",
                "Reflect on how this feeling of love impacts your daily decisions.",
                "Notice what helps you feel connected—and seek more of it.",
                "Think of a simple way to show this love through action."
            ],
            'sadness': [
                "Do something gentle: rest, walk, or write.",
                "Let yourself sit with the sadness without trying to fix it.",
                "Talk to someone who listens well, even if you just need quiet company.",
                "Reflect on what this sadness is asking you to pay attention to."
            ],
            'anger': [
                "Write a letter you won't send.",
                "Name exactly what triggered the anger, without judgement.",
                "Move your body to release that built-up energy.",
                "Notice what your anger might be protecting or standing up for."
            ],
            'fear': [
                "List what you *can* control in this situation.",
                "Write out the fear in detail—sometimes clarity helps soften it.",
                "Try grounding yourself with breath, then re-read what scared you.",
                "Ask yourself: what would you do if you trusted yourself more?"
            ],
            'surprise': [
                "Reflect on how you typically handle the unexpected.",
                "Note what exactly caught you off guard and why.",
                "Think about whether this opened a new opportunity.",
                "Share the story with someone—it might bring new perspective."
            ]
        }
    }