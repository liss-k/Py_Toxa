import random, math
from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

global game_dic
game_dic={}


def mainGame(bot,update,user_game_param):
    text=update.message.text.lower()
    chat_id=update.message.chat.id
    reply_markup = ReplyKeyboardRemove()

    print('mainGame')
    print(user_game_param)
    if user_game_param.get('i_amnt')>1:
        if user_game_param['game_stage']==1:
            user_game_param['whose_turn']=text
            if user_game_param['whose_turn']=='ты':
                user_game_param=myGame(bot,update,user_game_param)
                user_game_param['game_stage']=2
                
            elif user_game_param['whose_turn']=='я':
                user_game_param['game_stage']=2
                update.message.reply_text('К возлияниям! Сколько выпьешь?',reply_markup=reply_markup)
                
            else:
                update.message.reply_text('Ты или я? Я или ты? Ты? Я? Или ты???? Кто? Ктоооо??? КТОООО???!!!')
            return user_game_param

        elif user_game_param['game_stage']==2:
            if user_game_param['whose_turn']=='ты':
                user_game_param=myGame(bot,update,user_game_param)
                return user_game_param

            elif user_game_param['whose_turn']=='я': 
                user_game_param=uGame(bot,update,user_game_param)
                if user_game_param['whose_turn']=='ты':
                    return mainGame(bot,update,user_game_param)

                elif user_game_param['whose_turn']=='я':
                    return user_game_param
    else:
        user_game_param=final(bot,update,user_game_param)
        return user_game_param

def final(bot,update,user_game_param):
    chat_id=update.message.chat.id
    glass=user_game_param['glass']

    if user_game_param['whose_turn']=='ты':
        update.message.reply_text('Ого, остался один {}...тут без вариантов'.format(glass))
        bot.send_document(chat_id, 'https://media.giphy.com/media/26DMUw7wxnu5GeZeo/giphy.gif')
        update.message.reply_text('Ты меня уделал, умник;)....Пойду приходить в себя после нашего алко-поединка')
        user_game_param['game_stage']=4
        return user_game_param
    elif user_game_param['whose_turn']=='я':
        update.message.reply_text('...и ты проиграл, белковая твоя голова)) Давай ещё раз')
        user_game_param['game_stage']=0
        return zeroStage(bot,update,user_game_param)


def myGame(bot,update,user_game_param):
    chat_id=update.message.chat.id
    i_amnt=user_game_param['i_amnt']
    reply_markup = ReplyKeyboardRemove()
    glass=user_game_param['glass']
    if i_amnt!=1:
        print('myGame')
        right_decision={0:3,1:random.randint(1,3),2:1,3:2}
        my_i_amnt=right_decision[i_amnt-math.floor(i_amnt/4)*4]
        update.message.reply_text('Я выпью {}{}'.format(my_i_amnt,glass*my_i_amnt), reply_markup=reply_markup)
        user_game_param['i_amnt']=i_amnt-my_i_amnt
        user_game_param['whose_turn']='я'

        if i_amnt-my_i_amnt>1:
            update.message.reply_text('Осталось {}{}'.format(i_amnt-my_i_amnt,glass*(i_amnt-my_i_amnt)))
            update.message.reply_text('Сколько ты выпьешь?')
        elif i_amnt-my_i_amnt==1:
            update.message.reply_text('Остался {}{}...'.format(i_amnt-my_i_amnt,glass))
            return mainGame(bot,update,user_game_param)
   
        return user_game_param
    else:
        print('Я выпью последний')
        return i_amnt-1

def uGame(bot,update,user_game_param):
    text=update.message.text
    chat_id=update.message.chat.id
    reply_markup = ReplyKeyboardRemove()
    i_amnt=user_game_param['i_amnt']
    if i_amnt==1:
        return mainGame(bot,update,user_game_param)
    print('in_uGame')
    try:
        u_i_amnt=int(text)
        print(u_i_amnt)
        if u_i_amnt<4 and u_i_amnt>0 and u_i_amnt<=i_amnt:
            user_game_param['i_amnt']=i_amnt-u_i_amnt
            user_game_param['whose_turn']='ты'
            return user_game_param
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
    user_game_param['whose_turn']='я'
    return user_game_param

def champagneGame(bot,update):
    global game_dic
    chat_id=update.message.chat.id    
    user_game_param=game_dic.get(chat_id)

    if user_game_param==None:
        game_dic={chat_id:{}}
        user_game_param=game_dic.get(chat_id)
        user_game_param=zeroStage(bot,update,user_game_param)
    elif user_game_param['game_stage']==1 or user_game_param['game_stage']==2:  
        user_game_param=mainGame(bot,update,user_game_param)
    elif user_game_param['game_stage']==0:    
        user_game_param=zeroStage(bot,update,user_game_param)
    
    if user_game_param['game_stage']==4:
        the_stage='after_party'
    else:    
        the_stage='champagne_game'
    return the_stage


def zeroStage(bot,update,user_game_param):
    chat_id=update.message.chat.id

    if user_game_param.get('game_stage')==None:
        user_game_param['try']=1
        update.message.reply_text('Правила такие: у нас есть 21 или 22 бокала с бухлишком, мы по очереди выпиваем по 1, 2 или 3 бокала. '+
                                'Кто выпьет последний - тот проиграл. Я выбираю, сколько будет бокалов. Но зато ты решаешь, кто пьет первым;)')
        update.message.reply_text('Наа-а-а-аачинаем вечеринку!')
        bot.send_document(chat_id, 'https://media.giphy.com/media/l4pTddm2KUc4CKnKg/giphy.gif')
        return gameParam(bot,update,user_game_param)
    elif user_game_param.get('game_stage')==0:
        user_game_param['try']+=1
        update.message.reply_text('Правила те же: пьем по 1-му, 2 или 3 бокала. Я выбираю сколько всего выпивки, зато ты выбираешь, кто пьет первым.')
        return gameParam(bot,update,user_game_param)


def gameParam(bot,update,user_game_param):
    chat_id=update.message.chat.id

    glass=['🍷','🥃','🍸'][random.randint(0,2)]

    i_amnt=random.randint(21,22)
    if i_amnt==21:
        update.message.reply_text(('Я налила {}{} бокал'.format(i_amnt,glass*i_amnt)))
    elif i_amnt==22:
        update.message.reply_text(('Я налила {}{} бокала'.format(i_amnt,glass*i_amnt)))
    whoseTurn(bot,update)

    user_game_param['game_stage']=1
    user_game_param['i_amnt']=i_amnt
    user_game_param['glass']=glass
    return user_game_param


def whoseTurn(bot,update):
    chat_id=update.message.chat.id
    custom_keyboard = [['Я', 'Ты']]
    reply_markup = ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True, one_time_keyboard=False)
    bot.send_message(chat_id=chat_id, 
                    text="Выбери, кто будет пить первым", 
                    reply_markup=reply_markup)
