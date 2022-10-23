import os

from celery import Celery

from app.nlp.model import cached_nlp as nlp
from app.nlp.token import get_token_data


app = Celery(os.environ["CELERY_MAIN"])
app.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
app.conf.result_backend = os.environ.get(
    "CELERY_RESULT_BACKEND", "redis://localhost:6379"
)


@app.task(name="ner")
def ner(text: str):
    doc = nlp(text)
    result = [
        {"text": ent.text, "start": ent.start, "end": ent.end, "label": ent.label_}
        for ent in doc.ents
    ]

    return result


@app.task(name="token")
def token(text: str, sum_up: bool):
    keep_when_sum_up = "text", "start", "end"

    doc = nlp(text)
    result = [get_token_data(t) for t in doc]

    if sum_up:
        result = [{k: v for k, v in t.items() if k in keep_when_sum_up} for t in result]

    return result
