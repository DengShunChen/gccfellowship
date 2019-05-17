#!/usr/bin/env python 
import urllib.request as ur
from imgurpython import ImgurClient

class Toolbox():
  def __init__(self):
    print('Using Toolbox')

  def download_image(self,image_url,image_name):
    ur.urlretrieve(image_url,image_name) 

  def download_image(self,image_url,image_name):
    print("Downloading image... ")
    img_data = ur.get(image_url).content
    with open(image_name, 'wb') as handler:
      handler.write(img_data)
    print("Done")

  def upload_photo(self,photo_path):
    client_id = '1abfc96a9fd1cc6'
    client_secret = 'b90e27ab19ee4f3893c4442c2a4a3fba9035f0d0'
    access_token = '0cd8b2fe6740013637b3c1fd62954237540d4529'
    refresh_token = '0811df48b103bbdb19fdaeec1b4f5912bf8e8319'
    client = ImgurClient(client_id, client_secret, access_token, refresh_token)
    album = None # You can also enter an album ID here
    config = {
      'album': album,
    }
  
    print("Uploading image... ")
    image = client.upload_from_path(photo_path, config=config, anon=False)
    print("Done")
    return image['link']

