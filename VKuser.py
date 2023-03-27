from datetime import datetime as dt
import requests


class VkUser:
    url = 'https://api.vk.com/method/'

    def __init__(self, token, version):
        self.all_photos_count = 0
        self.cur_photo_json = {}
        self.all_photos_from_vk = []
        self.params = {
            'access_token': token,
            'v': version
        }

    def get_photos(self, user_id, album_id, offset=0):
        photos_url = self.url + 'photos.get'
        photos_params = {
            'owner_id': user_id,
            'offset': offset,
            'album_id': album_id,
            'extended': 1,
            'photo_sizes': 0,
            'rev': 1,
            'count': 300
        }
        response = requests.get(photos_url, params={**self.params, **photos_params})
        self.cur_photo_json = response.json()
        self.all_photos_count = self.cur_photo_json['response']['count']
        return self.cur_photo_json

    def get_photos_params(self, photo_names):
        for elem in self.cur_photo_json['response']['items']:
            file_name = str(elem['likes']['count']) + '.jpeg'
            if file_name in photo_names:
                file_name = file_name[:-5] + '_' + str(dt.now().strftime("%d-%m-%Y_%H-%M-%S")) + '.jpeg'
            photo_names.append(file_name)
            photo = elem['sizes'][-1]
            photo.update({'filename': file_name})
            self.all_photos_from_vk.append(photo)
        return self.all_photos_from_vk
