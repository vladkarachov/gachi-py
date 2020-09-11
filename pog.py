import datetime

import numpy
from telegram.ext import Updater

import moonphase

pog_users_time = dict()
poggers=dict()

def get_probability_for_pog():
    phase = moonphase.position()
    # формула взята с потолка не ищите особого смысла
    prob = numpy.sin(float(phase)*numpy.pi/2)/4+0.1
    return [1-prob, prob]

def pog(update: Updater, context):
    stickers = ['CAACAgIAAxkBAANmXxNz2XBHKMFWmTqR6xW2qnj_7o8AArsDAALgeVIHucUjaLiR8vMaBA',
                "CAACAgIAAxkBAANJXxNsRjCVRDHdh2qDEk5ELDMYOaAAAvoDAALgeVIHi6_ino1KLzUaBA"]
    sticker = numpy.random.choice(stickers, p=get_probability_for_pog())
    # cooldown func (against spam)
    last_time = pog_users_time.get(update.effective_user.id, 0)
    if last_time != 0 and \
            last_time + datetime.timedelta(minutes=1) > update.effective_message.date:
        update.message.reply_text('не погай')
    else:
        context.bot.sendSticker(update.effective_chat.id,
                                sticker=sticker)
        pog_users_time[update.effective_user.id] = update.effective_message.date


def get_pog_stats(update: Updater, context):
    pass
