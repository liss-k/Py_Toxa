import random
import IIII_game_tg
from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

def firstStage(bot, update, reload_mark, game_stage_dic):
    chat_id=update.message.chat.id
    text=update.message.text

    try:
        game_stage_dic['chat_stage']
    except (KeyError, NameError):
        game_stage_dic={'stage_name':'first_stage','chat_stage':0,'is_angry':False,'all_msg_counter':0,'stage_msg_counter':0, 'know_about':False}

    if reload_mark==True:
        game_stage_dic['is_angry']=False
        game_stage_dic['stage_msg_counter']=0    
        game_stage_dic['chat_stage']=0
        game_stage_dic['edit_msg']=0


    if game_stage_dic['chat_stage']==0:
        return chatStage0(bot, update, game_stage_dic)
    elif game_stage_dic['chat_stage']==1:
        return chatStage1(bot, update, game_stage_dic)
    elif game_stage_dic['chat_stage']==2:
        return chatStage2(bot, update, game_stage_dic)
    elif game_stage_dic['chat_stage']==3:
        return chatStage3(bot, update, game_stage_dic)    
    elif game_stage_dic['chat_stage']==4:
        return chatStage4(bot, update, game_stage_dic) 
    elif game_stage_dic['chat_stage']==5:
        return chatStage5(bot, update, game_stage_dic) 


def chatStage0 (bot, update, game_stage_dic):
    chat_id=update.message.chat.id
    text=update.message.text
    game_stage_dic['all_msg_counter']+=1
    game_stage_dic['stage_msg_counter']+=1        
    

    if text=='Ну, нафиг!' and game_stage_dic['is_angry']==False:
        game_stage_dic['is_angry']=True
        reply_markup=ReplyKeyboardRemove()
        bot_answer='Ну ок, че'
    
    elif game_stage_dic['is_angry']==True:
        bot_answer=angryStage(bot, update, game_stage_dic)
        reply_markup=ReplyKeyboardRemove()
    
    elif text=='Давай' and game_stage_dic['is_angry']==False:
        game_stage_dic['is_angry']=False
        game_stage_dic['chat_stage']=1
        game_stage_dic['stage_msg_counter']=0
        if game_stage_dic['know_about']==False:
            bot_answer='Я люблю 🎁, синий цвет, 🛏↕️😉 и кибернетику, потому что она приближает нас к бессмертию'
        elif game_stage_dic['know_about']==True:
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
        game_stage_dic['message_id']=msg_to_edit.message_id

        bot_answer='Расскажи что-нибудь о себе...... как ты считаешь, копенгагенская или многомировая интерпретация?'
        custom_keyboard=[['Копенгагенская!','Я за "параллельные вселенные"'],['Ты такая умная😍','Детка, это зашквар!']]
        reply_markup = ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True, one_time_keyboard=False)
         
    bot.send_message(chat_id=chat_id, text=bot_answer, reply_markup=reply_markup)

    return game_stage_dic

def chatStage1 (bot, update, game_stage_dic):
    chat_id=update.message.chat.id
    text=update.message.text
    game_stage_dic['all_msg_counter']+=1
    game_stage_dic['stage_msg_counter']+=1

    try:
        if game_stage_dic['edit_msg']==0:
            bot.edit_message_text(chat_id=chat_id, message_id=game_stage_dic['message_id'], text="Я люблю пыщь, пыщь, пыщь и пыщь")
            game_stage_dic['edit_msg']=1      
    except (KeyError, NameError):
        game_stage_dic['edit_msg']=1
        bot.edit_message_text(chat_id=chat_id, message_id=game_stage_dic['message_id'], text="Я люблю пыщь, пыщь, пыщь и пыщь")

    if text in ['Копенгагенская!','Я за "параллельные вселенные"'] and game_stage_dic['is_angry']==False:
        game_stage_dic['is_angry']=True
        reply_markup=ReplyKeyboardRemove()
        bot_answer='Я бы с тобой согласилась, но тогда мы оба будем не правы😑'
    elif text=='Ты такая умная😍' and game_stage_dic['is_angry']==False:
        game_stage_dic['is_angry']=True
        reply_markup=ReplyKeyboardRemove()
        bot_answer='Перпетуум кобеле😑'

    elif game_stage_dic['is_angry']==True:
        bot_answer=angryStage(bot, update, game_stage_dic)
        reply_markup=ReplyKeyboardRemove()
    
    elif text=='Детка, это зашквар!' and game_stage_dic['is_angry']==False:
        game_stage_dic['is_angry']=False
        game_stage_dic['chat_stage']=2
        game_stage_dic['stage_msg_counter']=0

        bot_answer='Ого, какая пьянящая смесь невежества и энтузиазма!😉'
        bot.send_message(chat_id=chat_id, text=bot_answer)

        bot_answer='Она навела меня на мысль...а в чем ты обычно спишь?'
        custom_keyboard=[['Есть веская причина повременить с ответом'],['Обычно голым и перед зеркалом','👙'],['В окружении множества женщин!']]
        reply_markup = ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True, one_time_keyboard=False)    
    else:
        return game_stage_dic

    bot.send_message(chat_id=chat_id, text=bot_answer, reply_markup=reply_markup)
    return game_stage_dic

def chatStage2 (bot, update, game_stage_dic):
    chat_id=update.message.chat.id
    text=update.message.text

    game_stage_dic['all_msg_counter']+=1
    game_stage_dic['stage_msg_counter']+=1
    if text in ['👙','Есть веская причина повременить с ответом'] and game_stage_dic['is_angry']==False:
        game_stage_dic['is_angry']=True
        reply_markup=ReplyKeyboardRemove()
        bot_answer='Неубедительно😑'

    elif text=='В окружении множества женщин!' and game_stage_dic['is_angry']==False:
        game_stage_dic['is_angry']=True
        reply_markup=ReplyKeyboardRemove()
        bot_answer='Не думаю, что ложь - это правильный выход из ситуации😑'

    elif game_stage_dic['is_angry']==True:
        bot_answer=angryStage(bot, update, game_stage_dic)
        reply_markup=ReplyKeyboardRemove()
    
    elif text=='Обычно голым и перед зеркалом' and game_stage_dic['is_angry']==False:
        game_stage_dic['is_angry']=False
        game_stage_dic['chat_stage']=3
        game_stage_dic['stage_msg_counter']=0

        bot_answer='Щегол)'
        bot.send_message(chat_id=chat_id, text=bot_answer)

        bot_answer='Слуууушай, вот предположим, я пишу все, что ты мне говоришь, в лог и обязательно обсужу это с парой знакомых. Это повлияло бы на твое отношение ко мне?'
        custom_keyboard=[['Думаю, мне надо выпить...'],['Это бы повлияло на их отношение ко мне)'],['Это будоражит...я молод, горяч и меня всегда всё будоражит']]
        reply_markup = ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True, one_time_keyboard=False)    
    else:
        return game_stage_dic

    bot.send_message(chat_id=chat_id, text=bot_answer, reply_markup=reply_markup)
    return game_stage_dic

def chatStage3 (bot, update, game_stage_dic):
    chat_id=update.message.chat.id
    text=update.message.text

    game_stage_dic['all_msg_counter']+=1
    game_stage_dic['stage_msg_counter']+=1
    if text=='Думаю, мне надо выпить...' and game_stage_dic['is_angry']==False:
        bot_answer='Выпить почти всем надо, только они об этом не знают' 
    
    elif text in ['Это бы повлияло на их отношение ко мне)','Это будоражит...я молод, горяч и меня всегда всё будоражит'] and game_stage_dic['is_angry']==False:
        bot_answer='А ты хорош!)'
    else:
        return game_stage_dic

    game_stage_dic['is_angry']=False
    game_stage_dic['chat_stage']=4
    game_stage_dic['stage_msg_counter']=0
    bot.send_message(chat_id=chat_id, text=bot_answer)

    bot_answer='Помнишь, в самом начале я говорила тебе о 4 вещах, которые я люблю? Перечисли в одном сообщении хотя бы 3 из них, пожалуйста, чтобы я знала, что ты внимательно меня слушаешь😈'
    reply_markup = ReplyKeyboardRemove()    
    bot.send_message(chat_id=chat_id, text=bot_answer, reply_markup=reply_markup)
    bot_answer="""И перематывать назад чат бесполезно - я только что отредачила ТО сообщение. 
Попыток у тебя две"""

    bot.send_message(chat_id=chat_id, text=bot_answer, reply_markup=reply_markup)
    return game_stage_dic

def chatStage4 (bot, update, game_stage_dic):
    chat_id=update.message.chat.id
    text=update.message.text.lower()

    game_stage_dic['know_about']=True
    game_stage_dic['all_msg_counter']+=1
    game_stage_dic['stage_msg_counter']+=1

    yes=0
    if text.find('синий')>-1 and game_stage_dic['is_angry']==False:
        yes+=1
    if text.find('кибернетик')>-1 and game_stage_dic['is_angry']==False:
        yes+=1
    if (text.find('🎁')>-1 or text.find('подар')>-1) and game_stage_dic['is_angry']==False:
        yes+=1
    if text.find('🛏↕️😉')>-1 and game_stage_dic['is_angry']==False:
        yes+=1

    if yes>=3:
        custom_keyboard=[['Что дальше?']]
        reply_markup = ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True, one_time_keyboard=False)  
        bot_answer='Ну, примерно) Молодец!💋'
        game_stage_dic['chat_stage']=5
    elif game_stage_dic['is_angry']==True:
        bot_answer=angryStage(bot, update, game_stage_dic)
        reply_markup=ReplyKeyboardRemove()
    elif game_stage_dic['stage_msg_counter']==1:
        reply_markup=ReplyKeyboardRemove()
        bot_answer='Боже...чё люди нифига не слушают! В самом начале же было про ВНИМАТЕЛЬНОСТЬ. Вторая попытка😈'
    elif game_stage_dic['stage_msg_counter']>=2:
        game_stage_dic['is_angry']=True
        reply_markup=ReplyKeyboardRemove()
        bot_answer='Ну ок, че'  

    try:
        bot.send_message(chat_id=chat_id, text=bot_answer, reply_markup=reply_markup)
    except:
        pass
    return game_stage_dic

def chatStage5 (bot, update, game_stage_dic):
    chat_id=update.message.chat.id
    text=update.message.text

    if text=='Что дальше?':
        reply_markup=ReplyKeyboardRemove()
        bot_answer='А дальше сыграем в игру...И знай, это будет вызов'
        bot.send_message(chat_id=chat_id, text=bot_answer, reply_markup=reply_markup)
        game_stage_dic={}
        game_stage_dic['stage_name']='champagne_game'
        return IIII_game_tg.champagneGame(bot,update,game_stage_dic)
    game_stage_dic['chat_stage']==5
    return game_stage_dic


def angryStage(bot, update, game_stage_dic):
    chat_id=update.message.chat.id
    text=update.message.text
    angry_list=['😤🖕','😑🖕','😶🖕','💩','💩💩💩','💣']
    game_stage_dic['chat_stage']=0

    if game_stage_dic['stage_msg_counter']>2:
        bot_answer=angry_list[random.randint(0,len(angry_list)-1)]
    else:
        bot_answer="""Ты конечно же не догадался сразу: я обиделась! Сильно! Но ты всегда можешь стереть мне память, отправив "/start"...очень удобно"""
    return bot_answer