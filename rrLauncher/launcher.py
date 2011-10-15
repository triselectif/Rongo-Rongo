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
from kivy.uix.video import Video
from kivy.properties import ObjectProperty, NumericProperty, StringProperty, \
    BooleanProperty, DictProperty, ListProperty
from kivy.core.image import Image
from kivy.graphics import Color, Line, Rectangle, LineWidth, BorderImage
from kivy.vector import Vector
from kivy.clock import Clock

from datetime import datetime, timedelta
from random import random
       

class Square(Scatter):
    geometry_id = NumericProperty(None)#location on the field where the Square sits
    #content
    id = StringProperty('')
    title = StringProperty(None)
    app_type = StringProperty(None) #'info', 'service', 'jeu'
    authors = StringProperty(None)
    main_media_type = StringProperty(None) #'image' or 'video'
    image_path = StringProperty(None)
    video_path = StringProperty(None)
    alternative_image_path = StringProperty(None)
    main_description = StringProperty(None)
    long_description = StringProperty(None)
    info_title = StringProperty(None)
    info_text = StringProperty(None)
    info_conclusion = StringProperty(None)
    #shape
    rotation_90d = NumericProperty(0)
    style = DictProperty( {
                          'square_texture_path' : 'style/border31.png',
                          'color' : '0,0,0,0'
                          } )
    layout_type = StringProperty(None) #'icon'/'small'/'medium' or 'large'
    icon_size = ObjectProperty( None )
    small_size = ObjectProperty( None )
    medium_size = ObjectProperty( None )
    large_size = ObjectProperty( None )
    #internal variables
    touches = DictProperty( {} ) #current active touches on the widget
    #buttons = DictProperty( {} ) #store buttons widgets

    def __init__(self,**kwargs) :
        super(Square,self).__init__(**kwargs)
        
        if self.main_media_type == 'video' :
            self.video = Video(source = self.video_path, play=False, options = {'eos':'loop'} )
            Clock.schedule_once(self.start_video,0.2)
            Clock.schedule_once(self.start_video,2.4) 
            #self.add_widget(self.video)
            #self.play_but = Button(text = 'play')
            
            self.buttons = BoxLayout(orientation = 'vertical' )
            self.buttons.padding = 5 #box.height*0.15
            self.buttons.spacing = 5# self.layout_type2size(text)[0]*0.46
            self.play_button = Button(text ='play\nstop', size_hint = (1,0.5) )
            self.play_button.bind( on_press = self.start_video )
            """
            from kivy.core.image import Image
            texture = Image('style/play.png').texture
            with self.play_button.canvas:
                Color(1., 1., 0)
                Rectangle(size=self.play_button.size, texture = texture)
            #self.play_button.texture = texture
            """
            self.buttons.add_widget( self.play_button )
            self.sound_button = Button(text ='mute\nunmute', size_hint = (1,0.5) )
            self.sound_button.bind( on_press = self.unmute )
            self.buttons.add_widget( self.sound_button )
            
             
        self.init_layouts()  

        #init video to the front at the right location
        #self.layout_type2function(self.layout_type)


    def start_video(self,a) :
            m = self.video 
            if m.play == False : 
                m.play=True
                self.unmute(self.uid)
                self.play_button.text = 'stop'
            else : 
                m.play=False
                self.play_button.text = 'play'

    def mute(self):
        if self.main_media_type == 'video' :
            self.video.volume = 0
            self.sound_button.text = 'unmute'
   
    def unmute(self,a):
        if self.main_media_type == 'video' :
            if self.video.volume == 1:
                self.video.volume = 0
                self.sound_button.text = 'unmute'
            else :     
                self.video.volume = 1
                self.parent.mute(self.uid)
                self.sound_button.text = 'mute'
  
    def init_layouts(self):
        #create a layout for each size so that we can switch
        #easily from one to another 
    
        texture_path = self.style['square_texture_path']
        from kivy.core.image import Image
        texture = Image(texture_path).texture
        layout_type = self.layout_type

        def create_layout(text):
            with self.layout_type2layout(text).canvas :
                Color(a, b, c)
                BorderImage(source = texture_path,border = (12,12,12,12), size = self.layout_type2size(text) )        
                #Rectangle(texture = texture, size = self.layout_type2size(text) )
            #l = Label(text=text)
            #l.pos = self.center
            #self.layout_type2layout(text).add_widget( l )

        def app_type2name(app_type):
            if app_type == 'info' : return 'Info'
            elif app_type == 'service' : return 'Service'
            elif app_type == 'jeu' : return 'Jeu'
            else : return ''

        

        #color
        a = random()
        b = random()
        c = random()
        ######################### ICON LAYOUT ############################################################
        texture_path = 'style/square_icon.png'#self.style['square_texture_path']
        from kivy.core.image import Image
        texture = Image(texture_path).texture
  
        self.icon_layout = BoxLayout(orientation = 'vertical', size = self.icon_size)
        #create_layout('icon')
        text = 'icon'
        with self.layout_type2layout(text).canvas :
                Color(a, b, c)
                BorderImage(source = texture_path,border = (12,12,12,12), size = self.layout_type2size(text) )        
                #Rectangle(texture = texture, size = self.layout_type2size(text) )
        l = Label(text=self.title, font_size = 8)
        self.layout_type2layout(text).add_widget( l )
        from kivy.uix.image import Image
        alternative_image = Image(source = self.alternative_image_path)
        self.layout_type2layout(text).add_widget( alternative_image )

        ######################### LARGE LAYOUT ##########################################################
        """
        #self.large_layout = BoxLayout(orientation = 'vertical', size = self.large_size)
        create_layout('large')   
        """
        texture_path='style/square_large.png'#self.style['square_texture_path']
        from kivy.core.image import Image
        texture = Image(texture_path).texture
        
        self.large_layout = BoxLayout(orientation = 'vertical', size = self.large_size)
        create_layout('large')        
        text = 'large'
        
        with self.layout_type2layout(text).canvas :
                Color(a, b, c)
                #BorderImage(source = 'style/square_medium.png',border = (12,12,12,12), size = self.layout_type2size(text) )        
                Rectangle(texture = texture, size = self.layout_type2layout(text).size )

        box = BoxLayout(orientation = 'horizontal', size_hint = (1,0.15) )
        l1 = Label(text=self.title, font_size = 32 )
        box2 = BoxLayout(orientation = 'vertical', size_hint = (0.4,1) )
        l2 = Label(text = app_type2name(self.app_type), font_size = 16, halign = 'right' )
        l3 = Label(text = self.authors, font_size = 10, halign = 'right' )
        box2.add_widget(l2)
        box2.add_widget(l3)
        box.add_widget(l1)
        box.add_widget(box2)
        self.layout_type2layout(text).add_widget( box )

        main_box = BoxLayout(orientation = 'vertical', size_hint = (1,0.75) )

        box = BoxLayout(orientation = 'horizontal', size_hint = (1,0.6) )
        if self.main_media_type == 'image' : 
            from kivy.uix.image import Image
            image_large = Image(source = self.alternative_image_path, size_hint = (1,1) )
            box.add_widget( image_large ) 
        elif self.main_media_type == 'video' : 
            box2 = BoxLayout(orientation = 'vertical', size_hint = (1,1) )
            self.video_box_large = BoxLayout(orientation = 'horizontal', size_hint = (1,1) )
            box2.add_widget( self.video_box_large)
            box.add_widget( box2 )            

        main_box.add_widget(box)   

        box = BoxLayout(orientation = 'horizontal', size_hint = (1,0.4) )
        #alternative image
        from kivy.uix.image import Image
        alternative_image = Image(source = self.alternative_image_path, size_hint = (0.25,1) )
        box.add_widget( alternative_image )
        #main description
        box2 = BoxLayout(orientation = 'vertical', size_hint = (0.25,1) )
        l = Label(text = self.main_description, size_hint = (1,1), halign = 'left',font_size = 12 )
        box2.add_widget( l )
        box.add_widget( box2 )
        #long description        
        box3 = BoxLayout(orientation = 'horizontal', size_hint = (0.5,1) )
        l = Label(text = self.long_description, size_hint = (1,1), halign = 'left', font_size = 12 )
        box3.add_widget( l )
        box.add_widget(box3)    

        main_box.add_widget(box)

        self.layout_type2layout(text).add_widget( main_box ) 

        box = BoxLayout(orientation = 'horizontal', size_hint = (1,0.07) )
        box.padding = 10 #box.height*0.15
        box.spacing = self.layout_type2size(text)[0]*0.72
        vote_button = Button(text = 'vote') #, size = (box.width*0.25 - margin[0], box.height - 2*margin[1]), pos=margin) #size_hint = (0.5,1) )
        vote_button.bind( on_press = self.vote )
        box.add_widget( vote_button ) 
        launch_button = Button(text = 'lancer') #, size = (box.width*0.25, box.height - 2*margin[1]), pos=(box.width - margin[0], margin[1]) ) 
        launch_button.bind( on_press = self.launch ) 
        box.add_widget( launch_button )

        self.layout_type2layout(text).add_widget( box )
        
        
        ######################### MEDIUM LAYOUT ##########################################################
        """
        #self.medium_layout = BoxLayout(orientation = 'vertical', size = self.medium_size)
        create_layout('medium')
        """
        texture_path = 'style/square_medium.png'#self.style['square_texture_path']
        from kivy.core.image import Image
        texture = Image(texture_path).texture
        
        self.medium_layout = BoxLayout(orientation = 'vertical', size = self.medium_size)
        create_layout('medium')
        text = 'medium'
        
        with self.layout_type2layout(text).canvas :
                Color(a, b, c)
                #BorderImage(source = 'style/square_medium.png',border = (12,12,12,12), size = self.layout_type2size(text) )        
                Rectangle(texture = texture, size = self.medium_layout.size )
        
        box = BoxLayout(orientation = 'horizontal', size_hint = (1,0.13) )
        l1 = Label(text=self.title, font_size = 24 )
        box2 = BoxLayout(orientation = 'vertical', size_hint = (0.4,1) )
        l2 = Label(text = app_type2name(self.app_type), font_size = 12, halign = 'right' )
        l3 = Label(text = self.authors, font_size = 8, halign = 'right' )
        box2.add_widget(l2)
        box2.add_widget(l3)
        box.add_widget(l1)
        box.add_widget(box2)
        self.layout_type2layout(text).add_widget( box ) 

        box = BoxLayout(orientation = 'horizontal', size_hint = (1,0.8) )
        if self.main_media_type == 'image' : 
            from kivy.uix.image import Image
            image_medium = Image(source = self.alternative_image_path, size_hint = (1,1) )
            box.add_widget( image_medium ) 
        elif self.main_media_type == 'video' : 
            box2 = BoxLayout(orientation = 'horizontal', size_hint = (1,1) )
            self.video_box_medium = BoxLayout(orientation = 'horizontal', size_hint = (1,1) )
            box2.add_widget( self.video_box_medium )
            box.add_widget( box2 ) 

        self.layout_type2layout(text).add_widget( box ) 

        box = BoxLayout(orientation = 'horizontal', size_hint = (1,0.1) )
        box.padding = 5 #box.height*0.15
        box.spacing = self.layout_type2size(text)[0]*0.46
        vote_button = Button(text = 'voter') #, size = (box.width*0.25 - margin[0], box.height - 2*margin[1]), pos=margin) #size_hint = (0.5,1) )
        vote_button.bind( on_press = self.vote )
        box.add_widget( vote_button ) 
        launch_button = Button(text = 'lancer') #, size = (box.width*0.25, box.height - 2*margin[1]), pos=(box.width - margin[0], margin[1]) ) 
        launch_button.bind( on_press = self.launch ) 
        box.add_widget( launch_button )
        
        self.medium_layout.add_widget( box )
        
        ######################### SMALL LAYOUT ##########################################################
        texture_path = 'style/square_small.png'#self.style['square_texture_path']
        from kivy.core.image import Image
        texture = Image(texture_path).texture
        
        self.small_layout = BoxLayout(orientation = 'vertical', size = self.small_size)
        #create_layout('icon')
        text = 'small'
        
        with self.layout_type2layout(text).canvas :
                Color(a, b, c)
                #BorderImage(source = 'style/square_medium.png',border = (12,12,12,12), size = self.layout_type2size(text) )        
                Rectangle(texture = texture, size = self.small_layout.size )
        
        box = BoxLayout(orientation = 'horizontal', size_hint = (1,0.2) )
        l1 = Label(text=self.title, font_size = 16 )
        box2 = BoxLayout(orientation = 'vertical', size_hint = (0.4,1) )
        l2 = Label(text = app_type2name(self.app_type), font_size = 10, halign = 'right' )
        box2.add_widget(l2)
        box.add_widget(l1)
        box.add_widget(box2)
        self.small_layout.add_widget( box )
        from kivy.uix.image import Image
        alternative_image = Image(source = self.alternative_image_path, size_hint = (1,0.6) )
        self.small_layout.add_widget( alternative_image )
        
        box = BoxLayout(orientation = 'horizontal', size_hint = (1,0.2) )
        box.padding = 2 #box.height*0.15
        box.spacing = self.layout_type2size(text)[0]*0.5
        vote_button = Button(text = 'vote') #, size = (box.width*0.25 - margin[0], box.height - 2*margin[1]), pos=margin) #size_hint = (0.5,1) )
        vote_button.bind( on_press = self.vote )
        box.add_widget( vote_button ) 
        launch_button = Button(text = 'lancer') #, size = (box.width*0.25, box.height - 2*margin[1]), pos=(box.width - margin[0], margin[1]) ) 
        launch_button.bind( on_press = self.launch ) 
        box.add_widget( launch_button )
        
        self.small_layout.add_widget( box )
        
        #add a random layout so that it can be removed by the next function
        #self.layout = BoxLayout()
        #self.add_widget(self.layout) 
        #display the right layout
        self.layout_type2function(layout_type, True)        

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

    def layout_type2function(self,layout_type, startup) :
        layout = self.layout_type2layout(layout_type)
        #self.layout_type = layout_type
        return self.set_new_layout( layout, layout_type, startup )
    
    def set_new_layout(self, new_layout, layout_type, startup) :
        #self.new_layout = new_layout
        """
        animation = Animation(size = new_layout.size, duration = 1,t='in_quad')
        animation.bind(on_complete = self.set_new_layout2)
        animation.start(self.layout)
        """
        #def set_new_layout2(self,a,b) :
        #self.remove_widget(self.layout)
        self.clear_widgets()
        self.layout = new_layout
        self.add_widget(self.layout)
        self.size = self.layout.size
        
        if self.main_media_type == 'video':
            self.fit_video(layout_type, startup)
        
        """
        buttons = self.buttons
        for key,val in buttons.iteritems(): 
            val.size = self.get_launch_button_size(key) 
            self.add_widget( buttons[key] )
        """

    def fit_video(self, layout_type, startup):
        if not startup == True : 
            if layout_type == 'medium':
                self.video.pos = self.video_box_medium.pos
                self.video.size = self.video_box_medium.size
            elif layout_type == 'large':
                self.video.pos = self.video_box_large.pos
                self.video.size = self.video_box_large.size
            elif layout_type in ['small','icon']:
                self.video.size = (0,0)
        else : #self.video_box_large.size is nul at startup..
            #print self.video_box_large.size  
            if layout_type == 'medium':
                #self.video.pos = self.video_box_medium.pos
                #print self.video_box_medium.size
                self.video.size = self.size
            elif layout_type == 'large':
                #self.video.pos = self.video_box_large.pos
                self.video.size = self.size
            elif layout_type in ['small','icon']:
                self.video.size = (0,0)
                
        #video back to the front on top of the layout
        self.remove_widget(self.video)
        self.add_widget(self.video)
        
        self.buttons.pos = self.video.pos
        self.buttons.width = self.video.width /4
        self.buttons.height = self.video.height /3
        self.remove_widget(self.buttons)
        if not layout_type in ['small','icon']:
            self.add_widget(self.buttons)


    def launch(self,a):
        print 'launch app ' + self.title 

    def vote(self,a):
        print 'vote for app ' + self.title       
    
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
    style = DictProperty({'color':(0.5,0.5,0.5,0.5), 'texture_path':'style/border31.png' })
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
            #Rectangle(texture = texture, size =self.size)
            BorderImage(source = texture_path,border = (5,5,5,5), size = self.size )    
        

class Field(Widget):
    app = ObjectProperty(None)
    style = DictProperty({'geometry_square_margin':13  })
    activate_animations = BooleanProperty( False )
    #internal variables
    squares = DictProperty( {} )#stores all the squares widgets
    geometry = DictProperty( {} )#geometry = squares' target relative positions and sizes on the field
    geometry_detailed = DictProperty( {} ) #real positions on the field
    geometry_squares = DictProperty( {} ) 
    #stores all the geometry empty squares as widgets so that we can easily
    #compare their positions with the real squares
    apps = DictProperty( {} )#stores all the apps information

    #bar variables
    bar_width = NumericProperty(155)
    bar_start_geometry_id = NumericProperty(0)

    def __init__(self,**kwargs) :
        super(Field, self).__init__(**kwargs)
        self.init_geometry()
        self.init_geometry_detailed()
        self.draw_geometry()
        self.init_apps()
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
        if square.geometry_id < self.bar_start_geometry_id :
            return False
        else : return True
    
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
        self.bar_start_geometry_id = max + 1

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
                           do_rotation = False, 
                           do_translation = False, 
                           auto_bring_to_front = False
                           )
            self.add_widget( self.geometry_squares[str(min+i)] ) 
    
    def init_apps(self):
        #Import the json file that defines apps

        file_path = join(dirname(__file__), 'apps','detail')
        self.apps = {}
        nb = 0
        for subdir, dirs, files in walk(file_path):
            for file in files:
                print file
                with open(file_path +'/'+file, 'r') as fd:
                    t = loads(fd.read())
                    self.apps[str(nb)] = t 
                nb +=1

        if self.apps is None:
            print 'Unable to load', file_path
            return
        print self.apps
        

        
        

    def init_squares(self):
        #create and display squares
        apps = self.apps
        
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

                            id = apps[key]['id'],
                            title = apps[key]['title'],
                            app_type = apps[key]['app_type'],
                            authors = apps[key]['authors'],
                            main_media_type = apps[key]['main_media_type'],
                            image_path = apps[key]['image_path'],
                            video_path = apps[key]['video_path'],
                            alternative_image_path = apps[key]['alternative_image_path'],
                            main_description = apps[key]['main_description'] ,
                            long_description = apps[key]['long_description'],
                            info_title = apps[key]['info_title'],
                            info_text = apps[key]['info_text'],
                            info_conclusion = apps[key]['info_conclusion']
                            )
                
                self.add_widget(self.squares[id])

                #in case the screen is displayed vertically
                if self.geometry["vertical"] == 'True' :
                    self.squares[id].rotation_90d -= 90
                    self.rotate(self.squares[id], -90)

    def process_touch_up(self, square) :
            #focus on rotation
            #calculate angle between previous pos and now
            a = square.rotation
            b = square.rotation_90d
            if a > (b + 45) : 
                square.rotation_90d +=90
            elif a < (b - 45) : 
                square.rotation_90d -=90
            self.rotate(square, square.rotation_90d)
            #fix an issue : flip 180 when smallest angle is negative
            smallest_angle = min( (180 - abs(a - b), abs(a - b)) )
            if smallest_angle <0 : 
                self.rotate(square, square.rotation_90d + 180)

            #focus on translation
            matcher = self.find_matcher(square)
            if matcher is not None :
                self.switch(square, matcher)
            else : 
                self.push_back_into_place(square)

        
    def push_back_into_place(self,square) :
        id = str(square.geometry_id)
        if self.activate_animations : 
            animation = Animation(pos = self.geometry_squares[id].pos, duration = 0.9,t='in_out_back')
            animation.start(square)
        else : 
            square.pos = self.geometry_squares[id].pos

    def rotate(self,square, rotation) :
        square.rotation = rotation  
        
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
        
        def find(x1,y1,target_is_bar) : 
            matching_list = []
            for key,val in geometry_squares.iteritems() :
                if not str(key) == geometry_id :
                    if target_is_bar is False :
                        if val.collide_point(x1,y1) :
                            matching_list.append(key)
                    else :
                        #all the icons are possibly a potential location   
                        if key >= self.bar_start_geometry_id :
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
        
        if m == None and not self.square_is_in_the_bar(square) :
            #one more try if square comes from outside of the bar
            #check if within the fast launcher bar
            #if yes, better use the left border than the center
            #the left border center becomes the reference
            bar_width = self.bar_width
            #rot = square.rotation_90d
            
            #chosen to be independant from the rotation
            x1 = square.x + square.width/2
            y1 = square.y + square.height/2
            
            if x1 < bar_width :
                #print "in the bar"
                #find the most accurate position
                m = find(x1,y1,True)
                return m 
            else : 
                return None
        else : 
            return m 


    def switch(self, square, matcher) :    
        #switch position with another widget

        def get_layout_type(geometry_id) :
            if int(geometry_id) >= self.bar_start_geometry_id :
                return 'icon'
            else : 
                return self.geometry[ str(geometry_id) ][2]
 
        #get current properties of the target empty square to switch with
        target = self.geometry_squares[matcher]
        target_layout = get_layout_type(int(matcher))
        target_pos = target.pos
        target_size = target.size #target_size = self.get_size(target_layout)        

        #get current square properties
        #current_layout = square.layout_type #this way was buggy
        current_layout = get_layout_type(square.geometry_id)
        current_pos = self.geometry_squares[str(square.geometry_id)].pos
        current_size = square.size #current_size = self.get_size(current_layout)#target.size

        #get the target square
        target = 0
        for key,val in self.squares.iteritems() :
            if val.geometry_id == int(matcher) : 
                target = self.squares[key]
        #if empty location
        
        def place_square():
            #move to there
            if target_layout == 'icon' and square.rotation_90d ==0 : square.pos = target_pos
            if self.activate_animations : 
                animation = Animation(pos = target_pos, size = target_size, duration = 0.9,t='in_out_back')
                animation.start(square)
            else : 
                square.size = target_size
                square.pos = target_pos
                
            #resize
            square.layout_type2function(target_layout, False)
            square.geometry_id = int(matcher)
        
        #fake a different pos to match user behaviour (i.e. placing the square in the center of the target)
        #square.center = square.pos #(changes with rotation .. )        
 
        if target == 0 :
            place_square()
            return
        
        #switch pos and size
        if self.activate_animations : 
            animation = Animation(pos = target_pos, size = target_size, duration = 0.9,t='in_out_back')
            animation.start(square)
        else :
            square.size = target_size
            square.pos = target_pos
            
        if self.activate_animations : 
            animation = Animation(pos = current_pos, size = current_size, duration = 0.9,t='in_out_back')
            animation.start(target)
        else :
            target.size = current_size
            target.pos = current_pos
            

        #switch layouts
        square.layout_type = target_layout
        target.layout_type = current_layout
        #if square.layout_type <> target.layout_type :
        square.layout_type2function(target_layout, False)
        target.layout_type2function(current_layout, False)
        #store pos
        target.geometry_id = square.geometry_id
        square.geometry_id = int(matcher) 
             
         
    def mute(self,uid):
        #mute all the square, unmute the given one
        for i in self.squares.itervalues():
            if not i.uid == uid :
                i.mute()

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
        
        self.field = Field(app=self, activate_animations = True)
        self.appview.add_widget(self.field)
        
        #self.field.load_bank() 
        
        #self.theoric_field_setup() 

        return self.appview    


if __name__ in ('__android__', '__main__'):
    LauncherApp().run()
