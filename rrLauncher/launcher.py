from json import loads
from os.path import join, dirname, exists
from os import walk

from kivy.app import App
from kivy.animation import Animation
#from kivy.clock import Clock
from kivy.uix.scatter import Scatter
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
#from kivy.uix.stacklayout import StackLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.widget import Widget
#from kivy.uix.video import Video
from kivy.uix.scrollview import ScrollView
from kivy.properties import ObjectProperty, NumericProperty, StringProperty, \
    BooleanProperty, DictProperty, ListProperty
from kivy.core.image import Image
from kivy.graphics import Color, Line, Rectangle, BorderImage#LineWidth, 
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.utils import interpolate

from datetime import datetime, timedelta
from random import random

from video_player import VideoPlayer
from bar_image import BarImage
from super_button import SuperButton

class VideoPlayer2(VideoPlayer):
    def on_touch_down(self,touch):
        super(VideoPlayer2,self).on_touch_down(touch)  
        return True      

class Bar(FloatLayout):
    objects = DictProperty( {} )
    app = ObjectProperty(None)
    apps = DictProperty( {} )
    element_size = ObjectProperty( (70,70) )
    sorting_condition = StringProperty( 'app_type' )
    
    def __init__(self,**kwargs):
        super(Bar,self).__init__(**kwargs)
        self.apps = self.app.field.init_apps()
        self.size_hint = (None,1)
        self.width = 155
        self.geometry_squares = {}
        self.images = {}
        self.sorting = []  
        #self.scroll = ScrollView( size_hint=(1, None), height = 1500 )
        #self.add_widget(self.scroll) 
        self.layout = Widget(size_hint = (1,1) )#self.add_widget(self.layout)
        self.add_widget(self.layout)
        self.draw_empty_squares()
        self.sort()
        self.fill()

    def sort(self):
        #list of app keys in order
        #if self.sorting_condition == 'app_type':
        self.sorting = self.apps.keys()

    def resort(condition):
        self.sorting_condition = condition
        self.sort()
        #animate icons now

    def fill(self):
        #print 'apps'
        #print self.apps
        gs = self.geometry_squares 
        s = self.sorting
        for key,val in self.apps.iteritems() :
            #get destination gs
            g = gs[ str( s.index(key) ) ]
            center = g.center 
            self.add_app(key,val,center)    

    def add_app(self, key, app, center):
        # Nop.
        self.images[key] = BarImage( source= str(app["image_path"]) , app =self.app, bar=self, key=key, center =center, initial_center = center )
        #self.images[key].center = center
        
        self.layout.add_widget(self.images[key])

    def draw_empty_squares(self):
        apps = self.apps
        m = self.app.field.style['geometry_square_margin']
        padding_left = int((self.width - self.element_size[0])/2) 
        max = len(apps)       

        for i in xrange(0,max):
            self.geometry_squares[str(i)] = GeometrySquare(
                           geometry_id = i, 
                           pos = (padding_left,m+(self.element_size[1]+m)*i), 
                           size = self.element_size, 
                           layout_type = "icon", 
                           do_scale = False, 
                           do_rotation = False, 
                           do_translation = False, 
                           auto_bring_to_front = False
                           )
            self.layout.add_widget( self.geometry_squares[str(i)] ) 

    def put_on_field(self, key, touch):
        self.app.field.add_app(key, touch)
   

class Square(Scatter):
    geometry_id = NumericProperty(None)#location on the field where the Square sits
    #content
    id = StringProperty('')
    title = StringProperty(None)
    app_type = StringProperty(None) #'info', 'service', 'jeu'
    color = ObjectProperty( (.82,.82,.82,1) )
    color_down = ObjectProperty( (1,1,0,1) )
    color_up = ObjectProperty( (.1,.1,.1,1) )
    authors = StringProperty(None)
    main_media_type = StringProperty(None) #'image' or 'video'
    image_path = StringProperty(None)
    video_path = StringProperty(None)
    #shape
    rotation_90d = NumericProperty(0)
    layout_type = StringProperty(None) #'icon'/'small'/'medium' or 'large'
    icon_size = ObjectProperty( None )
    small_size = ObjectProperty( None )
    medium_size = ObjectProperty( None )
    large_size = ObjectProperty( None )
    #internal variables
    touches = DictProperty( {} ) #current active touches on the widget
    #buttons = DictProperty( {} ) #store buttons widgets
    square_parameters = DictProperty( {} ) #initial parameters of the square
    texture_path = StringProperty("")
    layout = ObjectProperty( None )#base layout for all the widgets
    layers = DictProperty( {} )#stores background text layers of each size
    layer_texture_path = StringProperty( '' )
    process_touch_up_forbidden = BooleanProperty(False)
    padding = NumericProperty(10) #square layout padding

    def __init__(self,**kwargs) :
        super(Square,self).__init__(**kwargs)  

        if self.main_media_type == 'video' :
            self.video = VideoPlayer(source = self.video_path)
            self.video.bind(on_unmute =self.on_unmute)
            self.video.bind(on_start=self.on_start)
            self.video.bind(on_fullscreen = self.on_fullscreen)
            self.video.bind(on_leave_fullscreen = self.on_leave_fullscreen)
        
        l,h = self.size
        pad = self.padding
        self.layout = BoxLayout(orientation = 'vertical', size = (l -2*pad,h -2*pad), pos = (pad,pad) )           
        self.init_layouts() 
    
    def on_start(self, a):
        try :
            self.parent.mute(self.uid) #mute other parents' video players
        except:
            pass
        self.video.unmute(1) #unmute the player

    def on_unmute(self,a):
        try :
            self.parent.mute(self.uid)                
        except : 
            pass

    def mute(self):
        if self.main_media_type == 'video':
            self.video.mute(1)
 
    def on_fullscreen(self, a):
        self.video.stop(1)
        vid = self.video
        self.parent.play_video_fullscreen(self.video_path, self.to_parent(vid.x,vid.y) , self.video.size, self.video.video.position)
        
    def on_leave_fullscreen(self, a):
        pass 

    def process_font_size(self, text, font_size):
        #in case the text is multiline, reduce the font size
        multiline = False
        for i in text : 
            if i == '\n' : multiline = True
        if not multiline : return font_size
        else : return font_size - 6            

    def init_layouts(self):
        
        layout_type = self.layout_type
        param = self.square_parameters[layout_type] #load parameters specific to that size (small, medium, large)
        
        #color
        a,b,c,d = self.color_up
        
        ######################### LAYOUT ##########################################################
        
        self.texture_path = texture_path = str(param['texture_path']) #self.style['square_texture_path']
        #text layer
        self.layer_texture_path = self.layers[layout_type]
        """
        from kivy.uix.image import Image
        self.layer = Image(source = "apps/layers/xyz/large.png", size_hint = (1,1))
        self.layout.add_widget(self.layer)
        """         
        #top part : Title, app_type, authors
        self.box_top = BoxLayout(orientation = 'horizontal', size_hint = param['box_top_size_hint'] )
        font_size = self.process_font_size( self.title, int( param['title_label_font_size']) )
        self.title_label = Label(text=self.title, font_size = font_size, color = self.color_down, halign = 'left')#, padding_x = 5  )
        self.box2 = BoxLayout(orientation = 'vertical', size_hint = param['box2_size_hint'], padding = 2 )
        from kivy.uix.image import Image
        self.app_type_pic = Image(source = str(self.app_type), size_hint = (1,3) )      
        self.authors_label = Label(text = self.authors, font_size = int( param['authors_label_font_size'] ), color = self.color_up, halign = 'right' )
        self.box2.add_widget(self.app_type_pic)
        self.box2.add_widget(self.authors_label)
        self.box_top.add_widget(self.title_label)
        self.box_top.add_widget(self.box2)
        self.layout.add_widget( self.box_top ) 
        
        #middle part : Image or Video
        self.box_middle = BoxLayout(orientation = 'horizontal', size_hint = param['box_middle_size_hint'] )
        self.box_middle1 = BoxLayout(orientation = 'horizontal', size_hint = param['box_middle1_size_hint'], padding = 0, spacing = 0 )
        self.box_middle2 = BoxLayout(orientation = 'horizontal', size_hint = param['box_middle2_size_hint'], padding = 0, spacing = 0 )
        self.box_middle.add_widget( self.box_middle1 ) 
        self.box_middle.add_widget( self.box_middle2 ) 
        if self.main_media_type == 'image' : 
            from kivy.uix.image import Image
            image = Image(source = self.alternative_image_path, size_hint = (1,1) )
            self.box_middle1.add_widget( image ) 
        elif self.main_media_type == 'video' : 
            self.box_middle1.add_widget( self.video ) 
        self.layout.add_widget( self.box_middle ) 

        #Bottom part : buttons
        self.box_bottom = BoxLayout(orientation = 'horizontal', size_hint = param['box_bottom_size_hint'] )
        self.box_bottom.padding = int( param['box_bottom_padding'] ) #box.height*0.15
        self.vote_button = Button(text = 'voter', size_hint = (None,None), size=param["vote_button_size"] ) #, size = (box.width*0.25 - margin[0], box.height - 2*margin[1]), pos=margin) #size_hint = (0.5,1) )
        self.vote_button.bind( on_press = self.vote )
        self.box_bottom.add_widget( self.vote_button ) 
        self.launch_button = Button(text = 'lancer', size_hint = (None,None), size=param["launch_button_size"] ) #, size = (box.width*0.25, box.height - 2*margin[1]), pos=(box.width - margin[0], margin[1]) )
        #self.launch_button = SuperButton(source = 'style/square_icon.png', size_hint = (None,None), size=param["launch_button_size"] ) 
        self.launch_button.bind( on_press = self.launch ) 
        self.box_bottom.add_widget( self.launch_button )
        self.box_bottom.spacing = (self.layout.width - self.vote_button.width - self.launch_button.width)#*0.97
        self.layout.add_widget( self.box_bottom )

        self.add_widget(self.layout)
    

    def layout_type2size(self,layout_type) :
        #print layout_type
        pad = self.padding
        if layout_type == 'large':
            l,h = self.large_size
            s = (l -2*pad,h -2*pad)
        elif layout_type == 'medium': 
            l,h = self.medium_size
            s = (l -2*pad,h -2*pad)
        elif layout_type == 'small': 
            l,h = self.small_size
            s = (l -2*pad,h -2*pad)
        elif layout_type == 'icon': 
            l,h = self.icon_size
            s = (l -2*pad,h -2*pad)
        return s     

    def refresh_layout(self, layout_type) :
        size = self.layout_type2size(layout_type)
        pad = self.padding
        self.layout_type = layout_type
        
        kwargs = {'duration' : 1.1,'t':'in_quart'}
        anim = Animation(pos = (pad,pad), size = size, **kwargs)
        anim.start(self.layout)
        
        #refresh background texture
        Clock.schedule_once(self.refresh_background, 1.1)

    def refresh_background(self, a):
        self.texture_path = str( self.square_parameters[self.layout_type]['texture_path'] )
        self.layer_texture_path = self.layers[self.layout_type]

    def launch(self,a):
        print 'launch app ' + self.title 

    def vote(self,a):
        print 'vote for app ' + self.title       
    
    def on_touch_down(self, touch):
        #analyse and store touches so that we know on_touch_up which
        #square was concerned by the touch_up 
        if self.collide_point(touch.x,touch.y):
            self.touches[touch.id] = touch
            #enlarge a bit
            self.reshape_when_touch_down(touch, 2)     
        super(Square, self).on_touch_down(touch)  
    
    def on_touch_up(self, touch):
        super(Square, self).on_touch_up(touch)
        if not touch.id in self.touches : return
        del self.touches[touch.id]

        if self.collide_point(touch.x,touch.y):
            #print self.rotation
            if not self.process_touch_up_forbidden : 
                self.parent.process_touch_up(self)
            #reduce size a bit
            self.reshape_when_touch_up(touch)  
            return True   
    
    def reshape_when_touch_down(self, touch, intensity):
        self.color = self.color_down
        self.pos = (self.x + intensity, self.y + intensity)
        self.title_label.color = self.color_up
        self.texture_path = 'style/square_large_touch_down.png'
        #self.app_type_label.color = self.color_up
        #self.size = (self.width + 3, self.height + 3)
        #a = Animation(center = self.center, size = self.size)
        #a.start(self)

    def reshape_when_touch_up(self, touch):
        self.color = self.color_up
        self.title_label.color = self.color_down
        #self.app_type_label.color = self.color_up
        self.texture_path = 'style/square_large.png'
        pass

    
        
         
class GeometrySquare(Scatter):
    style = DictProperty({'texture_path':'style/slider-sous-tommette2.png' })
    layout_type = StringProperty('')
    geometry_id = NumericProperty(0)#location on the field
    
    def __init__(self,**kwargs) :
        super(GeometrySquare, self).__init__(**kwargs)
        #draw
        style = self.style
        texture_path = style['texture_path']    
        

class Field(Widget):
    app = ObjectProperty(None)
    style = DictProperty({'geometry_square_margin':13  })
    activate_animations = BooleanProperty( False )
    #internal variables
    squares = DictProperty( {} )#stores all the squares widgets
    geometry = DictProperty( {} )#geometry = squares' target relative positions and sizes on the field
    geometry_detailed = DictProperty( {} ) #real positions on the field
    geometry_squares = DictProperty( {} )
    square_parameters = DictProperty( {} ) #defines the details of the square 
    #stores all the geometry empty squares as widgets so that we can easily
    #compare their positions with the real squares
    apps = DictProperty( {} )#stores all the apps information
    video = ObjectProperty( None )
    video_size_pos = DictProperty( {} )
    bar_width = NumericProperty(155)
    square_padding = NumericProperty(10)

    def __init__(self,**kwargs) :
        super(Field, self).__init__(**kwargs)
        self.init_geometry()
        self.init_geometry_detailed()
        self.draw_geometry()
        self.apps = self.init_apps()
        self.init_square_parameters()
        self.init_squares()       

    def get_size(self, layout_type) :
        if layout_type == 'icon':
            l,h = self.geometry["icon_px"]
            return (l,h) 
        margin = self.style['geometry_square_margin']
        #Current screen size is applied
        #width,height = self.size
        width,height = self.geometry["screen_size"]
        l,h = self.geometry[layout_type]
        l = l * width - 2*margin 
        h = h * height - 2*margin 
        return (l,h) 

    def square_is_in_the_bar(self,square):
        return False
        
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
             if i not in ["screen_size","vertical", "icon_px","small","medium", "large"]:
                 i = int(i)
                 if i > max : max = i 
        #self.bar_start_geometry_id = max + 1

    
    def init_geometry_detailed(self):
        #calculates detailed geometry
        style = self.style
        margin = style['geometry_square_margin']
        bar_width = self.bar_width
        #Current screen size is applied
        #width,height = self.size
        width,height = self.geometry["screen_size"]       
        
        for key,val in self.geometry.iteritems() :
            if not key in ["screen_size","icon_px","large","medium","small","vertical"]: 
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
                           auto_bring_to_front = False, 
                           )
                self.add_widget( self.geometry_squares[id] )
        print self.geometry_squares
    
    def init_square_parameters(self):
        #Import the json files that defines each type of square
        for i in ['small','medium','large']:
            file_path = join(dirname(__file__), i)
            print file_path
                
            with open(file_path, 'r') as fd:
                self.square_parameters[i] = loads(fd.read())
                print self.square_parameters[i]

            if self.square_parameters[i] is None:
                print 'Unable to load', file_path
                return
        #print self.square_parameters 

    def init_apps(self):
        #Import the json file that defines apps
        file_path = join(dirname(__file__), 'apps','detail')
        apps = {}
        nb = 0
        for subdir, dirs, files in walk(file_path):
            for file in files:
                print file
                with open(file_path +'/'+file, 'r') as fd:
                    t = loads(fd.read())
                    apps[str(nb)] = t 
                nb +=1

        if apps is None:
            print 'Unable to load', file_path
            return
        return apps    

    def init_squares(self):
        #create and display squares
               
        for key,val in self.geometry_detailed.iteritems():
            id = key
            pos = val['pos']
            size = val['size']
            layout_type = val['layout_type']
            square = self.init_square(self.apps, key, pos, size, layout_type)
            self.add_square(square)

    def add_square(self, square):
            id = str(square.id)
            self.squares[id] = square
            self.add_widget( self.squares[id] )

            #in case the screen is displayed vertically
            if self.geometry["vertical"] == 'True' :
                self.squares[id].rotation_90d -= 90
                self.rotate(self.squares[id], -90)
            
    def remove_square(self,square, animation, touch):
            if animation :
                #remove some elements
                for i in square.children :
                    square.remove_widget(i)
                kwargs = {'duration' : 1.1,'t':'in_quart'} 
                anim = Animation(pos = touch.pos, size = (0,0), **kwargs )
                anim.bind(on_complete = self.remove_square2 )
                anim.start(square)
                
            else :
                self.remove_square2(1,square)

    def remove_square2(self,a,square):
            self.remove_widget( square )
            id = str(square.id)
            if id in self.squares.keys():
                del(self.squares[id] )
                     

    def init_square(self,apps,key,pos,size, layout_type):

            return Square(
                            pos = pos, 
                            size = size, 
                            layout_type = layout_type, 
                            do_scale = False, 
                            geometry_id = int(key),
                            icon_size = self.get_size('icon'),
                            small_size = self.get_size('small'),
                            medium_size = self.get_size('medium'),
                            large_size = self.get_size('large'),

                            id = key,
                            title = apps[key]['title'],
                            app_type = apps[key]['app_type'],
                            color_up = apps[key]['color_up'],
                            color_down = apps[key]['color_down'],
                            authors = apps[key]['authors'],
                            main_media_type = apps[key]['main_media_type'],
                            image_path = apps[key]['image_path'],
                            video_path = apps[key]['video_path'],
                            layers = {
                                      "large" : str( apps[key]['layer_large'] ), 
                                      "medium" : str( apps[key]['layer_medium'] ), 
                                      "small": str( apps[key]["layer_small"] )
                                     },
 
                            alternative_image_path = apps[key]['alternative_image_path'],
                            main_description = apps[key]['main_description'] ,
                            long_description = apps[key]['long_description'],
                            info_title = apps[key]['info_title'],
                            info_text = apps[key]['info_text'],
                            info_conclusion = apps[key]['info_conclusion'],

                            square_parameters = self.square_parameters,
                            padding = self.square_padding
                            )

    def geometry_square2square(self,key):
        ret = None
        g = self.geometry_squares
        for i,val in self.squares.iteritems() :
            #print val.geometry_id
            if g[key].collide_point(*val.center) :
                #if int(key) == val.geometry_id : 
                ret = i
        return ret
                
    def add_app(self, key, touch):
            #function to be used by the bar to add an app to the field
            #print 'add_app_key :'+ key
            if key in self.squares.keys():
                square  = self.squares[key]
                square.reshape_when_touch_down(touch,6)
                square.reshape_when_touch_up(touch)
                self.process_touch_up( square )
            else : 
                #create the square 
                square = self.init_square(self.apps,key,touch.pos, self.get_size('small'), 'small')
                      
                #find matching location
                #focus on translation
                matcher = self.find_matcher(square)#matcher = the key of geometry_squares that fits the best
                
                if matcher is not None :
                    #find the square that sits on matcher
                    matching_square = self.geometry_square2square(matcher)
                    #print "matcher: "+matcher
                    #sq = geometry_id = str(square.geometry_id)
                    self.add_square(square)
                    print 'add square '+key  
                    self.switch(square, matcher)
                    if matching_square in self.squares.keys():
                        self.remove_square( self.squares[str(matching_square)], True, touch )
                        print 'remove square '+matching_square
                    else :
                        print matching_square +' not in self.squares'
                else : 
                    #destroy square
                    self.remove_square(square, False, touch)
            #print self.squares.keys()  
            #switch
            #remove current app from the field
            #send back the bar icon to its location
            
                            

    def process_touch_up(self, square) :
            if square.process_touch_up_forbidden : return
            
            #focus on translation
            matcher = self.find_matcher(square)
            if matcher is not None :
                self.switch(square, matcher)
            else : 
                self.push_back_into_place(square)

            #focus on rotation
            #calculate angle between previous pos and now
            a = square.rotation
            b = square.rotation_90d
            if a > (b + 45) : 
                square.rotation_90d +=90
            elif a < (b - 45) : 
                square.rotation_90d -=90
            rot = square.rotation_90d
            #fix an issue : flip 180 when smallest angle is negative
            smallest_angle = min( (180 - abs(a - b), abs(a - b)) )
            if smallest_angle <0 : 
                rot = rot + 180
            
            self.rotate(square, rot)

            

        
    def push_back_into_place(self,square) :
        id = str(square.geometry_id)
        if self.activate_animations : 
            animation = Animation(pos = self.geometry_squares[id].pos, duration = 0.9,t='in_out_back')
            animation.start(square)
        else : 
            square.pos = self.geometry_squares[id].pos

    def rotate(self,square, rotation) :
        #animation = Animation(rotation = rotation, duration =0.2)
        #animation.start(square)
        square.rotation = rotation  
        
    
    def find_matcher(self,square):
        geometry_id = str(square.geometry_id)
        geometry_squares = self.geometry_squares
        
        def find(x1,y1,target_is_bar) : 
            matching_list = []
            for key,val in geometry_squares.iteritems() :
                if not str(key) == geometry_id :
                    if target_is_bar is False :
                        if val.collide_point(x1,y1) :
                            matching_list.append(key)
                    
            l = len(matching_list)
            #one matches
            if l == 1:
                return matching_list[0]
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
            #none matches
            elif l == 0 : 
                return None

        #the center of the current widget is the reference
        x1,y1 = square.center
        m = find(x1,y1, False)

        return m

    def switch(self, square, matcher) :    
        #switch position with another widget
        #self.activate_animations = False

        def get_layout_type(geometry_id) :
            return self.geometry[ str(geometry_id) ][2]

        def switch_layouts():
            square.layout_type = target_layout
            target.layout_type = current_layout
            #if square.layout_type <> target.layout_type :
            square.refresh_layout(target_layout)
            target.refresh_layout(current_layout)
        
        def place_square(square):
            animate_square(square, target_layout, target_param,target_pos, target_size)
            square.refresh_layout(target_layout)
            square.geometry_id = int(matcher)

        def animate_square(square,layout_type,param,pos,size):#move, resize etc
          if self.activate_animations :
            kwargs = {'duration' : 1.1,'t':'in_quart'}
            square.process_touch_up_forbidden = True            
            #switch pos and size 
            animation = Animation(pos = pos, size = size, **kwargs) #+ Animation(size = target_size, duration = 0.5,t='in_quart') 
            animation.bind(on_complete = self.allow_process_touch_up) 
            animation.start(square)
            #title size
            font_size = square.process_font_size( square.title ,int( param['title_label_font_size'] ) )
            animation = Animation(font_size = font_size, **kwargs)
            animation.start(square.title_label)
            #authors
            animation = Animation(font_size = int( param['authors_label_font_size'] ), **kwargs)
            animation.start(square.authors_label)
            #box top size
            animation = Animation(size_hint = param['box_top_size_hint'], **kwargs)
            animation.start(square.box_top)
            #box middle size
            animation = Animation(size_hint = param['box_middle_size_hint'], **kwargs)
            animation.start(square.box_middle)
            animation = Animation(size_hint = param['box_middle1_size_hint'], **kwargs)
            animation.start(square.box_middle1)
            animation = Animation(size_hint = param['box_middle2_size_hint'], **kwargs)
            animation.start(square.box_middle2)
            #box bottom size
            animation = Animation(size_hint = param['box_bottom_size_hint'], **kwargs)
            animation.start(square.box_bottom)
            #animation.bind(on_complete = self.switch_layouts)
            box_bottom_spacing = (self.get_size(layout_type)[0] -2*square.padding - param['vote_button_size'][0] - param['launch_button_size'][0]) #* 0.97
            animation = Animation(spacing = box_bottom_spacing, **kwargs)
            animation.start(square.box_bottom)
          else :
            square.size = size
            square.center = pos                           
            
        #get current properties of the target empty square to switch with
        target = self.geometry_squares[matcher]
        target_layout = get_layout_type(int(matcher))
        target_param = self.square_parameters[target_layout]
        target_pos = target.pos
        target_size = target.size #target_size = self.get_size(target_layout) 
        
        #if current place cannot be found
        if str(square.geometry_id) not in self.geometry.keys():
            place_square(square)
            return

        #get current square properties
        #current_layout = square.layout_type #this way was buggy
        current_layout = square.layout_type#get_layout_type(square.geometry_id)
        current_param = self.square_parameters[current_layout]
        current_pos = self.geometry_squares[str(square.geometry_id)].pos
        current_size = square.size #current_size = self.get_size(current_layout)#target.size

        #get the target square
        target = 0
        for key,val in self.squares.iteritems() :
            if val.geometry_id == int(matcher) : 
                target = self.squares[key]
                break
        """
        #adjust square pos in order to avoid jumping while changing layout
        if not target_size == current_size :    
            if target_size > current_size : 
                d = 1#and not target_size == current_size :
            elif target_size < current_size :
                d = -1
            #get differencial vector between current square pos and future layout square pos
            #case of an empty destination 
            if target == 0 and not target_layout == 'icon':
                if target_size > current_size :
                    delta_square = Vector( (-d*target_size[0]*0.4, -d*target_size[1]*0.4) )
                elif target_size < current_size :
                    delta_square = Vector( (-d*target_size[0]*0.9, -d*target_size[1]*0.9) )
            #case of an empty destination in the margin
            elif target_layout == 'icon':
                delta_square = Vector( (-d*current_size[0]*0.7, -d*current_size[1]*0.7) )
            else : 
                delta_square = ( d*Vector( target.pos ) - d*Vector( target.center ) )
            rot = round(square.rotation,0)
            #print rot, delta_square
            a = (1,1)
            if rot == 90 : a = (-1,1)
            elif rot == 180 : a = (-1,-1)
            elif rot == 270 : a= (1,-1)
            b,c = a
            square.x += b * delta_square.x/2
            square.y += c * delta_square.y/2           
        """
        
        
        #fake a different pos to match user behaviour (i.e. placing the square in the center of the target)
        #square.center = square.pos #(changes with rotation .. )        
        
        #if empty location
        if target == 0 :
            place_square()
            return
        
        #square
        animate_square(square, target_layout, target_param, target_pos, target_size) 
 
        #switch layouts
        switch_layouts() 
        
        #adjust square pos in order to avoid jumping while changing layout
        if not target_size == current_size and not current_layout == 'icon':
            #case of an empty destination 
            #if target == 0:
            if target_size > current_size :
                d = 1
            elif target_size < current_size :
                d = -1 
            delta_target = d*Vector( target_pos ) - d*Vector( target.pos )
            rot = round(target.rotation,0)
            a = (1,1)
            if rot == 90 : 
                if target_size > current_size : a = (1,1)
                elif target_size < current_size : a = (-2,1)
            elif rot == 180 : a = (-1,-1)
            elif rot == 270 : a= (1,-1)
            b,c = a
            target.x += b * delta_target.x/2
            target.y += c * delta_target.y/2 
        
        #target
        animate_square(target, current_layout, current_param, current_pos, current_size)
        
        #store pos
        target.geometry_id = square.geometry_id
        square.geometry_id = int(matcher)    
    
    def allow_process_touch_up(self,a,square):
        square.process_touch_up_forbidden = False
   
    def switch_layouts(self, animation,square):
        def get_layout_type(geometry_id) :
            return self.geometry[ str(geometry_id) ][2]

        #get target layout
        target_layout = get_layout_type(square.geometry_id)
        square.layout_type = target_layout
        square.refresh_layout(target_layout)
 
    def mute(self,uid):
        #mute all the square, unmute the given one
        for i in self.squares.itervalues():
            if not i.uid == uid :
                i.mute()
    
    def play_video_fullscreen(self, video_path, pos, size, position):
        self.video = VideoPlayer2(source = video_path, options = {'position':position} )
        self.video.bind(on_leave_fullscreen = self.on_leave_fullscreen)
        self.video.size = size
        self.video.pos = pos
        self.add_widget(self.video)
        #store size and pos for later
        self.video_size_pos = {'size':size, 'pos':pos}
        Clock.schedule_once(self.video.start, 2.5)
        window_size = (self.width - self.bar_width,self.height)#self.get_parent_window().size
        anim = Animation(size = window_size, pos = (self.x +self.bar_width, self.y) )
        anim.start(self.video)

    def on_leave_fullscreen(self,a):
        size = self.video_size_pos['size']
        pos = self.video_size_pos['pos']
        anim = Animation(size = size, pos = pos)
        anim.bind(on_complete = self.after_leaving_fullscreen)
        anim.start(self.video)

    def after_leaving_fullscreen(self,a,b):
        self.video.video.volume = 0
        self.remove_widget(self.video )

"""
class Bar(ScrollView):
    app = ObjectProperty(None)
    style = DictProperty( {'texture_path':'style/border31.png', 'geometry_square_margin' : 13} )
    geometry = DictProperty( {} )
    icon_size = ObjectProperty( None )
    start_geometry_id = NumericProperty( None ) #so that there's no common index with the field
    geometry_squares = DictProperty( {} )

    def __init__(self,**kwargs) :
        super(Bar, self).__init__(**kwargs) 
        Rectangle(texture = texture, size =self.size)
        
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
             if i not in ["screen_size","vertical", "icon_px","small","medium", "large"]:
                 i = int(i)
                 if i > max : max = i 
        self.start_geometry_id = max + 1

    def process_touch_up(self, square) :
        #check a drag n drop to the field occured
        if square.center[0] > self.width :
            print "out"
        else : print "in" 
        
    def add_square(self,square):
        self.layout.add_widget(square)
"""

class AppView(FloatLayout):
    app = ObjectProperty(None)
    texture_sidebar = ObjectProperty(None)
    texture = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(AppView, self).__init__(**kwargs)
         
        from kivy.core.image import Image
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
        
        self.field = Field(app=self, activate_animations = True)
        self.appview.add_widget(self.field)
        
        self.bar = Bar(app = self )
        self.appview.add_widget(self.bar)

        #self.field.load_bank() 
        
        #self.theoric_field_setup() 

        return self.appview    


if __name__ in ('__android__', '__main__'):
    LauncherApp().run()
