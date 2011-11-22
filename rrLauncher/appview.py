#from kivy.uix.floatlayout import FloatLayout
#from kivy.uix.scrollview import ScrollView
from kivy.uix.scatter import Scatter
from kivy.properties import ObjectProperty, NumericProperty, StringProperty, \
    BooleanProperty, DictProperty, ListProperty
from kivy.core.image import Image
from kivy.graphics import Color, Line, Rectangle, BorderImage#LineWidth, 
from kivy.animation import Animation
from kivy.gesture import Gesture, GestureDatabase
from kivy.vector import Vector

from random import random


class AppView(Scatter):
    app = ObjectProperty(None)
    texture_sidebar = ObjectProperty(None)
    texture = ObjectProperty(None)
    bar_width = NumericProperty(155)
    bar_translation_min_distance = NumericProperty(400)

    def __init__(self, **kwargs):
        super(AppView, self).__init__(**kwargs)    
        print self.size
        #internal variables
        self.touches2 = {}
        self.translation_allowed = False
        self.gesture_found = False
        self.position_left = True

        #from kivy.core.image import Image
        tex = Image('style/bar/slider-fond.png').texture
        tex.wrap = 'repeat'
        self.texture_sidebar = tex
        #tex = Image('style/1.png').texture
        if tex is not None:
            tex.wrap = 'repeat'
            self.texture = tex

        # Create a gesture
        g = Gesture()
        g.add_stroke(point_list=[(0,0),(10,0)])
        g.normalize()

        # Add it to database
        self.gdb = GestureDatabase()
        self.gdb.add_gesture(g)
    
    def on_touch_down(self,touch):
        id = touch.id
        if touch.x < self.x + self.bar_width :
            self.touches2[id] = touch.pos  
        self.allow_translation()
        #self.move_bar_to_right()
        
        return super(AppView, self).on_touch_down(touch)
    
    def on_touch_up(self,touch):
        id = touch.id
        if id in self.touches2.keys():
            origin = self.touches2[id]
            current = touch.pos
            dist = Vector(origin).distance( Vector(current) )
            if dist >= self.bar_translation_min_distance :
                # try to find a gesture 
                g = Gesture()
                g.add_stroke(point_list=[origin,current])
                g.normalize()
                gest = self.gdb.find(g)
                try : 
                    if gest[0] > 0.95 : #gesture found 
                        if len(self.touches2) == 1: #no touch left on bar 
                            self.move_bar_to_right()              
                except : 
                    self.move_back()
            else : self.move_back()
            del self.touches2[id]
        self.allow_translation()        
        return super(AppView, self).on_touch_up(touch) 

    def on_touch_move(self,touch):
        #if not self.translation_allowed : return
        super(AppView, self).on_touch_move(touch)

    def allow_translation(self):
        if len(self._touches) < 2 :
            self.translation_allowed = False
        else : 
            self.translation_allowed = True
        #print self.translation_allowed
     
    def move_bar_to_right(self):
        if self.position_left :
            a = Animation(x = self.width - 1.5*self.bar_width, duration = 1.5)
            a.start(self)
            self.position_left = False
        
    def move_bar_to_left(self):   
        self.position_left = True

    def move_back(self):
        if self.position_left :
            x = 0
        else : 
            x = self.width - 1.5*self.bar_width   
        a = Animation(x = x, t='out_circ')
        a.start(self)
    
