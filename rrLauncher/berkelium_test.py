'''
Berkelium extension demo
========================

Check http://github.com/tito/kivy-berkelium for more information.
You must have berkelium-1.0 extension installed before running the demo

'''
from kivy.uix.scatter import Scatter
from kivy.uix.floatlayout import FloatLayout
from kivy.app import App

from kivy.ext import load
berkelium = load('berkelium', (1, 1))

#urls = ( 'http://kivy.org','http://www.google.com')
urls = ('file://apps/html/app1/large.html', 'file://apps/html/app1/medium.html','file://apps/html/app1/small.html')

class BerkeliumBrowserApp(App):
    def build(self):
        root = FloatLayout()
        size = (600, 600)
        for url in urls:
            scatter = Scatter(size=size)
            bk = berkelium.Webbrowser(url=url, size=size)
            scatter.add_widget(bk)
            root.add_widget(scatter)
        return root

if __name__ == '__main__':
    BerkeliumBrowserApp().run()
