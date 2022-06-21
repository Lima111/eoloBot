import math as m
from telegram.ext import *
from geopy.geocoders import Nominatim


with open("token.txt", "r", ) as f:
    TOKEN = f.read()
    print("Il tuo token è: ", TOKEN)


def get_loc(street: str) -> str:
    geolocator = Nominatim(user_agent="TelegramWindBot")
    location = geolocator.geocode(street)
    return location.address


def cloasest(update, context):  # TODO Make the bot take the adress as INPUT
    street = "Via Salvo d'acquisto,1 37122 Verona"
    update.message.reply_text(get_loc(street))


def dist(lat1, lon1, lat2, lon2) -> float:
    """Calcutaes the distance between two coords

    Args:
        lat1 (float): latitude of first pos
        lon1 (float): longitude of first pos
        lat2 (float): latitude of second pos
        lon2 (float): longitude of second pos

    Returns:
        float: Distace in ? 
    """
    num1 = m.sin((m.radians(lat2) - m.radians(lat1)) / 2)
    num2 = m.sin((m.radians(lon2) - m.radians(lon1)) / 2)
    return 6371 * 2 * m.asin(m.sqrt(m.pow(num1, 2) + m.cos(lat1) * m.cos(lat2) * m.pow(num2, 2)))


def start(update, context):
    """First msg the bot sends
    """
    update.message.reply_text("Ciao! Benvenuto nel bot prova /help")


def help(update, context):
    update.message.reply_text("""
    Sono disponibili i seguenti comandi:


    /start --> Messaggio di benvenuto
    /help --> Questo messaggio
    /close --> la stazione piu vicina(attualmente solo il return del input)
    """)


def reply(update, context):
    user_input = update.message.text
    update.message.reply_text(user_input)


def error(update, context):
    print(f"Update {update} caused error {context.error}")


def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("close", cloasest))
    dp.add_handler(MessageHandler(Filters.text, reply))

    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
