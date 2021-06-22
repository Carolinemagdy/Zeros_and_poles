from bokeh.models.layouts import Row
from bokeh.layouts import *
from bokeh.models import *
from bokeh.palettes import *
from bokeh.plotting import *
from math import *
from scipy.signal import freqz
import numpy as np
from scipy.signal import zpk2ss, ss2zpk, tf2zpk, zpk2tf
from cmath import *

# prepare the graph figures
system = figure(plot_width=400, plot_height=400, match_aspect=True, tools='save', margin=10,
title="Zeros and Poles Control System", toolbar_location="above")
magnitude= figure( tools=['save'],title='Magnitude',
plot_width=500, plot_height=300 ,  margin=10, toolbar_location="above")
phase= figure( tools=['save'],title='Phase',
plot_width=500, plot_height=300, margin=10, toolbar_location="above")

####### Unit Circle #############
system.circle(0, 0, radius=1.0, fill_alpha=0,color='blue')
system.line((0, 1), (0, 0),color='blue')
system.line((0, -1), (0, 0),color='blue')
system.line((0, 0), (0, 1),color='blue')
system.line((0, 0), (0, -1),color='blue')



######## conjugate_zeros ######
conjugate_zeros = ColumnDataSource(data=dict(x_of_zeros_conjugate=[], y_of_zeros_conjugate=[]))

conjugate_zeros_renderer = system.circle(x="x_of_zeros_conjugate", y="y_of_zeros_conjugate", source=conjugate_zeros,color='red', size=10)
conjugate_zeros_columns = [TableColumn(field="x_of_zeros_conjugate", title="x_of_zeros_conjugate"),
           TableColumn(field="y_of_zeros_conjugate", title="y_of_zeros_conjugate")
           ]
conjugate_zeros_table = DataTable(source=conjugate_zeros, columns=conjugate_zeros_columns, editable=True, height=200)



######## conjugate_poles ######
conjugate_poles = ColumnDataSource(data=dict(x_of_poles_conjugate=[], y_of_poles_conjugate=[]))

conjugate_poles_renderer = system.x(x="x_of_poles_conjugate", y="y_of_poles_conjugate", source=conjugate_poles,line_width=3, color='yellow', size=15)
conjugate_poles_columns = [TableColumn(field="x_of_poles_conjugate", title="x_of_poles_conjugate"),
           TableColumn(field="y_of_poles_conjugate", title="y_of_poles_conjugate")
           ]
conjugate_poles_table = DataTable(source=conjugate_poles, columns=conjugate_poles_columns, editable=True, height=200)


######## Pole ######
poles_source = ColumnDataSource(data=dict(x_of_poles=[], y_of_poles=[]))

poles_renderer = system.x(x="x_of_poles", y="y_of_poles", source=poles_source,line_width=3, color='yellow', size=15)
poles_columns = [TableColumn(field="x_of_poles", title="x_of_poles"),
           TableColumn(field="y_of_poles", title="y_of_poles")
           ]
poles_table = DataTable(source=poles_source, columns=poles_columns, editable=True, height=200)

########## Zero ########
zeros_source = ColumnDataSource(data=dict(x_of_zeros=[], y_of_zeros=[]))

zeros_render = system.circle(x='x_of_zeros', y='y_of_zeros', source=zeros_source, color='red', size=10)
zeros_columns = [TableColumn(field="x_of_zeros", title="x_of_zeros"),
           TableColumn(field="y_of_zeros", title="y_of_zeros")
           ]
zeros_table = DataTable(source=zeros_source, columns=zeros_columns, editable=True, height=200)

# choose to add zero or pole in the Radiobutton
LABELS = ["Zero", "Pole"]

radio_group = RadioGroup(labels=LABELS, active=None, width=400)
radio_group.js_on_click(CustomJS(code="""
    console.log('radio_group: active=' + this.active, this.toString())
"""))

# check whether pole or zero is activated
def zero_or_pole(new):
    if new == 0:
        draw_tool = PointDrawTool(renderers=[zeros_render], empty_value='red')
    else:
        draw_tool = PointDrawTool(renderers=[poles_renderer], empty_value='yellow')
    system.add_tools(draw_tool)
    system.toolbar.active_tap = draw_tool

radio_group.on_click(zero_or_pole)

########## check cojugate option #####

LABELS = ["Conjugate"]

checkbox_group = CheckboxGroup(labels=LABELS, active=[])
checkbox_group.js_on_click(CustomJS(code="""
    console.log('checkbox_group: active=' + this.active, this.toString())
"""))
flag=1


def conjugate(new):
    # clear all zeros and poles
    global flag
    if new == [0]:   
        flag=0
    else:
        flag=1
    zeros_source.data = {k: [] for k in zeros_source.data}
    poles_source.data = {k: [] for k in poles_source.data}
    conjugate_zeros.data = {k: [] for k in conjugate_zeros.data}
    conjugate_poles.data = {k: [] for k in conjugate_poles.data}

checkbox_group.on_click(conjugate)

######## Clear Buttons ########

reset_button = Button(label="Reset",  button_type="success", width=140,margin=0)
reset_button.js_on_click(CustomJS(code="console.log('button: click!', this.toString())"))

clear_zeros_button = Button(label="Clear Zeros", button_type="success",width=140,margin=0)
clear_zeros_button.js_on_click(CustomJS(code="console.log('button: click!', this.toString())"))

clear_poles_button = Button(label="Clear Poles", button_type="success",width=140,margin=0)
clear_poles_button.js_on_click(CustomJS(code="console.log('button: click!', this.toString())"))

def reset():
    # clear all zeros and poles
    zeros_source.data = {k: [] for k in zeros_source.data}
    poles_source.data = {k: [] for k in poles_source.data}
reset_button.on_click(reset)

def clear_zeros():
    # clear all zeroes
    zeros_source.data = {k: [] for k in zeros_source.data}
clear_zeros_button.on_click(clear_zeros)


def clear_poles():    
    # clear all poles
    poles_source.data = {k: [] for k in poles_source.data}
clear_poles_button.on_click(clear_poles)

####### magnitude ######
magnitude_source= ColumnDataSource({
    'h':[], 'm':[]
})

magnitude.line(x='h',y='m',source=magnitude_source,color='springgreen',width=3)

phase_source= ColumnDataSource({
    'w':[], 'p':[]
})

phase.line(x='w',y='p',source=phase_source, color='springgreen',width=3)


def update(attr, old, new):
    global Zero,Pole
    Zero = []
    Pole = []
    new_x_of_zeros =[]
    new_y_of_zeros = []
    new_x_of_poles =[]
    new_y_of_poles = []
    if flag == 0:
        for i in range(len(zeros_source.data['x_of_zeros'])):
            Zero.append(zeros_source.data['x_of_zeros'][i]+zeros_source.data['y_of_zeros'][i]*1j)        
            new_x_of_zeros.append(zeros_source.data['x_of_zeros'][i])
            new_y_of_zeros.append(zeros_source.data['y_of_zeros'][i]*-1)
        
        conjugate_zeros.data = dict(x_of_zeros_conjugate=new_x_of_zeros, y_of_zeros_conjugate=new_y_of_zeros)
        conjugate_zeros_renderer = system.circle(x="x_of_zeros_conjugate", y="y_of_zeros_conjugate", source=conjugate_zeros,color='red', size=10)

        for i in range(len(poles_source.data['x_of_poles'])):
            Pole.append(poles_source.data['x_of_poles'][i]+poles_source.data['y_of_poles'][i]*1j)
            new_x_of_poles.append(poles_source.data['x_of_poles'][i])
            new_y_of_poles.append(poles_source.data['y_of_poles'][i]*-1)
        
        conjugate_poles.data = dict(x_of_poles_conjugate=new_x_of_poles, y_of_poles_conjugate=new_y_of_poles)
        conjugate_poles_renderer = system.x(x="x_of_poles_conjugate", y="y_of_poles_conjugate", source=conjugate_poles,line_width=3, color='yellow', size=15)

    else:
        for i in range(len(zeros_source.data['x_of_zeros'])):
            Zero.append(zeros_source.data['x_of_zeros'][i]+zeros_source.data['y_of_zeros'][i]*1j)
        for i in range(len(poles_source.data['x_of_poles'])):
            Pole.append(poles_source.data['x_of_poles'][i]+poles_source.data['y_of_poles'][i]*1j)   

    magnitude_phase()
    
def magnitude_phase():
    phase_source.data={
    'w':[], 'p':[]
    }

    magnitude_source.data={
    'h': [], 'm': []
    }
   
    num, den=zpk2tf(Zero,Pole,1)
    w,h=freqz(num,den,worN=10000)
    magnitude1=np.sqrt(h.real**2+h.imag**2)
    phase=np.arctan(h.imag/h.real)
    magnitude_source.stream({
    'h': w, 'm': magnitude1
    })
    phase_source.stream({
        'w':w, 'p':phase
    })


zeros_source.on_change('data',update)
poles_source.on_change('data',update)

# layout
plot=Row(zeros_table,poles_table)
radio_button_group=Row(reset_button,clear_zeros_button,clear_poles_button)
first_column= column(system,radio_group,radio_button_group,background='darkgrey')
second_column=column(magnitude,phase ,checkbox_group)
curdoc().theme = 'dark_minimal'
curdoc().add_root(Row(first_column,second_column,plot,background='darkgrey'))