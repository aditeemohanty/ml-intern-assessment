import random

class TrigramModel:
    def __init__(self):
        """
        Initializes the TrigramModel.
        """
        self.counts = {}
        self.vocab = set()
        self.START = "<s>"
        self.END = "</s>"
        self.UNK = "<unk>"
        self.context_totals = {}

    def fit(self, text):
        if not isinstance(text, str):
            raise ValueError("text must be a string")
        lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
        if not lines:
            lines = [text.strip()]

        for line in lines:
            tokens = line.lower().split()
            if not tokens:
                continue
            for t in tokens:
                self.vocab.add(t)
            padded = [self.START, self.START] + tokens + [self.END]
            for i in range(len(padded) - 2):
                w1, w2, w3 = padded[i], padded[i+1], padded[i+2]
                ctx = (w1, w2)
                self.counts.setdefault(ctx, {})
                self.counts[ctx][w3] = self.counts[ctx].get(w3, 0) + 1

        self.context_totals = {ctx: sum(targets.values()) for ctx, targets in self.counts.items()}

    def generate(self, max_length=50):
        if not self.counts:
            return ""

        generated = []
        w1, w2 = self.START, self.START

        for _ in range(max_length):
            ctx = (w1, w2)
            choices = self.counts.get(ctx)
            if not choices:
                agg = {}
                for (a, b), targets in self.counts.items():
                    if b == w2:
                        for t, c in targets.items():
                            agg[t] = agg.get(t, 0) + c
                if agg:
                    choices = agg
                else:
                    top = None
                    top_count = 0
                    for targets in self.counts.values():
                        for t, c in targets.items():
                            if c > top_count:
                                top_count = c
                                top = t
                    next_word = top or self.END
                    if next_word == self.END:
                        break
                    generated.append(next_word)
                    w1, w2 = w2, next_word
                    continue

            words = list(choices.keys())
            counts = [choices[w] for w in words]
            total = sum(counts)
            r = random.random() * total
            cum = 0.0
            next_word = words[-1]
            for w, c in zip(words, counts):
                cum += c
                if r <= cum:
                    next_word = w
                    break

            if next_word == self.END:
                break
            generated.append(next_word)
            w1, w2 = w2, next_word

        return " ".join(generated)
