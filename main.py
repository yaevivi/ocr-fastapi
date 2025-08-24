from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import easyocr
import uvicorn
import os
import shutil
from typing import List

app = FastAPI(title="EasyOCR API", description="OCR service using EasyOCR", version="1.0")

# Crear el lector con soporte multilenguaje y GPU si está disponible
reader = easyocr.Reader(['en', 'es'], gpu=True)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.post("/ocr/")
async def perform_ocr(file: UploadFile = File(...)):
    try:
        # Guardar el archivo temporalmente
        file_location = os.path.join(UPLOAD_FOLDER, file.filename)
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Ejecutar OCR
        results = reader.readtext(file_location, detail=1, paragraph=True)

        # Eliminar el archivo una vez procesado
        os.remove(file_location)

        return JSONResponse(content={"results": results})

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def root():
    return {"message": "EasyOCR API is running"}

# Para ejecución local:
# if __name__ == "__main__":
#     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
