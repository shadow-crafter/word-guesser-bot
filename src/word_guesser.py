from gensim.models import KeyedVectors
import gensim.downloader as api
import numpy as np


class WordGuesser:
    def __init__(self) -> None:
        self.model: KeyedVectors = api.load("word2vec-google-news-300") # type: ignore
        self.already_guessed = []

    def guess_next_word(self, word_list: list[str]) -> tuple[str | None, float]:
        words_to_exclude = set(word_list).union(self.already_guessed)

        embeddings = [self.model[w] for w in word_list if w in self.model]
        if not embeddings:
            return None, 0.0

        cluster_center = np.mean(embeddings, axis=0)
        similar_words: list[tuple[str, float]] = self.model.most_similar(positive=[cluster_center], topn=10)

        for word, score in similar_words:
            if word not in words_to_exclude:
                return word, score

        return None, 0.0
