import nltk
import string
from collections import defaultdict
from nltk.tokenize import sent_tokenize, word_tokenize

nltk.download("punkt")

def summarize_text(text, max_sentences=5):
    if not text or len(text.strip()) == 0:
        return ""

    sentences = sent_tokenize(text)
    words = word_tokenize(text.lower())

    words = [
        word for word in words
        if word.isalnum() and word not in string.punctuation
    ]

    word_freq = defaultdict(int)
    for word in words:
        word_freq[word] += 1

    max_freq = max(word_freq.values(), default=1)
    for word in word_freq:
        word_freq[word] /= max_freq

    sentence_scores = defaultdict(float)
    for sentence in sentences:
        for word in word_tokenize(sentence.lower()):
            if word in word_freq:
                sentence_scores[sentence] += word_freq[word]

    ranked_sentences = sorted(
        sentence_scores,
        key=sentence_scores.get,
        reverse=True
    )

    return " ".join(ranked_sentences[:max_sentences])
