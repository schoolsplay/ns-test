from kivy import Config

import time

Config.set('modules', 'inspector', '')

from kivy.core.window import Window
Window.clearcolor = (0.96, 0.96, 0.96, 1)

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout

from testen.test1 import Sheet



class MyApp(App):

    def cbf_test1(self, *args):
        self.screen.remove_widget(self.grid)
        self.current_sheet = Sheet(self.finished)
        self.screen.add_widget(self.current_sheet)

    def cbf_test2(self, *args):
        print "test 2"

    def cbf_test3(self, *args):
        print "test 3"

    def cbf_test4(self, *args):
        print "test 4"

    def build(self):
        self.screen = FloatLayout()
        self.grid = GridLayout(cols=2, spacing=24, padding=24)
        for s in ["Cirkel, vierkant, hode en lage tonen",
                  "Cirkel en vierkant.",
                  "Vierkant",
                  "Knoppenkast"]:
            but = Button(text=s, font_size='24dp', size_hint=(0.4, 0.4), padding=(24, 24))
            but.bind(on_press=self.cbf_test1)
            self.grid.add_widget(but)
        self.screen.add_widget(self.grid)

        return self.screen

    def finished(self, *args):
        print "from app finished"
        self.screen.clear_widgets()
        self.screen.add_widget(self.grid)
        events = self.current_sheet.eventbag.get_events()
        total = len(events)
        total_user_events = 0
        total_fake_events = 0
        total_user_events_hit = 0
        total_fake_user_events_hit = 0
        for e in events:
            if e.user_event:
                total_user_events += 1
            if e.hit_user_event:
                total_user_events_hit += 1
            if e.fake_user_event:
                total_fake_events += 1
            if e.hit_fake_user_event:
                total_fake_user_events_hit += 1

        print "Totaal user events", total_user_events, "waarvan", total_user_events_hit, "geraakt zijn"
        print "Totaal user events", total_fake_events, "waarvan", total_fake_user_events_hit, "geraakt zijn"

MyApp().run()
