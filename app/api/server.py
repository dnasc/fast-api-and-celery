from typing import List, Dict

from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

from app.api.model.base import (
    LabeledOffsetTextResponseModel as NERResponseModel,
)
from app.api.celery_worker import app as app_celery
from app.api.routes import TextRouteMaker


app = FastAPI()
make_text_route = TextRouteMaker(app, app_celery)


@app.get("/")
async def root():
    return PlainTextResponse("Olá!")


@app.get(
    "/healthcheck", summary="Healthcheck", description="Application healthcheck route."
)
def healthcheck():
    return ""


make_text_route(
    "ner",
    run_config={
        "summary": "Named Entity Recognition",
        "description": "Runs named entity recognition.",
    },
    result_config={"response_model": List[NERResponseModel]},
)

make_text_route(
    "token",
    run_config={"summary": "Tokenization", "description": "Runs tokenization."},
    result_config={"response_model": List[Dict]},
    enable_sum_up=True,
)
