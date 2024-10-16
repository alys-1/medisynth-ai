from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import HTMLResponse, JSONResponse
from pathlib import Path
import os
from model.model import analyze_image

app = FastAPI()

# Path where images will be uploaded
UPLOAD_DIR = Path("uploads")

if not UPLOAD_DIR.exists():
    os.makedirs(UPLOAD_DIR)

@app.get("/")
def read_root():
    # Serve a simple HTML form for uploading images and text input
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>X-ray Upload</title>
    </head>
    <body>
        <h1>Upload an X-ray Image</h1>
        <form action="/upload/" method="post" enctype="multipart/form-data">
            <label for="file">Choose X-ray image (Thorax):</label>
            <input type="file" name="file" accept="image/*" required>
            <br><br>
            <label for="condition">Enter any medical conditions (optional):</label>
            <input type="text" name="condition" placeholder="E.g., cough, fever, shortness of breath">
            <br><br>
            <button type="submit">Upload</button>
        </form>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


@app.post("/upload/")
async def upload_image(file: UploadFile = File(...), condition: str = Form(...)):
    # Save uploaded file to disk
    file_path = UPLOAD_DIR / file.filename
    with open(file_path, "wb") as f:
        f.write(file.file.read())
    
    # Analyze the image
    try:
        result = analyze_image(file_path, condition)
        return JSONResponse(content=result)
    except Exception as e:
        return {"error": str(e)}


# Static files handling (for CSS, images, etc.)
@app.get("/static/{file_name}")
def static_file(file_name: str):
    static_path = Path("static")
    file_path = static_path / file_name
    if file_path.exists():
        return FileResponse(file_path)
    return {"error": "File not found"}
