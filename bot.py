from data.loader import bot
import handlers


if __name__ == "__main__":
    try:
        print("bot started")
        bot.polling(none_stop=True)
    except Exception as e:
        pass
