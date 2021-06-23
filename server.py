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
system = figure(plot_width=400, plot_height=400, match_aspect=True,x_range=(-2,2), y_range=(-2, 2), tools='save', margin=10,
title="Zeros and Poles Control System", toolbar_location="above")
magnitude= figure( tools=['save'],title='Magnitude',
plot_width=500, plot_height=300 ,  margin=10, toolbar_location="above")
phase= figure( tools=['save'],title='Phase',
plot_width=500, plot_height=300, margin=10, toolbar_location="above")
filter = figure(plot_width=400, plot_height=400, match_aspect=True,x_range=(-2,2), y_range=(-2, 2), tools='save', margin=10,
title="Custom Filter", toolbar_location="above")
phase_filter= figure( tools=['save'],title='Phase',
plot_width=500, plot_height=300, margin=10, toolbar_location="above")

####### Unit Circle #############
system.circle(0, 0, radius=1.0, fill_alpha=0,color='blue')
system.line((0, 1), (0, 0),color='blue')
system.line((0, -1), (0, 0),color='blue')
system.line((0, 0), (0, 1),color='blue')
system.line((0, 0), (0, -1),color='blue')

filter.circle(0, 0, radius=1.0, fill_alpha=0,color='blue')
filter.line((0, 1), (0, 0),color='blue')
filter.line((0, -1), (0, 0),color='blue')
filter.line((0, 0), (0, 1),color='blue')
filter.line((0, 0), (0, -1),color='blue')
####### magnitude ######
magnitude_source= ColumnDataSource({
    'h':[], 'm':[]
})

magnitude.line(x='h',y='m',source=magnitude_source,color='springgreen',width=3)

phase_source= ColumnDataSource({
    'w':[], 'p':[]
})

phase.line(x='w',y='p',source=phase_source, color='springgreen',width=3)

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

########## Filter ########## 

######## Pole ######
poles_filter_source = ColumnDataSource(data=dict(x_of_poles_filter=[], y_of_poles_filter=[]))

poles_filter_renderer = filter.x(x="x_of_poles_filter", y="y_of_poles_filter", source=poles_filter_source,line_width=3, color='yellow', size=15)
poles_filter_columns = [TableColumn(field="x_of_poles_filter", title="x_of_poles_filter"),
           TableColumn(field="y_of_poles_filter", title="y_of_poles_filter")
           ]
poles_filter_table = DataTable(source=poles_filter_source, columns=poles_filter_columns, editable=True, height=200)

########## Zero ########
zeros_filter_source = ColumnDataSource(data=dict(x_of_zeros_filter=[], y_of_zeros_filter=[]))

zeros_filter_render = filter.circle(x='x_of_zeros_filter', y='y_of_zeros_filter', source=zeros_filter_source, color='red', size=10)
zeros_filter_columns = [TableColumn(field="x_of_zeros_filter", title="x_of_zeros_filter"),
           TableColumn(field="y_of_zeros_filter", title="y_of_zeros_filter")
           ]
zeros_filter_table = DataTable(source=zeros_filter_source, columns=zeros_filter_columns, editable=True, height=200)

######## relative_zeros ######
relative_zeros = ColumnDataSource(data=dict(x_of_zeros_relative=[], y_of_zeros_relative=[]))

relative_zeros_renderer = filter.circle(x="x_of_zeros_relative", y="y_of_zeros_relative", source=relative_zeros,color='red', size=10)
relative_zeros_columns = [TableColumn(field="x_of_zeros_relative", title="x_of_zeros_relative"),
           TableColumn(field="y_of_zeros_relative", title="y_of_zeros_relative")
           ]
relative_zeros_table = DataTable(source=relative_zeros, columns=relative_zeros_columns, editable=True, height=200)

######## relative_poles ######
relative_poles = ColumnDataSource(data=dict(x_of_poles_relative=[], y_of_poles_relative=[]))

relative_poles_renderer = filter.x(x="x_of_poles_relative", y="y_of_poles_relative", source=relative_poles,line_width=3, color='yellow', size=15)
relative_poles_columns = [TableColumn(field="x_of_poles_relative", title="x_of_poles_relative"),
           TableColumn(field="y_of_poles_relative", title="y_of_poles_relative")
           ]
relative_poles_table = DataTable(source=relative_poles, columns=relative_poles_columns, editable=True, height=200)

###### Phase filter ##########
phase_filter_source= ColumnDataSource({
    'x':[], 'y':[]
})

phase_filter.line(x='x',y='y',source=phase_filter_source, color='springgreen',width=3)


# choose to add zero or pole in the filter
LABELS = ["Zero", "Pole"]

radio_group_filter = RadioGroup(labels=LABELS, active=None, width=400)
radio_group_filter.js_on_click(CustomJS(code="""
    console.log('radio_group_filter: active=' + this.active, this.toString())
"""))

# check whether pole or zero is activated
def zero_or_pole_filter(new):
    if new == 0:
        draw_tool1 = PointDrawTool(renderers=[zeros_filter_render], empty_value='red')
    else:
        draw_tool1 = PointDrawTool(renderers=[poles_filter_renderer], empty_value='yellow')
    filter.add_tools(draw_tool1)
    filter.toolbar.active_tap = draw_tool1

radio_group_filter.on_click(zero_or_pole_filter)

######### Update filter data ######

Zero = []
Pole = []
Zero_filter = []
Pole_filter = []

def update_filter(attr, old, new):
    global Zero_filter,Pole_filter,Zero,Pole
    new_x_of_zeros=[]
    new_y_of_zeros=[]
    new_x_of_poles=[]
    new_y_of_poles=[]    
    Zero_filter = []
    Pole_filter = []

    for i in range(len(zeros_filter_source.data['x_of_zeros_filter'])):
        Zero_filter.append(zeros_filter_source.data['x_of_zeros_filter'][i]+zeros_filter_source.data['y_of_zeros_filter'][i]*1j)
        den= ((zeros_filter_source.data['x_of_zeros_filter'][i])**2)+((zeros_filter_source.data['y_of_zeros_filter'][i])**2)
        Pole_filter.append(((zeros_filter_source.data['x_of_zeros_filter'][i])/den)+ ((zeros_filter_source.data['y_of_zeros_filter'][i])/den)*1j)
        new_x_of_poles.append((zeros_filter_source.data['x_of_zeros_filter'][i])/den)
        new_y_of_poles.append((zeros_filter_source.data['y_of_zeros_filter'][i])/den)

    relative_poles.data = dict(x_of_poles_relative=new_x_of_poles, y_of_poles_relative=new_y_of_poles)
    relative_poles_renderer = filter.x(x="x_of_poles_relative", y="y_of_poles_relative", source=relative_poles,line_width=3, color='yellow', size=15)
    relative_poles_renderer1 = system.x(x="x_of_poles_relative", y="y_of_poles_relative", source=relative_poles,line_width=3, color='yellow', size=15)
    zeros_renderer2 = system.circle(x="x_of_zeros_filter", y="y_of_zeros_filter", source=zeros_filter_source,color='red', size=10)

    
    for i in range(len(poles_filter_source.data['x_of_poles_filter'])):
        Pole_filter.append(poles_filter_source.data['x_of_poles_filter'][i]+poles_filter_source.data['y_of_poles_filter'][i]*1j)
        den= ((poles_filter_source.data['x_of_poles_filter'][i])**2)+((poles_filter_source.data['y_of_poles_filter'][i])**2)
        Zero_filter.append(((poles_filter_source.data['x_of_poles_filter'][i])/den)+ ((poles_filter_source.data['y_of_poles_filter'][i])/den)*1j)
        new_x_of_zeros.append((poles_filter_source.data['x_of_poles_filter'][i])/den)
        new_y_of_zeros.append((poles_filter_source.data['y_of_poles_filter'][i])/den)

    relative_zeros.data = dict(x_of_zeros_relative=new_x_of_zeros, y_of_zeros_relative=new_y_of_zeros)
    relative_zeros_renderer3 = filter.circle(x="x_of_zeros_relative", y="y_of_zeros_relative", source=relative_zeros,color='red', size=10)     
    poles_renderer4 = system.x(x="x_of_poles_filter", y="y_of_poles_filter", source=poles_filter_source,line_width=3, color='yellow', size=15)
    relative_zeros_renderer5 = system.circle(x="x_of_zeros_relative", y="y_of_zeros_relative", source=relative_zeros,color='red', size=10)     

    filter_phase()
    magnitude_phase()
    
def filter_phase():
    phase_filter_source.data={
    'x':[], 'y':[]
    }
    num, den=zpk2tf(Zero_filter,Pole_filter,1)
    w,h=freqz(num,den,worN=10000)
    phase=np.arctan(h.imag/h.real)
    phase_filter_source.stream({
        'x':w, 'y':phase
    })


######## Clear Buttons filter ########

reset_button_filter = Button(label="Reset",  button_type="success", width=140,margin=0)
reset_button_filter.js_on_click(CustomJS(code="console.log('button: click!', this.toString())"))

def reset_filter():
    # clear all zeros and poles
    zeros_filter_source.data = {k: [] for k in zeros_filter_source.data}
    poles_filter_source.data = {k: [] for k in poles_filter_source.data}
reset_button_filter.on_click(reset_filter)



menu = [("Filter 1", "filter_1"), ("Filter 2", "filter_2"), ("Filter 3", "filter_3"), ("Filter 4", "filter_4")]

dropdown = Dropdown(label="Filters", button_type="success", menu=menu)
dropdown.js_on_event("menu_item_click", CustomJS(code="console.log('dropdown: ' + this.item, this.toString())"))

def dropdown_filter( new):
    reset_filter()
    if new.item== "filter_1":
        k=[-0.7,0.2]
        p=[0.3,0.7]
        zeros_filter_source.stream({'x_of_zeros_filter': k, 'y_of_zeros_filter': p})

    elif new.item== "filter_2":
        k=[1.4,0.9]
        p=[0.7,0.2]
        zeros_filter_source.stream({'x_of_zeros_filter': k, 'y_of_zeros_filter': p})
    
    elif new.item== "filter_3":
        k=[-1.2,-0.6]
        p=[0.1,0.2]
        poles_filter_source.stream({'x_of_poles_filter': k, 'y_of_poles_filter': p})
    elif new.item== "filter_4":
        k=[-0.5,0.9]
        p=[0.1,0.4]
        poles_filter_source.stream({'x_of_poles_filter': k, 'y_of_poles_filter': p})

dropdown.on_click(dropdown_filter)



zeros_filter_source.on_change('data',update_filter)
poles_filter_source.on_change('data',update_filter)

################# End of filters #############




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
    Zero_plot=[]
    Pole_plot=[]
    Zero_plot.extend(Zero)
    Zero_plot.extend(Zero_filter)
    Pole_plot.extend(Pole)
    Pole_plot.extend(Pole_filter)
    num, den=zpk2tf(Zero_plot,Pole_plot,1)
    w,h=freqz(num,den,worN=10000)
    num1, den1=zpk2tf(Zero,Pole,1)
    w1,h1=freqz(num1,den1,worN=10000)
    magnitude1=np.sqrt(h1.real**2+h1.imag**2)
    phase=np.arctan(h.imag/h.real)
    magnitude_source.stream({
    'h': w1, 'm': magnitude1
    })
    phase_source.stream({
        'w':w, 'p':phase
    })


zeros_source.on_change('data',update)
poles_source.on_change('data',update)

# layout
radio_button_group=Row(reset_button,clear_zeros_button,clear_poles_button)
first_column= column(system,radio_group,radio_button_group,checkbox_group,filter,radio_group_filter,reset_button_filter)
second_column=column(magnitude,phase ,dropdown,phase_filter )
curdoc().theme = 'dark_minimal'
curdoc().add_root(Row(first_column,second_column,background='darkgrey'))