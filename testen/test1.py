import random
from functools import partial
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout

import time
from kivy.uix.label import Label

from Constants import YOURFINISHED, BLACK, DURATION_1, GREY
from items import Square, Circle, FinishedButton
from kivy.core.window import Window

from items import Event, EventBag


class Sheet(FloatLayout):
    def __init__(self, observer, **kwargs):
        super(Sheet, self).__init__(**kwargs)
        self.observer = observer

        self.current_object = None
        self.current_event = None
        self.grey_event = False
        self.exercise = False

        self.eventbag = EventBag()
        self.square = Square()
        self.circle = Circle()
        self.objects = [self.square, self.circle]

        base_pos_0 = ((Window.width - self.square.width) / 2 ,
                         (Window.height -self.square.height) / 4)
        base_pos_1 = base_pos_0[0], base_pos_0[1] + self.square.height + Window.height / 10
        self.positions = [base_pos_0, base_pos_1]

        self.start_time = time.time()
        self.duration = DURATION_1

        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_key_down)

        # we want 5% of the exercises to contain a real user event and 5% fakes.
        # So an exercise takes 3 seconds so DURATION / 3 = n; number of exercises.
        # (DURATION / 3) * 0.1 = 1/2 real and 1/2 fake
        # And 3% sound events.
        # (DURATION / 3) * 0.01 = 1/3 high, 1/3 low and 1/3 tone_event
        n = DURATION_1 / 3
        E = int(n * 0.1)

        self.eventslist = ['no_event'] * (n - (E + E / 5)) + ['event'] * (E / 2) + ['fake_event'] * (E / 2) +\
                            ['tone_event'] * (E / 5)
        random.shuffle(self.eventslist)

        self._next_exercise()
        self.main_event = Clock.schedule_interval(self._clear_screen, 3)

    def _keyboard_closed(self):
        print('My keyboard have been closed!')
        self._keyboard.unbind(on_key_down=self._on_key_down)
        self._keyboard = None


    def _on_key_down(self, obj, key, *args):
        print key[0]
        if self.current_event == 'event':
            if key[0] == 13:
                self.event.hit_user_event = True
        elif self.current_event == 'fake_event':
            self.event.hit_fake_user_event = True


    def _next_exercise(self, *args):
        if self.exercise:
            self.eventbag.push(self.event)

        if self.start_time + self.duration <= time.time():
            return self.finished()

        self.event = Event()

        self.exercise = True
        self.current_object = None
        self.grey_event = False

        # determine which event we have
        try:
            event = self.eventslist.pop()
        except IndexError:
            event = random.choice(['no_event', 'no_event', 'no_event', 'no_event',
                                   'no_event', 'no_event', 'event', 'fake_event'])

        # state can be:
        # 0 - show both
        # 1+2+3 - show circle
        # 4+5+6 - show square
        # This way we have more change of showing one or the other.
        # if we have an real event state must be 0 or 1 (50% chance for a circle or both)
        if event == 'event':
            state = random.choice([0, 1])

        elif event == 'fake_event':
            state = random.choice([0, 4])
        else:
            state = random.choice(range(7))
        if state == 0:
            random.shuffle(self.positions)
            self.square.pos = self.positions[0]
            self.add_widget(self.square)
            self.circle.pos =self.positions[1]
            self.add_widget(self.circle)
            self.current_object = None
        elif 0 < state < 4:
            self.circle.pos =self.positions[1]
            self.add_widget(self.circle)
            self.current_object = self.circle
        else:
            self.square.pos = self.positions[0]
            self.add_widget(self.square)
            self.current_object = self.square

        if event == 'event':
            # it must be a circle
            self.event.user_event = 'grey circle'
            Clock.schedule_once(partial(self._trigger_grey_event, (self.circle,)))
        elif event == 'fake_event':
            # it must be a square
            self.event.fake_user_event = 'grey square'
            Clock.schedule_once(partial(self._trigger_grey_event, (self.square,)))
        self.current_event = event

    def finished(self):
        print "finished"
        self.main_event.cancel()
        [self.remove_widget(obj) for obj in self.objects]
        self.add_widget(Label(text=YOURFINISHED, color=BLACK, font_size='36dp',
                              size_hint_y=0.4, pos_hint={'top': 0.8}))
        self.add_widget(FinishedButton(self.observer))

        return False

    def _clear_screen(self, *args):
        for obj in self.objects:
            obj.bg_color = BLACK
            self.remove_widget(obj)
        Clock.schedule_once(self._next_exercise, 1)

    def _trigger_grey_event(self, data, *args):
        print "grey_event triggered"
        obj = data[0]

        def set_grey(*args):
            obj.bg_color = GREY
            return False

        Clock.schedule_once(set_grey, 0.75)
        self.grey_event = True
