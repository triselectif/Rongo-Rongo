from json import loads
from os.path import join, dirname, exists
from os import walk

from kivy.properties import ObjectProperty, NumericProperty,StringProperty, \
    BooleanProperty, DictProperty, ListProperty
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.vector import Vector
from kivy.animation import Animation
from kivy.clock import Clock

from video_player import VideoPlayer
from square import Square, GeometrySquare


class VideoPlayer2(VideoPlayer):
    def on_touch_down(self,touch):
        super(VideoPlayer2,self).on_touch_down(touch)  
        return True      
        

class Field(Widget):
    app = ObjectProperty(None)
    style = DictProperty({'geometry_square_margin':0  })
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
    #bar_width = NumericProperty(135)
    spacing = NumericProperty(0.0)
    square_padding = NumericProperty(10)
    title = StringProperty('')

    def __init__(self,**kwargs) :
        super(Field, self).__init__(**kwargs)
        
        self.init_geometry()
        self.init_app()
        self.init_geometry_detailed()
        self.draw_geometry()
        self.apps = self.init_apps()
        self.init_square_parameters()
        self.init_squares()       

    def get_field_size(self):
        width,height = self.geometry["screen_size"]
        spacing = s= self.spacing#0.012# = 0.02
        #bar = self.bar_width / width
        width_wb = 0.90 #int(width) - bar#width without bar
        """
        #Explanation of the math calculation
        #1)
        large = 3*small + 2*s
        large = 2*medium + s
        small = 2/3*medium - 1/3*s
        #2)
        width_wb = 4*s + large + medium + small
        #inject 1 into 2
        width_wb = 4*s + 2*medium + s + medium + 2/3*medium - 1/3*s
        width_wb = s*(5 -1/3) + medium * (3+ 2/3)
        """
        medium = (width_wb - s*(5 -1/3)) / (3+ 2/3)  
        #get the rest
        large = 2*medium + s 
        small = 0.66666*medium - 0.33333*s
               
        #large = self.geometry['large']
        height = large *width# * float(large[0])
        return width*width_wb, height*width_wb, small*width_wb, medium*width_wb, large*width_wb

    def get_size(self, layout_type) :
        if layout_type == 'icon':
            l,h = self.geometry["icon_px"]
            return (l,h) 
        #Current screen size is applied
        width,height,small,medium,large = self.get_field_size()
        #in px
        small = small * width
        medium = medium * width
        large = large * width  
        
        x = eval(layout_type)
        return (x,x)
        #return (l,h) 

    def square_is_in_the_bar(self,square):
        return False

    def init_app(self):
        #Import the json file that defines it
        file_path = join(dirname(__file__), 'config')
                
        with open(file_path, 'r') as fd:
            config = loads(fd.read())
            #print self.geometry

        if config is None:
            print 'Unable to load', file_path
            return

        self.title = config['title']
        width,height,sm,me,la = self.get_field_size()  
        self.title_label = Label(text = self.title, pos = (width*0.835,-20), font_size = 22, color = (.3,.3,.3,1), halign = 'right' )
        self.add_widget(self.title_label)
        
    def init_geometry(self):
        #Import the json file that defines it
        file_path = join(dirname(__file__), 'field_geometry')
                
        with open(file_path, 'r') as fd:
            self.geometry = loads(fd.read())
            #print self.geometry

        if self.geometry is None:
            print 'Unable to load', file_path
            return

        self.bar_width = int(self.geometry['bar_width'])
        #self.spacing = float(self.geometry['spacing'])
    
    def init_geometry_detailed(self):
        #calculates detailed geometry
        style = self.style
        #margin = style['geometry_square_margin']
        #bar_width = self.bar_width
        
        #Current screen size is applied
        #width,height = self.size
        width,height,sm,me,la = self.get_field_size()
        screen_size = self.geometry['screen_size']   
        bar_width = int(screen_size[0]) - width
        margin_height = (int(screen_size[1]) - height*0.9)*0.5
        print bar_width,height,margin_height
        if margin_height < 0: margin_height = 0
        #print self.geometry['screen_size'][1], height, margin_height
        spacing = self.spacing
        
        #MODE AUTO : calculates every dimensions based on screen size, but for a specific arrow
        #draw small
        array = { 0:["small","small","small"], 1:["medium","medium"], 2:["large"] }
        x_hint = 0
        key = 0
        for i,list in array.iteritems():
            size = self.get_size( list[0] )
            l,h = size   
            x_hint = x_hint + spacing
            index = 0
            y_hint = 0
            for j in list:
                #update geometry_detailed
                self.geometry[str(key)] = [x_hint,y_hint,list[0]]
                x = x_hint *width + bar_width
                y = y_hint *height + margin_height
                self.geometry_detailed[str(key)] = {'pos':(x,y),'size':(l,h),'layout_type':list[0]}
                index += 1
                y_hint = (index) * (float(h)/height+spacing)
                key += 1
            x = x + size[0]
            x_hint = x_hint + float(l)/width
        #print self.geometry #:insert that into field_geometry for specific array
        #and apply code below instead 

        """
        #in case we refer to all the dimensions inside the field_geometry file
        for key,val in self.geometry.iteritems() :
            if not key in ["screen_size","icon_px","vertical","bar_width","spacing"]:
                x,y,square_layout_type = val
                x = x * width + bar_width #+ self.x #+ margin
                y = y * height +margin_height#+ self.y #+ margin
                l,h = self.get_size(square_layout_type)
                #print (l,h)
 
                #update geometry_detailed
                self.geometry_detailed[key] = {'pos':(x,y),'size':(l,h), 'layout_type':square_layout_type }
        
        """

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
        #print self.geometry_squares
    
    def init_square_parameters(self):
        #Import the json files that defines each type of square
        for i in ['small','medium','large']:
            file_path = join(dirname(__file__), i)
            #print file_path
                
            with open(file_path, 'r') as fd:
                self.square_parameters[i] = loads(fd.read())
                #print self.square_parameters[i]

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
            #avoid sound running after widget being removed and deleted
            if square.main_media_type == 'video':
                    square.video.mute(1)
            self.remove_widget( square )
            id = str(square.id)
            if id in self.squares.keys():
                del(self.squares[id] )
                     

    def init_square(self,apps,key,pos,size, layout_type):

            return Square(
                            app =self.app,
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
                            color_text = apps[key]['color_text'],
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

    def shake_square(self, touch, key, intensity):
        square  = self.squares[key]
        square.reshape_when_touch_down(touch,intensity)
        square.reshape_when_touch_up(touch)
        self.process_touch_up( square )
                
    def add_app(self, key, touch):
            #function to be used by the bar to add an app to the field
            #print 'add_app_key :'+ key
            if key in self.squares.keys():
                self.shake_square(touch,key,6)
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
        #animation = Animation(rotation = rotation, duration =0.3)
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
            animation.bind(on_complete = self.adjust_position) 
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
            #launch button size
            animation = Animation(size = param["launch_button_size"], **kwargs)
            animation.start(square.launch_button)
            #vote button size
            animation = Animation(size = param["vote_button_size"], **kwargs)
            animation.start(square.vote_button)
            #spacing
            box_bottom_spacing = (self.get_size(layout_type)[0] -2*square.padding - param['vote_button_size'][0] - param['launch_button_size'][0]) * 0.97
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
        """
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
        """
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

    def adjust_position(self,a,square):
        gs= self.geometry_squares
        key = str(square.geometry_id)
        if not key in gs.keys():return
        match = gs[key]
        #pos size
        anim = Animation(pos = match.pos, size = match.size, duration = 0.2)
        anim.start(square)
        #layout
        #square.layout.pos = (square.padding, square.padding)
        #box bottom
        param = self.square_parameters[square.layout_type]
        box_bottom_spacing = (self.get_size(square.layout_type)[0] -2*square.padding - param['vote_button_size'][0] - param['launch_button_size'][0]) * 0.97
        anim = Animation(pos = square.layout.pos, spacing = box_bottom_spacing, duration = 0.2)
        anim.start(square.box_bottom) 

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
        w,h,s,m,l = self.get_field_size()#(self.width - self.bar_width,self.height)#
        anim = Animation(size = (w,h), pos = (self.x +self.bar_width, self.y) )
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

