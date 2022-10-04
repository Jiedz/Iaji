"""
This module defines some utility classes and functions for GUI programming with Qt
"""
# In[imports]
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg,
    NavigationToolbar2QT as NavigationToolbar)

from matplotlib import pyplot
from matplotlib.figure import Figure
from PyQt5.QtCore import Qt, QRect
from PyQt5.Qt import QFont
from PyQt5.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDateEdit,
    QDateTimeEdit,
    QDial,
    QDoubleSpinBox,
    QFontComboBox,
    QHBoxLayout,
    QLabel,
    QLCDNumber,
    QLineEdit,
    QMainWindow,
    QProgressBar,
    QPushButton,
    QRadioButton,
    QSlider,
    QSpinBox,
    QTabWidget,
    QTextEdit,
    QTimeEdit,
    QVBoxLayout,
    QBoxLayout,
    QGridLayout,
    QWidget,
)

import numpy
from Iaji.Utilities.strutils import any_in_string
# In[Label + edit widget]
class LabelEditWidget(QWidget):
    def __init__(self, label:str="label", text:str="", orientation:str = "horizontal", edit_type:str ="linedit", **kwargs):
        super().__init__()
        self.orientation = orientation
        if self.orientation == "horizontal":
            self.layout = QHBoxLayout()
        else:
            self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        #Label
        self.label = QLabel()
        self.label.setText(label)
        self.layout.addWidget(self.label)
        #Linedit
        if edit_type == "linedit":
            self.linedit = QLineEdit(text)
            self.layout.addWidget(self.linedit)
        elif edit_type == "textedit":
            self.textedit = QTextEdit(text)
            self.layout.addWidget(self.textedit)
        else:
            items_list = kwargs["items_list"]
            self.combobox = QComboBox()
            self.combobox.addItems(items_list)
            self.layout.addWidget(self.combobox)
        self.set_style()
    #-----------------------------
    def set_style(self, style = None):
        if not style:
            self.style_sheets = WidgetStyle().style_sheets
        else:
            self.style_sheets = style.style_sheets
        #self.style_sheets["main"] = "LabelTexteditWidget \n {" + \
        #    self.style_sheets["main"] + "}"
        self.setStyleSheet(self.style_sheets["main"])
        excluded_strings = ["layout", "callback", "clicked", "toggled", "changed", "edited", "checked"]
        for widget_type in ["label", "linedit", "textedit"]:
            widgets = [getattr(self, name) for name in list(self.__dict__.keys()) if
                       widget_type in name and not any_in_string(excluded_strings, name)]
            for widget in widgets:
                widget.setStyleSheet(self.style_sheets[widget_type])
        # -------------------------------------
# In[Pyplot widget]
class PyplotWidget(QWidget):
    """
    This class describes a Qt widget that contains a matplotlib.pyplot figure
    """
    #-------------------------------------
    def __init__(self, figure:Figure = None, name="Plot"):
        """
:param figure:matplotlib.figure.Figure
            figure
:param name:str
            name of the plot
        """
        super().__init__()
        self.figure = figure
        if self.figure is None:
            figure = pyplot.figure()
        self.canvas = FigureCanvas(self.figure)
        self.name = name
        #Window title
        self.setWindowTitle(self.name)
        #Layout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        # Matplotlib navigation toolbar
        self.navigation_toolbar = NavigationToolbar(self.canvas, self)
        self.layout.addWidget(self.navigation_toolbar)
        #Figure widget
        self.layout.addWidget(self.canvas)
    # -------------------------------------
    def set_style(self, theme):
        self.setStyleSheet(self.style_sheets["main"][theme])
        excluded_strings = ["layout", "callback", "clicked", "toggled", "changed", "edited", "checked"]
        for widget_type in ["label", "button", "tabs"]:
            widgets = [getattr(self, name) for name in list(self.__dict__.keys()) if
                       widget_type in name and not any_in_string(excluded_strings, name)]
            for widget in widgets:
                widget.setStyleSheet(self.style_sheets[widget_type][theme])
    # -------------------------------------
    def update(self):
        self.canvas.draw_idle()
'''
class PyplotWidget(FigureCanvasQTAgg):
    """
    This class describes a Qt widget that contains a matplotlib.pyplot figure
    """
    #-------------------------------------
    def __init__(self, name="Plot"):
        """
:param figure:matplotlib.figure.Figure
            figure
:param name:str
            name of the plot
        """
        super().__init__()
        self.name = name
        #Window title
        self.setWindowTitle(self.name)
        #Layout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
    # -------------------------------------
    def set_style(self, theme):
        self.setStyleSheet(self.style_sheets["main"][theme])
        excluded_strings = ["layout", "callback", "clicked", "toggled", "changed", "edited", "checked"]
        for widget_type in ["label", "button", "tabs"]:
            widgets = [getattr(self, name) for name in list(self.__dict__.keys()) if
                       widget_type in name and not any_in_string(excluded_strings, name)]
            for widget in widgets:
                widget.setStyleSheet(self.style_sheets[widget_type][theme])
    # -------------------------------------
    #def update(self):
   #     self.canvas.draw_idle()
'''


class WidgetStyle:
    def __init__(self, colors=None, font=None):
        """
        

        Parameters
        ----------
        colors:(str, str, str), optional
            (background color, text color, border color). The default is None.
        font:(str, int), optional
            (font family, biggest font size). The default is None.

        Returns
        -------
        None.

        """
        self.widget_types = ["main", "button", "label", "title_label", "slider", "tabs", "radiobutton", "doublespinbox", \
                             "linedit", "textedit", "checkbox", "combobox", "calendar"]
        if not font:
            self.font = {"family":"Times New Roman", \
                         "size":24}
        else:
            self.font = dict(zip(["family", "size"], font))
        if not colors:
            self.colors = {"main background":"#082032", \
                           "widget background":"#2C394B", \
                       "text":"#EEEEEE", \
                       "border":"#EEEEEE"}
        else:
            self.colors = dict(zip(["main background", "widget background", "text", "border"], colors))
        self.style_sheets = {}
        #Set style sheets
        self.style_sheets["main"] = """
background-color:; 
color:;
"""
        self.style_sheets["title_label"] = """
QLabel
{
background-color:; 
color:;
border-color:; 
border:2px;
font-family: ;
font-size:24pt;
max-width:400px;
max-height:50px;
}
"""
        self.style_sheets["label"] = """
QLabel
{
background-color:; 
color:;
border-color:; 
border:2px;
font-family:;
font-size:18pt;
max-width:400px;
max-height:50px;
}
"""
        self.style_sheets["button"] = """
QPushButton
{
background-color:; 
color:; 
border:1.5px solid #C4C4C3;
border-color:;
border-top-left-radius:4px;
border-top-right-radius:4px;
border-bottom-left-radius:4px;
border-bottom-right-radius:4px;
max-width:200px;
max-height:30px;
font-family:;
font-size:13pt;
}
QPushButton:pressed
{
background-color:; 
color:#2C394B;
}
QPushButton:hover
{
background-color:; 
color:#2C394B;
}
"""
        self.style_sheets["radiobutton"] = """
QRadioButton
{
background-color:; 
color:; 
border:1.5px solid #C4C4C3;
border-color:;
border-top-left-radius:4px;
border-top-right-radius:4px;
border-bottom-left-radius:4px;
border-bottom-right-radius:4px;
max-width:200px;
max-height: 30px;
font-family:;
font-size:13pt;
}
QPushButton:pressed
{
background-color:; 
color:#2C394B;
}
QPushButton:hover
{
background-color:; 
color:#2C394B;
}
"""
        self.style_sheets["tabs"] ="""
QTabBar::tab 
{
background:qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #E1E1E1, stop:0.4 #DDDDDD,
        stop:0.5 #D8D8D8, stop:1.0 #D3D3D3);
border:2px solid #C4C4C3;
border-bottom-color:; /* same as the pane color */
border-top-left-radius:4px;
border-top-right-radius:4px;
min-width:8ex;
width:250px;
height:30px;
padding:2px;
color:black;
font-family:;
font-size:13pt;z`
}
"""
        self.style_sheets["slider"] = """
QSlider
{
background-color:;
color:;
border:1px solid #C4C4C3;
border-color:;
max-width:200px;
max-height: 20px;
}
QSlider::handle
{
color:;
background-color:;
width:18px;
height:35px;
border-radius:4px;
border:1px solid #C4C4C3;
border-color:; 
}
QSlider::groove
{
background-color:;
color:;
}
"""
        self.style_sheets["checkbox"] = """
QCheckBox
{
background-color:; 
color:; 
border-color:;
border:1.5px solid #C4C4C3;
font-family:;
font-size:13pt;
max-width:200px;
max-height: 20px;
}
"""
        self.style_sheets["linedit"] = """
QLineEdit
{""
background-color:;
border-color:;
color:;
font-family:;
font-size:12pt;
}
"""
        self.style_sheets["textedit"] = """
QTextEdit
{
background-color:;
border-color:;
color:;
font-family:;
font-size:12pt;
}
"""
        self.style_sheets["doublespinbox"] = """
QDoubleSpinBox
{
background-color:;
border-color:;
color:;
font-family:;
font-size:12pt;
}
"""
        self.style_sheets["combobox"] = """
QComboBox
{
background-color:; 
color:; 
border-color:;
border:1.5px solid #C4C4C3;
font-family:;
font-size:13pt;
max-width:200px;
max-height: 20px;
}
"""
        self.style_sheets["calendar"] = """
QMenu { 
    font-size:16px; width:150px; left:20px;
    font-family:
    background-color:;
    }
"""
        for widget_type in self.widget_types:
            #Set font
            self.style_sheets[widget_type] = \
                self.style_sheets[widget_type].replace("\nfont-family:", "\nfont-family:%s"%self.font["family"])
            #Set colors
            self.style_sheets[widget_type] = \
                self.style_sheets[widget_type].replace("\ncolor:", "\ncolor:%s"%self.colors["text"])\
                    .replace("\nbackground-color:", "\nbackground-color:%s"%self.colors["main background"])\
                        .replace("\nborder-color:", "\nborder-color:%s"%self.colors["border"])
        

