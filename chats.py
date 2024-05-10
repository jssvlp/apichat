# coding=utf-8
import os
import re
import utils
import json
import sqlite3





def get_paginated_data(page, per_page):
    conn = sqlite3.connect('database/chats')
    cursor = conn.cursor()
    offset = (page - 1) * per_page
    cursor.execute(f"SELECT message, media, date, user FROM messages LIMIT ? OFFSET ?", (per_page, offset))
    data = cursor.fetchall()
    conn.close()
    return beatify_data(data)


def beatify_data( data ):

    parsed = [];

    for row in data:
        parsed_row = {
            'message': row[0],
            'media': row[1],
            'date': row[2],
            'user': row[3]
        }
        parsed.append(parsed_row)

    return parsed

def parseFlatFile():
    parsed_chat = []
    with open('_chat.txt') as chat:
        for line in chat:
            info = extraer_info(line)
            if info:
                fileName = getMessageMedia(info['message'])

                if fileName:
                    media = {
                        "fileName" : fileName ,
                        "type": utils.get_mimetype(fileName)
                    }
                    info['media'] = media
            parsed_chat.append(info)
    return parsed_chat


def getFromJson():
    with open('data.json') as chat:
        data = json.load(chat)
        return data

def getMessageMedia(message):
    patron = r"<adjunto:\s*(\S+)>"
    coincidencia = re.search(patron, message)
    fileName = ""
    messageType = "text"
    if coincidencia:
        # Obtener el nombre del archivo desde el grupo de captura
        fileName = coincidencia.group(1)
        return fileName


def extraer_info(texto):
    # Patrón para extraer la fecha, nombre de usuario y mensaje
    patron = r"\[(.*?)\]\s*(.*?):\s*(.*)"

    # Buscar coincidencias en el texto
    coincidencias = re.findall(patron, texto)

    if coincidencias:
        # Crear un objeto con la información extraída
        info = {
            'date': coincidencias[0][0],
            'user': coincidencias[0][1],
            'message': coincidencias[0][2],
            'media': None
        }
        return info
    else:
        return None

if __name__ == "__main__":
    messages = getFromJson()
    print(messages)

