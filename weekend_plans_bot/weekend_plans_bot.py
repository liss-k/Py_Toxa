# weekendChannel chat_id=-1001345851244

import settings
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, JobQueue


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

import requests
import pandas as pd
from bs4 import BeautifulSoup


def startBot(bot, update, job_queue):
    chat_id=update.message.chat.id

    chat_id_series = pd.read_csv('bot_user_base.csv', sep='\t', encoding='utf-8', squeeze = True, header = None)
    if chat_id not in chat_id_series.tolist():
        chat_id_series.append(pd.Series([chat_id])).to_csv('bot_user_base.csv', sep = '\t', encoding = 'utf-8', index = False
            , header = None)

    logging.info("User {} (username {}) has pressed the button /start".format(update.message.chat.first_name, update.message.chat.username))

    if len(job_queue.jobs())>=1:
        pass
    else:
        update_job = job_queue.run_repeating(updatePlans, interval=10800, first=0, context = chat_id)

def stopBot(bot, update):
    chat_id = update.message.chat.id
    chat_id_series = pd.read_csv('bot_user_base.csv', sep='\t', encoding='utf-8', squeeze = True, header = None)
    if chat_id in chat_id_series.tolist():
        chat_id_series.append(pd.Series([chat_id])).to_csv('bot_user_base.csv', sep = '\t', encoding = 'utf-8', index = False
            , header = None)
    chat_id_series[chat_id_series != chat_id].to_csv('bot_user_base.csv', sep = '\t', encoding = 'utf-8', index = False
        , header = None)
        


def updatePlans(bot, job):
    title_base_df = pd.read_csv('title_base.csv', sep = '\t', encoding='utf-8')
    source_list = title_base_df.iloc[:,0].tolist()
    for source in source_list:
        if source == 'the_village':
            url = 'https://www.the-village.ru/village/weekend/weekend-plans/'
            main_link = 'https://www.the-village.ru'
            class_to_find_for_title = "post-title"
        elif source == 'afisha':
            url = 'https://daily.afisha.ru/series/62-plany-na-vyhodnye/'
            main_link = 'https://daily.afisha.ru'
            class_to_find_for_title = "entry__title"
        elif source == 'tatler':
            url = 'https://www.tatler.ru/guide/'
            main_link = 'https://www.tatler.ru'
            class_to_find_for_title = "title title--type-3 mt-5-m"
        elif source == 'vogue':
            return None    



        r = requests.get(url)
        if r.status_code != 200:
            last_title = 'Что-то не так с ресурсом "{}"'.format(source)
            last_link = None
        soup = BeautifulSoup(r.text, 'html.parser')
    # найти все названия
    #     print(soup.find_all(class_="post-title"))
        last_title = soup.find(class_=class_to_find_for_title).text.strip()
        
        
        prev_title = pd.Series.tolist(title_base_df[title_base_df['source'] == source]['title'])
        if last_title == prev_title[0]:
            pass
        else:
            if source == 'the_village':
                last_link = soup.find(class_="post-block post-block-featured post-block-featured-h201").find('a', href=True)['href']
            elif source == 'afisha':
                last_link = soup.find(class_="entry__link")['href']
            elif source == 'tatler':
                last_link = soup.find(class_="title title--type-3 mt-5-m").find('a', href=True)['href']


            source_index = title_base_df[title_base_df['source'] == source].index
            title_base_df.loc[source_index, 'title'] = last_title
            title_base_df.loc[source_index, 'link'] = last_link
            title_base_df.to_csv('title_base.csv', sep = '\t', encoding='utf-8', index = False)
            sendText(bot, last_title, last_link, main_link)




def sendText(bot, last_title, last_link, main_link):
    chat_id_series = pd.read_csv('bot_user_base.csv', sep='\t', encoding='utf-8', squeeze = True, header = None)
    for chat_id in chat_id_series.tolist():
        bot.send_message(chat_id=chat_id, text="{}{}".format(main_link, last_link))

    

def main():
    updtr=Updater(settings.WEEKEND_BOT_KEY)

# Добавляем хендлеры в диспетчер    
    updtr.dispatcher.add_handler(CommandHandler("start", startBot, pass_job_queue=True))
    updtr.dispatcher.add_handler(CommandHandler("stop", stopBot))
    # updtr.dispatcher.add_handler(MessageHandler(Filters.text, chatParametrs, pass_job_queue=True))

# Начинаем поиск обновлений
    updtr.start_polling()
# Останавливаем бота, если были нажаты Ctrl + C
    updtr.idle()


if __name__=="__main__":
    logging.info('Bot started')
    main()

