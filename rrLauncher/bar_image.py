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
        self.down_before_bar_is_moving = []

    def bar_is_moving(self):
        touches2 = self.app.appview.touches2
        if len(touches2)>1 : 
            return True
        else : return False

    def on_touch_down(self, touch):
        if not self.collide_point(*touch.pos):
            return False
        #print 'A barimage on: '+ str(touch.id)+ '  touches2 len: '+ str(len(self.app.appview.touches2) )
        if self.bar_is_moving() :
            #pass touch to appview:
            touch.grab_current = self.app.appview
            # let the child widgets handle the event if they want (copied from Scatter)
            touch.push()
            touch.apply_transform_2d(self.to_local)
            if super(Scatter, self).on_touch_down(touch):
                touch.pop()
                return True
        else :
            #store touch in case another touch is pressed on bar before touch is up, 
            #store touch in order to send a touch up event when removed from bar
            self.down_before_bar_is_moving.append(touch.id) 
        super(BarImage,self).on_touch_down(touch)
        #print 'B barimage on: '+ str(touch.id)+ '  touches2 len: '+ str(len(self.app.appview.touches2) )
        self.app.bar.on_image_touch_down(touch,self.key)
        #self.shake()
    
    def on_touch_up(self,touch):
        #print 'A barimage up: '+ str(touch.id) + '  touches2 len: '+ str(len(self.app.appview.touches2) )
        if self.bar_is_moving() :
            #ignore touch on barimage if bar is moving
            #except if touch is already on, in this case : send a up  
            if touch.id in self.down_before_bar_is_moving:
                self.down_before_bar_is_moving.remove(touch.id) 
                super(BarImage,self).on_touch_up(touch)
                #print 'B barimage up: '+ str(touch.id) + '  touches2 len: '+ str(len(self.app.appview.touches2) )
            else : 
                return False 
        if self.collide_point(*touch.pos):
            #if image outside of bar : set the square on the field 
            if not self.bar.collide_point(*touch.pos):
                if self.app.appview.position_left : #bar is on the left side
                    self.bar.put_on_field(self.key, touch)
            #move back icon to bar
            self.go_back_to_pos()
        #print 'B barimage up: '+ str(touch.id) + '  touches2 len: '+ str(len(self.app.appview.touches2) )
        super(BarImage,self).on_touch_up(touch)
 
    def on_touch_move(self,touch):
        if self.bar_is_moving() or self.app.appview.position_left == False: 
            #stick icon to the bar
            return False
        """
        #get currrent touches 
        touches = self.app.appview.touches2
        if len(touches) > 1:
            return False
        """
        super(BarImage,self).on_touch_move(touch)
    
    def go_back_to_pos(self):
        pos = self.initial_center
        kwargs = {'duration' : 0.9,'t':'in_out_expo'}       
        a = Animation(center = pos, **kwargs)
        a.start(self)

    def shake(self):
        self.center_x +=2
        self.center_y +=2
