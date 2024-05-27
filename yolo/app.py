import newrelic.agent
from fastapi import FastAPI

from yolo.yolo.configs.settings import YoloConfig
from yolo.yolo.controllers.image_controller import router as image_router

app = FastAPI()

# Initialize New Relic
if YoloConfig.environment == "PROD":
    newrelic.agent.initialize('newrelic.ini')
    newrelic.agent.register_application()


@app.get("/api/health")
def health_check():
    return {"status": "ok"}


app.include_router(image_router, prefix="/api/yolo/image")
