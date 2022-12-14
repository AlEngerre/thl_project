import logging
from aiogram import Bot, Dispatcher, executor, types
from db_work import db_search_task, answer_cor

API_TOKEN = 'BOT TOKEN HERE'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token="5815294036:AAEdxHUA0luistp4N3kpT-RdMOYIvB4uMbA")
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.answer("Привет!\nНапиши /решать (номер задания), чтобы начать решение заданий")

@dp.message_handler(commands=['решать'])
async def start_session(message: types.Message):
    try:
        inp = message.text.split()

        task_data = db_search_task(int(inp[1].strip()), message.from_user['id'])
        if task_data == 'no act':
            await message.answer(
                "Вы решили все возможные типы этого задания, которые были на нашей платформе.\nВскоре мы добавим другие вариации, а пока попрактикуйтесь в выполнении других заданий")
            return
        await message.answer_photo(open("tasks/" + task_data[1], "rb"))
        if task_data[2]:
            await message.answer_photo(open(task_data[2], "rb"))
    except:
        await message.answer("Введите корректный номер задания")


@dp.message_handler()
async def answer_check(message: types.Message):
    user_id = message.from_user["id"]
    print(user_id)
    result = answer_cor(user_id, message.text.strip())
    if result == 'no_act':
        await message.answer("Ошибка ввода.Для начала решения задач напишите /решать(номер задания)")
        return
    if result[0]:
        await message.answer("Ваш ответ верный!\n\n" + result[1])
    else:
        await message.answer("Ответ неправильный. Правильный ответ: " + result[1] + "\n\n" + result[2])


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
