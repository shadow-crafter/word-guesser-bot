from gensim.models import KeyedVectors
import gensim.downloader as api
import numpy as np


def guess_next_word(model: KeyedVectors,word_list: list[str], ignore_list: list[str]) -> tuple[str | None, float]:
    words_to_exclude = set(word_list).union(ignore_list)

    embeddings = [model[w] for w in word_list if w in model]
    if not embeddings:
        return None, 0.0

    cluster_center = np.mean(embeddings, axis=0)
    similar_words: list[tuple[str, float]] = model.most_similar(positive=[cluster_center], topn=10)

    for word, score in similar_words:
        if word not in words_to_exclude:
            return word, score

    return None, 0.0

model: KeyedVectors = api.load("word2vec-google-news-300") # type: ignore

target = "teacher"
guess = ""
guesses = ["apple", "school", "person"]
while guess != target:
    guess, confidence = guess_next_word(model, guesses, [])
    if guess:
        guesses.append(guess)
        print(f"Guessed word: {guess} (confidence: {confidence:.2f})")
