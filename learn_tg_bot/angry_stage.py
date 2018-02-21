import random
from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
# -*- coding: UTF-8 -*-

def angryStage(bot,update):
    text=update.message.text
    chat_id=update.message.chat.id
    if text=='Бывает, просто молчишь, а тебя уже неправильно поняли((':
        return 'angry_stage'

    global ANGRY_STAGE_DIC
    try:
        ANGRY_STAGE_DIC[chat_id]['msg_counter']+=1
    except (KeyError, NameError, UnboundLocalError):
        ANGRY_STAGE_DIC={chat_id:{'msg_counter':0, 'score':0, 'used_list':[], 'know_rules':False}}

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
            if text in ANGRY_STAGE_DIC[chat_id]['used_list']:
                bot_answer='Что-то похожее уже было...А я во всем люблю разнообразие'
            else:
                
                bot_answer=good_gift_dic[key]
                ANGRY_STAGE_DIC[chat_id]['score']+=1
                ANGRY_STAGE_DIC[chat_id]['used_list'].extend(key)
                if ANGRY_STAGE_DIC[chat_id]['know_rules']==True:
                    if ANGRY_STAGE_DIC[chat_id]['score']==4:
                        bot_answer2='Ты победитель, ботов укротитель!!!!!'
                    else:
                        bot_answer2='Еще {} и Виктория посыпется'.format(4-ANGRY_STAGE_DIC[chat_id]['score'])
    

    for key in bad_gift_dic.keys():
        if text in key:
            if text in ANGRY_STAGE_DIC[chat_id]['used_list']:
                bot_answer='Что-то такое уже было...И нет, ни со второго, ни с третьего раза это не прокатит))'
            else:
                bot_answer=bad_gift_dic[key]
                ANGRY_STAGE_DIC[chat_id]['used_list'].extend(bad_gift_dic[key])
                ANGRY_STAGE_DIC[chat_id]['used_list'].extend(key)

    if ANGRY_STAGE_DIC[chat_id]['msg_counter']>1 and ANGRY_STAGE_DIC[chat_id]['know_rules']==False:
        custom_keyboard=[['Я не понимаю, что мне делать???']]
        reply_markup = ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True, one_time_keyboard=False)
    else:
        reply_markup=ReplyKeyboardRemove()


    try:
        if bot_answer=='Во имя луны! Но нет...это не то...':
            bot.send_document(chat_id, 'https://media.giphy.com/media/26gBjmGEsrFQlj8g8/giphy.gif')
        elif bot_answer=='Твои подарки делают меня счастливой! А на прыгающую от счастья женщину можно смотреть бесконечно...)':
            bot.send_document(chat_id, 'https://media.giphy.com/media/MYwekYh3UIHGE/giphy.gif')
        elif bot_answer=='Ааааа, с ума сойти!!! Спасибо тебе!!!!':
            bot.send_document(chat_id, 'https://media.giphy.com/media/3oEhn7OTiXi4mYReyQ/giphy.gif')
        bot.send_message(chat_id=chat_id, text=bot_answer, reply_markup=reply_markup)
        try:
            bot.send_message(chat_id=chat_id, text=bot_answer2)
        except (UnboundLocalError):
            pass

    except (UnboundLocalError):
        if text=='Я не понимаю, что мне делать???':
            ANGRY_STAGE_DIC[chat_id]['know_rules']=True
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
    
    if ANGRY_STAGE_DIC[chat_id]['score']==4:
        return 'final_stage'
    else:
        return 'angry_stage'
