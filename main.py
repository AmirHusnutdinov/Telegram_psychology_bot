import logging
from telegram.ext import Application, MessageHandler, filters, CommandHandler, ConversationHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
import random
import aiohttp

# from telegram.ext import ApplicationBuilder
BOT_TOKEN = '6188292983:AAEiOG7lgCOOUT85Sam83Zq2q_55U1N2ZV0'

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)


def main():
    # proxy_url = "socks5://user:pass@host:port"
    # app = ApplicationBuilder().token(BOT_TOKEN).proxy_url(proxy_url).build()
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("help", help_))
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("close", close_keyboard))
    application.add_handler(CommandHandler("site", site))
    application.add_handler(CommandHandler("about", about))
    application.add_handler(CommandHandler("posts", posts))
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("answers", answers)],
        states={
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, first_response)],
            2: [MessageHandler(filters.TEXT & ~filters.COMMAND, second_response)],
            3: [MessageHandler(filters.TEXT & ~filters.COMMAND, third_response)],
            4: [MessageHandler(filters.TEXT & ~filters.COMMAND, fourth_response)],
            5: [MessageHandler(filters.TEXT & ~filters.COMMAND, fifth_response)]
        },
        fallbacks=[CommandHandler("stop", stop)]
    )

    application.add_handler(conv_handler)
    application.add_handler(MessageHandler(filters.TEXT, dialog))
    application.run_polling()


async def dialog(update, _):
    phrase = []
    alfabet = list('abcdefghijklmnopqrstuvwxyzабвгдеёжзийклмнопрстуфхцчшщъыьэюя ')

    for char in list(update.message.text.lower()):
        if char.lower() in alfabet:
            phrase.append(char)
    phrase = ''.join(phrase)

    hello = ['привет', 'здравствуй', 'здравствуйте', 'приветствую',
             'доброго времени суток', 'бонжур', 'намасте', 'hello', 'hi', 'доброе утро', 'добрый день',
             'добрый вечер', 'доброй ночи', 'утречко']

    answer_for_hello = ['Привет', 'Здравствуй', 'Здравствуйте', 'Приветствую', 'Доброго времени суток', 'Бонжур',
                        'Намасте', 'Пока:) Извините я шучу, рад вас видеть', 'Давненько не виделись', 'Рад вас видеть',
                        'Хай']

    hau = ['как дела', 'как жизнь', 'как настроение', 'как настрой', 'как поживаете', 'как вы себя чувствуете',
           'как прошел ваш день', 'как вы себя чувствуете', 'как твои дела', 'как ваши дела', 'как делишки', 'а у вас',
           'а как вы поживаете', 'а вы', 'а у вас как']

    mates = ['сука', 'нахуй', 'блять', 'пиздец', 'пизда', 'ебать', 'заебись', 'пидор', 'хуй', 'пидорас']
    mate_flag = False

    conditions_good = ['хорошо', 'отлично', 'замечательно', 'великолепно', 'пойдет', 'словно',
                       'превосходно', 'фантастически', 'сказочно', 'на 5 с плюсом', 'неплохо', 'супер', 'круто']

    conditions_bad = ['плох', 'ужасн', 'грустн', 'печальн', 'одинок', 'противн', 'мерзк', 'отвратительн',
                      'угнетающе', 'гнетуще', 'не очень', 'разочарованн', 'безысходн' 'паршив']

    for mate in mates:
        if mate in phrase:
            await update.message.reply_text('Я вас прошу глубоко вдохните, выдохните и больше не материтесь')
            mate_flag = True
            break

    if not mate_flag:
        for word_hello in hello:
            if word_hello in phrase:
                await update.message.reply_text(f'{answer_for_hello[random.randrange(0, 11)]},'
                                                f' {hau[random.randrange(0, len(hau))]}?')
                break

        for word_hau in hau:
            if word_hau in phrase:
                await update.message.reply_text(f'{conditions_good[random.randrange(0, len(conditions_good))]},'
                                                f' спасибо')
                break

        bad_flag = False
        for condition in conditions_bad:
            if condition in phrase:
                await update.message.reply_text('Сочувствую вам, если так бывает слишком часто, то я думаю вам '
                                                'бы стоило написать нашим психологам они точно вам помогут!')
                bad_flag = True
                break

        if not bad_flag:
            for condition in conditions_good:
                if condition in phrase:
                    await update.message.reply_text('Я очень за вас рад!')
                    break


async def start(update, _):
    reply_keyboard = [['/posts', '/events', '/about', '/answers'],
                      ['/site', '/start', '/close', '/stop']]

    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

    user = update.effective_user
    answer_for_hello = ['Привет', 'Здравствуй', 'Здравствуйте', 'Приветствую',
                        'Доброго времени суток', 'Бонжур', 'Намасте', 'Рад вас видеть',
                        'Хай']

    hau = ['как дела', 'как жизнь', 'как настроение', 'как настрой',
           'как поживаете', 'как вы себя чувствуете', 'как прошел ваш день', 'как вы себя чувствуете']

    await update.message.reply_text(
        f"{answer_for_hello[random.randrange(0, len(answer_for_hello))]}"
        f" {user.mention_html().split('>')[1].split('<')[0]}👋.\nМеня зовут бот Эрнис,"
        f" {hau[random.randrange(0, len(hau))]}?",
        reply_markup=markup
    )


async def help_(update, _):
    await update.message.reply_text(
        "Доступные команды:\n")


async def close_keyboard(update, _):
    await update.message.reply_text(
        "Ok",
        reply_markup=ReplyKeyboardRemove()
    )


async def site(update, _):
    user = update.effective_user
    await update.message.reply_text(f"{user.mention_html().split('>')[1].split('<')[0]} это наш сайт,\n"
                                    "переходи, там так много всего интересного и"
                                    " познавательного👇\n http://127.0.0.1:8080/")


async def about(update, _):
    await update.message.reply_text("Mindease\nМы предоставляет квалифицированную психологическую помощь"
                                    " подросткам,\nкоторые сталкиваются с жизненными трудностями.\n"
                                    " Проводим частные виртуальные консультации, а также групповые программы и"
                                    " семинары с целью повышения самосознания и управления эмоциями.\n"
                                    " Наша цель — помочь вам найти эффективные механизмы выживания и"
                                    " достичь более высокого уровня жизни.\n\nЗаинтересовало?\nТогда скорей переходи по"
                                    " этой ссылке на сайт👇\n http://127.0.0.1:8080/")


async def posts(update, _):
    blog_api_url = "http://127.0.0.1:8080/api/blog"
    response = await get_response(blog_api_url, params={
        "apikey": "Your Api key",
        "format": "json"
    })

    if not response:
        await update.message.reply_text('Ошибка выполнения запроса!')
    else:
        for i in response:
            await update.message.reply_text(i)


async def answers(update, _):
    await update.message.reply_text('Итак чтобы задать вопрос пожалуйста напишите почту,\n'
                                    'на которую вы хотите получить ответ.\n'
                                    'Если хотите прервать задавание вопроса впишите команду /stop')
    return 1


async def first_response(update, context):
    context.user_data['email'] = update.message.text
    await update.message.reply_text(
        f"Отлично, почта у нас есть, хотелось бы узнать ваше имя")
    return 2


async def second_response(update, context):
    context.user_data['name'] = update.message.text
    await update.message.reply_text(f"Отлично {update.message.text} внимательно слушаю твой вопрос")
    return 3


async def third_response(update, context):
    context.user_data['answer'] = update.message.text
    reply_keyboard = [['да', 'имя', 'почта', 'сам вопрос']]

    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    await update.message.reply_text(f"Отлично {context.user_data['name']} теперь проверь все ли ты указал верно:\n"
                                    f"Имя -- {context.user_data['name']}\n"
                                    f"Почта -- {context.user_data['email']}\n"
                                    f"Вопрос-- {context.user_data['answer']}\n\nЕсли все верно то напиши 'да' если нет,"
                                    f" то напиши в чем описался\n"
                                    f"Для удобства можешь воспользоваться кнопками", reply_markup=markup)
    return 4


async def fourth_response(update, context):
    if update.message.text.lower() == 'да':
        answers_api_url = "http://127.0.0.1:8080/api/add_answer"
        email = context.user_data['email']
        name = context.user_data['name']
        answer = context.user_data['answer']
        response = await get_response(answers_api_url, params={
            "apikey": "Your Api key",
            "format": "json",
            "email": email,
            "name": name,
            "answer": answer
        })
        if not response:
            await update.message.reply_text('Тут происходят пространственные аномалии')
        for key in response:
            if key == 'success':
                await update.message.reply_text('Вопрос успешно отправлен, будут еще пишите, не стесняйтесь')
                return ConversationHandler.END

            elif key == 'error':
                await update.message.reply_text('Простите какие-то неполадки с сервером, попробуйте позже')
                return ConversationHandler.END
            else:
                await update.message.reply_text('Тут происходят пространственные аномалии')
                return ConversationHandler.END

    elif update.message.text.lower() == 'имя':
        context.user_data['change'] = 'name'
        await update.message.reply_text('Введите нужное имя')
        return 5

    elif update.message.text.lower() == 'почта':
        context.user_data['change'] = 'email'
        await update.message.reply_text('Введите нужную почту')
        return 5

    elif update.message.text.lower() == 'вопрос':
        context.user_data['change'] = 'answer'
        await update.message.reply_text('Введите свой вопрос')
        return 5


async def fifth_response(update, context):
    if context.user_data['change'] == 'name':
        context.user_data['name'] = update.message.text
    elif context.user_data['change'] == 'email':
        context.user_data['email'] = update.message.text
    elif context.user_data['change'] == 'answer':
        context.user_data['answer'] = update.message.text
    await update.message.reply_text(f"Понял, принял, обработал")

    answers_api_url = "http://127.0.0.1:8080/api/add_answer"
    email = context.user_data['email']
    name = context.user_data['name']
    answer = context.user_data['answer']
    response = await get_response(answers_api_url, params={
        "apikey": "Your Api key",
        "format": "json",
        "email": email,
        "name": name,
        "answer": answer
    })
    for key in response:
        if key == 'success':
            await update.message.reply_text('Вопрос успешно отправлен, будут еще пишите, не стесняйтесь')
            return ConversationHandler.END

        elif key == 'error':
            await update.message.reply_text('Простите какие-то неполадки с сервером, попробуйте позже')
            return ConversationHandler.END
        else:
            await update.message.reply_text('Тут происходят пространственные аномалии')
            return ConversationHandler.END


async def stop(update, context):
    await update.message.reply_text("Всего доброго!")
    return ConversationHandler.END


async def get_response(url, params):
    logger.info(f"getting {url}")
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as resp:
            return await resp.json()

if __name__ == '__main__':
    main()
