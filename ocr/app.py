import newrelic.agent
from fastapi import FastAPI

from ocr.ocr.controllers.image_controller import router as image_router
from ocr.ocr.configs.settings import OcrConfig

app = FastAPI()

# Initialize New Relic
if OcrConfig.environment == "PROD":
    newrelic.agent.initialize('newrelic.ini')
    newrelic.agent.register_application()


@app.get("/api/health")
def health_check():
    return {"status": "ok"}


app.include_router(image_router, prefix="/api/ocr/image")
