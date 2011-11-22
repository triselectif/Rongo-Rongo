#import os
#os.environ['KIVY_VIDEO'] = 'ffmpeg'
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.scatter import Scatter
from kivy.properties import ObjectProperty, NumericProperty, StringProperty, \
    BooleanProperty, DictProperty, ListProperty
from kivy.core.image import Image
from kivy.graphics import Color, Line, Rectangle, BorderImage#LineWidth, 
from kivy.animation import Animation

from random import random

from field import Field
from bar import Bar



class AppView(Scatter):
    app = ObjectProperty(None)
    texture_sidebar = ObjectProperty(None)
    texture = ObjectProperty(None)
    bar_width = NumericProperty(155)

    def __init__(self, **kwargs):
        super(AppView, self).__init__(**kwargs)    
 
        self.touches = {}

        #from kivy.core.image import Image
        tex = Image('style/slider-fond.png').texture
        tex.wrap = 'repeat'
        self.texture_sidebar = tex
        #tex = Image('style/1.png').texture
        if tex is not None:
            tex.wrap = 'repeat'
            self.texture = tex
    """
    def on_touch_down(self,touch):
        if not self.collide_point(*touch.pos):return
        if not touch.x > self.x + self.bar_width :
            self.touches[touch.id] = touch
        self.allow_translation() 
        return super(AppView, self).on_touch_down(touch)
    
    def on_touch_up(self,touch):
        if touch.id in self.touches.keys():
            del self.touches[touch.id]
        self.allow_translation() 
        return super(AppView, self).on_touch_down(touch)     

    def allow_translation(self):
        if len(self.touches) >= 2 :
            self.do_translation_x = False
        else : self.do_translation_x = True
    """    

class LauncherApp(App):

    def build(self):
        self.appview = AppView(app=self, do_rotation = False, do_scale = False, do_translation_y = False )
        
        self.field = Field(app=self, activate_animations = True)
        self.appview.add_widget(self.field)
        
        self.bar = Bar(app = self )
        self.appview.add_widget(self.bar)

        return self.appview    

        self.background = ScrollView()
        self.background.add_widget(self.appview)
        #return self.background

if __name__ in ('__android__', '__main__'):
    LauncherApp().run()
