import settings, random, time, re
import first_stage, IIII_game_tg, after_party, angry_stage
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove


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

global USER_DIC
USER_DIC={}


def startBot(bot, update):
	global USER_DIC
	chat_id=update.message.chat.id

	try:
		USER_DIC[chat_id]['game_stage']['job'].schedule_removal()
	except (KeyError, NameError):
		pass
	logging.info("User {} (username {}) has pressed the button /start".format(update.message.chat.first_name, update.message.chat.username))
	chat_id=update.message.chat.id
	print(chat_id)

	first_name=update.message.chat.first_name
	if first_name==None or first_name=='None':
		first_name='Мистер Ноунейм'
	hello_text="""Привет, {}!

Погрузись в эпос и докажи всем, что ты выдающийся интеллектуал, победив в вербальной схватке Галину!

Галина - роскошная женщина, про таких говорят "приятнее отказывают, чем она даёт". Поэтому будь внимателен и бесстрашен! Помни: ты здесь ради того, ради чего ты здесь!	
	""".format(first_name)
	bot.send_message(chat_id=chat_id, text=hello_text)

	hello_text="""Я повторю это еще раз и капслоком: будь ВНИМАТЕЛЕН"""
	bot.send_message(chat_id=chat_id, text=hello_text)
	
	try:
		USER_DIC[chat_id]['game_stage']={'stage_name':'first_stage','know_about':True}
		USER_DIC[chat_id]['all_msg_counter']+=1
		USER_DIC[chat_id]['in_try_msg_counter']=0
	except (KeyError, NameError):
		USER_DIC[chat_id]={'all_msg_counter':0,'in_try_msg_counter':0,'game_stage':{'stage_name':'first_stage'}}
	
	USER_DIC[chat_id]['is_angry_vic']=False
	bot_answer='https://media.giphy.com/media/l4pTjmrL1LKiYrHDW/giphy.gif'
	bot.send_document(chat_id, bot_answer)

	if USER_DIC[chat_id]['all_msg_counter']>3:
		bot_answer="""Хорошо, сделаю вид, что твой "/start" и впрямь заставил меня все забыть и давай знакомиться заново"""
	else:
		bot_answer='Что ж...давай знакомиться'
	custom_keyboard=[['Давай','Ну, нафиг!']]
	reply_markup = ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True, one_time_keyboard=False)
	bot.send_message(chat_id=chat_id, text=bot_answer, reply_markup=reply_markup)


def chatParametrs(bot,update,job_queue):
	text=update.message.text
	chat_id=update.message.chat.id
	first_name=update.message.chat.first_name
	username=update.message.chat.username

	logging.info("{} (username {}) has written {}".format(first_name, username, re.sub(r'[^\w\s]', '', text)))

	
	global USER_DIC
	USER_DIC[chat_id]['all_msg_counter']+=1
	USER_DIC[chat_id]['in_try_msg_counter']+=1
	if USER_DIC[chat_id]['in_try_msg_counter']==1:
		reload_mark=True
	else:
		reload_mark=False

	try:
		USER_DIC[chat_id]['game_stage']
	except KeyError:
		bot_answer='Что-то пошло не так, нажми /start'
		return bot.send_message(chat_id=chat_id, text=bot_answer, reply_markup=reply_markup)

	game_stage_dic=USER_DIC[chat_id]['game_stage']

	if game_stage_dic['stage_name']=='first_stage':
		game_stage_dic=first_stage.firstStage(bot,update,reload_mark,game_stage_dic)
	
	elif game_stage_dic['stage_name']=='champagne_game':
		game_stage_dic=IIII_game_tg.champagneGame(bot,update,game_stage_dic)
	
	elif game_stage_dic['stage_name']=='after_party':
		game_stage_dic=after_party.afterParty(bot,update,job_queue,game_stage_dic)
		if game_stage_dic['stage_name']=='angry_stage':
			game_stage_dic=angry_stage.angryStage(bot,update,game_stage_dic)
	
	elif game_stage_dic['stage_name']=='angry_stage' or game_stage_dic['stage_name']=='final_stage':
		game_stage_dic=angry_stage.angryStage(bot,update,game_stage_dic)

	USER_DIC[chat_id]['game_stage']=game_stage_dic


def chatSticker(bot,update):
	text=update.message.text
	chat_id=update.message.chat.id

	general_answer=['Меня на такое не программировали','Вся жизнь театр, а мы в ней - лишь актеры','Давай без этого']
	update.message.reply_text(general_answer[random.randint(0,len(general_answer)-1)])

# Bot.SendChatAction(update.Message.Chat.Id, ChatAction.Typing)
	

def main():
	updtr=Updater(settings.TG_YET_ANOTHER_BORING_BOT_KEY)
# Добавляем хендлеры в диспетчер	
	updtr.dispatcher.add_handler(CommandHandler("start", startBot))
	updtr.dispatcher.add_handler(MessageHandler(Filters.text, chatParametrs, pass_job_queue=True))
	updtr.dispatcher.add_handler(MessageHandler(Filters.sticker, chatSticker))
# Начинаем поиск обновлений
	updtr.start_polling()
# Останавливаем бота, если были нажаты Ctrl + C
	updtr.idle()


if __name__=="__main__":
	logging.info('Bot started')
	main()
