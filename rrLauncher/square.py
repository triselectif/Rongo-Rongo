from kivy.properties import ObjectProperty, NumericProperty, StringProperty, \
    BooleanProperty, DictProperty, ListProperty
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.scatter import Scatter
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.animation import Animation
from kivy.clock import Clock

from video_player import VideoPlayer
from super_button import SuperButton




class Square(Scatter):
    app = ObjectProperty( None )
    geometry_id = NumericProperty(None)#location on the field where the Square sits
    #content
    id = StringProperty('')
    title = StringProperty(None)
    app_type = StringProperty(None) #'info', 'service', 'jeu'
    color = ObjectProperty( (.82,.82,.82,1) )
    color_text = ObjectProperty( (.82,.82,.82,1) )
    color_down = ObjectProperty( (1,1,0,1) )
    color_up = ObjectProperty( (.1,.1,.1,1) )
    authors = StringProperty(None)
    main_media_type = StringProperty(None) #'image' or 'video' or 'webpage'
    image_path = StringProperty(None)
    video_path = StringProperty(None)
    webpage_path = StringProperty("http://www.google.com")
    vote_feedback = NumericProperty(0) #value between 0 and 1
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
    layer_texture_path = ObjectProperty( None )
    process_touch_up_forbidden = BooleanProperty(False)
    padding = NumericProperty(10) #square layout padding
    berkelium_is_installed = BooleanProperty(False)

    def __init__(self,**kwargs) :

        super(Square,self).__init__(**kwargs)

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
        x,y = vid.pos
        self.parent.play_video_fullscreen(self.video_path, self.to_parent(x,y) , self.video.size, self.video.video.position)
        
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

        def layers2texture(layers, berkelium):
            #convert either an image or an html webpage to texture
            #to be used as a background by the square
            converted_layers = {}
            bk = {}
            for key,path in layers.iteritems():
                #fileName, fileExtension = os.path.splitext(path)
                #if fileName[4] in ['http','file']: #fileExtension in ['.org','.com','.fr','.html','.htm'] :
                if path[:4] in ['http','file']:
                    if self.berkelium_is_installed == False : return None
                    size = (600,600)
                    bk[key] = berkelium.Webbrowser(url=path, size=size)
                    texture = bk[key]._bk.texture
                    converted_layers[key] = texture
                    #finally delete the berkelium instance
                    del bk[key]   
                else :
                    from kivy.uix.image import Image
                    img = Image(source=path)
                    texture = img.texture
                    converted_layers[key] = texture
            #print path, texture
            return converted_layers   
        
        #load berkelium
        berkelium = None
        if self.berkelium_is_installed == True : 
            from kivy.ext import load
            berkelium = load('berkelium', (1, 1))            

        #extract textures from layouts
        self.layers = layers2texture(self.layers, berkelium)

        #get current layout
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
        self.box_top = BoxLayout(size_hint = param['box_top_size_hint'] )#orientation = 'horizontal', 
        font_size = self.process_font_size( self.title, int( param['title_label_font_size']) )
        text_size = (len(self.title)*font_size +100,None )
        self.title_label = Label( text=self.title, font_size = font_size, color = self.color_text, halign = 'left', valign = 'top',text_size = text_size, padding = (5,0) ) #font_name = 'DEJAVU SANS CONDENSED', bold = False
        self.box2 = BoxLayout(orientation = 'horizontal',  size_hint = (None,1) , width = self.title_label.text_size[0], pos_hint={'top': 1,'left':1} )
        #self.app_type_pic = Image(source = str(self.app_type), pos_hint={'top': 1,'right':1}, size_hint = (1,3) )
        #self.box3 = AnchorLayout( anchor_x = 'right', anchor_y = 'bottom')
        #self.authors_label = Label(text = self.authors, font_size = int( param['authors_label_font_size'] ), pos_hint ={'right':1},  color = self.color_text, halign = 'right') #, pos_hint={'bottom': 1,'right':1} )        
        self.box2.add_widget(self.title_label)
        self.box_top.add_widget(self.box2)
        #self.box3.add_widget(self.authors_label)
        #self.box_top.add_widget(self.box3)
        self.layout.add_widget( self.box_top )
        
        #middle part : Image or Video
        self.box_middle = BoxLayout(orientation = 'horizontal', size_hint = param['box_middle_size_hint'] )
        self.box_middle1 = BoxLayout(orientation = 'horizontal', size_hint = param['box_middle1_size_hint'], padding = 0, spacing = 0 )
        self.box_middle2 = BoxLayout(orientation = 'horizontal', size_hint = param['box_middle2_size_hint'], padding = 0, spacing = 0 )
        self.box_middle.add_widget( self.box_middle1 ) 
        self.box_middle.add_widget( self.box_middle2 )
 
        if self.main_media_type == 'webpage' :
            #berkelium installed was already checked by field
            try : 
                self.webpage = berkelium.Webbrowser(url=self.webpage_path, size=(50,50) )
                self.box_middle1.add_widget( self.webpage ) 
            except :
                print 'Cannot load url: '+str(self.webpage_path)
                self.main_media_type = 'image'
            
        if self.main_media_type == 'image' : 
            from kivy.uix.image import Image
            image = Image(source = self.image_path, allow_stretch = True, keep_ratio = False, size_hint = (1,1), pos_hint={'left': 1, 'top' : 1} )
            self.box_middle1.add_widget( image ) 

        elif self.main_media_type == 'video' :
            #if self.main_media_type == 'video' :
            self.video = VideoPlayer(source = self.video_path)
            self.video.bind(on_unmute =self.on_unmute)
            self.video.bind(on_start=self.on_start)
            self.video.bind(on_fullscreen = self.on_fullscreen)
            self.video.bind(on_leave_fullscreen = self.on_leave_fullscreen)
            self.box_middle1.add_widget( self.video ) 
        
        self.layout.add_widget( self.box_middle ) 

        #Bottom part : buttons
        self.box_bottom = BoxLayout(orientation = 'horizontal', size_hint = param['box_bottom_size_hint'] )
        self.subbox = BoxLayout(orientation = 'horizontal' )
        self.box_bottom.padding = int( param['box_bottom_padding'] ) #box.height*0.15 
        self.vote_button = SuperButton(background_normal = 'style/square/bouton-vote-T2-off.png', background_down = 'style/square/bouton-vote-T2-on.png', size_hint = (None,None), size=param["vote_button_size"] )
        self.vote_button.bind( on_press = self.vote ) 
        self.subbox.add_widget( self.vote_button )
        #vote feedback
        from kivy.uix.image import Image
        self.fb = Image(source = 'style/square/like'+self.convert_vote_feedback()+'.png', size_hint=(None,None), size=param["vote_feedback_size"])
        self.subbox.add_widget( self.fb )
        self.box_bottom.add_widget(self.subbox)
        self.launch_button = SuperButton(background_normal = 'style/square/bouton-lancer-T2-off.png',background_down = 'style/square/bouton-lancer-T2-on.png', size_hint = (None,None), size=param["launch_button_size"] ) 
        self.launch_button.bind( on_press = self.launch ) 
        self.box_bottom.add_widget( self.launch_button )
        self.box_bottom.spacing = (self.layout.width - self.vote_button.width - self.launch_button.width)*0.97
        self.layout.add_widget( self.box_bottom )

        self.add_widget(self.layout)
        #Clock.schedule_once(self.update_canvas, 4)

    def convert_vote_feedback(self):
        vf = self.vote_feedback
        if vf > 1 : vf =1
        elif vf < 0 : vf = 0
        vf = int(vf*6)
        return str(vf)    

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
        self.app.appview.launch_app(id, self.title)

    def vote(self,a):
        print 'vote for app ' + self.title
        self.vote_feedback += 0.05
        self.fb.source = 'style/square/like'+ self.convert_vote_feedback() +'.png'        
    
    def on_touch_down(self, touch):
        #analyse and store touches so that we know on_touch_up which
        #square was concerned by the touch_up 
        if self.collide_point(touch.x,touch.y):
            self.touches[touch.id] = touch
            #enlarge a bit
            self.reshape_when_touch_down(touch, 0)     
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
        #self.title_label.color = self.color_up
        self.texture_path = 'style/square/square_'+str(self.layout_type)+'_touch_down.png'
        #self.app_type_label.color = self.color_up
        #self.size = (self.width + 3, self.height + 3)
        #a = Animation(center = self.center, size = self.size)
        #a.start(self)

    def reshape_when_touch_up(self, touch):
        self.color = self.color_up
        #self.title_label.color = self.color_down
        #self.app_type_label.color = self.color_up
        self.texture_path = 'style/square/square_'+str(self.layout_type)+'.png'
        pass

    def update_canvas(self,a):
        self.canvas.ask_update()

    
        
         
class GeometrySquare(Scatter):
    style = DictProperty({'texture_path':'style/square/slider-sous-tommette2.png' })
    layout_type = StringProperty('')
    geometry_id = NumericProperty(0)#location on the field
    
    def __init__(self,**kwargs) :
        super(GeometrySquare, self).__init__(**kwargs)
        #draw
        style = self.style
        texture_path = style['texture_path']    
