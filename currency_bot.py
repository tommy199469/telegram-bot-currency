from telegram.ext import Updater, CommandHandler
import logging
import urllib.request
import json
# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.

name = "Bitch"

def exchange(bot, update , args):

    target_currency = None
    amount  = None
    output_str =""
    url = ""
    curr_id =""
    if not args:
        output_str += "你唔撚入野 我點幫你 唔識用就打 /help 睇下點用啦 \n"
        update.message.reply_text(output_str)
        return

    try:
        target_currency = args[1]
        curr_id = args[0] + "_" + target_currency
        print(curr_id)
        url = 'https://free.currencyconverterapi.com/api/v5/convert?q='+curr_id+'&compact=y'
    except IndexError:
        output_str += "你想換咩錢阿 唔入我會知? \n"
        update.message.reply_text(output_str)
        return

    try:
        amount = args[2]
    except IndexError:
        output_str += "少左D 錢阿 \n"
        update.message.reply_text(output_str)
        return


    output_str = '計數都唔撚識 我幫下你啦 屌你 \n \n'
    req = urllib.request.urlopen(url)
    result = json.loads(req.read());

    if result:
        result = output_str + str( round(result[curr_id]['val'] * float(amount) , 2)   ) + target_currency

    update.message.reply_text(result)

def list_currency(bot,update):
    """ get all list of currency """
    req = urllib.request.urlopen('https://free.currencyconverterapi.com/api/v5/currencies')
    result = json.loads(req.read());
    currency_array = []
    if result['results']:
        for item in result['results']:
            currency_array.append(item)

    ouput_list = "List阿柒頭 \n"
    if currency_array:
        for i, currency_array_item in enumerate(currency_array):
                ouput_list += currency_array_item
                if len(currency_array)-1 != i:
                    ouput_list += ", "
    else:
        ouput_list += "\n Empty list"

    update.message.reply_text(ouput_list)

def help(bot, update):
    update.message.reply_text("例子: /exchange HKD USD 1000 , 姐係用港幣$1000換美金 \n 唔知有咩貨幣就打 /list 啦")

def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('error "%s"', error)

def main():
    """Run bot."""
    updater = Updater("471130525:AAEMz5zwj6KaRePBmpSyOZrwXcFw_pxEpqQ")
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("exchange", exchange,pass_args=True))
    dp.add_handler(CommandHandler("list", list_currency))
    dp.add_handler(CommandHandler("help", help))
    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
