from pydantic.dataclasses import dataclass


@dataclass
class Text:
    text: str


@dataclass
class OffsetTextResponseModel:
    text: str
    start: int
    end: int


@dataclass
class LabeledOffsetTextResponseModel(OffsetTextResponseModel):
    label: str


@dataclass
class TokenResponseModel(OffsetTextResponseModel):
    lemma: str
    pos: str
    tag: str
    dep: str
    alpha: bool
    stop: bool
