import spacy
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')

nlp = spacy.load('en_core_web_sm')

def remove_stopwords(tokens):
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token.text not in stop_words]
    return tokens

def lemmatize_tokens(tokens):
    lemmas = [token.lemma_ for token in tokens]
    return lemmas


def preprocess_text(text, remove_stops=True, lemmatize=True):
    try:
        doc = nlp(text)
        tokens = [token for token in doc]

        if remove_stops:
            tokens = remove_stopwords(tokens)

        if lemmatize:
            tokens = lemmatize_tokens(tokens)

        return ' '.join(tokens)
    except Exception as e:
        print(f"Error preprocessing text: {e}")
        return ""
