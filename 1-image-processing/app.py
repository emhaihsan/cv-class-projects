import base64 # to handle base64 image
import io # handle input and output

import cv2 # computer vision library
import numpy as np
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware  # Tambahkan impor ini

from PIL import Image, ImageOps # image processing library
import uvicorn


app = FastAPI() # initialize fast api# convert PIL image to base64

# Tambahkan konfigurasi CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Izinkan semua asal, Anda bisa membatasi ini ke domain tertentu
    allow_credentials=True,
    allow_methods=["*"],  # Izinkan semua metode HTTP
    allow_headers=["*"],  # Izinkan semua header
)

# Helper funtion to convert PIL image to base64
def pil_image_to_base64(image: Image.Image):
    """
    Helper function to convert PIL image to base64 string
    
    Parameters:
    image (Image.Image): PIL image to be converted
    
    Returns:
    str: base64 string of the PIL image
    """
    buffered = io.BytesIO() # to handle input and output
    image.save(buffered, format="JPEG") # convert PIL image to base64
    return base64.b64encode(buffered.getvalue()).decode("utf-8") # convert base64 to string

# Helper function to convert OpenCV image to base64
def cv2_image_to_base64(image):
    """
    Helper function to convert OpenCV image to base64 string
    
    Parameters:
    image (OpenCV image): OpenCV image to be converted
    
    Returns:
    str: base64 string of the OpenCV image
    """
    _, buffer = cv2.imencode(".jpg", image) # convert OpenCV image to base64
    return base64.b64encode(buffer).decode("utf-8") # convert base64 to string

def open_image(image_bytes):
    """
    Helper function to convert image bytes to OpenCV image
    
    Parameters:
    image_bytes (bytes): image bytes to be converted
    
    Returns:
    OpenCV image: OpenCV image from the given image bytes
    """
    image = Image.open(io.BytesIO(image_bytes)) # convert bytes to PIL image
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR) # convert PIL image to OpenCV image
    return image # return OpenCV image

# 1. Image cropping
@app.post("/crop")
async def crop_image(
    image_file: UploadFile = File(),
    x: int = 0,
    y: int = 0,
    width: int = 100,
    height: int = 100,
):
    """
    Crop the given image file with the given parameters
    
    Parameters:
    image_file (UploadFile): image file to be cropped
    x (int): left coordinate of the cropping area
    y (int): top coordinate of the cropping area
    width (int): width of the cropping area
    height (int): height of the cropping area
    
    Returns:
    dict: dictionary containing the cropped image as base64 string
    """
    x1 = x # left
    y1 = y # top
    x2 = x + width # right
    y2 = y + height # bottom
    image = open_image(image_bytes=await image_file.read()) # convert bytes to PIL image
    cropped_image = image[y1:y2, x1:x2] # crop image
    return {"image_base64": cv2_image_to_base64(cropped_image)} # convert OpenCV image to base64


# 2. Grayscaling
@app.post("/grayscale")
async def grayscaling_image(image_file: UploadFile = File()):
    """
    Convert the given image file to grayscale
    
    Parameters:
    image_file (UploadFile): image file to be converted
    
    Returns:
    dict: dictionary containing the grayscale image as base64 string
    """
    image = open_image(image_bytes=await image_file.read())
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return {"image_base64": cv2_image_to_base64(gray)}


# 3. Image Convolution
@app.post("/convolution")
async def convolve_image(image_file: UploadFile = File()):
    """
    Convolve the given image file with a 5x5 kernel
    
    Parameters:
    image_file (UploadFile): image file to be convolved
    
    Returns:
    dict: dictionary containing the convolved image as base64 string
    """
    image = open_image(image_bytes=await image_file.read())
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Konversi ke grayscale
    kernel = np.ones((5, 5), np.float32) / 25  # Kernel 5x5 untuk blur
    convolved_image = cv2.filter2D(gray, -1, kernel)  # Konvolusi pada gambar grayscale
    return {"image_base64": cv2_image_to_base64(convolved_image)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)