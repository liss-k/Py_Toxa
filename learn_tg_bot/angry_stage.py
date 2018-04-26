import random
from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
# -*- coding: UTF-8 -*-

def angryStage(bot,update,game_stage_dic):
    text=update.message.text
    chat_id=update.message.chat.id
    if text=='Бывает, просто молчишь, а тебя уже неправильно поняли((':
        return {'stage_name':'angry_stage'}

    if game_stage_dic['stage_name']=='final_stage':
        return finalStage(bot,update,game_stage_dic)

    try:
        game_stage_dic['msg_counter']+=1
    except (KeyError, NameError, UnboundLocalError):
        game_stage_dic={'msg_counter':0, 'score':0, 'used_list':[], 'know_rules':False}

    good_gift_dic={('🎁'):'Твои подарки делают меня счастливой! А на прыгающую от счастья женщину можно смотреть бесконечно...)',
                ('💍','💎'):'Мощно! И даже драматично!) Спасибо, милый!💖',
                ('👚','👗','👙','👠','👡','👢','👒','🎒','👝','👛','👜'):'И как ты только умудряешься угадывать, чего я хочу?)',
                ('👑'):'Ааааа, с ума сойти!!! Это приятнее, чем 10 фильмов со счастливым концом!',
                ('🕺'):'Ты подарил мне танец))) Огонь!',
                ('🌎','🌍','🌏'):'Ты готов бросить к моим ногам весь мир? Мой рыцарь!',
                ('🌞','💫','⭐️','🌟','✨','☀️'):'Звезда с неба...Это так притягательно...если ты понимаешь каламбуры про гравитацию))'
                }
    bad_gift_dic={('🥀'):'Квёлая роза чёт не возбуждает',
                ('💩'):'Какуля??? Ты подарил мне какулю???!! Очевидное, но бесполезое решение',
                ('☔','🌂','☂'):'Ваааа-а-ажнеее-ей всегоооо, погоооода в до-о-оме...Ну такое',
                ('🍆'):'🍆💦',
                ('🥄','🍴','🍽','🥣','🥡','🥢'):'А еды? Еды дадут?',
                ('🥛','🍼','🥤'):'Это нас ни к чему не приведет...',
                ('🌕','🌖','🌗','🌘','🌑','🌒','🌓','🌔','🌚','🌝','🌛','🌜','🌙'):'Во имя луны! Но нет...это не то...',
                ('❤️','❤','💚','💛','💙','💜','🖤','💘','💖','💗','💓','💞','💕','❣️','💝','💟','😘'):'Ого, слова любви...с козырей пошел?) Но я, знаешь ли, материалистка',
                ('💐','🌷','🌹','🌻','🌼','🌸','🌺'):'Фак, еееаахх! Но, может, что-то чуточку менее банальное?',
                ('🍶','🍺','🍻','🥂','🍷','🥃','🍸','🍹','🍾'):'Ты лучший, правда! Но сегодня пить я уже больше не могу((( Сама не рада((',
                ('🍏','🍎','🍐','🍊','🍋','🍌','🍉','🍇','🍓','🍈','🍑','🍒','🥠','🥧',
                '🍍','🥝','🥑','🍅','🥒','🥕','🌽','🌶','🥔','🍠','🌰','🥥','🥦','🥨',
                '🍳','🥚','🧀','🥖','🍞','🥐','🍯','🥜','🥓','🥞','🍤','🍗','🥩','🥪','🥫',
                '🍖','🍕','🌭','🍔','🍜','🍝','🥘','🥗','🌯','🌮','🥙','🍟','🥟',
                '🍲','🍥','🍣','🍱','🍛','🍙','🍚','🍘','🍮','🎂','🍰','🍦',
                '🍨','🍧','🍡','🍢','🍭','🍬','🍫','🍿','🍩','🍪'):'Оооо, едааа!! Это чтобы я не подохла с голоду, пока ты думаешь, как растопить лёд между нами?',
                ('☕️','🍵'):'Ты такой внимательный💋 Засчитаю этот жест за половину подарка🤗'
                }


    for key in good_gift_dic.keys():
        if text in key:
            if text in game_stage_dic['used_list']:
                bot_answer='Что-то похожее уже было...А я во всем люблю разнообразие'
            else:
                bot_answer=good_gift_dic[key]

                game_stage_dic['score']+=1
                game_stage_dic['used_list'].extend(key)
                if game_stage_dic['score']==4:
                    return finalStage(bot,update,game_stage_dic)
                else:
                    if game_stage_dic['score']==3:
                        present='подарок'
                    else:
                        present='подарка'
                    bot_answer2='Еще {} {} и Виктория посыпется'.format(4-game_stage_dic['score'],present)


    for key in bad_gift_dic.keys():
        if text in key:
            if text in game_stage_dic['used_list']:
                bot_answer='Что-то такое уже было...И нет, ни со второго, ни с третьего раза это не прокатит))'
            else:
                bot_answer=bad_gift_dic[key]
                game_stage_dic['used_list'].extend(key)

    if game_stage_dic['msg_counter']>1 and game_stage_dic['know_rules']==False:
        custom_keyboard=[['Я не понимаю, что мне делать???']]
        reply_markup = ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True, one_time_keyboard=False)
    else:
        reply_markup=ReplyKeyboardRemove()


    try:
        if bot_answer=='Во имя луны! Но нет...это не то...':
            bot.send_document(chat_id, 'https://media.giphy.com/media/26gBjmGEsrFQlj8g8/giphy.gif')
        elif bot_answer=='Твои подарки делают меня счастливой! А на прыгающую от счастья женщину можно смотреть бесконечно...)':
            bot.send_document(chat_id, 'https://media.giphy.com/media/MYwekYh3UIHGE/giphy.gif')
        elif bot_answer=='Ааааа, с ума сойти!!! Это приятнее, чем 10 фильмов со счастливым концом!':
            bot.send_document(chat_id, 'https://media.giphy.com/media/3oEhn7OTiXi4mYReyQ/giphy.gif')
        bot.send_message(chat_id=chat_id, text=bot_answer, reply_markup=reply_markup)

    except (UnboundLocalError):
        if text=='Я не понимаю, что мне делать???':
            game_stage_dic['know_rules']=True
            reply_markup=ReplyKeyboardRemove()
            bot_answer='Мужчины...'
            bot.send_message(chat_id=chat_id, text=bot_answer, reply_markup=reply_markup)
            bot_answer='Ты глубоко ранил меня своей холодностью и равндушием...Не знаю, может быть подарки, штуки 4, помогли бы затянуться моей ране быстрее?'
            bot.send_message(chat_id=chat_id, text=bot_answer)
            bot_answer='Уверена, в местном наборе эмодзи найдется то, что нужно😉 Только давай не больше одного за сообщение - я люблю растягивать удовольствие'
            bot.send_message(chat_id=chat_id, text=bot_answer)
        else:
            lol_answer_list=['Ты вообще умеешь угождать?','А ведь взрослый, умный мужчина...эх...','🤦‍♀️']    
            bot_answer=lol_answer_list[random.randint(0,len(lol_answer_list)-1)]  
            bot.send_message(chat_id=chat_id, text=bot_answer, reply_markup=reply_markup)
    try:
        bot.send_message(chat_id=chat_id, text=bot_answer2)
    except (UnboundLocalError):
        pass

    game_stage_dic['stage_name']='angry_stage'
    return game_stage_dic

def finalStage(bot,update,game_stage_dic):
    text=update.message.text
    chat_id=update.message.chat.id
    bot.send_document(chat_id, 'https://media.giphy.com/media/2wScRSlgARKGggbIq9/giphy.gif')
    bot.send_message(chat_id=chat_id, text='Ты победитель, ботов укротитель!!!!!')
    game_stage_dic['stage_name']='final_stage'
    return game_stage_dic
