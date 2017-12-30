from kivy.lang import Builder
from kivy.uix.button import Button

import time
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.widget import Widget

import os

from Constants import BASEDIR, BLACK, BUTTONKLAAR

Builder.load_file(os.path.join(BASEDIR, 'testen', 'items.kv'))

class Square(Widget):

    bg_color = ObjectProperty(BLACK)

    def __init__(self, **kwargs):
        super(Square, self).__init__(**kwargs)

class Circle(Widget):

    bg_color = ObjectProperty(BLACK)

    def __init__(self, **kwargs):
        super(Circle, self).__init__(**kwargs)

class FinishedButton(Button):

    label_text = StringProperty(BUTTONKLAAR)

    def __init__(self, observer, **kwargs):
        super(FinishedButton, self).__init__(**kwargs)
        self.observer = observer

    def on_button_clicked(self, *args):
        self.observer()

class Event:
    """
    Object to store an event. We define default attributes.
    """
    def __init__(self):
        self.start_time = time.time()
        self.end_time = 0
        # user_event is an event that the user must acknowledge
        self.user_event = False
        # User should acted but didn't
        self.missed_user_event = False
        # User should acted and did
        self.hit_user_event = False
        # fake user_event is an event that the user must *not* acknowledge
        self.fake_user_event = False
        # User acted on fake event
        self.hit_fake_user_event = False



class EventBag:
    """
    Simple FIFO stack to hold events
    """
    def __init__(self):
        self.events = []

    def push(self, obj):
        self.events.append(obj)

    def pull(self):
        if self.events:
            return self.events.pop()

    def get_events(self):
        return self.events
