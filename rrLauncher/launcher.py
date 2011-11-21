#import os
#os.environ['KIVY_VIDEO'] = 'ffmpeg'
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scrollview import ScrollView
from kivy.properties import ObjectProperty, NumericProperty, StringProperty, \
    BooleanProperty, DictProperty, ListProperty
from kivy.core.image import Image
from kivy.graphics import Color, Line, Rectangle, BorderImage#LineWidth, 

from random import random

from field import Field
from bar import Bar



class AppView(FloatLayout):
    app = ObjectProperty(None)
    texture_sidebar = ObjectProperty(None)
    texture = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(AppView, self).__init__(**kwargs)
         
        #from kivy.core.image import Image
        tex = Image('style/slider-fond.png').texture
        tex.wrap = 'repeat'
        self.texture_sidebar = tex
        #tex = Image('style/1.png').texture
        if tex is not None:
            tex.wrap = 'repeat'
            self.texture = tex


class LauncherApp(App):

    def build(self):
        self.appview = AppView(app=self)
        
        self.field = Field(app=self, activate_animations = True)
        self.appview.add_widget(self.field)
        
        self.bar = Bar(app = self )
        self.appview.add_widget(self.bar)

        return self.appview    


if __name__ in ('__android__', '__main__'):
    LauncherApp().run()
