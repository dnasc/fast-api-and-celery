from functools import wraps

import spacy
from cachetools import cached, LFUCache


nlp = spacy.load("pt_core_news_sm")


@cached(LFUCache(maxsize=1024))
@wraps(nlp)
def cached_nlp(text: str):
    return nlp(text)
