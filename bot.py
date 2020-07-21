import random
import re
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)
from PIL import Image, ImageDraw, ImageFont
import os
import io
import numpy

font_size = 40  # for name tag
token = os.environ['TOKEN']


def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def rap(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('йоу сабаки!')


def create_image(bkg, profile_pic, res, name_tag):
    # background resize and pasting
    ratio = bkg.width / bkg.height
    dst = Image.new('RGB', (bkg.width, bkg.height))
    dst.paste(bkg, (0, 0))
    dst = dst.resize((1024, int(1024 / ratio)))

    # pasting profile pic and text on it
    size = min(dst.height, dst.width)
    profile_pic = profile_pic.resize((int(size // 2), int(size // 2)))
    # center of quadrant
    loc = ((dst.width // 2 - profile_pic.width) // 2, (dst.height // 2 - profile_pic.height) // 2)
    dst.paste(profile_pic, loc)
    d = ImageDraw.Draw(dst)
    font = ImageFont.truetype('RobotoMono-Bold.ttf', font_size, encoding="unic")
    d.multiline_text((profile_pic.height // 20, 5),
                     name_tag[0:25], font=font, fill="black")

    # pasting result of test
    res = res.resize((int(dst.width // 2.1), int(dst.height // 2.1)))
    # немножко в сторону
    dst.paste(res, (int(dst.width // 1.9), int(dst.height // 1.9)))

    return dst


def pog(update: Updater, context):
    stickers = ['CAACAgIAAxkBAANmXxNz2XBHKMFWmTqR6xW2qnj_7o8AArsDAALgeVIHucUjaLiR8vMaBA',
                "CAACAgIAAxkBAANJXxNsRjCVRDHdh2qDEk5ELDMYOaAAAvoDAALgeVIHi6_ino1KLzUaBA"]
    sticker = numpy.random.choice(stickers, p=[0.9, 0.1])
    context.bot.sendSticker(update.effective_chat.id,
                            sticker=sticker)


def get_mess(update: Updater, context):
    # regex handler
    # build in regex doesnt have lower
    if update.effective_message.text==None:
        return 0
    message = update.effective_message.text.lower()
    if re.search(r"(\b(пог)\b|\b(pog)\b)", message):
        pog(update, context)
    # тире не работает с регекспом почему-то
    if message.find('тестик-') != -1:
        who(update, context)
    return 0


def select_pictures():
    dir_bkg = 'Who\\WhoTitles'
    dir_res = 'Who\\WhoAnswers'
    bkg = Image.open(os.path.join(dir_bkg, random.choice(os.listdir(dir_bkg))))
    res = Image.open(os.path.join(dir_res, random.choice(os.listdir(dir_res))))
    return bkg, res


def who(update: Updater, context):
    bkg, res = select_pictures()
    userid = update.effective_user.id
    username = update.effective_user.full_name
    try:
        photo_id = context.bot.getUserProfilePhotos(userid)["photos"][0][2].file_id
    except BaseException:
        try:
            photo_id = context.bot.getUserProfilePhotos(userid)["photos"][0][0].file_id
        except BaseException:
            photo_id = None
            return 1
            # ну що поделать потом какую-то картинку вставлю
            # а вообще оно при эксепшенах не крашит все
    # хз говнокод какой-то
    # надо редаунлоад почистить будет
    # капец конечно картинку с интернета сложно скачать
    profile_pic_link = context.bot.getFile(photo_id)
    profile_pic_bytes = profile_pic_link.download_as_bytearray()
    profile_pic = Image.open(io.BytesIO(profile_pic_bytes))
    testik = create_image(bkg, profile_pic, res, username)

    # сереализируем и отправляем назад (в помойку)
    testik_bytes = io.BytesIO()
    testik_bytes.name = "GachiTestik.jpeg"
    testik.save(testik_bytes, 'JPEG')
    testik_bytes.seek(0)
    update.message.reply_photo(testik_bytes)
    return 0


def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(token, use_context=True)
    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("rap", rap))
    dp.add_handler(CommandHandler("who", who))

    # dp.add_handler(MessageHandler(filters=Filters.regex(r"(\b([П|п]ог)\b|\b([P|p]og)\b)"), callback=pog))

    dp.add_handler(MessageHandler(filters=Filters.all, callback=get_mess))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
