from crypt_image import CryptImage
from PIL import Image

i = Image.open("../SMILE.jpg")
c = CryptImage(i, None)

c.encrypt("cyber")