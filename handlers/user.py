import json
import time

import requests
from telebot.types import Message

from data.loader import bot
from data.utils import get_data_from_excel_file
from settings import API_URL


@bot.message_handler(commands=["start"])
def handle_command_start(message: Message):
    chat_id = message.from_user.id
    bot.send_message(chat_id, "Отправьте эксель файл с обновленными данными")


@bot.message_handler(content_types=["document"])
def receive_data_from_excel_file(message: Message):
    document_id = message.document.file_id

    _file = bot.get_file(document_id)
    file = bot.download_file(_file.file_path)

    with open(f"data.xlsx", mode="wb") as f:
        f.write(file)

    data = get_data_from_excel_file("data.xlsx")

    bot.send_message(5090318438, f'Всего книг: {len(data)}')
    count = 1
    for item in data:
        barcode = item.get("Баркод")

        if not barcode:
            print('no barcode, continue')
            bot.send_message(5090318438, f'no barcode, continue')
            continue

        age = item.get("Возраст")
        size = item.get("Габариты см")
        publisher = item.get("Издательство")
        category = item.get("Категория")
        pages = item.get("Кол-во страниц")
        weight = item.get('Вес гр', '')
        title = item.get("Название")
        description = item.get("Описание")
        binding = item.get("Переплёт")
        subcategory = item.get("Под категория")
        image_url = item.get("Ссылка на фото")
        price = item.get("Цена")


        json_data = {
            "barcode": barcode,
            "age": age,
            "size": size if size is not None else "",
            "publisher": publisher,
            "main_category": category,
            "price": str(price),
            "preview": image_url,
            "pages": str(pages),
            "weight": str(weight),
            "title": title,
            "subcategory": subcategory,
            "description": description,
            "binding": binding,
        }

        print(f'{barcode=}=={size=}')

        r = requests.post(
            f"{API_URL}/products/",
            data=json.dumps(json_data),
        )
        bot.send_message(5090318438, f'{r.json()}')

        time.sleep(3)
        result = r.json()
        bot.send_message(5090318438, f'{json.dumps(result, indent=4, ensure_ascii=False)}')
        msg = f'{count} Запись с штрихкодом: {barcode} была {"Создана" if result.get("is_created") else "Обновлена"}'
        bot.send_message(message.from_user.id, msg)
        count += 1

        # try:
        #
        #     r = requests.post(
        #         f"{API_URL}/products/",
        #         data=json.dumps(json_data),
        #     )
        #     time.sleep(3)
        #     result = r.json()
        #     bot.send_message(5090318438, f'{json.dumps(result, indent=4, ensure_ascii=False)}')
        #     msg = f'{count} Запись с штрихкодом: {barcode} была {"Создана" if result.get("is_created") else "Обновлена"}'
        #     bot.send_message(message.from_user.id, msg)
        #     count += 1
        # except Exception as e:
        #     bot.send_message(5090318438, f'{barcode} {str(e)}: {e.__class__.__name__}')
        #     print(e, e.__class__)


    bot.send_message(message.from_user.id, "Записи были обновлены")
