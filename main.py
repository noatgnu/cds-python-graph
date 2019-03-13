
# coding: utf-8

# In[ ]:


import pandas as pd


# # Working with real world data

# In[ ]:


file_path = "../data/WHS8_110.csv"
measles_1 = pd.read_csv(file_path)
# Column name incorrect
measles_1.head()


# In[ ]:


measles_1 = pd.read_csv(file_path, header=[0, 1])
# Multilevel column name
measles_1.head()


# In[ ]:


measles_1 = pd.read_csv(file_path, header=[0, 1], index_col=0)
# Indexed at country name
measles_1.head()


# In[ ]:


measles_1.columns
# name too long and there are space infront of year
# Index type is immutable so we can't just change the value within the index
# Index have to be unique


# In[ ]:


measles_1.columns.names = ["Dose", "Year"]
measles_1.head()


# In[ ]:


measles_1.columns = measles_1.columns.set_levels(["M1"], level=0)
measles_1.columns


# In[ ]:


measles_1.columns = measles_1.columns.set_levels([int(i.strip()) for i in measles_1.columns.levels[1]], level=1)
measles_1.columns


# # Plotting with Matplotlib

# In[ ]:


measles_1["M1"].head()


# In[ ]:


import matplotlib.pyplot as plt
plt.scatter(measles_1.loc["Australia"]["M1"].index, measles_1.loc["Australia"]["M1"])


# In[ ]:


plt.plot(measles_1.loc["Australia"]["M1"].index, measles_1.loc["Australia"]["M1"])


# In[ ]:


plt.scatter(measles_1.loc["Australia"]["M1"].index, measles_1.loc["Australia"]["M1"])
plt.plot(measles_1.loc["Australia"]["M1"].index, measles_1.loc["Australia"]["M1"])


# In[ ]:


plt.plot(measles_1.loc["Australia"]["M1"].index, measles_1.loc["Australia"]["M1"])
plt.plot(measles_1.loc["United States of America"]["M1"])
plt.legend()


# In[ ]:


plt.plot(measles_1.loc["Australia"]["M1"].index, measles_1.loc["Australia"]["M1"], color='g')
plt.plot(measles_1.loc["United States of America"]["M1"], color='r')
plt.legend()


# In[ ]:


combined = measles_1.loc[["United States of America", "Australia"]]
combined.head()


# In[ ]:


combined.loc["Australia"].max()


# In[ ]:


combined.max()


# In[ ]:


# max() function did not work on a single data series but it work on a dataframe.


# In[ ]:


combined.max(numeric_only=True)


# In[ ]:


# All other column values are not integer type
combined = combined.applymap(lambda x: x if type(x) is not str else int(x))
combined.max(numeric_only=True)


# In[ ]:


combined["M1"]


# In[ ]:


# https://matplotlib.org/examples/color/colormaps_reference.html
fig, ax = plt.subplots()
hm = ax.pcolormesh(combined["M1"].values, cmap='plasma', vmin=0, vmax=100)

ax.set_xticks([i+0.5 for i in range(0, len(combined["M1"].columns))])
ax.set_xticklabels(combined["M1"].columns)
for label in ax.get_xticklabels():
    label.set_rotation(90)
ax.set_yticks([i+ 0.5 for i in range(0, len(combined["M1"].index))])
ax.set_yticklabels(combined["M1"].index)
cbar = plt.colorbar(hm, ax=ax, pad=.015, aspect=10)


# In[ ]:


# Now let do a heatmap of the whole dataset.


measles_1.applymap(lambda x: x if type(x) is not str else int(x))
# Error due to at least one value can't be converted into int


# In[ ]:


measles_1 = measles_1.applymap(lambda x: (x) if type(x) is not str else (int(x.split()[0]) if " " in x else int(x)))


# In[ ]:


measles_1.head()


# In[ ]:


fig2, ax2 = plt.subplots(figsize=(10,40))
hm = ax2.pcolormesh(measles_1["M1"].values, cmap='plasma', vmin=0, vmax=100)

ax2.set_xticks([i+0.5 for i in range(0, len(measles_1["M1"].columns))])
ax2.set_xticklabels(measles_1["M1"].columns)
for label in ax2.get_xticklabels():
    label.set_rotation(90)
ax2.set_yticks([i+ 0.5 for i in range(0, len(measles_1["M1"].index))])
ax2.set_yticklabels(measles_1["M1"].index)
cbar = plt.colorbar(hm, ax=ax2, pad=.015, aspect=10)


# In[ ]:


file_path2 = "..\data\MCV2.csv"
measles_2 = pd.read_csv(file_path2, header=[0, 1], index_col=0)
measles_2.columns.names = ["Dose", "Year"]
measles_2.columns = measles_2.columns.set_levels(["M2"], level=0)
measles_2.columns = measles_2.columns.set_levels([int(i.strip()) for i in measles_2.columns.levels[1]], level=1)
measles_2 = measles_2.applymap(lambda x: (x) if type(x) is not str else (int(x.split()[0]) if " " in x else int(x)))
measles = measles_1.join(measles_2)

measles.head()


# In[ ]:


def make_hm(ax, dose, title):
    hm = ax.pcolormesh(measles[dose].values, cmap='plasma', vmin=0, vmax=100)
    ax.set_xticks([i+0.5 for i in range(0, len(measles[dose].columns))])
    ax.set_xticklabels(measles[dose].columns)
    for label in ax.get_xticklabels():
        label.set_rotation(90)
    ax.set_yticks([i+ 0.5 for i in range(0, len(measles[dose].index))])
    ax.set_yticklabels(measles[dose].index)
    ax.set_title(title)
    cbar = plt.colorbar(hm, ax=ax, pad=.015, aspect=50)

fig3, (ax_m1, ax_m2) = plt.subplots(1, 2, figsize=(60,40))
make_hm(ax_m1, "M1", "Measles First Dose Statistics")
make_hm(ax_m2, "M2", "Measles Second Dose Statistics")


# In[ ]:


# Saving image in SVG format
fig3.savefig("measles.svg")


# # Plotting with Bokeh

# In[ ]:


# Plotting with Bokeh
from bokeh.plotting import figure, output_file, show, curdoc
m1 = measles.loc["Australia", "M1"]
m1.head()


# In[ ]:


m2 = measles.loc["Australia", "M2"]
m2.head()


# In[ ]:


output_file('measles.html')
p = figure(title="Measles", x_axis_label="Years", y_axis_label="Coverage (%)")


# In[ ]:


p.line(m1.index, m1, legend="M1")


# In[ ]:


show(p)


# In[ ]:


p.line(m2.index, m2, legend="M2", line_color="red")


# In[ ]:


show(p)


# In[ ]:


# Bring legend out
from bokeh.models import Legend
curdoc().clear()
output_file('measles.html')
p = figure(title="Measles", x_axis_label="Years", y_axis_label="Coverage (%)", toolbar_location="above")
m1 = p.line(m1.index , m1, line_color="green")
m2 = p.line(m2.index, m2, line_color="red")
legend = Legend(items=[
    ("M1", [m1]),
    ("M2", [m2])
], location=(10, 30))
p.add_layout(legend, 'right')

show(p)


# In[ ]:


# Combining line and circle
curdoc().clear()
TOOLS = "crosshair,pan,wheel_zoom,box_zoom,reset,box_select,lasso_select"
output_file('measles.html')
p = figure(title="Measles", x_axis_label="Years", y_axis_label="Coverage (%)", toolbar_location="above", tools=TOOLS)
m1_circle = p.circle(m1.index, m1, radius=0.3, fill_color="green", line_color=None)
m2_circle = p.circle(m2.index, m2, radius=0.3, fill_color="red", line_color=None)
m1_line = p.line(m1.index, m1, line_color="green")
m2_line = p.line(m2.index, m2, line_color="red")
legend = Legend(items=[
    ("M1", [m1_circle, m1_line]),
    ("M2", [m2_circle, m2_line])
], location=(10, 30))
p.add_layout(legend, 'right')

show(p)


# In[ ]:


# Multiple graphs
from bokeh.layouts import gridplot

data = measles.loc[["Australia", "United States of America"]]
data.head()


# In[ ]:


curdoc().clear()
TOOLS = "crosshair,pan,wheel_zoom,box_zoom,reset,box_select,lasso_select"
output_file('measles.html')
figure_list = []
for i in data.index:
    country_m1 = data.loc[i]["M1"]
    country_m2 = data.loc[i]["M2"]
    p = figure(title=i, x_axis_label="Years", y_axis_label="Coverage (%)", toolbar_location="above", tools=TOOLS)
    m1_triangle = p.triangle(country_m1.index, country_m1, size=10, fill_color="navy", line_color=None, alpha=0.5)
    m2_square = p.square(country_m2.index, country_m2, size=10, fill_color="olive", line_color=None, alpha=0.5)
    legend = Legend(items=[
        ("M1", [m1_triangle]),
        ("M2", [m2_square])
    ], location=(10, 30))
    p.add_layout(legend, "right")
    figure_list.append(p)
graph = gridplot([figure_list])
show(graph)


# In[ ]:


from bokeh.models import LinearColorMapper, BasicTicker, PrintfTickFormatter, ColorBar
from bokeh.palettes import Plasma


# In[ ]:


# Transpose the data so that years will become index and country become columns
data_t = data.T
data_t.columns.name = "Country"
# Get a list of years to be use as x axis of heatmap and convert them to categorical
years = list(data_t.loc["M1"].index.astype(str))
# Get a list of countries from columns attribute of the dataframe
countries = list(data_t.loc["M1"].columns)
# Reduce column index by one level and shift the removed index level into one column then convert Year into a normal column
data_long = data_t.loc["M1"].stack().reset_index()
data_long.head()


# In[ ]:


# Rename the newly created column 0 and convert Year column into categorical
data_long = data_long.rename({0:"Coverage"}, axis="columns")
data_long["Year"] = data_long["Year"].astype(str)
data_long.head()


# In[ ]:


# Heatmap using plasma color palette
color_list = Plasma[10]
curdoc().clear()
mapper = LinearColorMapper(palette=color_list, low=0, high=100)
p = figure(title="Measles First Dose Coverage", 
           x_range=years, 
           y_range=countries, 
           x_axis_location="above", plot_width=900, plot_height=200,
           tools=TOOLS, 
           toolbar_location='below')
p.grid.grid_line_color = None
p.axis.axis_line_color = None
p.axis.major_tick_line_color = None
p.axis.major_label_standoff = 0
p.xaxis.major_label_orientation = pi / 3

p.rect(x="Year", y="Country", width=1, height=1,
       source=data_long,
       fill_color={'field': 'Coverage', 'transform': mapper},
       line_color=None)

cbar = ColorBar(color_mapper=mapper, location=(0,0))
p.add_layout(cbar, "right")
show(p)


# In[ ]:


# Heatmap using custom color palette as well as adding annotation and other styling option
color_list = ['#550b1d', '#933b41', '#cc7878', '#ddb7b1', '#dfccce', '#e2e2e2', '#c9d9d3', '#a5bab7', '#75968f']
curdoc().clear()
mapper = LinearColorMapper(palette=color_list, low=0, high=100)
p = figure(title="Measles First Dose Coverage", 
           x_range=years, 
           y_range=countries, 
           x_axis_location="above", plot_width=900, plot_height=400,
           tools=TOOLS, 
           toolbar_location='below', tooltips=[('Year', '@Year'), ('Country', '@Country'), ('Coverage', '@Coverage%')])

p.grid.grid_line_color = None
p.axis.axis_line_color = None
p.axis.major_tick_line_color = None
p.axis.major_label_standoff = 0
p.xaxis.major_label_orientation = pi / 3

p.rect(x="Year", y="Country", width=1, height=1,
       source=data_long,
       fill_color={'field': 'Coverage', 'transform': mapper},
       line_color=None)

cbar = ColorBar(color_mapper=mapper,
                     ticker=BasicTicker(desired_num_ticks=len(color_list)),
                     formatter=PrintfTickFormatter(format="%d%%"),
                     label_standoff=6, border_line_color=None,location=(0,0))
p.add_layout(cbar, "right")
show(p)


# In[ ]:


# Gridplot with two heatmap of measles coverage with every country
curdoc().clear()
figures = []
data_t = measles.T
data_t.columns.name = "Country"
for i in data_t.index.levels[0]:
    years = list(data_t.loc[i].index.astype(str))
    countries = list(data_t.loc[i].columns)
    data_long = data_t.loc[i].stack().reset_index()
    data_long = data_long.rename({0:"Coverage"}, axis="columns")
    data_long["Year"] = data_long["Year"].astype(str)
    p = figure(title="{0} Coverage {1}-{2}".format(i, years[0], years[-1]), 
               x_range=years, 
               y_range=countries, 
               x_axis_location="above", plot_width=900, plot_height=4000,
               tools=TOOLS, 
               toolbar_location='below', tooltips=[('Year', '@Year'), ('Country', '@Country'), ('Coverage', '@Coverage%')])

    p.grid.grid_line_color = None
    p.axis.axis_line_color = None
    p.axis.major_tick_line_color = None
    p.axis.major_label_standoff = 0
    p.xaxis.major_label_orientation = pi / 3

    p.rect(x="Year", y="Country", width=1, height=1,
           source=data_long,
           fill_color={'field': 'Coverage', 'transform': mapper},
           line_color=None)

    cbar = ColorBar(color_mapper=mapper,
                         ticker=BasicTicker(desired_num_ticks=len(color_list)),
                         formatter=PrintfTickFormatter(format="%d%%"),
                         label_standoff=6, border_line_color=None,location=(0,0), height=200)
    p.add_layout(cbar, "right")
    figures.append(p)
grid = gridplot([figures])
show(grid)

