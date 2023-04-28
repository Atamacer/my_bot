# -*- coding: utf-8 -*-
# контакты:
# email: dan4ik-gp@yandex.ru
# discord: Atamacer#7213

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from config import main_token
import wikipedia
from youtubesearchpython import VideosSearch
from deep_translator import GoogleTranslator, single_detection

# класс ozon
class Ozon:
    def __init__(self):
        self.base_url = 'https://www.ozon.ru/category/elektronika-15500/?category_was_predicted=true&deny_category_prediction=true&from_global=true&text='

    # получение ссылки на товар
    def product_search(self):
        self.product = self.product.replace(' ', '+')

        if self.product[0] == '+':
            self.product = self.product[1:]

        self.base_url += self.product


    # получение результата
    def gettig_result(self, product):
        self.product = product
        self.product_search()

        return self.base_url

# класс wildberries
class Wildberries:

    #  иницилизация
    def __init__(self):
        self.base_url = 'https://www.wildberries.ru/catalog/0/search.aspx?search='

    # получение ссылки на товар
    def product_search(self):
        if self.product[0] == ' ':
            self.product = self.product[1:]

        self.product = self.product.replace(' ', '%20')
        self.base_url += self.product

    # получение результата
    def gettig_result(self, product):
        self.product = product
        self.product_search()

        return self.base_url


# класс переводчик
class Translate:
    def __init__(self):
        pass

    # определение языка на который нужно перевести ru или en
    def language_definition(self):
        self.lang = single_detection(
            self.msg,
            api_key='1e73b559f06e0ba73a0bba89ef403717'
        )
        if self.lang != 'ru':
            self.lang = 'ru'
        else:
            self.lang = 'en'

    # перевод сообщения
    def translator(self, msg):
        self.msg = msg
        self.language_definition()
        self.translated_msg = GoogleTranslator(source='auto', target=self.lang).translate(self.msg)
        return self.translated_msg


# класс youtube
class YouTube:

    # иницилизация
    def __init__(self, request):
        self.request = request
        self.videosSearch = VideosSearch(
            self.request,
            limit=1,
            region='ru'
        )

    # получение названия видео
    def getting_the_name(self):
        name = self.videosSearch.result()['result'][0]['title']
        return name

    # получение ссылки на видео
    def getting_a_link(self):
        link = self.videosSearch.result()['result'][0]['link']
        return link

    # получение результата
    def getting_result(self):
        result = f'Название: {self.getting_the_name()}\n{self.getting_a_link()}'
        return result


# класс википедия
class Wiki:

    # иницилизация
    def __init__(self, request):
        self.request = request

    # выбор языка
    def search_settings(self):
        wikipedia.set_lang('ru')

    # поиск контента
    def content_search(self):
        self.search_settings()
        self.wiki = wikipedia.search(self.request)
        self.page = wikipedia.page(self.wiki[0])
        self.title = self.page.title
        self.content = self.page.content

    # получение результата
    def getting_result(self):
        self.content_search()
        res = f'{self.title} \n {self.content}'
        res = res.split('\n\n')
        return res


# класс бот вк
class Bot:
    # иницилизация
    def __init__(self, main_token=main_token):
        self.vk_session = vk_api.VkApi(token=main_token)
        self.longpool = VkLongPoll(self.vk_session)

    # отправка сообщений
    def send(self, id, msg):
        self.vk_session.method(
            'messages.send',
            {'chat_id': id,
             'message': msg,
             'random_id': 0}
        )

    # проверка сообщений
    def check_msg(self, msg: str):

        try:

            if msg[0] == '!':

                msg = msg.replace(
                    '!', ''
                )

                if 'поиск в youtube' in msg:
                    msg = msg.replace(
                        'поиск в youtube', ''
                    )

                    youtube = YouTube(msg)
                    text = youtube.getting_result()

                    self.send(
                        self.id, text
                    )


                elif 'поиск в википедии' in msg:
                    msg = msg.replace(
                        'поиск в википедии', ''
                    )

                    wiki = Wiki(msg)
                    text = wiki.getting_result()

                    for msg in text:
                        try:
                            self.send(
                                self.id, msg
                            )
                        except:
                            pass

                elif 'перевод' in msg:
                    msg = msg.replace(
                        'перевод', ''
                    )

                    translate = Translate()
                    text = translate.translator(msg)
                    self.send(
                        self.id, text
                    )

                elif 'поиск в ozon' in msg:
                    msg = msg.replace(
                        'поиск в ozon', ''
                    )

                    ozon = Ozon()
                    text = ozon.gettig_result(msg)
                    self.send(
                        self.id, text
                    )


                elif 'поиск в wildberries' in msg:
                    msg = msg.replace(
                        'поиск в wildberries', ''
                    )

                    wildberries = Wildberries()
                    text = wildberries.gettig_result(msg)
                    self.send(
                        self.id, text.replace(' ', '%20')
                    )

                elif msg in ['help', 'помощь']:
                    text = '!поиск в youtube название видео \n' \
                           '!поиск в википедии название статьи \n' \
                           '!перевод слово или фраза которую нужно перевести \n' \
                           '!поиск в ozon название товара \n' \
                           '!поиск в wildberries название товара'

                    self.send(
                        self.id, text
                    )

        except:
            pass

    # прослушивание сообщений
    def listening(self):
        while True:
            for event in self.longpool.listen():
                if event.type == VkEventType.MESSAGE_NEW:
                    if event.to_me:
                        if event.from_chat:
                            self.msg = event.text.lower()
                            self.id = event.chat_id

                            self.check_msg(self.msg)

                            print(self.msg)


if __name__ == '__main__':
    bot = Bot()
    bot.listening()
