# # locallead/LocalLead Automator/api.py
# from fastapi import FastAPI, BackgroundTasks
# from pydantic import BaseModel
# from main import run_pipeline
# from fastapi.middleware.cors import CORSMiddleware
# import threading
#
# app = FastAPI()
#
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=[
#         "http://localhost:5173",
#         "http://127.0.0.1:5173",
#     ],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
#
# # Global state (local use only)
# pipeline_status = {
#     "state": "IDLE",
#     "message": "",
#     "stats": None,
# }
#
#
# class RunRequest(BaseModel):
#     businessType: str
#     location: str
#     maxResults: int
#
# def pipeline_task(data: RunRequest):
#     try:
#         def progress_cb(status):
#             pipeline_status["state"] = status
#
#         pipeline_status["state"] = "RUNNING"
#         pipeline_status["stats"] = None
#         pipeline_status["message"] = ""
#
#         stats = run_pipeline(
#             query=data.businessType,
#             location=data.location,
#             max_results=data.maxResults,
#             progress_cb=progress_cb,
#         )
#
#         pipeline_status["state"] = "DONE"
#         pipeline_status["stats"] = stats
#
#     except Exception as e:
#         pipeline_status["state"] = "ERROR"
#         pipeline_status["message"] = str(e)
#
#
#
#
# @app.post("/run")
# def run_pipeline_api(data: RunRequest, background_tasks: BackgroundTasks):
#     if pipeline_status["state"] == "RUNNING":
#         return {"error": "Pipeline already running"}
#
#     background_tasks.add_task(pipeline_task, data)
#     return {"status": "started"}
#
#
# @app.get("/status")
# def get_status():
#     return pipeline_status
#
#
# @app.get("/health")
# def health_check():
#     return {"status": "ok"}
#
#
#

# locallead/LocalLead Automator/api.py
from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
from main import run_pipeline
from fastapi.middleware.cors import CORSMiddleware
import time

PIPELINE_TIMEOUT_SECONDS = 300  # 5 minutes



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global state (local use only)
pipeline_status = {
    "state": "IDLE",
    "message": "",
    "stats": None,
    "started_at": None,
}


class RunRequest(BaseModel):
    businessType: str
    location: str
    maxResults: int

def pipeline_task(data: RunRequest):
    try:
        def progress_cb(status):
            pipeline_status["state"] = status

        pipeline_status["state"] = "STARTING"
        pipeline_status["stats"] = None
        pipeline_status["message"] = ""
        pipeline_status["started_at"] = time.time()

        stats = run_pipeline(
            query=data.businessType,
            location=data.location,
            max_results=data.maxResults,
            progress_cb=progress_cb,
        )

        pipeline_status["state"] = "DONE"
        pipeline_status["stats"] = stats

    except Exception as e:
        pipeline_status["state"] = "ERROR"
        pipeline_status["message"] = str(e)



@app.post("/run")
def run_pipeline_api(data: RunRequest, background_tasks: BackgroundTasks):
    if pipeline_status["state"] == "RUNNING":
        return {"error": "Pipeline already running"}

    background_tasks.add_task(pipeline_task, data)
    return {"status": "started"}


@app.get("/status")
def get_status():
    if pipeline_status["state"] in {
        "STARTING",
        "RUNNING",
        "SCRAPING",
        "FILTERING",
        "ENRICHING",
        "GENERATING",
    }:
        started = pipeline_status.get("started_at")
        if started and time.time() - started > PIPELINE_TIMEOUT_SECONDS:
            pipeline_status["state"] = "ERROR"
            pipeline_status["message"] = (
                "Lead generation timed out. This may be caused by slow internet, "
                "browser automation being blocked, or Google Maps not responding."
            )

    return pipeline_status



@app.get("/health")
def health_check():
    return {"status": "ok"}




