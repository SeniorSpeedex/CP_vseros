import os
import subprocess
from pytube import YouTube
import speech_recognition as sr

from aiogram import Bot, Dispatcher, types, executor

API_TOKEN = '7946623770:AAFSgy7AL1lgRxcHwawPZI-kJLUzJXivKXQ'
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
recognizer = sr.Recognizer()

VIDEOS_DB_FILE = 'fpo.txt'
BAN_LIST_FILE = 'ban_list.txt'

@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    await message.reply('Commands: /start.                                                                                   '
                       'Выберите действие',
                       reply_markup=types.InlineKeyboardMarkup(
                           inline_keyboard=[
                               [
                                   types.InlineKeyboardButton('Get video url', callback_data='1'),
                                   types.InlineKeyboardButton('Data Base videos', callback_data='2'),
                                   types.InlineKeyboardButton('Ban list', callback_data='3')
                               ]
                           ]
                       ))

@dp.callback_query_handler(lambda query: query.data in ('1', '2', '3'))
async def callback_handler(query: types.CallbackQuery):
    if query.data == '1':
        await query.message.reply('Отправьте url видеоролика')
    elif query.data == '2':
        await query.message.reply(read_file(VIDEOS_DB_FILE))
    elif query.data == '3':
        await query.message.reply(read_file(BAN_LIST_FILE))
    else:
        pass

def download_audio(url):
    try:
        yt = YouTube(url)
        audio = yt.streams.filter(only_audio=True).first()
        audio_file = f"{yt.title}.mp3"
        audio.download(filename=audio_file)
        print(f"Аудио '{audio_file}' успешно скачано.")
        return audio_file
    except Exception as e:
        print(f"Ошибка при скачивании аудио: {e}")
        return None

def transcribe_audio(audio_file):
    with sr.AudioFile(audio_file) as source:
        audio = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio, language="en-US")
        print("Распознанный текст:", text)
        return text
    except sr.UnknownValueError:
        print("Ошибка распознавания речи")
    except sr.RequestError as e:
        print("Ошибка сервиса Google Speech Recognition; {0}".format(e))
    return None

@dp.message_handler()
async def download_and_transcribe(message: types.Message):
    url = message.text
    audio_file = download_audio(url)
    if audio_file:
        text = transcribe_audio(audio_file)
        if text:
            await message.reply(text)

@dp.message_handler(commands=['blis'])
async def blis_handler(message: types.Message):
    # Здесь можно реализовать логику для команды /blis
    pass

def read_file(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        print(f"Файл '{file_path}' не найден.")
        return ''
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return ''

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
