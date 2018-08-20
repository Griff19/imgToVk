## Основной скрипт
## https://oauth.vk.com/authorize?client_id=6666555&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=groups,photos&response_type=token&v=5.80

import os
import requests
import vk
import data

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

## Получаем список файлов в директории
files = os.listdir(data.PHOTO_DIR)
i = 1
list_files = {}
for file in files:
    if file in lfs:
        continue
    list_files['file'+str(i)] = open(data.PHOTO_DIR + '/' +file, "rb")
    lfs.append(file)
    i += 1

print(list_files)
print (lfs)

f = open('files.txt', 'w')
for lf in lfs:
    f.write(lf + '\n')
f.close()

## Получаем адрес сервера для загрузки фото
server = api.photos.getUploadServer(album_id=data.ALBUM_ID, group_id=data.GROUP_ID)
print(server)

## Отправляем файл на сервер
request = requests.post(server['upload_url'], files=list_files)
print(request.json())

## Сохраняем файл в альбом группы
save = api.photos.save(album_id=data.ALBUM_ID, group_id=data.GROUP_ID, server=request.json()['server'], photos_list=request.json()['photos_list'], hash=request.json()['hash'])
print(save)
