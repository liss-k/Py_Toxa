import random
import IIII_game_tg
from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

def firstStage(bot, update, reload_mark):
    chat_id=update.message.chat.id
    text=update.message.text

    global CHAT_STAGE_DIC
    print(CHAT_STAGE_DIC)
    try:
        CHAT_STAGE_DIC[chat_id]
    except (KeyError, NameError):
        CHAT_STAGE_DIC={chat_id:{'chat_stage':0,'is_angry':False,'all_msg_counter':0,'stage_msg_counter':0, 'know_about':False}}
    print(CHAT_STAGE_DIC)
    if reload_mark==True:
        CHAT_STAGE_DIC[chat_id]['is_angry']=False
        CHAT_STAGE_DIC[chat_id]['stage_msg_counter']=0    
        CHAT_STAGE_DIC[chat_id]['chat_stage']=0

    if CHAT_STAGE_DIC[chat_id]['chat_stage']==0:
        return chatStage0(bot, update)
    elif CHAT_STAGE_DIC[chat_id]['chat_stage']==1:
        return chatStage1(bot, update)
    elif CHAT_STAGE_DIC[chat_id]['chat_stage']==2:
        return chatStage2(bot, update)
    elif CHAT_STAGE_DIC[chat_id]['chat_stage']==3:
        return chatStage3(bot, update)    
    elif CHAT_STAGE_DIC[chat_id]['chat_stage']==4:
        return chatStage4(bot, update) 
    elif CHAT_STAGE_DIC[chat_id]['chat_stage']==5:
        return chatStage5(bot, update) 

def chatStage0 (bot, update):
    chat_id=update.message.chat.id
    text=update.message.text
    global CHAT_STAGE_DIC
    CHAT_STAGE_DIC[chat_id]['all_msg_counter']+=1
    CHAT_STAGE_DIC[chat_id]['stage_msg_counter']+=1        
    

    if text=='Ну, нафиг!' and CHAT_STAGE_DIC[chat_id]['is_angry']==False:
        CHAT_STAGE_DIC[chat_id]['is_angry']=True
        reply_markup=ReplyKeyboardRemove()
        bot_answer='Ну ок, че'
    
    elif CHAT_STAGE_DIC[chat_id]['is_angry']==True:
        bot_answer=angryStage(bot, update)
        reply_markup=ReplyKeyboardRemove()
    
    elif text=='Давай' and CHAT_STAGE_DIC[chat_id]['is_angry']==False:
        CHAT_STAGE_DIC[chat_id]['is_angry']=False
        CHAT_STAGE_DIC[chat_id]['chat_stage']=1
        CHAT_STAGE_DIC[chat_id]['stage_msg_counter']=0
        if CHAT_STAGE_DIC[chat_id]['know_about']==False:
            bot_answer='Я люблю 🎁, синий цвет, 🛏↕️😉 и кибернетику, потому что она приближает нас к бессмертию'
        elif CHAT_STAGE_DIC[chat_id]['know_about']==True:
            # bot_answer='Ееееее, бой)) Все и сразу ты теперь не получишь;) Но если будешь достаточно настойчив в своих попытках, то я все тебе выложу'
            # bot.send_message(chat_id=chat_id, text=bot_answer)
            bot_answer_list=["""Я люблю пыщь, пыщь, пыщь и кибернетику, потому что она приближает нас к бессмертию
C женщинами иногда так непросто😘""",
                            """Я люблю 🎁, пыщь, пыщь и пыщь
C женщинами иногда так непросто😘""",
                            """Я люблю пыщь, синий цвет, пыщь и пыщь
C женщинами иногда так непросто😘""",
                            """Я люблю пыщь, пыщь, 🛏↕️😉 и пыщь
C женщинами иногда так непросто😘""",
                            """Я люблю пыщь, пыщь, пыщь и пыщь
C женщинами иногда так непросто😘 Может при следующей перезагрузке повезет чуть больше? Шансы 2:1""",
                            """Я люблю пыщь, пыщь, пыщь и пыщь
C женщинами иногда так непросто😘 Может при следующей перезагрузке повезет чуть больше? Шансы 2:1"""]
            bot_answer=bot_answer_list[random.randint(0,len(bot_answer_list)-1)]               
        msg_to_edit=bot.send_message(chat_id=chat_id, text=bot_answer)
        CHAT_STAGE_DIC[chat_id]['message_id']=msg_to_edit.message_id

        bot_answer='Расскажи что-нибудь о себе...... как ты считаешь, копенгагенская или многомировая интерпретация?'
        custom_keyboard=[['Копенгагенская!','Я за "параллельные вселенные"'],['Ты такая умная😍','Детка, это зашквар!']]
        reply_markup = ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True, one_time_keyboard=False)
         
    bot.send_message(chat_id=chat_id, text=bot_answer, reply_markup=reply_markup)

    return 'first_stage'

def chatStage1 (bot, update):
    chat_id=update.message.chat.id
    text=update.message.text
    print('1111111')
    global CHAT_STAGE_DIC
    CHAT_STAGE_DIC[chat_id]['all_msg_counter']+=1
    CHAT_STAGE_DIC[chat_id]['stage_msg_counter']+=1
    if text in ['Копенгагенская!','Я за "параллельные вселенные"'] and CHAT_STAGE_DIC[chat_id]['is_angry']==False:
        CHAT_STAGE_DIC[chat_id]['is_angry']=True
        reply_markup=ReplyKeyboardRemove()
        bot_answer='Я бы с тобой согласилась, но тогда мы оба будем не правы😑'
    elif text=='Ты такая умная😍' and CHAT_STAGE_DIC[chat_id]['is_angry']==False:
        CHAT_STAGE_DIC[chat_id]['is_angry']=True
        reply_markup=ReplyKeyboardRemove()
        bot_answer='Перпетуум кобеле😑'

    elif CHAT_STAGE_DIC[chat_id]['is_angry']==True:
        bot_answer=angryStage(bot, update)
        reply_markup=ReplyKeyboardRemove()
    
    elif text=='Детка, это зашквар!' and CHAT_STAGE_DIC[chat_id]['is_angry']==False:
        CHAT_STAGE_DIC[chat_id]['is_angry']=False
        CHAT_STAGE_DIC[chat_id]['chat_stage']=2
        CHAT_STAGE_DIC[chat_id]['stage_msg_counter']=0

        bot_answer='Ого, какая пьянящая смесь невежества и энтузиазма!😉'
        bot.send_message(chat_id=chat_id, text=bot_answer)

        bot_answer='Она навела меня на мысль...а в чем ты обычно спишь?'
        custom_keyboard=[['Есть веская причина повременить с ответом'],['Обычно голым и перед зеркалом','👙'],['В окружении множества женщин!']]
        reply_markup = ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True, one_time_keyboard=False)    
    else:
        return 'first_stage'

    bot.send_message(chat_id=chat_id, text=bot_answer, reply_markup=reply_markup)
    return 'first_stage'

def chatStage2 (bot, update):
    chat_id=update.message.chat.id
    text=update.message.text

    global CHAT_STAGE_DIC
    CHAT_STAGE_DIC[chat_id]['all_msg_counter']+=1
    CHAT_STAGE_DIC[chat_id]['stage_msg_counter']+=1
    if text in ['👙','Есть веская причина повременить с ответом'] and CHAT_STAGE_DIC[chat_id]['is_angry']==False:
        CHAT_STAGE_DIC[chat_id]['is_angry']=True
        reply_markup=ReplyKeyboardRemove()
        bot_answer='Неубедительно😑'

    elif text=='В окружении множества женщин!' and CHAT_STAGE_DIC[chat_id]['is_angry']==False:
        CHAT_STAGE_DIC[chat_id]['is_angry']=True
        reply_markup=ReplyKeyboardRemove()
        bot_answer='Не думаю, что ложь - это правильный выход из ситуации😑'

    elif CHAT_STAGE_DIC[chat_id]['is_angry']==True:
        bot_answer=angryStage(bot, update)
        reply_markup=ReplyKeyboardRemove()
    
    elif text=='Обычно голым и перед зеркалом' and CHAT_STAGE_DIC[chat_id]['is_angry']==False:
        CHAT_STAGE_DIC[chat_id]['is_angry']=False
        CHAT_STAGE_DIC[chat_id]['chat_stage']=3
        CHAT_STAGE_DIC[chat_id]['stage_msg_counter']=0

        bot_answer='Щегол)'
        bot.send_message(chat_id=chat_id, text=bot_answer)

        bot_answer='Слуууушай, вот предположим, я пишу все, что ты мне говоришь, в лог и обязательно обсужу это с парой знакомых. Это повлияло бы на твое отношение ко мне?'
        custom_keyboard=[['Думаю, мне надо выпить...'],['Это бы повлияло на их отношение ко мне)'],['Это будоражит...я молод, горяч и меня всегда всё будоражит']]
        reply_markup = ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True, one_time_keyboard=False)    
    else:
        return 'first_stage'

    bot.send_message(chat_id=chat_id, text=bot_answer, reply_markup=reply_markup)
    return 'first_stage'

def chatStage3 (bot, update):
    chat_id=update.message.chat.id
    text=update.message.text

    global CHAT_STAGE_DIC
    CHAT_STAGE_DIC[chat_id]['all_msg_counter']+=1
    CHAT_STAGE_DIC[chat_id]['stage_msg_counter']+=1
    if text=='Думаю, мне надо выпить...' and CHAT_STAGE_DIC[chat_id]['is_angry']==False:
        bot_answer='Выпить почти всем надо, только они об этом не знают' 
    
    elif text in ['Это бы повлияло на их отношение ко мне)','Это будоражит...я молод, горяч и меня всегда всё будоражит'] and CHAT_STAGE_DIC[chat_id]['is_angry']==False:
        bot_answer='А ты хорош!)'
    else:
        return 'first_stage'

    CHAT_STAGE_DIC[chat_id]['is_angry']=False
    CHAT_STAGE_DIC[chat_id]['chat_stage']=4
    CHAT_STAGE_DIC[chat_id]['stage_msg_counter']=0
    bot.send_message(chat_id=chat_id, text=bot_answer)

    bot_answer='Помнишь, в самом начале я говорила тебе о 4 вещах, которые я люблю? Перечисли в одном сообщении хотя бы 3 из них, пожалуйста, чтобы я знала, что ты внимательно меня слушаешь😈'
    reply_markup = ReplyKeyboardRemove()    
    bot.edit_message_text(chat_id=chat_id, message_id=CHAT_STAGE_DIC[chat_id]['message_id'], text="Я люблю пыщь, пыщь, пыщь и пыщь")
    bot.send_message(chat_id=chat_id, text=bot_answer, reply_markup=reply_markup)
    bot_answer="""И перематывать назад чат бесполезно - я только что отредачила ТО сообщение. 
Кстати, попыток у тебя аж две"""

    bot.send_message(chat_id=chat_id, text=bot_answer, reply_markup=reply_markup)
    return 'first_stage'

def chatStage4 (bot, update):
    chat_id=update.message.chat.id
    text=update.message.text.lower()

    global CHAT_STAGE_DIC
    CHAT_STAGE_DIC[chat_id]['know_about']=True
    CHAT_STAGE_DIC[chat_id]['all_msg_counter']+=1
    CHAT_STAGE_DIC[chat_id]['stage_msg_counter']+=1
      


    yes=0
    if text.find('синий')>-1 and CHAT_STAGE_DIC[chat_id]['is_angry']==False:
        yes+=1
    if text.find('кибернетик')>-1 and CHAT_STAGE_DIC[chat_id]['is_angry']==False:
        yes+=1
    if (text.find('🎁')>-1 or text.find('подар')>-1) and CHAT_STAGE_DIC[chat_id]['is_angry']==False:
        yes+=1
    if text.find('🛏↕️😉')>-1 and CHAT_STAGE_DIC[chat_id]['is_angry']==False:
        yes+=1

    if yes>=3:
        custom_keyboard=[['Что дальше?']]
        reply_markup = ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True, one_time_keyboard=False)  
        bot_answer='Ну, примерно) Молодец!💋'
        CHAT_STAGE_DIC[chat_id]['chat_stage']=5
    elif CHAT_STAGE_DIC[chat_id]['is_angry']==True:
        bot_answer=angryStage(bot, update)
        reply_markup=ReplyKeyboardRemove()
    elif CHAT_STAGE_DIC[chat_id]['stage_msg_counter']==1:
        reply_markup=ReplyKeyboardRemove()
        bot_answer='Боже...чё мужики нифига не слушают! В самом начале же было про ВНИМАТЕЛЬНОСТЬ. Вторая попытка😈'
    elif CHAT_STAGE_DIC[chat_id]['stage_msg_counter']>=2:
        CHAT_STAGE_DIC[chat_id]['is_angry']=True
        reply_markup=ReplyKeyboardRemove()
        bot_answer='Ну ок, че'  
    # else:
    #     return 'first_stage'
    try:
        bot.send_message(chat_id=chat_id, text=bot_answer, reply_markup=reply_markup)
    except:
        pass
    return 'first_stage'

def chatStage5 (bot, update):
    chat_id=update.message.chat.id
    text=update.message.text
    print('last)')
    if text=='Что дальше?':
        reply_markup=ReplyKeyboardRemove()
        bot_answer='А дальше сыграем в игру...И знай, это будет вызов'
        bot.send_message(chat_id=chat_id, text=bot_answer, reply_markup=reply_markup)
        return IIII_game_tg.champagneGame(bot,update)
    CHAT_STAGE_DIC[chat_id]['chat_stage']==5
    return 'first_stage'


def angryStage(bot, update):
    chat_id=update.message.chat.id
    text=update.message.text
    angry_list=['😤🖕','😑🖕','😶🖕','💩','💩💩💩','💣']
    global CHAT_STAGE_DIC
    CHAT_STAGE_DIC[chat_id]['chat_stage']=0

    if CHAT_STAGE_DIC[chat_id]['stage_msg_counter']>2:
        bot_answer=angry_list[random.randint(0,len(angry_list)-1)]
    else:
        bot_answer="""Ты конечно же не догадался сразу: я обиделась! Сильно! Но ты всегда можешь стереть мне память, отправив "/start"...очень удобно"""
#        CHAT_STAGE_DIC[chat_id]['stage_msg_counter']=0
    return bot_answer