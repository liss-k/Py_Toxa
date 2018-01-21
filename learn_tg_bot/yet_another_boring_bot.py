import settings
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# добавление логгирования бота
import logging
logging.basicConfig(format='%(name)s-%(asctime)s-%(levelname)s-%(message)s',
					level=logging.INFO,
					filename='bot.log'
					)
# asctime - время события, 
# levelname - тип события, 
# message - что произошло (задаем сами)
# ----------------------------

def start_bot(bot, update):
	print(update)
	hello_text="""Привет, {}!
Я дичайшее тупло, но ты поговори со мной, это в порядке вещей
	""".format(update.message.chat.first_name)
	update.message.reply_text(hello_text)

def chat(bot,update):
	text=update.message.text
	logging.info(text)
	update.message.reply_text(text)


def main():
	updtr=Updater(settings.TG_YET_ANOTHER_BORING_BOT_KEY)
	
	updtr.dispatcher.add_handler(CommandHandler("start", start_bot))
	updtr.dispatcher.add_handler(MessageHandler(Filters.text, chat))

	updtr.start_polling()
	updtr.idle()

if __name__=="__main__":
	logging.info('Bot started')
	main()