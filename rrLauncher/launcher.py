from json import loads
from os.path import join, dirname, exists
from kivy.app import App
from kivy.animation import Animation
#from kivy.clock import Clock
from kivy.uix.scatter import Scatter
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty, NumericProperty, StringProperty, \
    BooleanProperty, DictProperty, ListProperty
from kivy.core.image import Image
from kivy.graphics import Color, Line, Rectangle, LineWidth
from kivy.vector import Vector

from datetime import datetime, timedelta
from random import random

class Square(Scatter):
    geometry_id = NumericProperty(None)#location on the field where the Square sits
    #content
    name = StringProperty(None)
    image_source = StringProperty(None)
    description = StringProperty(None)
    screenshot_source = StringProperty(None)
    #shape
    rotation_90d = NumericProperty(0)
    style = DictProperty( {'square_texture_path' : 'style/border30.png'} )
    layout_type = StringProperty(None) #'icon'/'small'/'medium' or 'large'
    icon_size = ObjectProperty( None )
    small_size = ObjectProperty( None )
    medium_size = ObjectProperty( None )
    large_size = ObjectProperty( None )
    #internal variables
    touches = DictProperty( {} ) #current active touches on the widget
    

    def __init__(self,**kwargs) :
        super(Square,self).__init__(**kwargs)
        self.init_layouts()
        """
        from kivy.uix.image import Image
        self.icon = Image(source=self.image_source, size_hint=( None, None), size=(72,72) )
        """
    def init_layouts(self):
        #create a layout for each size so that we can switch
        #easily from one to another 
    
        texture_path = self.style['square_texture_path']
        texture = Image(texture_path).texture
        layout_type = self.layout_type

        def create_layout(text):
            with self.layout_type2layout(text).canvas :
                Color(a, b, c)        
                Rectangle(texture = texture, size = self.layout_type2size(text) )
            l = Label(text=text)
            l.pos = self.center
            self.layout_type2layout(text).add_widget( l )

        #color
        a = random()
        b = random()
        c = random()
        #icon
        self.icon_layout = BoxLayout(size = self.icon_size)
        create_layout('icon')
        #large
        self.large_layout = BoxLayout(size = self.large_size)
        create_layout('large')        
        #medium
        self.medium_layout = BoxLayout(size = self.medium_size)
        create_layout('medium') 
        #small
        self.small_layout = BoxLayout(size = self.small_size)
        create_layout('small') 

        #add a random layout so that it can be removed by the next function
        self.layout = BoxLayout()
        self.add_widget(self.layout) 
        #display the right layout
        self.layout_type2function(layout_type)

    def layout_type2layout(self,layout_type) :
        #print layout_type
        if layout_type == 'large': l = self.large_layout
        elif layout_type == 'medium': l = self.medium_layout
        elif layout_type == 'small': l = self.small_layout
        elif layout_type == 'icon': l = self.icon_layout
        return l

    def layout_type2size(self,layout_type) :
        #print layout_type
        if layout_type == 'large': s = self.large_size
        elif layout_type == 'medium': s = self.medium_size
        elif layout_type == 'small': s = self.small_size
        elif layout_type == 'icon': s = self.icon_size
        return s

    def layout_type2function(self,layout_type) :
        layout = self.layout_type2layout(layout_type)
        return self.set_new_layout( layout )
    """
    def lock(self):
        self.do_translation = False  

    def unlock(self):
        self.do_translation = True  
    """
    def set_new_layout(self, new_layout) :
        #self.new_layout = new_layout
        """
        animation = Animation(size = new_layout.size, duration = 1,t='in_quad')
        animation.bind(on_complete = self.set_new_layout2)
        animation.start(self.layout)
        """
        #def set_new_layout2(self,a,b) :
        self.remove_widget(self.layout)
        self.layout = new_layout
        self.add_widget(self.layout)
        self.size = self.layout.size
        """
        if new_layout == "icon" :
            self.lock()
        else : self.unlock()  
        """
    def on_touch_down(self, touch):
        #analyse and store touches so that we know on_touch_up which
        #square was concerned by the touch_up 
        if self.collide_point(touch.x,touch.y):
            self.touches[touch.id] = touch
        super(Square, self).on_touch_down(touch)       
    
    def on_touch_up(self, touch):
        super(Square, self).on_touch_up(touch)
        if not touch.id in self.touches : return
        del self.touches[touch.id]

        if self.collide_point(touch.x,touch.y):
            #print self.rotation
            self.parent.process_touch_up(self)
            return True
            
    
         
class GeometrySquare(Scatter):
    style = DictProperty({'color':(0.5,0.5,0.5,0.5), 'texture_path':'style/border29.png' })
    layout_type = StringProperty('')
    geometry_id = NumericProperty(0)#location on the field
    
    def __init__(self,**kwargs) :
        super(GeometrySquare, self).__init__(**kwargs)
        #draw
        style = self.style
        color = style['color']
        a,b,c,d = color
        texture_path = style['texture_path']
        texture = Image(texture_path).texture      

        with self.canvas :
            Color(a, b, c)        
            Rectangle(texture = texture, size =self.size)
        

class Field(Widget):
    app = ObjectProperty(None)
    style = DictProperty({'geometry_square_margin':13  })
    #internal variables
    squares = DictProperty( {} )#stores all the squares widgets
    geometry = DictProperty( {} )#geometry = squares' target relative positions and sizes on the field
    geometry_detailed = DictProperty( {} ) #real positions on the field
    geometry_squares = DictProperty( {} ) 
    #stores all the geometry empty squares as widgets so that we can easily
    #compare their positions with the real squares

    #bar variables
    bar_width = NumericProperty(155)
    bar_start_geometry_id = NumericProperty(0)

    def __init__(self,**kwargs) :
        super(Field, self).__init__(**kwargs)
        self.init_geometry()
        self.init_geometry_detailed()
        self.draw_geometry()
        self.init_squares()

    def get_size(self, layout_type) :
        if layout_type == 'icon':
            l,h = self.geometry["icon_px"]
            return (l,h) 
        margin = self.style['geometry_square_margin']
        width,height = self.size
        l,h = self.geometry[layout_type]
        l = l * width - 2*margin
        h = h * height - 2*margin
        return (l,h) 
    
    def init_geometry(self):
        #Import the json file that defines it
        file_path = join(dirname(__file__), 'field_geometry')
                
        with open(file_path, 'r') as fd:
            self.geometry = loads(fd.read())
            #print self.geometry

        if self.geometry is None:
            print 'Unable to load', file_path
            return

        #get the nb of squares in the field
        max = 0
        for i in self.geometry :
             if i not in ["vertical", "icon_px","small","medium", "large"]:
                 i = int(i)
                 if i > max : max = i 
        self.bar_start_geometry_id = max + 1

    def init_geometry_detailed(self):
        #calculates detailed geometry
        style = self.style
        margin = style['geometry_square_margin']
        bar_width = self.bar_width
        width,height = self.size       
        
        for key,val in self.geometry.iteritems() :
            if not key in ["icon_px","large","medium","small","vertical"]: 
                x,y,square_layout_type = val
                x = x * width + margin + self.x + bar_width
                y = y * height + margin + self.y
                l,h = self.get_size(square_layout_type)
 
                #update geometry_detailed
                self.geometry_detailed[key] = {'pos':(x,y),'size':(l,h),'layout_type':square_layout_type}
        
    def draw_geometry(self):
        self.draw_empty_squares()
    
    def draw_empty_squares(self):
        #draw the shape of all empty locations on the field
        for key,val in self.geometry_detailed.iteritems() :
                id = key    
                pos = val['pos']
                size = val['size']
                layout_type = val['layout_type']
                self.geometry_squares[key] = GeometrySquare(
                           geometry_id = int(id), 
                           pos = pos, 
                           size =size, 
                           layout_type = layout_type, 
                           do_scale = False, 
                           do_rotation = False, 
                           do_translation = False, 
                           auto_bring_to_front = False
                           )
                self.add_widget( self.geometry_squares[id] )

        #in the bar
        bar_width = self.bar_width
        m = self.style['geometry_square_margin']
        icon_size = self.get_size('icon')
        padding_left = int((bar_width - icon_size[0])/2) 
        #starting index
        min = self.bar_start_geometry_id
        #calculate the nb of squares that could fit in there without scrolling
        max = int( (self.height - m)/(icon_size[1]+m) )       

        for i in xrange(0,max):
            self.geometry_squares[str(min+i)] = GeometrySquare(
                           geometry_id = min+int(i), 
                           pos = (padding_left,m+(icon_size[1]+m)*i), 
                           size = icon_size, 
                           layout_type = "icon", 
                           do_scale = False, 
                           do_rotation = True, 
                           do_translation = False, 
                           auto_bring_to_front = False
                           )
            self.add_widget( self.geometry_squares[str(min+i)] ) 
    

    def init_squares(self):
        #create and display squares
        for key,val in self.geometry_detailed.iteritems():
                id = key
                pos = val['pos']
                size = val['size']
                layout_type = val['layout_type']
                self.squares[id] = Square(
                            pos = pos, 
                            size = size, 
                            layout_type = layout_type, 
                            do_scale = False, 
                            geometry_id = int(id),
                            icon_size = self.get_size('icon'),
                            small_size = self.get_size('small'),
                            medium_size = self.get_size('medium'),
                            large_size = self.get_size('large'),
                            image_source = "apps/icon.png"
                            )
                self.add_widget(self.squares[id])

                #in case the screen is displayed vertically
                if self.geometry["vertical"] == 'True' :
                    self.rotate(self.squares[id], 90)
                    self.squares[id].rotation_90d = 1

    def process_touch_up(self, square) :
            #focus on rotation
            current_rot = (90 * square.rotation_90d)%360
            #print current_rot
            if square.rotation > (current_rot + 45) : 
                target_rot = (current_rot + 90)
                square.rotation_90d +=1
            elif square.rotation < (current_rot - 45) : 
                target_rot = (current_rot + 270)
                square.rotation_90d +=1
            #elif square.rotation < (current_rot - 45) : target_rot = (current_rot - 90)
            else : target_rot = current_rot
            self.rotate(square, target_rot)

            #focus on translation
            """
            #check if within the fast launcher bar
            bar = self.app.bar.layout
            x,y = self.to_window(square.x,square.center[1])
            #print x,y,bar.width
            if bar.collide_point(x,y) or x < bar.x :
                print "in the bar"
                self.add_to_bar(square)
                return
            """
            matcher = self.find_matcher(square)
            if matcher is not None :
                self.switch(square, matcher)
            else : 
                self.push_back_into_place(square)

        
    def push_back_into_place(self,square) :
        id = str(square.geometry_id)
        animation = Animation(pos = self.geometry_squares[id].pos, duration = 0.2,t='in_quad')
        animation.start(square)

    def rotate(self,square, rotation) :
        animation = Animation(rotation = rotation, duration = 0.2,t='in_quad')
        animation.start(square)
    """
    def add_to_bar(self,square) :
        bar = self.app.bar
        #geometry id to unfill
        geometry_id = square.geometry_id
        self.remove_widget(square)
        bar.layout.add_widget(square)
        square.layout_type2function("icon")
        #square.size = self.get_size("icon")
        square.geometry_id = 1000
        print 'added to bar'        
    """
    def find_matcher(self,square):
        geometry_id = str(square.geometry_id)
        geometry_squares = self.geometry_squares
        
        #center of the current widget is the reference
        x1,y1 = square.center

        matching_list = [] 
        for key,val in geometry_squares.iteritems() :
            if not str(key) == geometry_id :
                if val.collide_point(x1,y1) :
                    matching_list.append(key)
        l = len(matching_list)
        #one matches
        if l == 1:
            return matching_list[0]
        #none matches
        elif l == 0 : 
            return None
        #several match, get the closest
        elif l>1 :
            closest_dist = 1000000000000000000000
            closest_widget = 0 
            for key in matching_list :
                #get distance to target widget center
                x2,y2 = geometry_squares[key].center        
                dist = Vector(x1,y1).distance( Vector(x2,y2) )
                if dist < closest_dist : 
                    closest_dist = dist
                    closest_widget = key
            return closest_widget

    def switch(self, square, matcher) :    
        #switch position with another widget
        #get current properties of the target empty square to switch with 
        target = self.geometry_squares[matcher]
        target_layout = target.layout_type
        target_pos = target.pos
        target_size = target.size
        #get current square properties
        current_layout = square.layout_type
        current_pos = self.geometry_squares[str(square.geometry_id)].pos
        current_size = square.size
        #get the target square
        target = 0
        for key,val in self.squares.iteritems() :
            if val.geometry_id == int(matcher) : 
                target = self.squares[key]
        #if empty location
        
        def place_square():
            if int(matcher) >= self.bar_start_geometry_id :
                layout_type = 'icon'
            else : layout_type = self.geometry[matcher][2]
            #move to there
            if layout_type == 'icon' and square.rotation_90d ==0 : square.pos = target_pos
            animation = Animation(pos = target_pos, size = target_size, duration = 0.5,t='in_out_cubic')
            animation.start(square)
            #resize
            square.layout_type2function(layout_type)
            square.geometry_id = int(matcher)
        
        if target == 0 :
            place_square()
            return
        #switch sizes
        if current_size <> target_size : 
            square.size = target_size
            target.size = current_size
        
        #switch pos and size
        animation = Animation(pos = target_pos, size = target_size, duration = 0.4,t='in_out_cubic')
        animation.start(square)
        animation = Animation(pos = current_pos, size = current_size, duration = 0.4,t='in_out_cubic')
        animation.start(target)
        #switch layouts
        square.layout_type = target_layout
        target.layout_type = current_layout
        #if square.layout_type <> target.layout_type :
        square.layout_type2function(target_layout)
        target.layout_type2function(current_layout)
        #store pos
        target.geometry_id = square.geometry_id
        square.geometry_id = int(matcher)                    
         





class Bar(ScrollView):
    app = ObjectProperty(None)
    style = DictProperty( {'texture_path':'style/border29.png', 'geometry_square_margin' : 13} )
    geometry = DictProperty( {} )
    icon_size = ObjectProperty( None )
    start_geometry_id = NumericProperty( None ) #so that there's no common index with the field
    geometry_squares = DictProperty( {} )

    def __init__(self,**kwargs) :
        super(Bar, self).__init__(**kwargs) 
        """
        #draw
        color = (1,1,1,1) 
        a,b,c,d = color
        texture_path = self.style['texture_path']
        texture = Image(texture_path).texture      

        with self.canvas :
            Color(a, b, c)        
            Rectangle(texture = texture, size =self.size)
        """

        m = self.style['geometry_square_margin']
        self.layout = Widget(size_x = 72, size_hint_y=None)
        self.init_geometry()

        #starting index
        min = self.start_geometry_id
        #calculate the nb of squares that could it in there without scrolling
        max = int( (self.height - m)/(self.icon_size[1]+m) )
        
        for i in xrange(0,max):
            self.geometry_squares[min+i] = GeometrySquare(
                           geometry_id = min+int(i), 
                           pos = (m,m+(self.icon_size[1]+m)*i), 
                           size = self.icon_size, 
                           layout_type = "icon", 
                           do_scale = False, 
                           do_rotation = True, 
                           do_translation = False, 
                           auto_bring_to_front = False
                           )
            self.layout.add_widget( self.geometry_squares[min+i] ) 
                           
        self.add_widget(self.layout)
    
    def init_geometry(self):
        #Import the json file that defines it
        file_path = join(dirname(__file__), 'field_geometry')
                
        with open(file_path, 'r') as fd:
            self.geometry = loads(fd.read())

        if self.geometry is None:
            print 'Unable to load', file_path
            return

        self.icon_size = self.geometry["icon_px"]
        print self.icon_size

        #get the nb of squares in the field
        max = 0
        for i in self.geometry :
             if i not in ["vertical", "icon_px","small","medium", "large"]:
                 i = int(i)
                 if i > max : max = i 
        self.start_geometry_id = max + 1

    def process_touch_up(self, square) :
        #check a drag n drop to the field occured
        if square.center[0] > self.width :
            print "out"
        else : print "in" 
        """
        matcher = self.find_matcher(square)
        if matcher is not None :
                self.switch(square, matcher)
        else : 
                self.push_back_into_place(square)
        """
    """
    def add_widget(self, widget):
        if self.container is None:
            return super(Bar, self).add_widget(widget)
        # Nop.
        image = BankImage(source=widget.source_side, bank=self)
        widget.bank = self
        self.objects[widget.source_side] = (widget, image)
        return self.container.add_widget(image)
    
    def remove_widget(self, widget):
        if self.container is None:
            return super(Bank, self).remove_widget(widget)
        return self.container.remove_widget(widget)
    
    def put_on_field(self, fn, touch):
        widget, image = self.objects[fn]
        self.container.remove_widget(image)
        self.app.field.add_and_track(widget, touch)

    def put_back(self, widget):
        widget, image = self.objects[widget.source_side]
        self.app.field.remove_widget(widget)
        self.container.add_widget(image)

    def on_touch_down(self, touch):
        if super(Bar, self).on_touch_down(touch):
            return True
        for child in self.parent.children:
            if child is self:
                continue
            child.close()
        self.open()

    def open(self):
        if self.container in self.children:
            return
        super(Bank, self).add_widget(self.container)

    def close(self):
        if self.container not in self.children:
            return
        super(Bank, self).remove_widget(self.container)
    """
    def add_square(self,square):
        self.layout.add_widget(square)

class AppView(FloatLayout):
    app = ObjectProperty(None)
    texture_sidebar = ObjectProperty(None)
    texture = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(AppView, self).__init__(**kwargs)

        tex = Image('style/sidebar.png').texture
        tex.wrap = 'repeat'
        self.texture_sidebar = tex
        tex = Image('style/1.png').texture
        if tex is not None:
            tex.wrap = 'repeat'
            self.texture = tex     


class LauncherApp(App):

    def build(self):
        self.appview = AppView(app=self)
        
        #self.bar = Bar(app = self )
        #self.appview.add_widget(self.bar)
        
        self.field = Field(app=self)
        self.appview.add_widget(self.field)
        
        #self.field.load_bank() 
        
        #self.theoric_field_setup() 

        return self.appview    


if __name__ in ('__android__', '__main__'):
    LauncherApp().run()
