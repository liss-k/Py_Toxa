import pandas as pd

import settings, random, time, re
# import first_stage, IIII_game_tg, after_party, angry_stage
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove


# добавление логгирования бота
import logging
logging.basicConfig(format='%(name)s-%(asctime)s-%(levelname)s-%(message)s',
                    level=logging.INFO,
                    filename='feb23_bot.log'
                    )
# asctime - время события, 
# levelname - тип события, 
# message - что произошло (задаем сами)
# ----------------------------



# создай файл feb23bot_user_base.csv
# создай файл feb23bot_user_base.csv
# создай файл feb23bot_user_base.csv
# создай файл feb23bot_user_base.csv
# создай файл feb23bot_user_base.csv
# создай файл feb23bot_user_base.csv

# проверить, на какой я кухне для чита


def startBot(bot, update):
    global USER_DIC
    chat_id = update.message.chat.id
    first_name = update.message.chat.first_name
    user_name = update.message.chat.username

    if first_name==None or first_name=='None':
        if user_name == None or user_name == 'None':
            gamer_name = 'Мистер Ноунейм'
        else:
            gamer_name = user_name
    else:
        gamer_name = first_name

    
    bot_user_base = pd.read_csv('feb23bot_user_base.csv', sep=';', encoding='utf-8')

    if chat_id in bot_user_base['chat_id'].tolist():
        user_index = bot_user_base.loc[bot_user_base['chat_id'] == chat_id].index
        game_stage = str(bot_user_base.loc[user_index, 'game_stage'].values[0])
        team = bot_user_base.loc[user_index, 'team'].values[0]
        quest = bot_user_base.loc[user_index, 'quest'].values[0]
    else:
        user_index = None
        game_stage = '0'
        team = 'no team'
        quest = '0'

    if game_stage == '0':
        game_stage = '1'
        hello_text="""Привет, {}!
А ты хорош...значит, нам с тобой будет интересно...

Повторю ещё раз: чтобы получить доступ к зонам развлечений (их 2: плойка и синяя яма), тебе с командой нужно пройти 7 станций.

Первые три открывают доступ к плойке, 4,5,6,7 - к возлияниям.

Теперь важный нюанс: путь к станциям могу указать только я, но я ничего не делаю просто так.
Тебе придется разгадать мой шифр и прислать мне код-ответ. Один код - одна станция. И кстати, чтобы найти первый код, у тебя уже всё есть;)
Но помни, у всего есть двойное дно...

Если с разгадкой не складывается, ты потерян и даже не представляешь, с чего начать, можешь попросить подсказку - их я даю просто так.
Если не складывается даже с подсказкой, обратитесь в службу поддержки. На проводе сегодня: Саша Разгуляева, Лена Гайван и Алина Жукова - они поддержат...возможо даже помогут

Думаю, ты разберёшься...если у тебя не ситец вместо мозга, конечно)
        """.format(gamer_name)
        bot.send_message(chat_id=chat_id, text=hello_text, reply_markup=ReplyKeyboardRemove())
       
        hello_text="""Напиши, плз, какой номер у твоей команды?
Его нельзя будет потом поменять, поэтому я рассчитываю на твоё обдуманное и взвешенное решение.""".format(gamer_name)
        bot.send_message(chat_id=chat_id, text=hello_text, reply_markup=ReplyKeyboardRemove())   
    elif game_stage == '1' and (team == None or team == 'no team'):
        hello_text="""Привет ещё раз, {}!
А ты зачастил) И всё так же хорош) Только напиши всё-таки номер своей команды
        """.format(gamer_name)       
        bot.send_message(chat_id=chat_id, text=hello_text, reply_markup=ReplyKeyboardRemove())
    else:
        hello_text="""Привет ещё раз, {}!
А ты зачастил) И всё так же хорош)
        """.format(gamer_name)       
        custom_keyboard = [['Ответ', 'Подсказка']]
        reply_markup = ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True, one_time_keyboard=False)
        bot.send_message(chat_id=chat_id, 
                text=hello_text, 
                reply_markup=reply_markup)
    
    if user_index is not None and team != 'no team':
        game_stage = '2'
        quest = '0'
        bot_user_base.loc[user_index, :] = [chat_id, game_stage, team, quest]
    elif user_index is not None:
        game_stage = '1'
        quest = '0'
        bot_user_base.loc[user_index, :] = [chat_id, game_stage, team, quest]        
    else:
        df = pd.DataFrame([[chat_id, str(game_stage), team, quest]]
            , columns = ['chat_id', 'game_stage', 'team', 'quest']
            )
        bot_user_base = bot_user_base.append(df, ignore_index=True)
    bot_user_base.to_csv('feb23bot_user_base.csv', sep = ';', encoding='utf-8', index = False)


def chatParametrs(bot,update,job_queue):
    text=str(update.message.text)
    chat_id=update.message.chat.id
    first_name=update.message.chat.first_name
    username=update.message.chat.username

    logging.info("{} (username {}) has written {}".format(first_name, username, re.sub(r'[^\w\s]', '', text)))


    bot_user_base = pd.read_csv('feb23bot_user_base.csv', sep=';', encoding='utf-8')

    user_index = bot_user_base.loc[bot_user_base['chat_id'] == chat_id].index
    game_stage = str(bot_user_base.loc[user_index, 'game_stage'].values[0])
    team = str(bot_user_base.loc[user_index, 'team'].values[0])
    quest = str(bot_user_base.loc[user_index, 'quest'].values[0])




    if game_stage=='1':
        if text in ['1','2','3','4','5','6','7']:
            team=text
            bot_answer = '''Поздравляю, ты в игре!

Теперь ты можешь присылать мне ответы на шифры и получать доступ к станциям в оффлайн. Работает это так:
1. Ты присылаешь мне номер загадки и код 
2. Я в ответ кидаю описание места, в которое нужно идти
...ну или издеваюсь над уровнем твоего интеллекта, если ты скинул что-то не то

Для первого этапа код - это кое-какое слово, которое можно найти на листе с поцелуйчиком... Только какое именно и как найти, да? Возможно, где-то есть то, что тебе поможет)
Чтобы прислать мне кодовое слово, нажми кнопку "Ответ", выбери "1" и скинь свой вариант.

Если твой iq не дотягивает до трехзначного числа, можешь просить у меня подсказки. Для этого нажми кнопку "Подсказка"
Правила не в лужу пёрнуть, конечно, но и ты не пальцем делан ;)
            '''
            
            custom_keyboard = [['Ответ', 'Подсказка']]
            reply_markup = ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True, one_time_keyboard=False)
            bot.send_message(chat_id=chat_id, 
                    text=bot_answer, 
                    reply_markup=reply_markup)

            game_stage = '2'

        else:
            bot_answer = '''Номер команды - это циферка от 1 до 7.
Одна цифра. 
От 1 до 7.
Соберись! Нет номера - нет игры. Такие дела
            '''
            bot.send_message(chat_id=chat_id, text=bot_answer)
            game_stage = '1'


        bot_user_base.loc[user_index, :] = [chat_id, game_stage, team, quest]
        bot_user_base.to_csv('feb23bot_user_base.csv', sep = ';', encoding='utf-8', index = False)

    else:
        if text.lower() in ['славься,гайван','славься, гайван','славься гайван'
        ,'славься,гайван!','славься, гайван!','славься гайван!']:
            bot_answer, custom_keyboard, quest, game_stage = cheatAnswer(bot,update)
            reply_markup = ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True, one_time_keyboard=False)    
            bot.send_message(chat_id=chat_id, 
                    text=bot_answer, 
                    reply_markup=reply_markup)

            bot_user_base.loc[user_index, :] = [chat_id, game_stage, team, quest]
            bot_user_base.to_csv('feb23bot_user_base.csv', sep = ';', encoding='utf-8', index = False)        
            return
        else:
            theGame(bot,update,job_queue,text,bot_user_base)

def theGame(bot,update,job_queue,text,bot_user_base):
    try:
        text=str(update.message.text).lower()
        chat_id=update.message.chat.id
        first_name=update.message.chat.first_name
        username=update.message.chat.username

        user_index = bot_user_base.loc[bot_user_base['chat_id'] == chat_id].index
        game_stage = str(bot_user_base.loc[user_index, 'game_stage'].values[0])
        team = str(bot_user_base.loc[user_index, 'team'].values[0])
        quest = str(bot_user_base.loc[user_index, 'quest'].values[0])   

        # в словаре первый ключ - номер команды, лист - порядок прохождения точек
        place_dict = {'1' : [0,1,2,3,4,5,6],
        '2' : [1,2,3,4,5,6,0],
        '3' : [2,3,4,5,6,0,1],
        '4' : [3,4,5,6,0,1,2],
        '5' : [4,5,6,0,1,2,3],
        '6' : [5,6,0,1,2,3,4],
        '7' : [6,0,1,2,3,4,5]
        }
        # сейчас 7 команд и 7 мест
        # по номеру из листа в place_dict выбирается место, К КОТОРОМУ команда пытается получить доступ
        place_list = ['переговорка Рио' # 'm0' - викторина, переговорка Рио
        ,'место Лены Коваленко' # 'm1' - стулья, место Лены Коваленко
        ,'Il Lago' # 'm2' - караоке, Il Lago
        ,'красный уголок напротив Миконоса' # 'm3' - аквагрим, красный уголок напротив Миконоса
        ,'столы HR' # 'm4' - паззлы, столы HR
        ,'красный уголок напротив Рио' # 'm5' - гадалка, красный уголок напротив Рио
        ,'переговорка Верона'] # 'm6' - рисунок на спине, переговорка Верона
        
        # в словаре первый ключ - номер команды, лист - порядок получения заданий
        task_dict = {'1' : ['1','2','3','4','5','6','7'],
        '2' : ['1','3','4','5','6','7','2'],
        '3' : ['1','4','5','6','7','2','3'],
        '4' : ['1','5','6','7','2','3','4'],
        '5' : ['1','6','7','2','3','4','5'],
        '6' : ['1','7','2','3','4','5','6'],
        '7' : ['1','7','6','5','4','3','2']
        }


       
        if game_stage == '2':
            custom_keyboard = [['1', '2', '3'], ['4', '5', '6'], ['7','Вернуться']]
            reply_markup = ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True, one_time_keyboard=False)
            if text == 'ответ':
                bot_answer = '''Для какой загадки у тебя готов ответ?
Загадки идут по-порядку, и на всякий случай номер загадки написан на конверте (ну или в чём там тебе её выдали)'''
                game_stage = '3'

            elif text =='подсказка':
                bot_answer = '''Для какой загадки тебе нужна подсказка?
Загадки идут по-порядку, и на всякий случай номер загадки написан на конверте (ну или в чём там тебе её выдали)'''
                game_stage = '4'
            
            elif text in ['1','2','3','4','5','6','7']:
                custom_keyboard = [['Ответ', 'Подсказка']]
                reply_markup = ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True, one_time_keyboard=False)
                bot_answer = '''Погоди, ну вот к чему эта цифра? Ты хочешь дать ответ или получить подсказку?
Я хочу ясности, поэтому введи "ответ" или "подсказка" (они, кстати, сейчас в выпадающей клавиатуре внизу).
И только потом вводи номер этапа.
            '''            

            else:
                custom_keyboard = [['Ответ', 'Подсказка']]
                reply_markup = ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True, one_time_keyboard=False)            
                chatSticker(bot,update,custom_keyboard)
     
            bot.send_message(chat_id=chat_id, 
                text=bot_answer, 
                reply_markup=reply_markup)
    #!!!!!!! проверить, какая стадия игры, если игрок пишет не тот ответ
            
            bot_user_base.loc[user_index, :] = [chat_id, game_stage, team, quest]
            bot_user_base.to_csv('feb23bot_user_base.csv', sep = ';', encoding='utf-8', index = False)

            return

    #выбирается этап, для которого потом будет писаться ответ
        elif game_stage == '3':     
            if text in ['1','2','3','4','5','6','7']:
                custom_keyboard = [['Вернуться']]
                quest = text
                bot_answer = '''Валяй, пиши свой ответ'''
                game_stage = '5'

            elif text == 'вернуться':
                bot_answer, custom_keyboard, quest, game_stage = backFunc()
            else:
                custom_keyboard = [['1', '2', '3'], ['4', '5', '6'], ['7','Вернуться']]
                chatSticker(bot,update,custom_keyboard)

            reply_markup = ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True, one_time_keyboard=False)
            bot.send_message(chat_id=chat_id, 
                text=bot_answer, 
                reply_markup=reply_markup)
            
            bot_user_base.loc[user_index, :] = [chat_id, game_stage, team, quest]
            bot_user_base.to_csv('feb23bot_user_base.csv', sep = ';', encoding='utf-8', index = False)

            return


        elif game_stage == '4':
            if text in ['1','2','3','4','5','6','7']:
                quest = text
                task_num = task_dict.get(team)[int(quest)-1]           
                hint_dic = {'1' : '''У всего есть двойное дно...
И у тебя есть коробка, у которой есть дно...
Двойное дно и коробка с дном...
Один плюс один равно три, не иначе
            ''',
            '2' : '''У тебя в руках трафарет, его нужно куда-то наложить и посмотреть, что получится.
На стенах нам рисовать нельзя, может быть поискать на стеклах? На стеклах переговорок? На 4-м этаже их не так много;)
            ''',
            '3' : '''Как же мы бесконечно далеки друг от друга... Ну поспрашивай у кого-нибудь, что это может быть за девушка.
И в конце концов, нас всего 40, можно и перебором отыскать.
            ''',
            '4' : '''Недостаточно горяч?) Возможно поможет открытое пламя? Она любит, когда на грани...Только не сожги её, просто согрей)
И не делай этого в помещении - нет ничего более унылого, чем пожарная тревога вместо праздника 
            ''',
            '5' : '''Тебе нужно найти два слова. Они даже курсивом выделены.
И у тебя есть 2 участка с буквами. Может быть поискать их там?
И в итоге из слов получится..........
            ''',
            '6' : '''Мысли широко! Делай больше, чем нужно! Просят сложить, а ты ещё и вычти. Два получившихся результата ничего не напоминают?
            ''',
            '7' : '''Ну я даже не знаю... У тебя есть слова песни и смартфон с гуглом... Понятия не имею, что препятствует поиску исполнителя.
            '''
                }
                bot_answer = hint_dic.get(task_num)
                custom_keyboard = [['Ответ', 'Подсказка']]
                game_stage = '2'            
            elif text == 'вернуться':
                bot_answer, custom_keyboard, quest, game_stage = backFunc()
            else:
                custom_keyboard = [['1', '2', '3'], ['4', '5', '6'], ['7','Вернуться']] 
                chatSticker(bot,update,custom_keyboard)

            reply_markup = ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True, one_time_keyboard=False)
            bot.send_message(chat_id=chat_id, 
                text=bot_answer, 
                reply_markup=reply_markup)
            
            bot_user_base.loc[user_index, :] = [chat_id, game_stage, team, quest]
            bot_user_base.to_csv('feb23bot_user_base.csv', sep = ';', encoding='utf-8', index = False)

            return



        elif game_stage == '5':
            custom_keyboard = [['Вернуться']]
            # в словаре первый ключ - номер задания, второй ключ - номер команды
            answer_dict = {
                '1' : {'1' : ['путь'], #двойное дно, одинаковое ДОДЕЛАТЬ
                       '2' : ['тигр'],
                       '3' : ['пуск'],
                       '4' : ['гром'],
                       '5' : ['трюк'],
                       '6' : ['блок'],
                       '7' : ['воин', 'вино']},
                    '2' : {'1' : ['зачет', 'зачёт'], #загадка на стеклах
                           '2' : ['снежинка'],
                           '3' : ['transparency'],
                           '4' : ['еда'],
                           '5' : ['сон'],
                           '6' : ['случай'],
                           '7' : ['бегает мокрая курица']},
                        '3' : {'1' : ['одуванчик'], #найти девушку, Вита
                               '2' : ['роза'], # Панкина
                               '3' : ['василек','василёк'], # Волкова
                               '4' : ['шиповник'], # Никулина
                               '5' : ['хризантема'], # Яна
                               '6' : ['мак'], # Катя
                               '7' : ['ландыш']}, # Женя
                            '4' : {'1' : '41', #мне холодно ДОДЕЛАТЬ
                                   '2' : '42',
                                   '3' : '43',
                                   '4' : '44',
                                   '5' : '45',
                                   '6' : '46',
                                   '7' : '47'},
                                '5' : {'1' : '31', #соединить буквы
                                       '2' : '51',
                                       '3' : '21',
                                       '4' : '27',
                                       '5' : '37',
                                       '6' : '57',
                                       '7' : '31'},
                                    '6' : {'1' : '214', #эйнштейн
                                           '2' : '113',
                                           '3' : '212',
                                           '4' : '210',
                                           '5' : '414',
                                           '6' : '216',
                                           '7' : '412'},
                                        '7' : {'1' : ['Queen'],
                                               '2' : ['Deep Purple'],
                                               '3' : ['The Beatles','beatles','битлы'],
                                               '4' : ['Adele', 'adelle'],
                                               '5' : ['Воскресенье'],
                                               '6' : ['R.E.M.','rem','r e m'],
                                               '7' : ['Ленинград']}
            }
            
            place = place_dict.get(team)[int(quest)-1]
            place_name = place_list[place]

            task_num = task_dict.get(team)[int(quest)-1]

            true_answer = answer_dict.get(task_num).get(team)

            if (task_num in ['1','2','3','7']
                and text.lower() in [x.lower() for x in true_answer]) or (task_num not in ['1','2','3','7'] and text.lower() == true_answer.lower()):        
                bot_answer = '''Всё верно, игрок из команды крутышей №{}
Тебе открыта новая станция
Место: {}
Иди же скорее туда и покажи это сообщение ведущей на станции, а то не пустят ;)'''.format(team, place_name)

                game_stage = '2'
                quest = '0'
                bot_user_base.loc[user_index, :] = [chat_id, game_stage, team, quest]
                bot_user_base.to_csv('feb23bot_user_base.csv', sep = ';', encoding='utf-8', index = False)
                custom_keyboard = [['Ответ', 'Подсказка']]
                reply_markup = ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True, one_time_keyboard=False)    
                bot.send_message(chat_id=chat_id, 
                        text=bot_answer, 
                        reply_markup=reply_markup)

                return           

            elif text == 'вернуться':
                bot_answer, custom_keyboard, quest, game_stage = backFunc()
            else:
                return wrongAnswer(bot,update,custom_keyboard)


            bot_user_base.loc[user_index, :] = [chat_id, game_stage, team, quest]
            bot_user_base.to_csv('feb23bot_user_base.csv', sep = ';', encoding='utf-8', index = False)

            # custom_keyboard = [['Ответ', 'Подсказка']]
            reply_markup = ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True, one_time_keyboard=False)    
            bot.send_message(chat_id=chat_id, 
                    text=bot_answer, 
                    reply_markup=reply_markup)

    except BaseException:
        bot_answer, custom_keyboard, quest, game_stage = catchException()
        bot_user_base.loc[user_index, :] = [chat_id, game_stage, team, quest]
        bot_user_base.to_csv('feb23bot_user_base.csv', sep = ';', encoding='utf-8', index = False)

        # custom_keyboard = [['Ответ', 'Подсказка']]
        reply_markup = ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True, one_time_keyboard=False)    
        bot.send_message(chat_id=chat_id, 
                    text=bot_answer, 
                    reply_markup=reply_markup)



def backFunc():
    angry_list=['😑😑😑','😑','😶','🙄','🙄🙄🙄']
    bot_answer=angry_list[random.randint(0,len(angry_list)-1)]
    custom_keyboard = [['Ответ', 'Подсказка']]
    quest = '0'
    game_stage = '2'
    return bot_answer, custom_keyboard, quest, game_stage

def catchException():
    bot_answer='Ты словил какую-то ошибку, поэтому я просто отмотаю немного назад. Ты хочешь ввести ответ или получить подсказку?'
    custom_keyboard = [['Ответ', 'Подсказка']]
    quest = '0'
    game_stage = '2'
    return bot_answer, custom_keyboard, quest, game_stage

def chatSticker(bot,update,custom_keyboard):
    text=str(update.message.text)
    chat_id=update.message.chat.id

    general_answer=['Меня на такое не программировали','Вся жизнь театр, а мы в ней - лишь актеры','Давай без этого']
    
    bot_answer = general_answer[random.randint(0,len(general_answer)-1)]
    reply_markup = ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True, one_time_keyboard=False)    
    bot.send_message(chat_id=chat_id, 
            text=bot_answer, 
            reply_markup=reply_markup)

def wrongAnswer(bot,update,custom_keyboard):
    text=str(update.message.text)
    chat_id=update.message.chat.id

    general_answer=['Я смотрю, интеллектуальные игры - не твоя сильная сторона...'
    ,'Хлебушек вместо мозга?'
    ,'Как думаешь, у тебя или у пшеницы выше IQ?'
    ,'Мысли как мюсли, а речь как кисель...'
    ,'Я где-то слышала, что у мужчин есть логика🤔'
    ,'Попки младенцев напоминают мне от твоём мозге'
    ,'Бооожееее...ты наугад тут что ли пишешь?'
    ,'Невежество порождает собственную истину...'
    ]
    
    bot_answer = general_answer[random.randint(0,len(general_answer)-1)]
    custom_keyboard = custom_keyboard
    reply_markup = ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True, one_time_keyboard=False)    
    bot.send_message(chat_id=chat_id, 
            text=bot_answer, 
            reply_markup=reply_markup)


def cheatAnswer(bot,update):
    bot_answer = '''Четкаааарь)) Подойди к Лене и покажи ей это сообщение.
Она водит жалом на кухне или сидит на своем месте - у неё для тебя есть немного кристаллической годноты
    '''
    custom_keyboard = [['Ответ', 'Подсказка']]
    quest = '0'
    game_stage = '2'
    return bot_answer, custom_keyboard, quest, game_stage    
    

    

def main():
    updtr=Updater(settings.FEB23_TG_BOT_KEY)
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
