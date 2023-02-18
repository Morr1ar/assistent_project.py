from assistent_project import Assistant

import func

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy import Config
from kivy.properties import ObjectProperty


class MainWidget(BoxLayout):
    text_label = ObjectProperty()
    btn_start = ObjectProperty()
    btn_reminder = ObjectProperty()
    btn_contacts = ObjectProperty()
    btn_instruction = ObjectProperty()
    btn_cleaner = ObjectProperty()
    scroll = ObjectProperty()

    def hide_all(self):
        self.btn_start.text = ''
        self.btn_start.size = (0, 0)
        self.btn_reminder.text = ''
        self.btn_reminder.size = (0, 0)
        self.btn_contacts.text = ''
        self.btn_contacts.size = (0, 0)
        self.btn_instruction.text = ''
        self.btn_instruction.size = (0, 0)
        self.btn_cleaner.size = (400, 100)
        self.btn_cleaner.text = 'Назад'

    def on_press_button_start(self):
        Assistant().start()

    def on_press_button_reminder(self):
        filename = 'reminder_list.txt'
        self.hide_all()
        self.text_label.text = func.text_wrap(filename)

    def on_press_button_contacts(self):
        filename = 'numbers_list.txt'
        self.hide_all()
        self.text_label.text = func.text_wrap(filename)

    def on_press_button_instruction(self):
        filename = 'instruction.txt'
        self.hide_all()
        self.text_label.text = func.text_wrap(filename)

    def on_press_button_cleaner(self):
        self.btn_start.size = (400, 100)
        self.btn_start.text = 'Старт'
        self.btn_reminder.size = (400, 100)
        self.btn_reminder.text = 'Справочник'
        self.btn_contacts.size = (400, 100)
        self.btn_contacts.text = 'Телефонная книжка'
        self.btn_instruction.size = (400, 100)
        self.btn_instruction.text = 'Инструкция'
        self.btn_cleaner.size = (0, 0)
        self.btn_cleaner.text = ''
        self.text_label.text = ""



class MainApp(App):
    def build(self):
        return MainWidget()



if __name__ == '__main__':
    Config.set("graphics", "resizable", 0)
    Config.set("graphics", "width", 400)
    Config.set("graphics", "height", 800)
    app = MainApp()
    app.run()
