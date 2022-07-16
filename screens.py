from kivy import platform
from kivy.app import App
from lineGraph import LineGraphApp as lga
from lineGraph import LineGraphWindow as lgw
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.relativelayout import RelativeLayout

# I should just make 4 Screens: 1 home, 1 data. The data windows slide based on pushing


class ScreensWindow(RelativeLayout):
    data = (['Organization', 'Employees', 'Customers'],
            ['Alphabet', 500, 100],
            ['Microsoft', 90, 200],
            ['Amazon', 30, 300],
            ['SquaredAnt', 700, 10])

    COLUMN = 1

    x_title = data[0][0]
    y_title = data[0][COLUMN]
    y_labs  = data[0][1:]
    x_labs  = [tpl[0] for tpl in data][1:]
    y_vals  = [tpl[1] for tpl in data][1:]
    min_y   = 0 # or min(y_vals)
    max_y   = max(y_vals)

    lgw.data = data

    sm = ScreenManager()

    def __init__(self, **kwargs):
        super(ScreensWindow, self).__init__(**kwargs)
        # set the data
        self.init_data()
        self.init_screens()
        #lga().run()


    def init_screens(self):
        screen = Screen(name='home')
        self.sm.add_widget(screen)
        for y in self.y_labs:
            screen = Screen(name=str(y))
            print(str(y))
            self.sm.add_widget(screen)
            # prepare dataframe
            # change to screen
            # run lga
        self.sm.current = 'home'
        #lgw()

    def init_data(self):
        self.x_title = self.data[0][0]
        self.y_title = self.data[0][self.COLUMN]
        self.x_labs  = [tpl[0] for tpl in self.data][1:]
        self.y_vals  = [tpl[1] for tpl in self.data][1:]
        self.min_y   = 0 # or min(y_vals)
        self.max_y   = max(self.y_vals)

    #class ScreensWindow(RelativeLayout):
    # Create the manager


        # By default, the first screen added into the ScreenManager will be
        # displayed. You can then change to another screen.

        # Let's display the screen named 'Title 2'
        # A transition will automatically be used.
        #sm.current = 'Title 2'


    # set the data









        # run the graph





#initiate app
class ScreensApp(App):
    pass

if __name__ == "__main__":
    ScreensApp().run()
