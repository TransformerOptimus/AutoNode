from fastapi import UploadFile, APIRouter, File, Request

from ocr.ocr.services.ocr_service import OcrService

router = APIRouter()


@router.post("/get_para_text")
async def read_para_text(request: Request):
    body = await request.json()
    return OcrService().get_para_text(image=body.get("image_path"))


@router.post("/get_text")
async def read_text(image: UploadFile = File(...)):
    return OcrService().get_text(await image.read())
