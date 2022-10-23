from spacy.tokens import Token


def get_token_data(token: Token) -> dict:
    return {
        "text": token.text,
        "start": token.idx,
        "end": token.idx + len(token.text),
        "lemma": token.lemma_,
        "tag": token.tag_,
        "dep": token.dep_,
        "alpha": token.is_alpha,
        "digit": token.is_digit,
        "lower": token.is_lower,
        "upper": token.is_upper,
        "title": token.is_title,
        "stop": token.is_stop,
        "space": token.is_space,
        "ascii": token.is_ascii,
        "quote": token.is_quote,
        "currency": token.is_currency
    }
