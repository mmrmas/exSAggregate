from kivy.config import Config
Config.set('graphics', 'width', '900')
Config.set('graphics', 'height', '400')

from kivy import platform
from kivy.app import App
from kivy.uix.relativelayout import RelativeLayout
from kivy.graphics.vertex_instructions import Line
from kivy.properties import NumericProperty
from kivy.uix.label import Label
from kivy.core.text import Label as CoreLabel
from kivy.graphics.vertex_instructions import Rectangle
import pandas as pd
import numpy as np
from kivy.properties import Clock
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.properties import ListProperty
from kivy.properties import StringProperty
from decimal import Decimal

class LineGraphWindow(Screen):
    this_width = NumericProperty(0)
    this_height = NumericProperty(0)
    font_size = NumericProperty(12)

    COLUMN = 0

    x_axis = None
    y_axis = None
    x1 = 0
    x2 = 0
    y1 = 0
    y2 = 0

    #set data
    data = (['Organization', 'Employees', 'Customers'],
            ['Alphabet', 500, 100],
            ['Microsoft', 90, 200],
            ['Amazon', 30, 300],
            ['SquaredAnt', 70, 800])

    df_data = pd.DataFrame(data[1:], columns = data[0])
    df_data = df_data.set_index(data[0][0])

    x_labs  = list(df_data.index)
    y_labs  = list(df_data.columns)
    y_vals  = list(df_data[df_data.columns[COLUMN]])
    min_y   = 0 # or min(y_vals)
    max_y   = max(y_vals)

    plotted_line = []
    plotted_x_labels = []
    plotted_y_labels = []
    plotted_y_lines = []

    step_size_ori = 0.000000001
    step_size = step_size_ori
    step_in_px = 0
    number_of_steps = 0

    button_down = False
    graphButton = Widget()

    def __init__(self, **kwargs):
        super(LineGraphWindow, self).__init__(**kwargs)
        self.init_data()
        print ("1")
        self.init_XY_axes()
        print ("2")
        self.init_x_line()
        print ("3")
        self.init_y_labels()
        print ("4")

    def on_size(self, *args):
        self.init_sizes()
        self.update()

    def init_data(self):
        #self.x_title = self.data[0][0]
        #self.y_title = self.data[0][self.COLUMN]
        self.x_labs  = list(self.df_data.index)
        self.y_labs  = list(self.df_data.columns)
        self.y_vals  = list(self.df_data[self.df_data.columns[self.COLUMN]])
        self.min_y   = 0 # or min(y_vals)
        self.max_y   = max(self.y_vals)
        print (self.y_vals)

    def init_sizes(self):
        self.this_width = self.width
        self.this_height = self.height
        self.font_size =  int(min(self.height * 0.05, self.width * 0.05))

    def init_XY_axes(self):
        with self.canvas:
            self.x_axis = Line()
            self.y_axis = Line()
            self.x_axis.points = [0, 0, 0, 0]
            self.y_axis.points = [0, 0, 0, 0]

    def init_x_line(self):
        with self.canvas:
            for i in range(len(self.x_labs)):
                print (f'xlab {i} {len(self.plotted_x_labels)}')
                self.plotted_line.append(Line())
                self.plotted_x_labels.append(Rectangle())

    def init_y_labels(self):
        with self.canvas:
            while (self.step_size * 10 <= self.max_y ):
                self.step_size = self.step_size * 10
            #how much px is a step?
            for y in np.arange(0, self.max_y, self.step_size):
                self.plotted_y_labels.append(Rectangle())
                self.plotted_y_lines.append(Line())
                self.number_of_steps = len(self.plotted_y_labels)

    def update_XY_axes(self):
        self.x1 = int(self.this_width * 0.1)
        self.x2 = int(self.this_width * 0.9)
        self.y1 = int(self.this_height * 0.1)
        self.y2 = int(self.this_height * 0.9)
        self.x_axis.points = [self.x1, self.y1, self.x2, self.y1]
        self.y_axis.points = [self.x1, self.y1, self.x1, self.y2]


    def update_plot(self):
        self.create_y_label()
        x_prev = 0
        y_prev = 0
        number_of_labels = len(self.x_labs)
        for i in range(number_of_labels):
            x = self.x1 + (self.x2 - self.x1) / (number_of_labels - 1)  * i
            y = self.y1 + (self.y2 - self.y1) * self.y_vals[i] / self.max_y
            x = int(x)
            y = int(y)
            # do not add prev if x == 0
            if i != 0:
                self.plotted_line[i].points = [x_prev, y_prev, x, y]
            # create labels
            [texture, texture_size] = self.create_label(self.x_labs[i])
            self.plotted_x_labels[i].texture = texture
            self.plotted_x_labels[i].size = texture_size
            self.plotted_x_labels[i].pos = (int(x) - texture_size[0]/2, 0.03 * self.this_height)
            x_prev = x
            y_prev = y

    def create_y_label(self):
        i = 0
        self.step_in_px = (self.y2 - self.y1) / self.max_y * self.step_size
        for y in np.arange(self.y1, self.y2, self.step_in_px):
            if i >= self.number_of_steps:
                break
            [texture, texture_size] = self.create_label(Decimal(str(self.step_size)) * (i+1))
            self.plotted_y_labels[i].texture = texture
            self.plotted_y_labels[i].size = texture_size
            self.plotted_y_labels[i].pos = (int(self.x1 - texture_size[0] - 0.03 * self.this_width), int(y + self.step_in_px - texture_size[1]/2))
            #also put the lines here
            self.plotted_y_lines[i].points = [int(self.x1), int(y+self.step_in_px), int(self.x2), int(y+self.step_in_px)]
            self.plotted_y_lines[i].dash_length = 1
            self.plotted_y_lines[i].dash_offset = 3
            i += 1

    def create_label(self, lab):
        mylabel = CoreLabel(text=str(lab), font_size = self.font_size, color=(1, 1, 1, 1))
        mylabel.refresh()
        texture = mylabel.texture
        texture_size = list(texture.size)
        return [texture, texture_size]

    def on_touch_down(self, touch):
        if 1 == 1:
            if touch.x < self.this_width /2 and self.COLUMN > 0 :
                self.COLUMN -= 1
                print (self.COLUMN)
            elif touch.x >= self.this_width /2 and self.COLUMN < len(self.y_labs)-1 :
                self.COLUMN += 1
                print (self.COLUMN)
            # make a new plot
            self.make_new_plot()
            return super(RelativeLayout, self).on_touch_down(touch)

    def remove_items(self, itemList):
        for item in itemList:
            self.canvas.remove(item)
        emptyList = []
        return emptyList

    def make_new_plot(self):
        self.step_size = self.step_size_ori
        self.plotted_y_labels = self.remove_items(self.plotted_y_labels)
        self.plotted_y_lines =  self.remove_items(self.plotted_y_lines)
        self.plotted_x_labels =  self.remove_items(self.plotted_x_labels)
        self.plotted_line =  self.remove_items(self.plotted_line)
        self.init_data()
        self.init_x_line()
        self.init_y_labels()
        self.update()

    def update(self):
        self.update_XY_axes()
        self.update_plot()
        self.add_widget(GraphButton())

    def on_leave(self, *args):
        self.COLUMN = 0
        self.make_new_plot()

    def on_enter(self, *args):
        self.make_new_plot()

# button on top of the graph
class GraphButton(Widget):
    #pressed = ListProperty([0, 0])
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            return super(GraphButton, self).on_touch_down(touch)

# Upload window
class UploadWindow(Screen):
    font_size = NumericProperty(12)
    text_input_str = StringProperty("foo")
    #https://www.dropbox.com/s/h9o01p36fqh4wf8/csv.csv?dl=1

    def __init__(self, **kwargs):
        super(UploadWindow, self).__init__(**kwargs)

    def on_text_validate(self,widget):
        self.text_input_str = widget.text
        df_csv = pd.read_csv(self.text_input_str)
        df_csv = df_csv.set_index(df_csv.columns[0])
        LineGraphWindow.df_data = df_csv
        LineGraphWindow()

    def on_size(self,*args):
        self.this_width = self.width
        self.this_height = self.height
        self.font_size =  int(min(self.height * 0.05, self.width * 0.05))

# initiate app
class WindowManager(ScreenManager):
    pass

class LineGraphApp(App):
    pass

if __name__ == "__main__":
    LineGraphApp().run()
