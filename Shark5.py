import json
import os
import sys
import asyncio
REQUIRED = ["numpy"]
os.system("clear")

missing = []
for lib in REQUIRED:
    try:
        __import__(lib)
    except ImportError:
        missing.append(lib)

if missing:
    print("Missing libraries:", ", ".join(missing))
    while True:
        c = input("Install required libraries? (yes/no): ").lower()
        if c == "yes":
            os.system("sudo DEBIAN_FRONTEND=noninteractive apt-get install -y -qq python3-numpy")
            print("Done. Restart the tool.")
            sys.exit(0)
        elif c == "no":
            print("Cannot run without required libraries.")
            sys.exit(1)


import numpy as np 
responses = {
    "hi": "hi how are you",
    "how are you": "i am fine, thanks!",
    "hello": "i am fine, thanks!",
    "Hello": "i am fine, thanks!",
    "milk": "Milk is a white liquid food produced by mammals."
    
}

STOP_WORDS = ["what", "be",  "is", "the", "a", "an", "who", "tell", "me", "about", "how", "make", "does", "why", "can", "things"]

class Tokenizer:
    def __init__(self, texts):
        words = sorted(list(set(" ".join(texts).lower().split())))
        self.stoi = {w:i for i,w in enumerate(words)}
        self.itos = {i:w for i,w in enumerate(words)}

    def encode(self, text):
        return [self.stoi[w] for w in text.lower().split() if w in self.stoi]

    def decode(self, tokens):
        return " ".join([self.itos[t] for t in tokens])


class Embedding:
    def __init__(self, vocab_size, dim):
        self.vocab_size = vocab_size
        self.dim = dim
        self.weight = np.random.randn(vocab_size, dim) * 0.01

    def forward(self, tokens):
        return np.array([self.weight[t] for t in tokens])


def softmax(x):
    e = np.exp(x - np.max(x, axis=-1, keepdims=True))
    return e / e.sum(axis=-1, keepdims=True)

def attention(Q, K, V):
    scores = np.dot(Q, K.T) / np.sqrt(Q.shape[1])
    weights = softmax(scores)
    out = np.dot(weights, V)
    return out


class TransformerBlock:
    def __init__(self, dim):
        self.dim = dim
        self.Wq = np.random.randn(dim, dim)
        self.Wk = np.random.randn(dim, dim)
        self.Wv = np.random.randn(dim, dim)

    def forward(self, x):
        Q = x @ self.Wq
        K = x @ self.Wk
        V = x @ self.Wv
        return attention(Q, K, V) + x  


def smart_search(q, lang="en"):
    try:
        q_clean = q.lower().replace("?", "")
        words = q_clean.split()
        keywords = [w for w in words if w not in STOP_WORDS]
        if not keywords:
            return "no result"
        query = "_".join(keywords)

        summary_cmd = f"curl -s 'https://{lang}.wikipedia.org/api/rest_v1/page/summary/{query}'"
        summary_result = os.popen(summary_cmd).read()
        summary = json.loads(summary_result)
        return summary.get("extract", "no result")
    except:
        return "search failed"


sample_texts = list(responses.keys())
tokenizer = Tokenizer(sample_texts)
embedding = Embedding(len(tokenizer.stoi), dim=16)
layers = [TransformerBlock(dim=16) for _ in range(2)]  

async def main():
    print("stopped aborting.. ")
    await asyncio.sleep(3)
    print("Done")

while True:
    q = input("Ask: ").strip()
    if q.lower() == "exit":
        break

    key = q.lower()
    if key in responses:
        print(responses[key])
    else:
        tokens = tokenizer.encode(q.lower())
        if tokens:
            x = embedding.forward(tokens)
            for layer in layers:
                x = layer.forward(x)
         
            print(tokenizer.decode(tokens))
        else:
        
            print(smart_search(q, lang="en"))
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[!] Interrupted")
    finally:
        input("\nended Press Enter if you want return to launcher...")

