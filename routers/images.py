import os
import shutil
import string
from fastapi import APIRouter, Depends, File, UploadFile
import random

from auth.oauth2 import get_current_user
from schemas import UserBase

router = APIRouter(
    prefix="/image",
    tags=["image"]
)

@router.post('/uploadfile')
def upload_image(upload_file: UploadFile = File(...), current_user: UserBase = Depends(get_current_user)):  # db: Session = Depends(get_db),
    
    letter = string.ascii_letters
    rand_string = ''.join(random.choice(letter) for i in range(6))
    new = f'_{rand_string}.'
    new_filename = new.join(upload_file.filename.rsplit('.', 1))
    path = f'images/{new_filename}'  #just new_filename #the rest is similar with while and return
    

    with open(path, "wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)
    image_url = f"/image/download/{new_filename}"
    return {'filename': new_filename, #upload_file.filename #new_filename
            'type': upload_file.content_type,
            'image_url': image_url
            }
    
    

# @router.get('/download/{name}', response_class=FileResponse)
# def download_image(name: str):  #db: Session = Depends(get_db),
#     path = f"images/{name}"
#     return (path)

@router.get('/get_image/{name}')
def get_image_by_name(name: str):  #, db: Session = Depends(get_db)
    image_url = f"/image/download/{name}"
    return {'image_url': image_url}

@router.get('/get_all_images')
def get_all_images():
    images_directory = 'images'
    image_files = os.listdir(images_directory)
    image_urls = []

    for filename in image_files:
        image_url = f"/image/download/{filename}"
        image_urls.append({
            'filename': filename,
            'image_url': image_url
        })

    return {'images': image_urls}