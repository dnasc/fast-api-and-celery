from celery import Celery
from celery.result import AsyncResult
from fastapi import FastAPI

from app.api.model.base import Text


class TextRouteMaker:
    def __init__(self, app_fastapi: FastAPI, app_celery: Celery):
        self._app_fastapi = app_fastapi
        self._app_celery = app_celery

    def __call__(
        self, task_name: str, *, run_config: dict = None, result_config: dict = None, enable_sum_up: bool = False
    ):
        if not enable_sum_up:
            self.make_run_route(task_name, run_config or {})
        else:
            self.make_run_sum_up_route(task_name, run_config or {})

        self.make_result_route(task_name, result_config or {})

    def make_run_route(self, task_name: str, config: dict):

        @self._app_fastapi.post(f"/run/{task_name}", **config)
        async def run(body: Text):
            task = self._app_celery.send_task(task_name, kwargs={"text": body.text})
            return task.id
        return run

    def make_run_sum_up_route(self, task_name: str, config: dict):
        @self._app_fastapi.post(f"/run/{task_name}", **config)
        async def run(body: Text, sum_up: bool = False):
            task = self._app_celery.send_task(task_name, kwargs={"text": body.text, "sum_up": sum_up})
            return task.id

        return run

    def make_result_route(self, task_name: str, config: dict):

        @self._app_fastapi.get(f"/run/{task_name}/{{task_id}}", **config)
        async def result(task_id: str):
            task = AsyncResult(task_id, app=self._app_celery)
            return task.result

        return result
