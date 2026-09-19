from sentence_transformers import SentenceTransformer, util

VOCAB = []

with open("vocab_list.txt", "r") as f:
    for l in f:
        VOCAB.append(l.strip().lower())

print(VOCAB[:10])

def find_similar_word(word_list: list[str]):
    excluded = set(word_list)

    model = SentenceTransformer('all-MiniLM-L6-v2')
    hint_embeddings = model.encode(word_list, convert_to_tensor=True)

    cluster_center = hint_embeddings.mean(dim=0)

    vocab_to_search = [w for w in VOCAB if w not in excluded]
    vocab_embeddings = model.encode(vocab_to_search, convert_to_tensor=True)

    sim = util.pytorch_cos_sim(cluster_center, vocab_embeddings)[0]
    best_idx = sim.argmax()

    return vocab_to_search[best_idx]

words = ["school", "student", "apple", "playground"]
guess = find_similar_word(words)
print(f"Guessed word: {guess}")
