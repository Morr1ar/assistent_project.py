from assistent_project import Assistant

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

    def on_press_button_start(self):
        Assistant().start()

    def on_press_button_reminder(self):
        filename = 'reminder_list.txt'
        text = ""
        text_list = [line.strip() for line in open(filename, encoding="utf-8").readlines()]
        if len(text_list) >= 15:
            count = 15
        else:
            count = len(text_list)
        for i in range(count):
            if len(text_list[i]) > 20:
                x = 0
                while x < len(text_list[i]):
                    text += text_list[i][x:x + 20] + '\n'
                    x += 20
            else:
                text += text_list[i] + '\n'
        self.text_label.text = text

    def on_press_button_contacts(self):
        filename = 'numbers_list.txt'
        text = ""
        text_list = [line.strip() for line in open(filename, encoding="utf-8").readlines()]
        if len(text_list) >= 15:
            count = 15
        else:
            count = len(text_list)
        for i in range(count):
            if len(text_list[i]) > 20:
                x = 0
                while x < len(text_list[i]):
                    text += text_list[i][x:x + 20] + '\n'
                    x += 20
            else:
                text += text_list[i] + '\n'
        self.text_label.text = text

    def on_press_button_instruction(self):
        filename = 'instruction.txt'
        text = ""
        text_list = [line.strip() for line in open(filename, encoding="utf-8").readlines()]
        if len(text_list) >= 15:
            count = 15
        else:
            count = len(text_list)
        for i in range(count):
            if len(text_list[i]) > 20:
                x = 0
                while x < len(text_list[i]):
                    text += text_list[i][x:x + 20] + '\n'
                    x += 20
            else:
                text += text_list[i] + '\n'
        self.text_label.text = text

    def on_press_button_cleaner(self):
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
