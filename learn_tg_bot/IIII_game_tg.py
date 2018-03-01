import random, math
from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove


def mainGame(bot,update,game_stage_dic):
    text=update.message.text.lower()
    chat_id=update.message.chat.id
    reply_markup = ReplyKeyboardRemove()

    if game_stage_dic.get('i_amnt')>1:
        if game_stage_dic['game_stage']==1:
            game_stage_dic['whose_turn']=text
            if game_stage_dic['whose_turn']=='ты':
                game_stage_dic=myGame(bot,update,game_stage_dic)
                game_stage_dic['game_stage']=2
                
            elif game_stage_dic['whose_turn']=='я':
                game_stage_dic['game_stage']=2
                update.message.reply_text('К возлияниям! Сколько выпьешь?',reply_markup=reply_markup)
                
            else:
                update.message.reply_text('Ты или я? Я или ты? Ты? Я? Или ты???? Кто? Ктоооо??? КТОООО???!!!')
            return game_stage_dic

        elif game_stage_dic['game_stage']==2:
            if game_stage_dic['whose_turn']=='ты':
                game_stage_dic=myGame(bot,update,game_stage_dic)
                return game_stage_dic

            elif game_stage_dic['whose_turn']=='я': 
                game_stage_dic=uGame(bot,update,game_stage_dic)
                if game_stage_dic['whose_turn']=='ты':
                    return mainGame(bot,update,game_stage_dic)

                elif game_stage_dic['whose_turn']=='я':
                    return game_stage_dic
    else:
        game_stage_dic=final(bot,update,game_stage_dic)
        return game_stage_dic

def final(bot,update,game_stage_dic):
    chat_id=update.message.chat.id
    glass=game_stage_dic['glass']

    if game_stage_dic['whose_turn']=='ты':
        update.message.reply_text('Ого, остался один {}...тут без вариантов'.format(glass))
        bot.send_document(chat_id, 'https://media.giphy.com/media/26DMUw7wxnu5GeZeo/giphy.gif')
        update.message.reply_text('Ты меня уделал, умник;)....Пойду приходить в себя после нашего алко-поединка')
        game_stage_dic['game_stage']=4
        return game_stage_dic
    elif game_stage_dic['whose_turn']=='я':
        update.message.reply_text('...и ты проиграл, белковая твоя голова)) Давай ещё раз')
        game_stage_dic['game_stage']=0
        return zeroStage(bot,update,game_stage_dic)


def myGame(bot,update,game_stage_dic):
    chat_id=update.message.chat.id
    i_amnt=game_stage_dic['i_amnt']
    reply_markup = ReplyKeyboardRemove()
    glass=game_stage_dic['glass']
    if i_amnt!=1:
        right_decision={0:3,1:random.randint(1,3),2:1,3:2}
        my_i_amnt=right_decision[i_amnt-math.floor(i_amnt/4)*4]
        update.message.reply_text('Я выпью {}{}'.format(my_i_amnt,glass*my_i_amnt), reply_markup=reply_markup)
        game_stage_dic['i_amnt']=i_amnt-my_i_amnt
        game_stage_dic['whose_turn']='я'

        if i_amnt-my_i_amnt>1:
            update.message.reply_text('Осталось {}{}'.format(i_amnt-my_i_amnt,glass*(i_amnt-my_i_amnt)))
            update.message.reply_text('Сколько ты выпьешь?')
        elif i_amnt-my_i_amnt==1:
            update.message.reply_text('Остался {}{}...'.format(i_amnt-my_i_amnt,glass))
            return mainGame(bot,update,game_stage_dic)
   
        return game_stage_dic
    else:
        return i_amnt-1

def uGame(bot,update,game_stage_dic):
    text=update.message.text
    chat_id=update.message.chat.id
    reply_markup = ReplyKeyboardRemove()
    i_amnt=game_stage_dic['i_amnt']
    if i_amnt==1:
        return mainGame(bot,update,game_stage_dic)

    try:
        u_i_amnt=int(text)

        if u_i_amnt<4 and u_i_amnt>0 and u_i_amnt<=i_amnt:
            game_stage_dic['i_amnt']=i_amnt-u_i_amnt
            game_stage_dic['whose_turn']='ты'
            return game_stage_dic
        elif u_i_amnt>=4:
            reply_txt='Полегче, тигр) Ты так быстро вылетишь из игры😉 Пей не больше 3 бокалов за раз'
        elif u_i_amnt<0:
            reply_txt='Ты такой блёвый!😎 Постарайся больше не расплескивать...жалко😉'
        elif u_i_amnt==0:
            reply_txt='Эээ, так все-таки сколько?'
        elif u_i_amnt>i_amnt:
            reply_txt='Здесь столько нету(( Похоже, мы почти все уговорили...'
    except (TypeError, ValueError):
        reply_txt='Всё? Допился? Тебе нужно ввести целое число от 1 до 3, а не эту муть🙄'
    update.message.reply_text(reply_txt)
    game_stage_dic['whose_turn']='я'
    return game_stage_dic

def champagneGame(bot,update,game_stage_dic):
    chat_id=update.message.chat.id

    try:
        if game_stage_dic['game_stage']==1 or game_stage_dic['game_stage']==2:  
            game_stage_dic=mainGame(bot,update,game_stage_dic)
        elif game_stage_dic['game_stage']==0:    
            game_stage_dic=zeroStage(bot,update,game_stage_dic)
    except (KeyError, NameError):
        game_stage_dic=zeroStage(bot,update,game_stage_dic)
    
    if game_stage_dic['game_stage']==4:
        game_stage_dic={}
        game_stage_dic['stage_name']='after_party'
    else:    
        game_stage_dic['stage_name']='champagne_game'
    return game_stage_dic


def zeroStage(bot,update,game_stage_dic):
    chat_id=update.message.chat.id

    if game_stage_dic.get('game_stage')==None:
        game_stage_dic['try']=1
        update.message.reply_text('Правила такие: у нас есть 21 или 22 бокала с бухлишком, мы по очереди выпиваем по 1, 2 или 3 бокала. '+
                                'Кто выпьет последний - тот проиграл. Я выбираю, сколько будет бокалов. Но зато ты решаешь, кто пьет первым;)')
        update.message.reply_text('Наа-а-а-аачинаем вечеринку!')
        bot.send_document(chat_id, 'https://media.giphy.com/media/l4pTddm2KUc4CKnKg/giphy.gif')
        return gameParam(bot,update,game_stage_dic)
    elif game_stage_dic.get('game_stage')==0:
        game_stage_dic['try']+=1
        update.message.reply_text('Правила те же: пьем по 1-му, 2 или 3 бокала. Я выбираю сколько всего выпивки, зато ты выбираешь, кто пьет первым.')
        return gameParam(bot,update,game_stage_dic)


def gameParam(bot,update,game_stage_dic):
    chat_id=update.message.chat.id

    glass=['🍷','🥃','🍸'][random.randint(0,2)]

    i_amnt=random.randint(21,22)
    if i_amnt==21:
        update.message.reply_text(('Я налила {}{} бокал'.format(i_amnt,glass*i_amnt)))
    elif i_amnt==22:
        update.message.reply_text(('Я налила {}{} бокала'.format(i_amnt,glass*i_amnt)))
    whoseTurn(bot,update)

    game_stage_dic['game_stage']=1
    game_stage_dic['i_amnt']=i_amnt
    game_stage_dic['glass']=glass
    return game_stage_dic


def whoseTurn(bot,update):
    chat_id=update.message.chat.id
    custom_keyboard = [['Я', 'Ты']]
    reply_markup = ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True, one_time_keyboard=False)
    bot.send_message(chat_id=chat_id, 
                    text="Выбери, кто будет пить первым", 
                    reply_markup=reply_markup)
