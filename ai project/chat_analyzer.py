import re
from collections import Counter
import emoji

def extract_emojis(text):
    return [char for char in text if char in emoji.EMOJI_DATA]

def clean_chat(filepath):
    with open(filepath, encoding="utf-8") as f:
        lines = f.readlines()

    messages = []
    for line in lines:
        if "-" in line and ":" in line:
            parts = line.split(":", 1)
            if len(parts) > 1:
                user_msg = parts[1].strip()
                messages.append(user_msg)
    return messages

def analyze_chat(filepath):
    messages = clean_chat(filepath)
    all_text = " ".join(messages)

    word_list = re.findall(r'\b\w+\b', all_text.lower())
    emoji_list = extract_emojis(all_text)

    word_freq = Counter(word_list).most_common(10)
    emoji_freq = Counter(emoji_list).most_common(5)

    return {
        "total_messages": len(messages),
        "total_words": len(word_list),
        "top_words": word_freq,
        "top_emojis": emoji_freq,
    }
