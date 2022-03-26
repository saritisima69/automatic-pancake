from fastapi import FastAPI, File, UploadFile
from werkzeug.utils import secure_filename
from PIL import Image
from os import getcwd
import pytesseract
import shutil


app = FastAPI()

PATH_FILES = getcwd() + "/"

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/images")
async def UploadImage(fichero: UploadFile = File(...)):
    NO_VALID_IMAGE = "No se ha proporcionado una imagen valida..."

    with open(PATH_FILES + fichero.filename, "wb") as myfile:
        content = await fichero.read()
        myfile.write(content)
        myfile.close()

    img = Image.open(PATH_FILES + fichero.filename)

    try:
        text = pytesseract.image_to_string(img, lang='spa')
    except Exception as e:
        text = NO_VALID_IMAGE        



    return {"info": text}