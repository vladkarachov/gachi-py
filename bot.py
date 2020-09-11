
import io
import os
import random
import time

import numpy
from PIL import Image, ImageDraw, ImageFont
from dotenv import load_dotenv
from telegram import ChatPermissions, error
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          )

from pog import pog

font_size = 40  # for name tag
load_dotenv()
token = os.environ['TOKEN']


def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def rap(update, context):
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





def mute(update: Updater, context):
    if update.effective_chat.type not in ('group', 'supergroup'):
        update.message.reply_text("Function can be used only in group chats")
    else:
        duration = numpy.random.choice([0, 1, 2, 3, 4, 5],
                                       p=[0.5, 0.1, 0.1, 0.1, 0.1, 0.1])
        if duration:
            permission = ChatPermissions(can_send_messages=False)
            try:
                context.bot.restrictChatMember(chat_id=update.effective_chat.id,
                                               user_id=update.effective_user.id,
                                               permissions=permission,
                                               until_date=int(time.time()) + int(duration * 60 * 60))
                update.message.reply_text("press F for " + str(update.effective_user.full_name)
                                          + " [" + str(duration) + "h]")
            except error.BadRequest:
                update.message.reply_text("Админов нельзя рестриктить " + str(update.effective_user.full_name) + "...")
        else:
            update.message.reply_text("На этот раз тебе повезло " + str(update.effective_user.full_name))


def get_mess(update: Updater, context):
    # regex handler
    # build in regex doesnt have lower
    if update.effective_message.text == None:
        return 0
    message = update.effective_message.text.lower()
    for word in message.split():
        if word in ('пог', 'pog'):
            pog(update, context)
            break
        elif word == 'тестик-':
            who(update, context)
            break
        elif word == 'мут-':
            mute(update, context)
            break


def select_pictures():
    dir_bkg = os.path.join('Who', 'WhoTitles')
    dir_res = os.path.join('Who', 'WhoAnswers')
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
    dp.add_handler(CommandHandler("mute", mute))
    dp.add_handler(CommandHandler("stat", mute))
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
