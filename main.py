## Основной скрипт

import os
import requests
import vk
import data

## Функция отправки изображений в альбом
def send_img(list_f, name_f):
    ## Получаем адрес сервера для загрузки изображений
    server = api.photos.getUploadServer(album_id=data.ALBUM_ID, group_id=data.GROUP_ID)
    # print(server)

    ## Отправляем файлы на сервер
    request = requests.post(server['upload_url'], files=list_f)
    print('Отправка файлов...')

    ## Сохраняем файл в альбом группы
    save = api.photos.save(album_id=data.ALBUM_ID, group_id=data.GROUP_ID, server=request.json()['server'],
                           photos_list=request.json()['photos_list'], hash=request.json()['hash'], caption=name_f)
    print(save)

    ##comment = api.photos.createComment(owner_id=save[0]['owner_id'], photo_id=save[0]['pid'], message=name_f, from_group=1)
    ##print(comment)
    return True


session = vk.Session(access_token=data.TOKEN)
api = vk.API(session, version='5.80')
""" Получаем группы
groups = api.groups.get(extended=1, filter='admin', fields='name')
del groups[0]
for item in groups:
    print(item['gid'], item['name'])
"""

""" Создаем фотоальбом в группе
photos = api.photos.createAlbum(title='Тест', group_id=data.GROUP_ID, description='Тестовый альбом')
"""
## Получаем список уже отправленных файлов
f = open('files.txt', 'r')
lfs = [line.strip() for line in f]
f.close()

list_files = {}
i = 1
## Получаем список файлов в директории
files = os.listdir(data.PHOTO_DIR)
for file in files:
    if file in lfs:
        continue

    print(i, file)
    list_files['file1'] = open(data.PHOTO_DIR + '/' + file, "rb")

    if send_img(list_files, file):
        lfs.append(file)

    list_files = {}

    i += 1
    ##if i > 1:
    ##    break

f = open('files.txt', 'w')
for lf in lfs:
    f.write(lf + '\n')
f.close()
