#!/home/ncsadmin/EnvPy/bStf-env/bin/python
import sys
import time
import telepot
from telepot.loop import MessageLoop
from pathlib import Path
import datetime
import glob
import subprocess
import logging
import findOrcs_bot
from findOrcs_bot import *

logging.basicConfig(filename='findOrk.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(content_type, chat_type, chat_id)
    logging.debug(content_type, chat_type, chat_id)
    if content_type == 'text' and 'start' not in msg["text"]:
        print(msg["text"])
        logging.debug(msg["text"])
        global name
        name = msg["text"]
        bot.sendMessage(chat_id, f"Дякую, працюємо з... {name}")
        # bot.sendMessage(chat_id, f"Перевіряємо орка по таких сайтах{main()}")
        who_sent = msg['from']['first_name']
        print(f'Name was sent by...{who_sent}')
        logging.debug(f'Name was sent by...{who_sent}')
        prepareFolder(chat_id, who_sent)
        subprocess.call(['bash', '../file_create.sh', name])
        run_script(chat_id)

    elif content_type == 'text':
        bot.sendMessage(chat_id, "Привіт, для перевірки орків. Напиши тут ім'я та призвіще орка "
                                 "\n або закинь сюди список орків у csv форматі")
        print(msg["text"])
        logging.debug(msg["text"])

    if content_type == 'document':
        print(msg)
        who_sent = msg['from']['first_name']
        print(f'Doc was sent by...{who_sent}')
        logging.debug(f'Doc was sent by...{who_sent}')
        prepareFolder(chat_id, who_sent)
        """processing file got from user. Saving and renaming it to keyword list"""
        file_id = msg['document']['file_id']
        print(file_id)
        logging.debug(file_id)
        inputFile = 'keyword_list.csv'
        print(f'Downloading file to {inputFile}')
        logging.debug(f'Downloading file to {inputFile}')
        bot.download_file(file_id, inputFile) #downloading file
        bot.sendMessage(chat_id, "Дякую, файл отриманий і опрацьовується... Треба почекати...")
        run_script(chat_id)

def prepareFolder(chat_id, who_sent):
    # ##### download_file, smaller than one chunk (65K)
    TIMESTAMP = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    os.chdir(f'{os.environ.get("HOME")}/PycharmProjects/pythonProject1')
    get_home_dir = os.getcwd()
    print(f'Working dir is changed to home folder {get_home_dir}')
    global directory
    directory = f'dir_{chat_id}_{who_sent}_{TIMESTAMP}'
    print(f'Directory: {directory}')
    logging.debug(f'Directory: {directory}')
    Path(directory).mkdir(exist_ok=True)  # creating a new directory if not exist
    print(f'Directory is made... {directory}')
    logging.debug(f'Directory is made... {directory}')
    os.chdir(f'./{directory}')  # changing directory to run script
    get_dir = os.getcwd()
    print(f'Working dir is changed to {get_dir}')
    return directory

def run_script(chat_id):
    findOrcs_bot.main() #EXECUTE MAIN SCRIPT
    # let the human know that the file is on its way
    bot.sendMessage(chat_id, "готую файл для відправки ...")
    file = glob.glob(f"output.csv")
    print(file)  # glob returns file in list format :(
    logging.debug(file)  # glob returns file in list format :(
    # send the pdf doc
    bot.sendDocument(chat_id=chat_id, document=open(file[0], 'rb'))
    bot.sendMessage(chat_id, "Тримай!")
    os.chdir(f'{os.environ.get("HOME")}/PycharmProjects/pythonProject1') #return to parent folder
    get_home_dir = os.getcwd()
    print(f'Done! Working dir is changed to home folder {get_home_dir}')
    bot.sendMessage(chat_id, "Чекаю ім'я іншого орка або список")


# replace XXXX.. with your token
TOKEN = os.environ.get('ORKBOT')

bot = telepot.Bot(TOKEN)
MessageLoop(bot, handle).run_as_thread()
print('Listening ...')
logging.debug('Listening ...')
# Keep the program running.
while 1:
    time.sleep(10)
