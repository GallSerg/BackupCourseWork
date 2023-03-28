import json
import time
import VKuser as vk
import YaDiskUser as ya


DEFAULT_PHOTO_COUNT_VALUE = 5
if __name__ == '__main__':
    # Get Yandex token from file ya_token.txt and create connect
    # with open('ya_token.txt', 'r') as file_object:
    #     token = file_object.read().strip()
    token = input('Print your Yandex Disk token: \n')
    ya_client = ya.YaUploader(token)

    # Get VK token from file ya_token.txt and create connect
    with open('vk_token.txt', 'r') as file_object:
        token = file_object.read().strip()
    vk_client = vk.VkUser(token, '5.131')

    # Get input data
    vk_user_id = input('Print VK user id: \n')
    new_directory = input('Do you need to create a new directory in Yandex Disk? (Yes/No/Root) \n')
    if new_directory == "Yes":
        new_directory_name = input("Print new directory's name in Yandex Disk: \n")
        ya_client.create_directory(new_directory_name)
        save_directory = new_directory_name
    elif new_directory == 'No':
        save_directory = input("Print directory's name in Yandex Disk to save photos: \n")
    else:
        save_directory = ''
        print('ATTENTION!!! Photos will be written in a root!')
    album_id = input("Print album's name for photos downloading (wall / profile): \n")

    # Get first page of photos and count all photos in album
    photo_res_json = vk_client.get_photos(vk_user_id, album_id)

    # Input needed photo count
    photos_count = int(input(f"User have {vk_client.all_photos_count} in album '{album_id}'. "
                             "How many photos do you want to upload on Yandex Disk? (print 0 for default value) \n"))

    # Check input count of photos
    if photos_count == 0:
        photos_count = DEFAULT_PHOTO_COUNT_VALUE
        print(f"{photos_count} photos will be uploaded (default value).")
    elif photos_count > vk_client.all_photos_count:
        photos_count = vk_client.all_photos_count
        print(f"{photos_count} photos will be uploaded (input value is bigger than the max photo count).")

    # Get photos from Yandex Disk directory and put in list their names
    time.sleep(1)
    print(f"Get names of photos from Yandex Disk directory {save_directory}.")
    photo_names = ya_client.get_dir_photos_list(save_directory)
    time.sleep(1)
    print(f'Done. Got {len(photo_names)} photo names.')

    # Get all photos from VK
    time.sleep(1)
    print("Get photos from VK.")
    all_photos_from_vk = vk_client.get_photos_params(photo_names)
    time.sleep(1)
    print('Done.')

    # Upload top photos_count images in Yandex Disk
    photo_meta = ya_client.upload_photos_in_dir(all_photos_from_vk, save_directory, photos_count)

    # Save metadata in json file
    with open('photo_meta.json', 'w') as file_object:
        json.dump(photo_meta, file_object)
