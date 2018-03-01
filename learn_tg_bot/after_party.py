import time, settings, random, angry_stage
from telegram.ext import Updater
from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

def callback_minute(bot, job):
    chat_id=job.context['chat_id']

    miss_u_dic={1:['Что нового?','Что не пишешь?)','Форматировала диск и вспомнила о тебе...','Кстати, ты мне недавно приснился))'],
                2:['CAADAgADQgIAAsxUSQlsqyxHz6F20QI','CAADAwADngUAAr-MkARFA8S_d7Z4JwI','CAADAgADog8AAkKvaQABg3l_IOROTQEC','CAADAQADxAUAAr-MkAR0SG3e07gfIwI'], 
                3:['Ты куда пропал, щегол?))','Ну гдеее ты?', 'Занят чем-то?'],
                4:['Ясно...','Очень по-мужски...'],
                5:['https://media.giphy.com/media/xUOwG2kp7QQMH28JnW/giphy.gif']
                }
    custom_keyboard_dic={1:'',
                        2:[['❤ Ты изысканна, как кровь единорога'],['☠ Выглядишь, как картофелина']], 
                        3:[['Выкладываю палец в инстаграм'],['Смакую горечь несбывшихся надежд']],
                        4:[['Бывает, просто молчишь, а тебя уже неправильно поняли((']],
                        }
    job.context['msg_counter']+=1
    job.interval=random.randint(15,25)

    answer_list=miss_u_dic[job.context['msg_counter']]
    bot_answer=answer_list[random.randint(0,len(answer_list)-1)]
    custom_keyboard=custom_keyboard_dic.get(job.context['msg_counter'])
 
    if job.context['msg_counter']==2:
        reply_markup = ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True, one_time_keyboard=False)
        bot.send_sticker(chat_id=chat_id, sticker=bot_answer, reply_markup=reply_markup)

    elif job.context['msg_counter']<5:    
        if job.context['msg_counter']==1:
            reply_markup=ReplyKeyboardRemove()
        else:
            reply_markup = ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True, one_time_keyboard=False)
        bot.send_message(chat_id=chat_id, text=bot_answer, reply_markup=reply_markup)

    elif job.context['msg_counter']==5:
        reply_markup=ReplyKeyboardRemove()
        bot.send_document(chat_id, bot_answer, reply_markup=reply_markup)
        bot.send_message(chat_id=chat_id, text='Это был последний шанс😤')
        job.schedule_removal()


def afterParty(bot,update,job_queue,game_stage_dic):
    chat_id=update.message.chat.id
    message_id=update.message.message_id
    text=update.message.text

    try:
        game_stage_dic['job'].schedule_removal()
        if game_stage_dic['job'].context['msg_counter']==4 and text=='Бывает, просто молчишь, а тебя уже неправильно поняли((':
            update.message.reply_text('В твоих словах чувствуется сила и глубина...Телкам нравятся глубокие личности;)', reply_markup=ReplyKeyboardRemove())
            update.message.reply_text('...но все равно я обиделась!😤')
            bot.send_document(chat_id, 'https://media.giphy.com/media/xUOwG2kp7QQMH28JnW/giphy.gif')
            game_stage_dic={'stage_name':'angry_stage'}
            return game_stage_dic
        elif game_stage_dic['job'].context['msg_counter']==5:
            game_stage_dic={'stage_name':'angry_stage'}
            return game_stage_dic
    except (KeyError, NameError):
        game_stage_dic={'stage_name':'after_party','message_id':message_id, 'msg_counter':0}
    
    pretense_list=['Что-то я устала...',
                    'Я не в настроении',
                    'Ээээ...знаешь, у меня тут планы...да, кое-какие другие планы',
                    'Ты можешь не дышать? Мне громко и дует😑',
                    '😑','🙄',
                    'Ммммм, мои рыбки заболели холерой, а ближайший специалист в Танзании... Мне надо ненадолго отъехать'
                    ]
    bot.send_message(chat_id=chat_id, text=pretense_list[random.randint(0,6)], reply_markup=ReplyKeyboardRemove())
    user_dic={}
    user_dic['chat_id']=chat_id
    user_dic['message_id']=message_id    
    user_dic['msg_counter']=0
    user_dic['job_queue']=job_queue


    j=job_queue.run_repeating(callback_minute, interval=15, first=15, context=user_dic)
    game_stage_dic['job']=j
    return game_stage_dic