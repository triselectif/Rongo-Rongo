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
from kivy.graphics.transformation import Matrix

from random import random


class AppView(Scatter):
    app = ObjectProperty(None)
    texture_sidebar = ObjectProperty(None)
    texture = ObjectProperty(None)
    bar_width = NumericProperty(135)
    bar_translation_min_distance = NumericProperty(250)
    content = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(AppView, self).__init__(**kwargs)          
 
        #internal variables
        self.touches2 = {}
        self.last_touch_id = -1
        #self.translation_allowed = False
        self.gesture_found = False
        self.position_left = True
        self.anim = False #currently animated

        self.set_texture('style/bar/slider-fond.png') 
        
        #add gestures
        self.gdb = GestureDatabase()
        self.create_gesture( [(0,0),(10,0)] )
        self.create_gesture( [(0,0),(-10,0)] )        
    '''
    def add_widget(self, child):
        if self.content:
            print child
            return self.content.add_widget(child)
        return super(AppView, self).add_widget(child)
    '''
    def set_texture(self,path):
        #from kivy.core.image import Image
        tex = Image(path).texture
        tex.wrap = 'repeat'
        self.texture_sidebar = tex
        #tex = Image('style/1.png').texture
        if tex is not None:
            tex.wrap = 'repeat'
            self.texture = tex

    def create_gesture(self,point_list):
        # Create a gesture
        g = Gesture()
        g.add_stroke(point_list)
        g.normalize()
        # Add it to database
        self.gdb.add_gesture(g)
    
    def on_touch_down(self,touch):
        id = touch.id
        if touch.x < self.x + self.bar_width :
            self.touches2[id] = touch.pos
            self.last_touch_id = id
        #if len(self._touches) <= 1 :
        #    return True

        l = len(self.touches2)
        if l > 1 :
            #if several touches on the bar
            self.set_texture('style/bar/slider-fond.png')
            
        return super(AppView, self).on_touch_down(touch)    

    def on_touch_up(self,touch):
        id = touch.id
        if id in self.touches2.keys() and len(self.touches2) == 2: 
            #still one more touch on bar
            #does the user want to translate the bar to the right or the left ?
            origin = self.touches2[id]#.pos
            current = touch.pos
            dist = Vector(origin).distance( Vector(current) )
            #print len(self.touches2), self.touches2[id], touch.pos, dist  

            #if touch.id in self.touches2.keys() :
            if dist >= self.bar_translation_min_distance : 
                  # try to find a gesture 
                  g = Gesture()
                  g.add_stroke(point_list=[origin,current])
                  g.normalize()
                  gest = self.gdb.find(g)
                  try : 
                    if gest[0] > 0.95 : #gesture found
                        if len(self.touches2) == 2: #no touch left on bar 
                            d = current[0] - origin[0]
                            if d > 0:
                                self.move_bar_to_right()
                            else : 
                                self.move_bar_to_left()              
                  except : 
                    self.move_back()

            else : self.move_back()

        if id in self.touches2.keys():
                del self.touches2[id]
        if len(self.touches2) <= 0 :
                self.set_texture('style/bar/slider-fond.png')      
        return super(AppView, self).on_touch_up(touch) 


    def on_touch_move(self,touch):
        #move only if several touches        
        if len(self.touches2) <= 1 :
            return True
        super(AppView, self).on_touch_move(touch)
    
    def transform_with_touch(self, touch):
        # PB : By default the kivy scatter does not translate if several touches are down
        # TRICK : So we have to set do_rotation to True and avoid rotation to occur ... 

        # just do a simple one finger drag DOES NOT OCCUR HERE
        #only the last touch moves it
        if not self.last_touch_id == touch.id : return
        
        # _last_touch_pos has last pos in correct parent space,
        # just like incoming touch
        dx = (touch.x - self._last_touch_pos[touch][0]) \
                    * self.do_translation_x
        dy = (touch.y - self._last_touch_pos[touch][1]) \
                    * self.do_translation_y
        if dx > 50 : return
        self.apply_transform(Matrix().translate(dx, dy, 0))
        return
    
    def move_bar_to_right(self):
        if self.position_left :
            #print 'bar : r'
            a = Animation(x = self.width - 1*self.bar_width, duration = 1.5)
            a.bind(on_complete=self.animation_is_over)
            a.start(self)
            self.position_left = False
            self.anim = True
            self.app.bar.unopacify()
        
    def move_bar_to_left(self):
        if self.position_left == False:
            #print 'bar : l'
            a = Animation(x = 0 , duration = 1.5)
            a.bind(on_complete=self.animation_is_over)
            a.start(self)  
            self.position_left = True
            self.anim = True
            self.app.bar.opacify()

    def animation_is_over(self,a,b):
        self.anim = False
        if self.position_left == False :
            self.app.bar.show_leave_app_button()

    def move_back(self):
        if self.anim : return
        #print 'bar : b'
        if self.position_left :
            x = 0
        else : 
            x = self.width - 1.0*self.bar_width   
        a = Animation(x = x, t='out_circ')
        a.start(self)

    def launch_app(self,id, title):
        print 'launch app ' + title
        if self.position_left : 
            self.move_bar_to_right() 

    def leave_current_app(self,a):
        print 'leave app'
        if not self.position_left : 
            self.move_bar_to_left()
        
    
