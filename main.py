## Основной скрипт

import os
import requests
import vk
import data
from base import Db
from datetime import date


# Функция отправки изображений в альбом
def send_img(list_f, name_f):
    # Получаем адрес сервера для загрузки изображений
    server = api.photos.getUploadServer(album_id=data.ALBUM_ID, group_id=data.GROUP_ID)
    #print(server)

    # Отправляем файлы на сервер
    request = requests.post(server['upload_url'], files=list_f)
    # print(request.json())

    # Сохраняем файл в альбом группы
    save = api.photos.save(album_id=data.ALBUM_ID, group_id=data.GROUP_ID, server=request.json()['server'],
                           photos_list=request.json()['photos_list'], hash=request.json()['hash'], caption=name_f)
    print(save)

    #comment = api.photos.createComment(owner_id=save[0]['owner_id'], photo_id=save[0]['pid'], message=name_f, from_group=1)
    #print(comment)
    return save


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
db = Db('images.db')

# Получаем список уже отправленных файлов
res = db.execute('SELECT local_name FROM image').fetchall()
lfs = [item[0].strip() for item in res]
# Если в базе нет данных пробуем получить из резервного файла
if not lfs:
    f = open('files.txt', 'r')
    lfs = [line.strip() for line in f]
    f.close()

list_files = {}
i = 1

# Получаем список файлов в директории
files = os.listdir(data.PHOTO_DIR)
for file in files:
    if file in lfs:
        continue

    print(i, file)
    list_files['file1'] = open(data.PHOTO_DIR + '/' + file, "rb")

    save = send_img(list_files, file)
    id_vk = 'https://vk.com/photo' + str(save[0]['owner_id']) + '_' + str(save[0]['pid'])

    if 'src_xxxbig' in save[0]: src = save[0]['src_xxxbig']
    elif 'src_xxbig' in save[0]: src = save[0]['src_xxbig']
    elif 'src_xbig' in save[0]: src = save[0]['src_xbig']
    else: src = save[0]['src_big']

    db.execute('INSERT INTO image (id_vk, local_name, url, date, timestamp, user) VALUES (?, ?, ?, ?, ?, ?)',
               (id_vk, file, src, date.today(), save[0]['created'], 'Griff'))
    lfs.append(file)

    list_files = {}

    i += 1
    #if i > 1:
    #    break

f = open('files.txt', 'w')
for lf in lfs:
    f.write(lf + '\n')
f.close()

db.connect.close()
