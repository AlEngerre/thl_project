import logging
from aiogram import Bot, Dispatcher, executor, types
from db_work import db_search_task, answer_cor, is_solving, del_by_id
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

r = {}
API_TOKEN = 'BOT TOKEN HERE'
print(r)
button_yes = KeyboardButton('Да')
button_no = KeyboardButton('Нет')

check_kb = ReplyKeyboardMarkup()
check_kb.add(button_yes)
check_kb.add(button_no)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token="")
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.answer(
        "Привет!\nНапиши /решать (номер задания), чтобы начать решение заданий(Пока в системе доступны задания 1-10)",
                                 reply_markup=ReplyKeyboardRemove(True))


@dp.message_handler(commands=['решать'])
async def start_session(message: types.Message):
    del_by_id(message.from_user['id'])
    while message.from_user['id'] in r.keys():
        del r[message.from_user['id']]
    try:
        inp = message.text.split()
        if int(inp[1]) > 15 or int(inp[1]) < 1:
            raise TypeError
        task_data = db_search_task(int(inp[1].strip()), message.from_user['id'])
        if task_data == 'no act':
            await message.answer(
                "Вы решили все возможные типы этого задания, которые были на нашей платформе.\nВскоре мы добавим другие вариации, а пока попрактикуйтесь в выполнении других заданий",
                                 reply_markup=ReplyKeyboardRemove(True))
            return
        print(task_data)
        if task_data[2]:
            await message.answer(task_data[2],
                                 reply_markup=ReplyKeyboardRemove(True))
        if task_data[1]:
            await message.answer_photo(open("tasks/" + task_data[1], "rb"),
                                 reply_markup=ReplyKeyboardRemove(True))

    except:
        await message.answer("Введите корректный номер задания",
                                 reply_markup=ReplyKeyboardRemove(True))


@dp.message_handler()
async def answer_check(message: types.Message):
    user_id = message.from_user["id"]
    if not is_solving(user_id):
        await message.reply("Ошибка ввода.Для начала решения задач напишите /решать и номер задания",
                                 reply_markup=ReplyKeyboardRemove(True))
        return
    if message.text.lower() == 'да' and user_id in r.keys():
        result = answer_cor(user_id, r[message.from_user["id"]])
        if result == 'no_act':
            await message.reply("Ошибка ввода.Для начала решения задач напишите /решать и номер задания",
                                 reply_markup=ReplyKeyboardRemove(True))
            return
        if result[0]:
            await message.answer("Ваш ответ верный!\n\n" + str(
                result[1] + '\nДля дальнейшего решения заданий напишите /решать и номер задания'),
                                 reply_markup=ReplyKeyboardRemove(True))
            del r[message.from_user["id"]]
        else:
            await message.answer("Ответ неправильный. Правильный ответ: " + str(result[1]) + "\n\n" + result[
                2] + '\nДля дальнейшего решения заданий напишите /решать и номер задания',
                                 reply_markup=ReplyKeyboardRemove(True))
            del r[message.from_user["id"]]
        return
    elif message.text.lower() == 'нет' and user_id in r.keys():
        del r[message.from_user['id']]
        await message.answer("Ваш ответ отменён",
                                 reply_markup=ReplyKeyboardRemove(True))
        return
    if message.from_user["id"] in r.keys():
        del r[message.from_user["id"]]
    r[user_id] = message.text.strip()
    await message.answer("Ваш ответ - " + message.text + '?',
                         reply_markup=check_kb)
    return


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
