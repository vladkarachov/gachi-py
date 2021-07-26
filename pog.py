import datetime

import numpy
from telegram.ext import Updater

import moonphase

pog_users_time = dict()
poggers_chats = dict()


def get_probability_for_pog():
    phase = moonphase.position()
    # формула взята с потолка не ищите особого смысла
    prob = numpy.sin(float(phase) * numpy.pi / 2) / 4 + 0.1
    return [1 - prob, prob]


def pog(update: Updater, context):
    # 2 пог классный 1 нет
    stickers = ['CAACAgIAAxkBAAObYP7yaBmTk2dWPQy69B55jExJsV4AAhUAA-vLHAMrbDkiR1mznyAE',
                'CAACAgIAAxkBAAOeYP7yyQUE3UeI3Xw1PnqIt-2fB3sAAhYAA-vLHAMsBUfCb3i2VSAE']
    sticker = numpy.random.choice(stickers, p=get_probability_for_pog())
    # cooldown func (against spam)
    last_time = pog_users_time.get(update.effective_user.id, 0)
    if last_time != 0 and \
            last_time + datetime.timedelta(minutes=1) > update.effective_message.date:
        update.message.reply_text('не погай')
    else:
        if sticker == stickers[1]:
            update_poggers_stats(update.effective_user.name, update.effective_chat.id, poggers_chats)
        context.bot.sendSticker(update.effective_chat.id,
                                sticker=sticker)
        pog_users_time[update.effective_user.id] = update.effective_message.date


def update_poggers_stats(userid, chatid, poggers_chats):
    # шоб людей не тегало
    userid = userid[1:]
    poggers_chat = poggers_chats.get(chatid, 0)
    if not poggers_chat:
        poggers_chat = {userid: 1}
        poggers_chats[chatid] = poggers_chat
    else:
        if poggers_chats[chatid].get(userid, -1) == -1:
            poggers_chats[chatid][userid] = 1
        else:
            poggers_chats[chatid][userid] += 1


def get_pog_stats(update: Updater, context):
    current_lunar_phase = get_probability_for_pog()
    poggers_list = ''
    i = 0
    poggers = poggers_chats.get(update.effective_chat.id, 0)
    if type(poggers) == type(dict()):
        for pogger in sorted(poggers, key=poggers.get, reverse=True):
            poggers_list += '\n' + str(pogger) + ":" + str(poggers[pogger])
            if i < 5:
                i += 1
            else:
                break
    if poggers_list!='':
        poggers_list='\nTop 5 poggers:'+ poggers_list
    update.message.reply_text("curren POG prob : "
                                  + str(float('{:.2f}'.format(current_lunar_phase[1])))
                                  + poggers_list)
