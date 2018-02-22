import settings, random, time
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

global game_dic, party_dic, USER_DIC
# excep_dic={"лена":"Мой бомбический создатель!", "тесла":"Будет расти", "тоха":"Ээээх", 
# 	       "ира":"Злобоглазый профессионал...", "надя":"Почетная бросальщица ","юля":"Гоу по кальяну?"}
USER_DIC={}
game_dic={}
party_dic={}

def startBot(bot, update):

	logging.info("User {} (username {}) has pressed the button /start".format(update.message.chat.first_name, update.message.chat.username))
	chat_id=update.message.chat.id
	if str(chat_id) not in ['328203998','543317664']:
		return update.message.reply_text('Я ещё не готова')

	first_name=update.message.chat.first_name
	if first_name==None or first_name=='None':
		first_name='Мистер Ноунейм'
	hello_text="""Привет, {}!

Классно было бы просто зайти сюда и получить свой подарок?))) Но нет, ради сомнительной награды, тебе придется погрузиться в эпос и доказать, что ты настоящий мужчина, победив в вербальной схватке Викторию.

Виктория - роскошная женщина, про таких говорят "приятнее отказывают, чем она даёт". Поэтому будь внимателен и бесстрашен! Помни: ты здесь ради того, ради чего ты здесь!	
	""".format(first_name)
	bot.send_message(chat_id=chat_id, text=hello_text)

	hello_text="""Я повторю это еще раз и капслоком: будь ВНИМАТЕЛЕН"""
	bot.send_message(chat_id=chat_id, text=hello_text)
	
	global GAME_STAGE, USER_DIC
	try:
		GAME_STAGE[chat_id]='first_stage'
	except (KeyError, NameError):
		GAME_STAGE={}
		GAME_STAGE[chat_id]='first_stage'		
	try:
		USER_DIC[chat_id]['all_msg_counter']+=1
		USER_DIC[chat_id]['in_try_msg_counter']=0
	except (KeyError, NameError):
		
		USER_DIC[chat_id]={'all_msg_counter':0,'in_try_msg_counter':0}
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

	logging.info("{} (username {}) has written {}".format(first_name, username, text))
	print(chat_id)
	global USER_DIC, GAME_STAGE
	USER_DIC[chat_id]['all_msg_counter']+=1
	USER_DIC[chat_id]['in_try_msg_counter']+=1
	if USER_DIC[chat_id]['in_try_msg_counter']==1:
		reload_mark=True
	else:
		reload_mark=False

	try:
		GAME_STAGE[chat_id]
	except KeyError:
		stage_list=['first_stage','pre_party','champagne_game','after_party','angry_stage']
	#=================================== temporary ==============================================
		the_stage=stage_list[3]
		GAME_STAGE[chat_id]=the_stage
		print(GAME_STAGE[chat_id])
	#=============================================================================================
	print(GAME_STAGE[chat_id])
	# or str(chat_id)=='63818817' - Рита Волкова
	#328203998
	#232455503 - Ира
#272424273 - Надя
	if GAME_STAGE[chat_id]=='first_stage':
		GAME_STAGE[chat_id]=first_stage.firstStage(bot,update,reload_mark)
		# if GAME_STAGE[chat_id]=='champagne_game':
		# 	GAME_STAGE[chat_id]=IIII_game_tg.champagneGame(bot,update)
	elif GAME_STAGE[chat_id]=='champagne_game':
		GAME_STAGE[chat_id]=IIII_game_tg.champagneGame(bot,update)
	elif GAME_STAGE[chat_id]=='after_party':
		GAME_STAGE[chat_id]=after_party.afterParty(bot,update,job_queue)
		if GAME_STAGE[chat_id]=='angry_stage':
			GAME_STAGE[chat_id]=angry_stage.angryStage(bot,update)
	elif GAME_STAGE[chat_id]=='angry_stage':
		GAME_STAGE[chat_id]=angry_stage.angryStage(bot,update)

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
