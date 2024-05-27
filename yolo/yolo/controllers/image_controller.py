from fastapi import APIRouter, UploadFile, File

from yolo.yolo.services.yolo_service import YoloService

router = APIRouter()


@router.post("/detect")
async def detect_object(image: UploadFile = File(...)):
    result = YoloService().detect(await image.read())
    return {"result": result, "success": True}
