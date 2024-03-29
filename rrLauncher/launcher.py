#import os
#os.environ['KIVY_VIDEO'] = 'ffmpeg'
from kivy.app import App

from field import Field
from bar import Bar
from appview import AppView

#from kivy.uix.scrollview import ScrollView

class LauncherApp(App):

    def build(self):
        self.appview = AppView(app=self, do_rotation = False, do_scale = False, do_translation_y = False, size_hint =(1,1) )
        
        self.field = Field(app=self, activate_animations = True)
        self.appview.add_widget(self.field)
        
        self.bar = Bar(app = self, element_size = self.field.geometry['icon_px'], size_hint = (None, None), height =2000)
        #root = ScrollView(size_hint=(None, None), size=(200, 800))
        #root.add_widget(self.bar)
        self.appview.add_widget(self.bar)

        return self.appview    

        

if __name__ in ('__android__', '__main__'):
    LauncherApp().run()
