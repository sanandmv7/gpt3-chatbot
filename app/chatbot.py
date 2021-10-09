from kivy.clock import Clock
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.label import MDLabel
from kivy.properties import StringProperty, NumericProperty
from kivy.core.text import LabelBase
import os
import openai

Window.size = (350, 550)
openai.api_key = os.getenv('OPENAI_APIKEY')


def gpt3(prompt, engine='davinci', response_length=64,
         temperature=0.5, top_p=1, frequency_penalty=0, presence_penalty=0,
         start_text='', restart_text='', stop_seq=[]):
    response = openai.Completion.create(
        prompt=prompt + start_text,
        engine=engine,
        max_tokens=response_length,
        temperature=temperature,
        top_p=top_p,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
        stop=stop_seq,
    )
    answer = response.choices[0]['text']
    new_prompt = prompt + start_text + answer + restart_text
    return answer, new_prompt


class Command(MDLabel):
    text = StringProperty()
    size_hint_x = NumericProperty()
    halign = StringProperty()
    font_name = "Poppins"
    font_size = 17


class Response(MDLabel):
    text = StringProperty()
    size_hint_x = NumericProperty()
    halign = StringProperty()
    font_name = "Poppins"
    font_size = 17


class ChatBot(MDApp):
    prompt = "The following is a conversation between a Human and an AI. The AI is helpful, creative, clever, and very friendly."

    def change_screen(self, name):
        screen_manager.current = name

    def build(self):
        global screen_manager
        screen_manager = ScreenManager()
        screen_manager.add_widget(Builder.load_file("Main.kv"))
        screen_manager.add_widget(Builder.load_file("Chats.kv"))
        return screen_manager

    def bot_name(self):
        if screen_manager.get_screen('main').bot_name.text != "":
            screen_manager.get_screen('chats').bot_name.text = screen_manager.get_screen('main').bot_name.text
            screen_manager.current = "chats"

    def response(self, *args):
        self.prompt += "\nHuman:" + value
        response, self.prompt = gpt3(self.prompt,
                                     temperature=0.6,
                                     frequency_penalty=1,
                                     presence_penalty=1,
                                     start_text='\nAI:',
                                     restart_text='\nHuman:',
                                     stop_seq=['\nHuman:', '\n'])
        screen_manager.get_screen('chats').chat_list.add_widget(Response(text=response, size_hint_x=.75))

    def send(self):
        global size, halign, value
        if screen_manager.get_screen('chats').text_input != "":
            value = screen_manager.get_screen('chats').text_input.text
            if len(value) < 6:
                size = .22
                halign = "center"
            elif len(value) < 11:
                size = .32
                halign = "center"
            elif len(value) < 16:
                size = .45
                halign = "center"
            elif len(value) < 21:
                size = .58
                halign = "center"
            elif len(value) < 26:
                size = .71
                halign = "center"
            else:
                size = .77
                halign = "left"

            screen_manager.get_screen('chats').chat_list.add_widget(
                Command(text=value, size_hint_x=size, halign=halign))
            Clock.schedule_once(self.response, 2)
            screen_manager.get_screen('chats').text_input.text = ""


if __name__ == '__main__':
    LabelBase.register(name="Poppins", fn_regular="Poppins-Regular.ttf")
    ChatBot().run()
