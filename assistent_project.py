# Импорт всех необходимых модулей
import pyttsx3  # Модуль для воспроизведения текста в речь
import speech_recognition as sr  # Модуль для прослушивания микрофона
import colorama
from fuzzywuzzy import fuzz   # Модуль для нечёткого распознавания речи
import datetime  # Модуль для определения время
from os import system
import sys
from random import choice
from pyowm import OWM
from pyowm.utils.config import get_default_config
import webbrowser  # Модуль для выполнения запросов и открытия вкладок в вашем браузере
import configparser

class Assistant:
    settings = configparser.ConfigParser()
    settings.read('settings.ini')

    config_dict = get_default_config()  # Инициализация get_default_config()
    config_dict['language'] = 'ru'  # Установка языка

    def __init__(self):       #конструктор
        # Глобальные переменные
        self.engine = pyttsx3.init()
        self.r = sr.Recognizer()  # Инициализация распознавателя
        self.text = ''  # Создание глобальной переменной text

        self.num_task = 0
        self.j = 0
        self.ans = ''

        # Словарь со всеми настройками
        self.cmds = {   # список функций и команд, при которых они выполняются
            ('текущее время', 'сейчас времени', 'который час'): self.time,
            ('привет', 'добрый день', 'здравствуй'): self.hello,
            ('пока', 'вырубись'): self.quite,
            ('выключи компьютер', 'выруби компьютер'): self.shut,
            ('запиши контакт', 'запиши номер телефона'): self.contacts_list_save,
            ('запомни', 'запомни и напомни попозже', 'сделай заметку'): self.save_reminder,
            ('посчитай', 'включи калькулятор', 'запусти калькулятор', 'калькулятор'): self.colculator,
            ('заметки', 'что на сегодня заплонированно', 'какие сегодня дела', 'есть какие нибудь напоминания на сегодня?',
            'есть какие нибудь заметки на сегодня?', 'открой заметки на сегодня', 'открой сегодняшние заметки'): self.reminder,
            ('какая погода', 'погода', 'погода на улице', 'какая погода на улице'): self.weather,
            ('номер телефона', 'список контактов', 'контакты'): self.contacts_reminder,
        }
        # список имен и слов на которые откликается ассистент
        self.ndels = ['морган', 'морген', 'моргэн', 'морг', 'ладно', 'не могла бы ты', 'пожалуйста',
                      'текущее', 'сейчас']
        # список команд
        self.commands = [
            'текущее время', 'сейчас времени', 'который час',
            'открой браузер', 'открой интернет', 'запусти браузер',
            'привет', 'добрый день', 'здравствуй',
            'пока', 'вырубись',
            'выключи компьютер', 'выруби компьютер',
            'какая погода', 'погода', 'погода на улице', 'какая погода на улице',
            'запиши', 'запиши контакт', 'запиши номер телефона',
            'запомни', 'запомни и напомни попозже', 'сделай заметку',
            'посчитай', 'включи калькулятор', 'запусти калькулятор', 'калькулятор',
            'заметки', 'что на сегодня заплонированно', 'какие сегодня дела', 'есть какие нибудь напоминания на сегодня?',
            'есть какие нибудь заметки на сегодня?', 'открой заметки на сегодня', 'открой сегодняшние заметки',
            'номер телефона', 'список контактов', 'контакты',
        ]

    def text_save(self, text, file_name):   # метод записывания текста в выбранный файл
        file = open(file_name, 'a+', encoding="utf-8")
        self.talk("Записываю...")
        file.write(text + "\n")
        file.close()

    #Должен запускаться по команде запиши номер телефона
    def contacts_list_save(self):   # метод записывания нового контакта в файл с контактами
        filename = "numbers_list.txt"
        index = False
        self.talk("Как назвать контакт?")
        self.listen()
        text_list = [line.strip() for line in open(filename, encoding="utf-8").readlines()]
        for i in range(len(text_list)):
            k = fuzz.ratio(self.text, text_list[i])
            if (k > 70) & (k > self.j):
                self.text = text_list[i]
                self.j = k
        if self.text in text_list:  # проверяет есть ли данный контакт в списке контактов
             for numb in range(len(text_list)):      # если есть то записывает новый номер рядом с имеющимся
                if self.text in text_list[numb]:
                    self.talk("Диктуй номер")
                    self.listen()
                    file = open(filename, 'r')
                    old_text = file.read()
                    new_text = old_text.replace(text_list[numb + 1], text_list[numb + 1] + "#" + self.text)
                    file.close()
                    file = open(filename, 'w')
                    file.write(new_text)
                    file.close()
                    break
                else:
                    continue
        else:   # если нет записывает новый контакт
            index = True
        if index:
            self.text_save(str(self.text), filename)
            self.talk("Диктуй номер")
            self.listen()
            self.text_save(self.text, filename)

    def contacts_reminder(self):
        filename = 'numbers_list.txt'
        self.talk(choice(["Чей номер вам напомнить?", "Чей номер вы хотите знать?", "Чей номер вам нужен?"]))
        self.listen()
        text_list = [line.strip() for line in open(filename, encoding="utf-8").readlines()]
        for i in range(len(text_list)):
            k = fuzz.ratio(self.text, text_list[i])
            if (k > 70) & (k > self.j):
                self.text = text_list[i]
                self.j = k
        if self.text in text_list:
            for numb in range(len(text_list)):
                if self.text in text_list[numb]:
                    numbers_list = text_list[numb + 1].split("#")
                    if len(numbers_list) > 1:
                        self.talk("Вот список номеров этого контакта:")     # он только печатает список номеров если их несколько
                        for i in range(len(numbers_list)):
                            print(numbers_list[i])
                    else:
                        self.talk("Номер: " + numbers_list[0])

    def colculator(self):   # простой калькулятор (4 операции)
        print('Скажите "Завершить" чтобы мы закончили!')
        while True:
            self.listen()
            if self.text == 'Завершить':
                break
            self.text = self.text.split()
            if '+' in self.text or '-' in self.text or '*' in self.text or '/' in self.text:
                x = int(self.text[0])
                y = int(self.text[2])
                if self.text[1] == '+':
                    self.talk("%.2f" % (x + y))
                elif self.text[1] == '-':
                    self.talk("%.2f" % (x - y))
                elif self.text[1] == '*':
                    self.talk("%.2f" % (x * y))
                elif self.text[1] == '/':
                    if y != 0:
                        self.talk("%.2f" % (x / y))
                    else:
                        self.talk("На ноль делить я еще не научилась!")
            else:
                self.talk("Не поняла!")

    def save_reminder(self):    # метод записывания новой заметки в файл с заметками
        filename = "reminder_list.txt"
        self.talk("Слушаю вас")
        self.listen()
        if self.text.startswith(('надо', 'нужно', 'напомни', 'напомни мне')):    # вырезает ненужные слова из сказанного текста
            for i in ('надо', 'нужно', 'напомни', 'напомни мне'):
                self.text = self.text.replace(i, '').strip()
                self.text = self.text.replace('  ', ' ').strip()
        self.text_save(self.text, filename)
        self.talk("Когда напомнить?")
        self.listen()
        self.text_save(self.time_converter(self.text), filename)
        self.talk("Во сколько?")
        self.listen()
        self.text_save(self.text, filename)


    def reminder(self): # напоминание заметок на сегодня
        filename = 'reminder_list.txt'
        text_list = [line.strip() for line in open(filename, encoding="utf-8").readlines()]
        date_today = str(datetime.date.today())[5:]
        if date_today in text_list:
            self.talk(choice(['Вам сегодня надо:', 'В списке ваших дел на сегодня:']))
            for numb in range(len(text_list)):
                if date_today in text_list[numb]:
                    self.talk(text_list[numb - 1] + ' ' + text_list[numb + 1] )
                else:
                    continue
        else:
            self.talk(choice(["На сегодня напоминаний нет", "На сегодня дел нет", "Сегодня дел никаких нет"]))

    def time_converter(self, text):     # метод изменения текста в дату. пример: 12 января 2023 --> 2023-01-12
        text = text.replace('января', '01')
        text = text.replace('февраля', '02')
        text = text.replace('марта', '03')
        text = text.replace('апреля', '04')
        text = text.replace('мая', '05')
        text = text.replace('июня', '06')
        text = text.replace('июля', '07')
        text = text.replace('августа', '08')
        text = text.replace('сентября', '09')
        text = text.replace('октября', '10')
        text = text.replace('ноября', '11')
        text = text.replace('декабря', '12')
        text = str("-".join(text.split()[::-1]))
        return text


    def cleaner(self, text):
        self.text = text

        for i in self.ndels:  # Создание цикла для очистки слов находящихся в словаре words в запросе
            self.text = self.text.replace(i, '').strip()  # Очистка ключевых слов, находящихся в словаре ndels с запроса
            self.text = self.text.replace('  ', ' ').strip()  # Очистка ключевых слов, находящихся в словаре ndels с запроса

        self.ans = self.text

        for i in range(len(self.commands)): # поиск совпадений в списке известных команд
            k = fuzz.ratio(text, self.commands[i])
            if (k > 70) & (k > self.j):
                self.ans = self.commands[i]
                self.j = k

        return str(self.ans)

    def recognizer(self):  # метод распознавания речи /  главная функция
        self.text = self.cleaner(self.listen())
        print(self.text)
        print('______')

        if self.text.startswith(('открой', 'запусти', 'зайди', 'зайди на')):    # если просьба начинается с этих команд выполняется специальная функция
            self.opener(self.text)

        for tasks in self.cmds:     # выбор и привод в действие нужной функции из списка команд
            for task in tasks:
                if fuzz.ratio(task, self.text) >= 80:
                    self.cmds[tasks]()

        self.engine.runAndWait()
        self.engine.stop()

    def time(self):     # метод который сообщает текущее время
        now = datetime.datetime.now()
        self.talk("Сейчас " + str(now.hour) + ":" + str(now.minute))

    def opener(self, task):     # метод для выполнения специальных функций
        links = {
            ('youtube', 'ютуб', 'ютюб'): 'https://youtube.com/',
            ('вк', 'вконтакте', 'vk'): 'https:vk.com/feed',
            ('браузер', 'интернет', 'browser'): 'https://google.com/',
            ('insta', 'instagram', 'инста', 'инсту'): 'https://www.instagram.com/',
            ('почта', 'почту', 'gmail', 'гмейл', 'гмеил', 'гмаил'): 'http://gmail.com/',
        }
        j = 0
        if 'и' in task:
            task = task.replace('и', '').replace('  ', ' ')
        double_task = task.split()
        if j != len(double_task):
            for i in range(len(double_task)):
                for vals in links:
                    for word in vals:
                        if fuzz.ratio(word, double_task[i]) > 75:
                            webbrowser.open(links[vals])
                            self.talk('Открываю ' + double_task[i])
                            j += 1
                            break

    def cfile(self):
        try:
            cfr = Assistant.settings['SETTINGS']['fr']
            if cfr != 1:
                file = open('settings.ini', 'w', encoding='UTF-8')
                file.write('[SETTINGS]\ncountry = UA\nplace = Kharkov\nfr = 1')
                file.close()
        except Exception as e:
            print('Перезапустите Ассистента!', e)
            file = open('settings.ini', 'w', encoding='UTF-8')
            file.write('[SETTINGS]\ncountry = UA\nplace = Kharkov\nfr = 1')
            file.close()

    def quite(self):    # метод выключения голосового ассистента по команде
        self.talk(choice(['Надеюсь мы скоро увидимся', 'Рада была помочь', 'Пока пока', 'Я отключаюсь']))
        self.engine.stop()
        system('cls')
        sys.exit(0)

    def shut(self):     # метод выключения компьютера по команде с подтверждением
        self.talk("Подтвердите действие!")
        text = self.listen()
        print(text)
        if (fuzz.ratio(text, 'подтвердить') > 60) or (fuzz.ratio(text, "подтверждаю") > 60):
            self.talk('Действие подтверждено')
            self.talk('До скорых встреч!')
            system('shutdown /s /f /t 10')
            self.quite()
        elif fuzz.ratio(text, 'отмена') > 60:
            self.talk("Действие не подтверждено")
        else:
            self.talk("Действие не подтверждено")

    def hello(self):    # метод приветствия
        self.talk(choice(['Привет, чем могу помочь?', 'Здраствуйте', 'Приветствую']))   # отвечает на мое приветствие
        self.reminder()     # говорит заметки на сегодня


    def weather(self):

        place = Assistant.settings['SETTINGS']['place']
        country = Assistant.settings['SETTINGS']['country']  # Переменная для записи страны/кода страны
        country_and_place = place + ", " + country  # Запись города и страны в одну переменную через запятую
        owm = OWM('ВАШ API KEY')  # Ваш ключ с сайта open weather map
        mgr = owm.weather_manager()  # Инициализация owm.weather_manager()
        observation = mgr.weather_at_place(country_and_place)
        # Инициализация mgr.weather_at_place() И передача в качестве параметра туда страну и город

        w = observation.weather

        status = w.detailed_status  # Узнаём статус погоды в городе и записываем в переменную status
        w.wind()  # Узнаем скорость ветра
        humidity = w.humidity  # Узнаём Влажность и записываем её в переменную humidity
        temp = w.temperature('celsius')[
            'temp']  # Узнаём температуру в градусах по цельсию и записываем в переменную temp
        self.talk("В городе " + str(place) + " сейчас " + str(status) +  # Выводим город и статус погоды в нём
                  "\nТемпература " + str(
            round(temp)) + " градусов по цельсию" +  # Выводим температуру с округлением в ближайшую сторону
                  "\nВлажность составляет " + str(humidity) + "%" +  # Выводим влажность в виде строки
                  "\nСкорость ветра " + str(w.wind()['speed']) + " метров в секунду")  # Узнаём и выводим скорость ветра

    def talk(self, text):
        # Вывод сказанного текста на экран и озвучивание
        print(text)
        self.engine.say(text)
        self.engine.runAndWait()

    def listen(self):  # метод прослушивания микрофона и обработки запроса
        with sr.Microphone() as source:  # Запуск прослушки микрофона и объявление что sr.Microphone() мы используем как source
            print(colorama.Fore.LIGHTGREEN_EX + "Я вас слушаю...")
            self.r.adjust_for_ambient_noise(source)  # Этот метод нужен для автоматического понижения уровня шума
            audio = self.r.listen(source)  # Инициализация r.listen(source) в переменную audio
            try:  # Создание обработчика ошибок
                self.text = self.r.recognize_google(audio, language="ru-RU").lower()  # Распознавание и преобразование речи в текст
            except Exception as e:
                print(e)
            return self.text  # Возвращаем переменную для передачи данных в другую функцию


Assistant().cfile()
def start():    # функция старт
    while True:  # Бесконечный цикл
        Assistant().recognizer()  # Вызов функции recognizer()
