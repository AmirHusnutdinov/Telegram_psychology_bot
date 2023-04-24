import logging
from telegram.ext import Application, MessageHandler, filters, CommandHandler, ConversationHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from data import db_session
from data.metrics import Metrics
import random
import aiohttp

# from telegram.ext import ApplicationBuilder
BOT_TOKEN = '6188292983:AAEiOG7lgCOOUT85Sam83Zq2q_55U1N2ZV0'

conditions_good = ['хорош', 'отличн', 'замечательн', 'великолепн', 'пойдет', 'славно',
                   'превосходн', 'фантастически', 'сказочн', 'на 5 с плюсом', 'неплохо', 'супер', 'круто']

conditions_bad = ['плох', 'ужасн', 'грустн', 'печальн', 'одинок', 'противн', 'мерзк', 'отвратительн',
                  'угнетающе', 'гнетуще', 'не очень', 'разочарованн', 'безысходн' 'паршив']

alfabet = list('abcdefghijklmnopqrstuvwxyzабвгдеёжзийклмнопрстуфхцчшщъыьэюя ')

hello = ['привет', 'здравствуй', 'здравствуйте', 'приветствую',
         'доброго времени суток', 'бонжур', 'намасте', 'hello', 'hi', 'доброе утро', 'добрый день',
         'добрый вечер', 'доброй ночи', 'утречко']

answer_for_hello = ['Привет', 'Здравствуй', 'Здравствуйте', 'Приветствую',
                    'Доброго времени суток', 'Бонжур', 'Намасте', 'Рад вас видеть',
                    'Хай']

hau = ['как дела', 'как жизнь', 'как настроение', 'как настрой',
       'как поживаете', 'как вы себя чувствуете', 'как прошел ваш день', 'как вы себя чувствуете']

mates = ['сука', 'нахуй', 'блять', 'пиздец', 'пизда', 'ебать', 'заебись', 'пидор', 'хуй', 'пидорас']

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)


def main():
    # proxy_url = "socks5://user:pass@host:port"
    # app = ApplicationBuilder().token(BOT_TOKEN).proxy_url(proxy_url).build()
    db_session.global_init('db/metrix.db')
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("help", help_))
    application.add_handler(CommandHandler("close", close_keyboard))
    application.add_handler(CommandHandler("site", site))
    application.add_handler(CommandHandler("about", about))
    application.add_handler(CommandHandler("posts", posts))
    application.add_handler(CommandHandler("events", events))

    conv_handler1 = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            '1_start': [MessageHandler(filters.TEXT & ~filters.COMMAND, first_response_start)],
            '2_start': [MessageHandler(filters.TEXT & ~filters.COMMAND, second_response_start)],
            '3_start': [MessageHandler(filters.TEXT & ~filters.COMMAND, third_response_start)]
        },
        fallbacks=[CommandHandler("stop", stop)]
    )

    conv_handler2 = ConversationHandler(
        entry_points=[CommandHandler("answers", answers)],
        states={
            '1_answer': [MessageHandler(filters.TEXT & ~filters.COMMAND, first_response_answer)],
            '2_answer': [MessageHandler(filters.TEXT & ~filters.COMMAND, second_response_answer)],
            '3_answer': [MessageHandler(filters.TEXT & ~filters.COMMAND, third_response_answer)],
            '4_answer': [MessageHandler(filters.TEXT & ~filters.COMMAND, fourth_response_answer)]
        },
        fallbacks=[CommandHandler("stop", stop)]
    )
    application.add_handler(conv_handler1)
    application.add_handler(conv_handler2)
    application.add_handler(MessageHandler(filters.TEXT, dialog))
    application.run_polling()


async def events(update, _):
    db_sess = db_session.create_session()
    metric = db_sess.query(Metrics).first()
    info = metric.events
    metric = db_sess.query(Metrics).filter(Metrics.id == 1).first()
    metric.event = info + 1
    db_sess.commit()

    event_api_url = "http://127.0.0.1:8080/api/blog"
    response = await get_response(event_api_url, params={
        "apikey": "Your Api key",
        "format": "json"
    })

    if not response:
        await update.message.reply_text('Ошибка выполнения запроса!')
    else:
        for i in response:
            await update.message.reply_text(i)


async def dialog(update, _):
    phrase = []

    for char in list(update.message.text.lower()):
        if char.lower() in alfabet:
            phrase.append(char)
    phrase = ''.join(phrase)

    for word_hello in hello:
        if word_hello in phrase:
            await update.message.reply_text(f'{answer_for_hello[random.randrange(0, 11)]}')
            break


async def start(update, context):
    db_sess = db_session.create_session()
    metric = db_sess.query(Metrics).first()
    info = metric.start
    metric = db_sess.query(Metrics).filter(Metrics.id == 1).first()
    metric.start = info + 1
    db_sess.commit()

    user = update.effective_user
    context.user_data['change_len_name'] = False
    context.user_data['name'] = user.mention_html().split('>')[1].split('<')[0]
    reply_keyboard = [['да', 'нет']]

    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

    await update.message.reply_text(
        f"{answer_for_hello[random.randrange(0, len(answer_for_hello))]}"
        f" {context.user_data['name']}👋.\nМеня зовут бот Ильяс.",
        reply_markup=markup
    )
    await update.message.reply_text(f"Могу ли я называть вас {user.mention_html().split('>')[1].split('<')[0]}?\n"
                                    f"Если хотите сменить имя напишите 'да'\nну а если все устраивает напишите 'нет'")
    return '1_start'


async def first_response_start(update, context):
    user = update.effective_user
    reply_keyboard = [['/posts', '/events', '/about', '/answers'],
                      ['/site', '/start', '/close', '/stop']]

    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    if update.message.text == 'да' or context.user_data['change_len_name']:
        await update.message.reply_text('Впишите имя которое хотите', reply_markup=markup)
        context.user_data['change_len_name'] = False
        return '3_start'

    elif update.message.text == 'нет':
        context.user_data['name'] = user.mention_html().split('>')[1].split('<')[0]
        await update.message.reply_text(f'Приятно познакомится {context.user_data["name"]}', reply_markup=markup)
        await update.message.reply_text(f' {hau[random.randrange(0, len(hau))]}?', reply_markup=markup)
        return '2_start'

    else:
        await update.message.reply_text('Еще разок "да" или "нет"', reply_markup=markup)
        return '1_start'


async def second_response_start(update, _):
    phrase = []

    for char in list(update.message.text.lower()):
        if char.lower() in alfabet:
            phrase.append(char)
    phrase = ''.join(phrase)

    mate_flag = False

    for mate in mates:
        if mate in phrase:
            await update.message.reply_text('Я вас прошу глубоко вдохните, выдохните и больше не материтесь')
            mate_flag = True
            break

    if not mate_flag:
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
        await update.message.reply_text('Хотите узнать что я могу?\nЕсли да то вам сюда /help')
        return ConversationHandler.END


async def third_response_start(update, context):
    if len(update.message.text) >= 10:
        await update.message.reply_text('Дружище твое имя слишком длинное,\nдавай что-нибудь умещающееся в 10 символов')
        context.user_data['change_len_name'] = True
        return '2_start'
    context.user_data['name'] = update.message.text
    await update.message.reply_text(f'Приятно познакомится {update.message.text}')
    await update.message.reply_text(f' {hau[random.randrange(0, len(hau))]}?')
    return '2_start'


async def help_(update, _):
    db_sess = db_session.create_session()
    metric = db_sess.query(Metrics).first()
    info = metric.help
    metric = db_sess.query(Metrics).filter(Metrics.id == 1).first()
    metric.help = info + 1
    db_sess.commit()

    await update.message.reply_text(
        "Доступные команды:\n\n/start - Обновление бота\n/close - Закрытие клавиатуры\n/stop - Прерывание диалога\n\n"
        "/answer - Задать вопрос эксперту\n/posts - Получить пост из блога\n/events - Получение ближайших событий\n"
        "/about - Получение информации о нас\n/site - Получение ссылки наш на сайт\n\n/help - Получение всех команд")


async def close_keyboard(update, _):
    db_sess = db_session.create_session()
    metric = db_sess.query(Metrics).first()
    info = metric.close
    metric = db_sess.query(Metrics).filter(Metrics.id == 1).first()
    metric.close = info + 1
    db_sess.commit()

    await update.message.reply_text(
        "Ok",
        reply_markup=ReplyKeyboardRemove()
    )


async def site(update, _):
    db_sess = db_session.create_session()
    metric = db_sess.query(Metrics).first()
    info = metric.site
    metric = db_sess.query(Metrics).filter(Metrics.id == 1).first()
    metric.site = info + 1

    db_sess.commit()
    user = update.effective_user
    await update.message.reply_text(f"{user.mention_html().split('>')[1].split('<')[0]} это наш сайт,\n"
                                    "переходи, там так много всего интересного и"
                                    " познавательного👇\n http://127.0.0.1:8080/")


async def about(update, _):
    db_sess = db_session.create_session()
    metric = db_sess.query(Metrics).first()
    info = metric.about
    metric = db_sess.query(Metrics).filter(Metrics.id == 1).first()
    metric.about = info + 1
    db_sess.commit()

    await update.message.reply_text("Mindease\nМы предоставляет квалифицированную психологическую помощь"
                                    " подросткам,\nкоторые сталкиваются с жизненными трудностями.\n"
                                    " Проводим частные виртуальные консультации, а также групповые программы и"
                                    " семинары с целью повышения самосознания и управления эмоциями.\n"
                                    " Наша цель — помочь вам найти эффективные механизмы выживания и"
                                    " достичь более высокого уровня жизни.\n\nЗаинтересовало?\nТогда скорей переходи по"
                                    " этой ссылке на сайт👇\n http://127.0.0.1:8080/")


async def posts(update, _):
    db_sess = db_session.create_session()
    metric = db_sess.query(Metrics).first()
    info = metric.posts
    metric = db_sess.query(Metrics).filter(Metrics.id == 1).first()
    metric.posts = info + 1
    db_sess.commit()

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


async def answers(update, context):
    db_sess = db_session.create_session()
    metric = db_sess.query(Metrics).first()
    info = metric.answers
    metric = db_sess.query(Metrics).filter(Metrics.id == 1).first()
    metric.answers = info + 1
    db_sess.commit()

    await update.message.reply_text(f'Итак {context.user_data["name"]} чтобы задать вопрос пожалуйста напишите почту,\n'
                                    'на которую вы хотите получить ответ.\n'
                                    'Если хотите прервать задавание вопроса впишите команду /stop')
    return '1_answer'


async def first_response_answer(update, context):
    context.user_data['email'] = update.message.text
    await update.message.reply_text(f"Отлично {context.user_data['name']} внимательно слушаю твой вопрос")
    return '2_answer'


async def second_response_answer(update, context):
    context.user_data['answer'] = update.message.text
    reply_keyboard = [['да', 'почта', 'сам вопрос']]

    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    await update.message.reply_text(f"Отлично {context.user_data['name']} теперь проверь все ли ты указал верно:\n"
                                    f"Имя -- {context.user_data['name']}\n"
                                    f"Почта -- {context.user_data['email']}\n"
                                    f"Вопрос-- {context.user_data['answer']}\n\nЕсли все верно то напиши 'да' если нет,"
                                    f" то напиши в чем описался\n"
                                    f"Для удобства можешь воспользоваться кнопками", reply_markup=markup)
    return '3_answer'


async def third_response_answer(update, context):
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
        reply_keyboard = [['/posts', '/events', '/about', '/answers'],
                          ['/site', '/start', '/close', '/stop']]

        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
        if not response:
            await update.message.reply_text('Тут происходят пространственные аномалии', reply_markup=markup)
        for key in response:
            if key == 'success':
                await update.message.reply_text('Вопрос успешно отправлен, будут еще пишите, не стесняйтесь',
                                                reply_markup=markup)
                return ConversationHandler.END

            elif key == 'error':
                await update.message.reply_text('Простите какие-то неполадки с сервером, попробуйте позже',
                                                reply_markup=markup)
                return ConversationHandler.END
            else:
                await update.message.reply_text('Тут происходят пространственные аномалии', reply_markup=markup)
                return ConversationHandler.END

    elif update.message.text.lower() == 'почта':
        context.user_data['change'] = 'email'
        await update.message.reply_text('Введите нужную почту')
        return '4_answer'

    elif update.message.text.lower() == 'вопрос':
        context.user_data['change'] = 'answer'
        await update.message.reply_text('Введите свой вопрос')
        return '4_answer'


async def fourth_response_answer(update, context):
    if context.user_data['change'] == 'email':
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
    reply_keyboard = [['/posts', '/events', '/about', '/answers'],
                      ['/site', '/start', '/close', '/stop']]

    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

    for key in response:
        if key == 'success':
            await update.message.reply_text('Вопрос успешно отправлен, будут еще пишите, не стесняйтесь',
                                            reply_markup=markup)
            return ConversationHandler.END

        elif key == 'error':
            await update.message.reply_text('Простите какие-то неполадки с сервером, попробуйте позже',
                                            reply_markup=markup)
            return ConversationHandler.END
        else:
            await update.message.reply_text('Тут происходят пространственные аномалии', reply_markup=markup)
            return ConversationHandler.END


async def stop(update, context):
    db_sess = db_session.create_session()
    metric = db_sess.query(Metrics).first()
    info = metric.stop
    metric = db_sess.query(Metrics).filter(Metrics.id == 1).first()
    metric.stop = info + 1
    db_sess.commit()
    reply_keyboard = [['/posts', '/events', '/about', '/answers'],
                      ['/site', '/start', '/close', '/stop']]

    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    await update.message.reply_text(f"Хорошо, {context.user_data['name']}, диалог окончен", reply_markup=markup)
    return ConversationHandler.END


async def get_response(url, params):
    logger.info(f"getting {url}")
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as resp:
            return await resp.json()


if __name__ == '__main__':
    main()
