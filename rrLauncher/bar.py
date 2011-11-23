from kivy.properties import ObjectProperty, NumericProperty, StringProperty, \
    BooleanProperty, DictProperty, ListProperty
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button 
from kivy.animation import Animation 

from bar_image import BarImage
from square import GeometrySquare
from super_button import SuperButton

class Bar(FloatLayout):
    objects = DictProperty( {} )
    app = ObjectProperty(None)
    apps = DictProperty( {} )
    element_size = ObjectProperty( (70,70) )
    spacing = NumericProperty(10)
    sorting_condition = StringProperty( 'app_type' )
    
    def __init__(self,**kwargs):
        super(Bar,self).__init__(**kwargs)
        self.apps = self.app.field.init_apps()
        self.size_hint = (None,1)
        #self.width = 135
        self.padding_left = int((self.width - self.element_size[0])/2) 
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
        #self.resort('title')

    def clear(self):
        for i in self.children :
            self.remove_widget(i)

    def sort(self):
        #list of app keys in order
        condition = self.sorting_condition
        self.sorting = self.apps.keys()
        
        if condition == 'title':
            l = []
            for i,val in self.apps.iteritems():
                t = val['title']
                l.append( [t,i] )    
        elif condition == 'app_type':
            l = []
            for i,val in self.apps.iteritems():
                t = val['app_type']
                l.append( [t,i] )
        else : 
            return
        l.sort()
        #print l
        sorting = []
        counter =0
        for i in l:
            if counter in [7,14,21,28]:
                #button
                sorting.append( 'b' )
            sorting.append( i[1] )
            counter +=1
        self.sorting = sorting

    def resort(self,condition):
        self.sorting_condition = condition
        self.sort()
        #self.clear()
        #animate icons now
        gs = self.geometry_squares
        print gs
        for key,val in gs.iteritems() :
            im_key = self.sorting[int(key)]
            if not im_key == 'b': #exception for buttons
                    #get destination gs
                    center = val.center
                    a = Animation(center = center)
                    im = self.images[ str(im_key) ]
                    im.initial_center = center
                    a.start( im )
                    #im.pos = center                  

    def fill(self):
        #print 'apps'
        #print self.apps
        gs = self.geometry_squares 
        s = self.sorting
        counter = 0
        for key,val in self.apps.iteritems() :
            #get destination gs
            g = gs[ str( s.index(key) ) ]
            center = g.center
            pos = g.pos
            self.add_app(key,val,center,pos)    
            counter +=1
        #add sorting buttons
        counter = 0
        for key in s :
            if key == "b":
                self.add_button(counter)
            counter +=1    
             

    def add_button(self, place):
        pos = self.geometry_squares[str(place)].pos
        buttons = GridLayout(cols=2, row_force_default=True, row_default_height=self.element_size[1]*0.5, size = self.element_size, pos = pos )
        but1 = SuperButton(background_normal = 'style/bar/slider-picto-type-off.png',background_down = 'style/bar/slider-picto-type-on.png')
        but1.bind(on_press = self.sort_by_app_type)
        but2 = Button(background_normal = 'style/bar/slider-picto-ABC-off.png',background_down = 'style/bar/slider-picto-ABC-on.png')
        but2.bind(on_press = self.sort_by_title)
        but3 = Button(background_normal = 'style/bar/slider-picto-90-off.png',background_down = 'style/bar/slider-picto-90-on.png')
        but3.bind(on_press = self.rotate_images)        
        but4 = Button(background_normal = 'style/bar/slider-picto-preSet-off.png',background_down = 'style/bar/slider-picto-preSet-on.png')

        buttons.add_widget(but1)
        buttons.add_widget(but2)
        buttons.add_widget(but3)  
        buttons.add_widget(but4)     
        self.layout.add_widget(buttons)

    def sort_by_app_type(self,a):
        self.resort('app_type')

    def sort_by_title(self,a):
        self.resort('title')

    def rotate_images(self,a):
        for i,val in self.images.iteritems():
            val.rotation = val.rotation + 90            

    def add_app(self, key, app, center, pos):
        # Nop.
        self.images[key] = BarImage( source= str(app["image_path"]) , app =self.app, bar=self, key=key, pos =pos, initial_center = center, size = self.element_size )
        if self.app.field.geometry["vertical"] == "True": 
            self.images[key].rotation += 270 
        self.layout.add_widget(self.images[key])

    def draw_empty_squares(self):
        apps = self.apps
        m = self.spacing#self.app.field.style['geometry_square_margin']
        padding_left = self.padding_left
        max = len(apps)
        #leave space for buttons
        r = max/7
        max +=int(r)
        
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

    def on_image_touch_down(self, touch, key):
        #check if already on field
        squares = self.app.field.squares
        if key in squares.keys() :
            self.app.field.shake_square( touch,key,10)
            
