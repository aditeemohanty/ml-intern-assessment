# Evaluation — Trigram Language Model

This document summarizes the design and implementation decisions for the trigram (N=3) language model implemented in `ml-assignment/src/ngram_model.py`.

Storage of n-gram counts:
- The model stores trigram frequencies in a nested mapping keyed by 2-word contexts: `counts[(w1, w2)][w3] = count`.
- The implementation uses Python dictionaries for clarity and efficient expected O(1) access per context.

Text cleaning, tokenization, padding and unknown words:
- Tokenization is simple and conservative: input is lowercased and split on whitespace. This keeps behavior predictable for the assignment tests; the tokenizer can be upgraded to a regex-based one if needed.
- Each sentence/line is padded with two start tokens `<s>` and an end token `</s>` so the model learns sentence-begin and sentence-end contexts.
- Vocabulary is built from training data. Unknown words are handled via backoff during generation (bigram-like aggregated fallback and global unigram fallback). The code is structured so an explicit `<unk>` mapping or Laplace smoothing can be added.

Training (`fit`) details:
- `fit` processes the input text line-by-line, lowercases and tokenizes, pads tokens, and accumulates trigram counts by sliding window.
- After counting, per-context totals are precomputed to speed up sampling.

Generation and probabilistic sampling (`generate`):
- Generation starts from the context `(<s>, <s>)` and samples the next token conditioned on the current two-word context.
- The implementation converts counts to a weighted distribution and samples by drawing a uniform random number and walking cumulative weights. For improved performance the optimized path uses `random.choices(population, weights=...)` or precomputed cumulative arrays.
- If a trigram context has no continuations, the generator backs off to an aggregated distribution of continuations sharing the last word (bigram backoff). If that fails, a global most-frequent unigram is used as fallback. This prevents generation from halting on unseen contexts.

Optimizations & tradeoffs:
- Precomputing candidate lists and cumulative weights per context reduces runtime overhead at generation time.
- Mapping tokens to integer ids and using `random.choices` or `bisect` on cumulative arrays are straightforward next steps for further speedups. For very high-throughput generation, building alias tables per context (Vose's algorithm) yields O(1) sampling at the cost of additional memory and build-time complexity.
- Smoothing (add-k / Laplace) is intentionally omitted by default to keep generated text closer to empirical counts used in tests; it can be enabled if a smoother distribution is desired.

Testing & usage notes:
- Tests are in `ml-assignment/tests/test_ngram.py`. Run them from the repository root with:
```
pytest ml-assignment/tests/test_ngram.py -q
```
- For reproducible generation set a random seed before calling `generate`, e.g. `random.seed(42)`.

Limitations:
- Tokenization is whitespace-based; for production use adopt a robust tokenizer and normalize punctuation.
- Backoff is heuristic; more principled smoothing (e.g., Kneser-Ney) would improve perplexity 

Overall, the implementation prioritizes clarity and correctness while leaving clear extension points for performance and smoothing improvements.

