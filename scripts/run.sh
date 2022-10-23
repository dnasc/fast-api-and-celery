#!/bin/bash

uvicorn app.api.server:app --host 0.0.0.0 --port 80 --reload
