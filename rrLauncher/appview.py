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

    def __init__(self, **kwargs):
        super(AppView, self).__init__(**kwargs)          
 
        #internal variables
        self.touches2 = {}
        self.last_touch_id = -1
        #self.translation_allowed = False
        self.gesture_found = False
        self.position_left = True

        self.set_texture('style/bar/slider-fond.png') 
        """
        #from kivy.core.image import Image
        tex = Image('style/bar/slider-fond.png').texture
        tex.wrap = 'repeat'
        self.texture_sidebar = tex
        #tex = Image('style/1.png').texture
        if tex is not None:
            tex.wrap = 'repeat'
            self.texture = tex
        """
        #add gestures
        self.gdb = GestureDatabase()
        self.create_gesture( [(0,0),(10,0)] )
        self.create_gesture( [(0,0),(-10,0)] )        

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
        #self.allow_translation()
        #if len(self._touches) <= 1 :
        #    return True
        #else :

        l = len(self.touches2)
        if l > 1 :
            #if several touches on the bar
            #print str(l)+' touches on bar'
            self.set_texture('style/bar/bouton-lancer-T2-off.png')   
            x, y = touch.x, touch.y
            # if the touch isnt on the widget we do nothing
            if not self.collide_point(x, y):
                return False

            #don't dispatch touches to children (icons)
            """
            # let the child widgets handle the event if they want
            touch.push()
            touch.apply_transform_2d(self.to_local)
            if super(Scatter, self).on_touch_down(touch):
                touch.pop()
                return True
            touch.pop()
            """
            
            # grab the touch so we get all it later move events for sure
            touch.grab(self)
            self._touches.append(touch)
            self._last_touch_pos[touch] = touch.pos
            
            #return True
        else :
            #regular behaviour 
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
            #3 conditions : 
            dist_c = False #distance from side
            in_bar_c = False #touches are in the bar
            two_touches_c = False #more than one touch

            

            #if touch.id in self.touches2.keys() :
            if dist >= self.bar_translation_min_distance : 
                    dist_c = True
            """
            if touch.x < self.x + self.bar_width : 
                    in_bar_c = True #current touch not outside of bar
                    #print "re"
            """
            if dist_c==True :#and in_bar_c==True :
                  #print "enter it"
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
            #self.allow_translation()      
        return super(AppView, self).on_touch_up(touch) 

    def on_touch_move(self,touch):
        #move only if several touches        
        if len(self.touches2) <= 1 :
            return True
        super(AppView, self).on_touch_move(touch)
    """
    def allow_translation(self):
        if len(self._touches) < 2 :
            self.translation_allowed = False
        else : 
            self.translation_allowed = True
        #print self.translation_allowed
    """
    
    def transform_with_touch(self, touch):
        # PB : By default the kivy scatter does not translate if several touches are down
        # TRICK : So we have to set do_rotation to True and avoid rotation to occur ... 

        # just do a simple one finger drag DOES NOT OCCUR HERE
        #only the last touch moves it
        if len(self._touches) == 1 or not self.last_touch_id == touch.id : return
        
        """
        # we have more than one touch...
        points = [Vector(self._last_touch_pos[t]) for t in self._touches]

        # we only want to transform if the touch is part of the two touches
        # furthest apart! So first we find anchor, the point to transform
        # around as the touch farthest away from touch
        anchor = max(points, key=lambda p: p.distance(touch.pos))

        # now we find the touch farthest away from anchor, if its not the
        # same as touch. Touch is not one of the two touches used to transform
        farthest = max(points, key=anchor.distance)
        if points.index(farthest) != self._touches.index(touch):
            return
        """
        # _last_touch_pos has last pos in correct parent space,
        # just like incoming touch
        dx = (touch.x - self._last_touch_pos[touch][0]) \
                    * self.do_translation_x
        dy = (touch.y - self._last_touch_pos[touch][1]) \
                    * self.do_translation_y
        self.apply_transform(Matrix().translate(dx, dy, 0))
        return
    
    def move_bar_to_right(self):
        #return
        if self.position_left :
            a = Animation(x = self.width - self.bar_width, duration = 1.5)
            a.start(self)
            self.position_left = False
        
    def move_bar_to_left(self):
        #return 
        if self.position_left == False:
            a = Animation(x = 0 , duration = 1.5)
            a.start(self)  
            self.position_left = True

    def move_back(self):
        if self.position_left :
            x = 0
        else : 
            x = self.width - 1.5*self.bar_width   
        a = Animation(x = x, t='out_circ')
        a.start(self)
    
