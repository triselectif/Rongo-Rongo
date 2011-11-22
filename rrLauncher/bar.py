from kivy.properties import ObjectProperty, NumericProperty, StringProperty, \
    BooleanProperty, DictProperty, ListProperty
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout

from bar_image import BarImage
from square import GeometrySquare

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
            pos = g.pos
            self.add_app(key,val,center,pos)    

    def add_app(self, key, app, center, pos):
        # Nop.
        self.images[key] = BarImage( source= str(app["image_path"]) , app =self.app, bar=self, key=key, pos =pos, initial_center = center, size = self.element_size )   
        self.layout.add_widget(self.images[key])

    def draw_empty_squares(self):
        apps = self.apps
        m = self.app.field.style['geometry_square_margin']
        padding_left = self.padding_left
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

    def on_image_touch_down(self, touch, key):
        #check if already on field
        squares = self.app.field.squares
        if key in squares.keys() :
            self.app.field.shake_square( touch,key,10)
            
