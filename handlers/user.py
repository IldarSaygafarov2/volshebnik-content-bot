import requests
from telebot.types import Message

from settings import API_URL
from data.loader import bot
from data.utils import get_data_from_excel_file


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
        pages = item.get("Кол-во страниц", "")
        title = item.get("Название")
        description = item.get("Описание")
        binding = item.get("Переплёт")
        subcategory = item.get("Под категория")
        image_url = item.get("Ссылка на фото")
        host = "//".join(list(filter(lambda x: x, image_url.split("/")[:3])))
        print(pages)
        r = requests.post(
            f"{API_URL}/products/",
            json={
                "barcode": barcode,
                "age": age,
                "size": size,
                "publisher": publisher,
                "main_category": category,
                "price": "",
                # "pages": pages,
                "title": title,
                "subcategory": subcategory,
                "description": description,
                "binding": binding,
            },
        )
        print(r.json())
