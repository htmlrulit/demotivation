import configparser
from configparser import ConfigParser, RawConfigParser
from simpledemotivators import Demotivator, Quote
from vkbottle.bot import Bot, Message
from vkbottle import PhotoMessageUploader
import requests
cfg = configparser.ConfigParser()
cfg.read("config.ini")
bot = Bot(token=(cfg["Main"]["BOT_TOKEN"]))
bot.labeler.vbml_ignore_case = True
arrange = True

@bot.on.message(text=['дем <text1>\n<text2>', 'демотиватор <text1>\n<text2>', 'dem <text1>\n<text2>'])
async def dem(ans: Message, text1, text2):
    dem = Demotivator(text1, text2)
    if ans.reply_message is not None:

        if ans.reply_message.attachments:
            image_url = ans.reply_message.attachments[0].photo.sizes[-5].url
            img_data = requests.get(image_url).content
            with open('demimg.jpg', 'wb') as handler:
                handler.write(img_data)
            dem = Demotivator(text1, text2)
            dem.create('demimg.jpg', arrange=arrange)
            photo_upd = PhotoMessageUploader(bot.api)
            photo = await photo_upd.upload("demresult.jpg")
            await ans.reply('Готово!', attachment=photo)

        elif (not ans.reply_message.attachments) and (not ans.attachments):
            await ans.reply('Для того, чтобы воспользоваться демотиватором, необходимо правильно заполнить сообщение\n\nСмотри, я покажу:')
            await ans.answer('демотиватор привет как дела', attachment='photo-59800369_456243914')

    elif ans.attachments is not None:
        image_url = ans.attachments[0].photo.sizes[-5].url
        img_data = requests.get(image_url).content
        with open('demimg.jpg', 'wb') as handler:
            handler.write(img_data)
        dem = Demotivator(text1, text2)
        dem.create('demimg.jpg', arrange=arrange)
        photo_upd = PhotoMessageUploader(bot.api)
        photo = await photo_upd.upload("demresult.jpg")
        await ans.reply('Готово!', attachment=photo)

@bot.on.message(text=['дем <text1>', 'демотиватор <text1>', 'dem <text1>'])
async def dem(ans: Message, text1):
    dem = Demotivator(text1)
    if ans.reply_message is not None:

        if ans.reply_message.attachments:
            image_url = ans.reply_message.attachments[0].photo.sizes[-5].url
            img_data = requests.get(image_url).content
            with open('demimg.jpg', 'wb') as handler:
                handler.write(img_data)
            dem = Demotivator(text1)
            dem.create('demimg.jpg', arrange=arrange)
            photo_upd = PhotoMessageUploader(bot.api)
            photo = await photo_upd.upload("demresult.jpg")
            await ans.reply('Готово!', attachment=photo)

        elif (not ans.reply_message.attachments) and (not ans.attachments):
            await ans.reply('Вы не прикрепили изображение')

    elif ans.attachments is not None:
        image_url = ans.attachments[0].photo.sizes[-5].url
        img_data = requests.get(image_url).content
        with open('demimg.jpg', 'wb') as handler:
            handler.write(img_data)
        dem = Demotivator(text1)
        dem.create('demimg.jpg', arrange=arrange)
        photo_upd = PhotoMessageUploader(bot.api)
        photo = await photo_upd.upload("demresult.jpg")
        await ans.reply('Готово!', attachment=photo)

@bot.on.message(text=['dem', 'дем', 'демотиватор'])
async def dem(ans: Message):
    if (ans.reply_message is not None) and ans.attachments:
        if ans.reply_message.text != '':
            image_url = ans.attachments[0].photo.sizes[-5].url
            img_data = requests.get(image_url).content
            with open('demimg.jpg', 'wb') as handler:
                handler.write(img_data)
            dem = Demotivator(ans.reply_message.text)
            dem.create('demimg.jpg', arrange=arrange)
            photo_upd = PhotoMessageUploader(bot.api)
            photo = await photo_upd.upload("demresult.jpg")
            await ans.reply('Готово!', attachment=photo)

        elif ans.reply_message.text == '':
            await ans.reply('Для того, чтобы воспользоваться демотиватором, необходимо правильно заполнить сообщение\n\nСмотри, я покажу:')
            await ans.answer('демотиватор привет как дела', attachment='photo-59800369_456243914')

    elif (ans.reply_message is not None) and (not ans.attachments):
        if ans.reply_message.text != '':
            await ans.reply('Для того, чтобы воспользоваться демотиватором, необходимо правильно заполнить сообщение\n\nСмотри, я покажу:')
            await ans.answer('демотиватор привет как дела', attachment='photo-59800369_456243914')
        
        elif (ans.reply_message.text == '') and (not ans.attachments):
            await ans.reply('Для того, чтобы воспользоваться демотиватором, необходимо правильно заполнить сообщение\n\nСмотри, я покажу:')
            await ans.answer('демотиватор привет как дела', attachment='photo-59800369_456243914')

    elif (ans.reply_message is None) and (not ans.attachments):
            await ans.reply('Для того, чтобы воспользоваться демотиватором, необходимо правильно заполнить сообщение\n\nСмотри, я покажу:')
            await ans.answer('демотиватор привет как дела', attachment='photo-59800369_456243914')

@bot.on.message(text='цитата')
async def quote(ans: Message):
    if ans.reply_message is not None:
        if ans.reply_message.text != '':
            try:
                user_ava = await bot.api.users.get(user_ids=ans.reply_message.from_id, fields='photo_max')
                user_photo = user_ava[0].photo_max
                name = user_ava[0].first_name + ' ' + user_ava[0].last_name
                img_data = requests.get(user_photo).content
                with open('userphoto.jpg', 'wb') as handler:
                    handler.write(img_data)
                dem = Quote(ans.reply_message.text, name)
                photo = dem.create(user_photo, use_url=True, quote_text_size=40)
                photo_upd = PhotoMessageUploader(bot.api)
                photo = await photo_upd.upload("qresult.png")
                await ans.answer(attachment=photo)
            except:
                group_id = ans.reply_message.from_id * (-1)
                user_ava = await bot.api.groups.get_by_id(group_id=group_id)
                user_photo = user_ava[0].photo_200
                name = user_ava[0].name
                img_data = requests.get(user_photo).content
                with open('userphoto.jpg', 'wb') as handler:
                    handler.write(img_data)
                dem = Quote(ans.reply_message.text, name)
                photo = dem.create(user_photo, use_url=True, quote_text_size=40, headline_text='Цитаты великих ботов')
                photo_upd = PhotoMessageUploader(bot.api)
                photo = await photo_upd.upload("qresult.png")
                await ans.answer(attachment=photo)
        elif ans.reply_message.text == '':
            await ans.reply('Для того, чтобы воспользоваться демотиватором, необходимо правильно заполнить сообщение\n\nСмотри, я покажу:')
            await ans.answer('демотиватор привет как дела', attachment='photo-59800369_456243914')
    elif ans.reply_message is None:
        await ans.reply('Для того, чтобы воспользоваться демотиватором, необходимо правильно заполнить сообщение\n\nСмотри, я покажу:')
        await ans.answer('демотиватор привет как дела', attachment='photo-59800369_456243914')


bot.run_forever()