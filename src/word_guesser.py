from gensim.models import KeyedVectors
import gensim.downloader as api
import numpy as np


class WordGuesser:
    def __init__(self, valid_words: set[str]) -> None:
        self.model: KeyedVectors = api.load("word2vec-google-news-300") # type: ignore
        self.valid_words = valid_words

    def guess_next_word(self, word_list: list[str], ignore: list[str]) -> tuple[str | None, float]:
        words_to_exclude = set(word_list).union(ignore)

        embeddings = [self.model[w] for w in word_list if w in self.model]
        if not embeddings:
            return None, 0.0

        cluster_center = np.mean(embeddings, axis=0)
        similar_words: list[tuple[str, float]] = self.model.most_similar(positive=[cluster_center], topn=150)

        for word, score in similar_words:
            if word[0].isupper():
                continue

            if word in words_to_exclude:
                continue

            if "_" in word or not word.isalpha(): #filter out compound words
                continue

            if word not in self.valid_words:
                continue

            if score < 0.6 and len(word_list) > 1:
                new_word_list = word_list[:-1]
                return self.guess_next_word(new_word_list, ignore)
            else:
                return word, score

        return None, 0.0
