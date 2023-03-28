import requests
import time
from tqdm.auto import tqdm


class YaUploader:
    def __init__(self, token: str):
        self.token = token

    def check_dir(self, directory):
        """Method returns information about input directory on Yandex Disk"""
        url = 'https://cloud-api.yandex.net:443/v1/disk/resources'
        request = requests.get(url, params={'path': directory}, headers={'Authorization': self.token})
        return request.json()

    def create_directory(self, dir_name):
        """Method creates new directory in Yandex Disk"""
        url = 'https://cloud-api.yandex.net/v1/disk/resources'
        request = requests.put(url, params={'path': dir_name}, headers={'Authorization': self.token})
        return request.status_code

    def upload(self, upload_path, download_url):
        """Method uploads file (based on file's URL) on Yandex Disk"""
        url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        request = requests.post(url,
                                headers={'Authorization': self.token},
                                params={'path': upload_path, 'url': download_url})
        return request.status_code

    def get_dir_photos_list(self, check_dir):
        photo_names = []
        yandex_current_photos = self.check_dir(check_dir)
        for photo in yandex_current_photos['_embedded']['items']:
            photo_name = (photo['path'].split('/'))[-1]
            photo_names.append(photo_name)
        return photo_names

    def upload_photos_in_dir(self, photos, save_directory, photos_count):
        photo_meta = []
        print('Start photo uploading process')
        for photo in tqdm(
                sorted(photos, key=lambda x: x['height'] * x['width'], reverse=True)[:photos_count],
                desc='Photos uploading'):
            if save_directory != '' and save_directory != ' ':
                self.upload(f"/{save_directory}/{photo['filename']}", photo['url'])
            else:
                self.upload(f"/{photo['filename']}", photo['url'])
            photo_meta.append({"file_name": photo['filename'], "size": photo['type']})
            time.sleep(0.33)
        print('Upload is succeeded')
        return photo_meta
