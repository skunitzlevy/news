from functools import lru_cache

from transformers import pipeline

MODEL_NAME = "cardiffnlp/twitter-roberta-base-sentiment-latest"


@lru_cache(maxsize=1)
def get_sentiment_model():
    """Load the model once and reuse it for subsequent headlines."""
    return pipeline(
        "text-classification",
        model=MODEL_NAME,
        top_k=None,
    )


def classify_headline(headline):
    """Return all sentiment labels and scores for one headline."""
    return get_sentiment_model()(headline)[0]


def print_headline_sentiment(headline, results=None):
    if results is None:
        results = classify_headline(headline)

    print(headline)

    for result in results:
        print(f"  {result['label']:8} {result['score']:.3f}")

    print()


def main():
    headlines = [
        "Robust Hiring Reinforces Strength of the U.S. Economy",
        "I Wasn’t Too Worried About the Hugging Face A.I. Hack. Then I Learned the Details.",
        "Quiet on the Court! As U.S. Open Grows, the Crowd Gets Rowdier.",
    ]

    for headline in headlines:
        print_headline_sentiment(headline)


if __name__ == "__main__":
    main()
