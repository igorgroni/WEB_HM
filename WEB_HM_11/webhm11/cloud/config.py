import cloudinary
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url
from conf.config import settings

# Налаштування Cloudinary
cloudinary.config(
    cloud_name=settings.cloud_name,
    api_key=settings.api_key,
    api_secret=settings.api_secret,
)
