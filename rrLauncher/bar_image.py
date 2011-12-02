from kivy.uix.image import Image
from kivy.uix.scatter import Scatter
from kivy.properties import ObjectProperty, NumericProperty, StringProperty, \
    BooleanProperty, DictProperty, ListProperty
from kivy.animation import Animation

class BarImage(Scatter):

    app = ObjectProperty(None)
    bar = ObjectProperty( None )
    key = StringProperty( -1 )
    source = StringProperty('')
    initial_center = ObjectProperty(None)#next pos to go to

    def __init__(self,**kwargs):
        super(BarImage,self).__init__(**kwargs)
        self.image = Image(source = self.source, size = self.size)
        self.add_widget(self.image)
        self.do_rotation = False
        self.do_scale = False
        self.do_translation = True
        self.auto_bring_to_front = True
        #self.down_before_bar_is_moving = []

    def bar_is_moving(self):
        touches2 = self.app.appview.touches2
        if len(touches2)>1 : 
            return True
        else : return False

    def on_touch_down(self, touch):
        if not self.collide_point(*touch.pos):
            return False
        if self.bar_is_moving() : 
            return False
        #else :
        #    self.down_before_bar_is_moving.append(touch.id) 
        super(BarImage,self).on_touch_down(touch)
        print 'barimage on: '+ str(touch.id)
        self.app.bar.on_image_touch_down(touch,self.key)
        
    
    def on_touch_up(self,touch):
        print 'barimage up: '+ str(touch.id) + '  touches2 len: '+ str(len(self.app.appview.touches2) )
        if not self.collide_point(*touch.pos):
            return False
        if self.bar_is_moving() : 
            #if touch.id in self.down_before_bar_is_moving:
            #    self.down_before_bar_is_moving.remove(touch.id) 
            #else : 
            return False
        if not self.bar.collide_point(*touch.pos):
            self.bar.put_on_field(self.key, touch)
        self.go_back_to_pos()
        
        super(BarImage,self).on_touch_up(touch)
 
    def on_touch_move(self,touch):
        if self.bar_is_moving() : 
            return False
        """
        #get currrent touches 
        touches = self.app.appview.touches2
        if len(touches) > 1:
            return False
        """
        super(BarImage,self).on_touch_move(touch)
    """
    def on_touch_down(self, touch):
        if not self.collide_point(*touch.pos):
            return False
        self.bar.put_on_field(self.key, touch)
    """
    def go_back_to_pos(self):
        pos = self.initial_center
        kwargs = {'duration' : 0.9,'t':'in_out_expo'}       
        a = Animation(center = pos, **kwargs)
        a.start(self)
