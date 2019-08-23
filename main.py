import random
import kivy

from kivy.app import App
from kivy.core.window import Window
from kivy.config import Config
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.properties import NumericProperty

Config.set("graphics", "width", 600)
Config.set("graphics", "height", 600)


class Box(Label):

    value = NumericProperty()

    def __init__(self, **kwargs):
        self.value = kwargs.pop("value")
        super(Box, self).__init__(**kwargs)


class GameSpace(GridLayout):

    def __init__(self, **kwargs):
        super(GameSpace, self).__init__(**kwargs)

        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self.on_keyboard_down)
        self._keyboard.bind(on_key_up=self.on_keyboard_up)

        grid_coor = [[0 for _ in range(row, row + 4)] for row in range(0, 16, 4)]
        for row in grid_coor:
            for value in row:
                self.add_widget(Box(value=value))
        self.new_box()
        self.new_box()

    def new_box(self):
        empty_boxed = []
        for each in self.children:
            if each.value == 0:
                empty_boxed.append(self.children.index(each))
        self.children[random.choices(empty_boxed)[0]].value = 2

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard.unbind(on_key_up=self._on_keyboard_up)
        self._keyboard = None

    def get_box(self, row, col):
        return self.children[-row * 4 + 4 - col]

    def check_value(self, current_box, next_box):
        if next_box.value == 0:
            next_box.value = current_box.value
            current_box.value = 0
            return next_box

    def on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == "up":
            for col in range(1, 5):
                for box in range(2, 5):
                    current_box = self.get_box(box, col)
                    for element in range(box - 1, 0, -1):
                        current_box = self.check_value(current_box, self.get_box(element, col))

        elif keycode[1] == "down":
            for col in range(1, 5):
                for box in range(1, 4):
                    current_box = self.get_box(box, col)
                    for element in range(box, 5,):
                        current_box = self.check_value(current_box, self.get_box(element, col))

        elif keycode[1] == "left":
            pass
        elif keycode[1] == "right":
            pass

    def on_keyboard_up(self, keyboard, keycode):
        pass


class NumberStackApp(App):
    pass


NumberStackApp().run()

