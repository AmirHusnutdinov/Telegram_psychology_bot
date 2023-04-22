import logging
from telegram.ext import Application, MessageHandler, filters, CommandHandler
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
    application.add_handler(MessageHandler(filters.TEXT, dialog))
    application.run_polling()


async def dialog(update, context):
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
                await update.message.reply_text(f'{conditions_good[random.randrange(0, len(conditions_good))]}, спасибо')
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


async def start(update, context):
    reply_keyboard = [['/posts', '/events', '/about'],
                      ['/site', '/start', '/close']]

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


async def help_(update, context):
    await update.message.reply_text(
        "Доступные команды:\n")


async def close_keyboard(update, context):
    await update.message.reply_text(
        "Ok",
        reply_markup=ReplyKeyboardRemove()
    )


async def site(update, context):
    user = update.effective_user
    await update.message.reply_text(f"{user.mention_html().split('>')[1].split('<')[0]} это наш сайт,\n"
                                    "переходи, там так много всего интересного и"
                                    " познавательного👇\n http://127.0.0.1:8080/")


async def about(update, context):
    await update.message.reply_text("Mindease\nМы предоставляет квалифицированную психологическую помощь"
                                    " подросткам,\nкоторые сталкиваются с жизненными трудностями.\n"
                                    " Проводим частные виртуальные консультации, а также групповые программы и"
                                    " семинары с целью повышения самосознания и управления эмоциями.\n"
                                    " Наша цель — помочь вам найти эффективные механизмы выживания и"
                                    " достичь более высокого уровня жизни.\n\nЗаинтересовало?\nТогда скорей переходи по"
                                    " этой ссылке на сайт👇\n http://127.0.0.1:8080/")


async def posts(update, context):
    geocoder_uri = "http://127.0.0.1:8080/api/blog"
    response = await get_response(geocoder_uri, params={
        "apikey": "Your Api key",
        "format": "json",
        "geocode": update.message.text
    })

    if not response:
        await update.message.reply_text('Ошибка выполнения запроса!')
    else:
        for i in response:
            await update.message.reply_text(i)


async def get_response(url, params):
    logger.info(f"getting {url}")
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as resp:
            return await resp.json()

if __name__ == '__main__':
    main()
