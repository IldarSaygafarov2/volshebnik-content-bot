import json
from pprint import pprint

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
def recieve_data_from_excel_file(message: Message):
    document_id = message.document.file_id

    _file = bot.get_file(document_id)
    file = bot.download_file(_file.file_path)

    with open(f"data.xlsx", mode="wb") as f:
        f.write(file)

    data = get_data_from_excel_file("data.xlsx")
    for item in data:
        barcode = item.get("Баркод")
        age = item.get("Возраст")
        size = item.get("Габариты")
        publisher = item.get("Издательство")
        category = item.get("Категория")
        pages = item.get("Кол-во страниц", "0")
        title = item.get("Название")
        description = item.get("Описание")
        binding = item.get("Переплёт")
        subcategory = item.get("Под категория")
        image_url = item.get("Ссылка на фото")
        price = item.get("Цена", "")

        json_data = {
            "barcode": barcode,
            "age": age,
            "size": size,
            "publisher": publisher,
            "main_category": category,
            "price": price if price is not None else "",
            "preview": image_url,
            "pages": str(pages),
            "title": title,
            "subcategory": subcategory,
            "description": description,
            "binding": binding
        }
        pprint(json_data)
    #
        try:
            r = requests.post(
                f"{API_URL}/products/",
                data=json.dumps(json_data),
            )
            result = r.json()

            msg = f'Запись с штрихкодом: {barcode} была {"Создана" if result.get("is_created") else "Обновлена"}'
            bot.send_message(message.from_user.id, msg)
        except Exception as e:
            bot.send_message(5090318438, f'{str(e)}: {e.__class__.__name__}')

    bot.send_message(message.from_user.id, "Записи были обновлены")
