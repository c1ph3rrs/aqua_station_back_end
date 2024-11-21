from fastapi import FastAPI, File, Form, UploadFile, HTTPException
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from db_connection import report_collection
import boto3
import uuid


router = APIRouter()


s3_client = boto3.client('s3')
S3_BUCKET = "your_s3_bucket_name"

@router.post("/problem")
async def upload_data(images: list[UploadFile] = File(...), text: str = Form(...)):
    if not images or not text:
        raise HTTPException(status_code=400, detail="Images and text are required")

    image_urls = []
    for image in images:
        image_filename = f"{uuid.uuid4()}.jpg"
        s3_client.upload_fileobj(image.file, S3_BUCKET, image_filename)
        image_url = f"https://{S3_BUCKET}.s3.amazonaws.com/{image_filename}"
        image_urls.append(image_url)

    document = {
        "text": text,
        "images": image_urls
    }
    report_collection.insert_one(document)

    return JSONResponse(content={"message": "Your request received"}, status_code=200)