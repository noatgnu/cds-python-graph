
# coding: utf-8

# # Data Visualization With Python
# 

# In[1]:


import pandas as pd
import numpy as np


# # Working with real world data
# 
# Real world data is often not perfect. We are likely encounter inconsistency within data formatting as well as multilevel headers. Thus, we will be getting familiar with some of the ways you can clean up your data.
# 
# Within the data repository of this workshop there are 4 files:
# 
# - countries.geojson (containing geolocation boundary of all countries in a text serialized format obtained from [here](https://github.com/datasets/geo-countries/blob/master/data/countries.geojson))
# - countries.regions.csv (CSV file containing designated geo-graphical label of all countries obtained from [here](https://github.com/lukes/ISO-3166-Countries-with-Regional-Codes/blob/master/all/all.csv))
# - WHS8_110.csv (CSV file of covarage statistics from WHO for Measles vaccine first dose obtained from [here](http://apps.who.int/gho/data/node.main.A826?lang=en))
# - MCV2.csv (CSV file of covarage statistics from WHO for Measles vaccine second dose obtained from [here](http://apps.who.int/gho/data/node.main.MCV2n?lang=en))
# 
# 
# Here we would first attempt to load a CSV files containing coverage statistics of the the first dose of the recommended two-dose Measles vaccine series.

# In[2]:


file_path = "../data/WHS8_110.csv"
measles_1 = pd.read_csv(file_path)
# Column name incorrect
measles_1.head()


# In[3]:


measles_1 = pd.read_csv(file_path, header=[0, 1])
# Multilevel column name
measles_1.head()


# In[4]:


measles_1 = pd.read_csv(file_path, header=[0, 1], index_col=0)
# Indexed at country name
measles_1.head()


# In[5]:


measles_1.columns
# name too long and there are space infront of year
# Index type is immutable so we can't just change the value within the index
# Index have to be unique


# In[6]:


measles_1.columns.names = ["Dose", "Year"]
measles_1.head()


# In[7]:


measles_1.columns = measles_1.columns.set_levels(["M1"], level=0)
measles_1.columns


# In[8]:


measles_1.columns = measles_1.columns.set_levels([int(i.strip()) for i in measles_1.columns.levels[1]], level=1)
measles_1.columns


# # Plotting with Matplotlib

# In[9]:


measles_1["M1"].head()


# In[10]:


import matplotlib.pyplot as plt
plt.scatter(measles_1.loc["Australia"]["M1"].index, measles_1.loc["Australia"]["M1"])
plt.xlabel("Year")
plt.ylabel("Coverage (%)")


# To add a simple trendline to this graph, we can use np.polyfit to derive the polynomial coefficients or b_0, b_1 in y = b_0 + b_1*x^1 . Then use np.poly1d to reconstruct the associate polynomial function from the coefficients.

# In[11]:


aus_m1 = measles_1.loc["Australia"]["M1"]
aus_m1 = aus_m1.dropna()
plt.scatter(aus_m1.index, aus_m1.values)

# deriving least squares polynomial coefficients 
z = np.polyfit(aus_m1.index, aus_m1.astype(int), 2)
# 1-dimensional polynomial function from the derived coefficients
p = np.poly1d(z)

plt.plot(aus_m1.index, p(aus_m1.index))

plt.xlabel("Year")
plt.ylabel("Coverage (%)")


# In[12]:


plt.plot(aus_m1.index, aus_m1)
plt.xlabel("Year")
plt.ylabel("Coverage (%)")


# In[13]:


us_m1 = measles_1.loc["United States of America"]["M1"]
plt.plot(aus_m1.index, aus_m1, color='g')
plt.plot(us_m1, color='r')
plt.xlabel("Year")
plt.ylabel("Coverage (%)")
plt.legend()


# In[14]:


fig, ax = plt.subplots()
N, bins, patches = ax.hist(measles_1["M1"][2017].values, 10)
for b, p in zip(bins, patches):
    if b > 90:
        p.set_facecolor("r")


# Adding a normal distribution curve to the histogram require first deriving of mu and sigma values using norm from scipy.stats package.

# In[15]:


from scipy.stats import norm

# Try to fit the values
mu, sigma = norm.fit(measles_1["M1"][2017].values)

fig, ax = plt.subplots()

# Start a second axis for distribution curve
ax2 = ax.twinx()

# density=True set y axis as probability density instead of count
N, bins, patches = ax.hist(measles_1["M1"][2017].values, 20, density=True)
for b, p in zip(bins, patches):
    if b > 80:
        p.set_facecolor("r")

# Get value of the normal distribution curve for graphing
hist_fit = norm.pdf(bins, mu, sigma)

# Plot fitted line
ax2.plot(bins, hist_fit, color="g")
bins


# In[16]:


combined = measles_1.loc[["United States of America", "Australia"]]
combined.head()


# In[17]:


combined.loc["Australia"].max()


# In[18]:


combined.max()


# max() function did not work on a single data series but it work on a dataframe.

# In[19]:


combined.max(numeric_only=True)


# Lambda function is a shorthand function. It should only be written for small and simple function.
# 
# ```python
# f = lambda x: x + 1
# ```
# 
# is equivalent to 
# 
# ```python
# def f(x):
#     return x + 1
# ```

# In[20]:


# All other column values are not integer type
f = lambda x: x if type(x) is not str else int(x)


# Here
# ```python
# f = lambda x: x if type(x) is not str else int(x)
# ```
# is equivalent to 
# ```python
# def f(x):
#     if type(x) is not str:
#         return x
#     else:
#         return int(x)
# ```

# In[21]:


combined = combined.applymap(f)
combined.max(numeric_only=True)


# In[22]:


combined["M1"].head()


# In[23]:


# https://matplotlib.org/examples/color/colormaps_reference.html
fig, ax = plt.subplots(figsize=(10,5))
hm = ax.pcolormesh(combined["M1"].values, cmap='plasma', vmin=0, vmax=100)

ax.set_xticks([i+0.5 for i in range(0, len(combined["M1"].columns))])
ax.set_xticklabels(combined["M1"].columns)
for label in ax.get_xticklabels():
    label.set_rotation(90)
ax.set_yticks([i+ 0.5 for i in range(0, len(combined["M1"].index))])
ax.set_yticklabels(combined["M1"].index)
cbar = plt.colorbar(hm, ax=ax, pad=.015, aspect=10)


# In[24]:


# Now let do a heatmap of the whole dataset.
measles_1.applymap(f)


# In[25]:


# Error due to at least one value can't be converted into int
f2 = lambda x: (x) if type(x) is not str else (int(x.split()[0]) if " " in x else int(x))
measles_1 = measles_1.applymap(f2)


# ```python
# f = lambda x: (x) if type(x) is not str else (int(x.split()[0]) if " " in x else int(x))
# ```
# is equivalent to 
# ```python
# def f(x):
#     if type(x) is not str:
#         return x
#     else:
#         if " " in x:
#             return int(x.split()[0])
#         else:
#             return int(x)
# ```

# In[26]:


measles_1.head()


# In[27]:


fig2, ax2 = plt.subplots(figsize=(10,40))
hm = ax2.pcolormesh(measles_1["M1"].values, cmap='plasma', vmin=0, vmax=100)

ax2.set_xticks([i+0.5 for i in range(0, len(measles_1["M1"].columns))])
ax2.set_xticklabels(measles_1["M1"].columns)
for label in ax2.get_xticklabels():
    label.set_rotation(90)
ax2.set_yticks([i+ 0.5 for i in range(0, len(measles_1["M1"].index))])
ax2.set_yticklabels(measles_1["M1"].index)
cbar = plt.colorbar(hm, ax=ax2, pad=.015, aspect=10)


# In[28]:


file_path2 = "..\data\MCV2.csv"
measles_2 = pd.read_csv(file_path2, header=[0, 1], index_col=0)
measles_2.columns.names = ["Dose", "Year"]

measles_2.columns = measles_2.columns.set_levels(["M2"], level=0)
measles_2.columns = measles_2.columns.set_levels([int(i.strip()) for i in measles_2.columns.levels[1]], level=1)

measles_2 = measles_2.applymap(f2)
measles = measles_1.join(measles_2)

measles.head()


# In[29]:


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


# In[30]:


# Saving image in SVG format
fig3.savefig("measles.svg")


# # Plotting with Bokeh

# In[31]:


# Plotting with Bokeh
from bokeh.plotting import figure, output_file, show, curdoc
m1 = measles.loc["Australia", "M1"].dropna()
m1.head()


# In[32]:


m2 = measles.loc["Australia", "M2"].dropna()
m2.head()


# In[33]:


output_file('measles.html')
curdoc().clear()
p = figure(title="Measles", x_axis_label="Years", y_axis_label="Coverage (%)")


# In[34]:


p.line(m1.index, m1, legend="M1")


# In[35]:


show(p)


# In[36]:


p.line(m2.index, m2, legend="M2", line_color="red")


# In[37]:


show(p)


# In[38]:


# Bring legend out
from bokeh.models import Legend
curdoc().clear()
output_file('measles.html')
p = figure(title="Measles", x_axis_label="Years", y_axis_label="Coverage (%)", toolbar_location="above")
m1_line = p.line(m1.index , m1, line_color="green")
m2_line = p.line(m2.index, m2, line_color="red")
legend = Legend(items=[
    ("M1", [m1_line]),
    ("M2", [m2_line])
], location=(10, 30))
p.add_layout(legend, 'right')

show(p)


# In[39]:


# Combining line and scatter plot
curdoc().clear()
TOOLS = "crosshair,pan,wheel_zoom,box_zoom,reset,box_select,lasso_select,save"
output_file('measles.html')
p = figure(title="Measles", x_axis_label="Years", y_axis_label="Coverage (%)", toolbar_location="above", tools=TOOLS)
m1_circle = p.circle(m1.index, m1, radius=0.3, fill_color="green", line_color=None)
m2_circle = p.triangle(m2.index, m2, size=10, fill_color="red", line_color=None)
m1_line = p.line(m1.index, m1, line_color="green", line_width=3)
m2_line = p.line(m2.index, m2, line_color="red", line_width=3)

# Adding trendline using the same functions earlier used with matplotlib
m1_fit = np.polyfit(m1.index, m1, 2)
m1_trend = p.line(m1.index, np.poly1d(m1_fit)(m1.index), line_color="blue")

m2_fit = np.polyfit(m2.index, m2, 2)
m2_trend = p.line(m2.index, np.poly1d(m2_fit)(m2.index), line_color="olive")

# Adding legend
legend = Legend(items=[
    ("M1", [m1_circle, m1_line]),
    ("M1 trendline", [m1_trend]),
    ("M2", [m2_circle, m2_line]),
    ("M2 trendline", [m2_trend]),
], location=(10, 30))
p.add_layout(legend, 'right')

show(p)


# In[40]:


# Multiple graphs
from bokeh.layouts import gridplot

data = measles.loc[["Australia", "United States of America"]]
data.head()


# In[41]:


curdoc().clear()
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


# In[42]:


from bokeh.models import LinearColorMapper, BasicTicker, PrintfTickFormatter, ColorBar
from bokeh.palettes import Plasma


# In[43]:


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


# In[44]:


# Rename the newly created column 0 and convert Year column into categorical
data_long = data_long.rename({0:"Coverage"}, axis="columns")
data_long["Year"] = data_long["Year"].astype(str)
data_long.head()


# In[45]:


# Heatmap using plasma color palette
from numpy import pi
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


# In[46]:


# Make another heatmap function to reuse
def make_bokeh_heatmap(data, years, countries, title, colors, plot_width, plot_height, color_bar_ticks):
    mapper = LinearColorMapper(palette=color_list, low=0, high=100)
    p = figure(title=title, 
               x_range=years, 
               y_range=countries, 
               x_axis_location="above", plot_width=plot_width, plot_height=plot_height,
               tools=TOOLS, 
               toolbar_location='below', 
               tooltips=[('Year', '@Year'), ('Country', '@Country'), ('Coverage', '@Coverage%')])

    p.grid.grid_line_color = None
    p.axis.axis_line_color = None
    p.axis.major_tick_line_color = None
    p.axis.major_label_standoff = 0
    p.xaxis.major_label_orientation = pi / 3

    p.rect(x="Year", y="Country", width=1, height=1,
           source=data,
           fill_color={'field': 'Coverage', 'transform': mapper},
           line_color=None)

    cbar = ColorBar(color_mapper=mapper,
                         ticker=BasicTicker(desired_num_ticks=color_bar_ticks),
                         formatter=PrintfTickFormatter(format="%d%%"),
                         label_standoff=6, border_line_color=None,location=(0,0))
    p.add_layout(cbar, "right")
    return p


# In[47]:


# Heatmap using custom color palette as well as adding annotation and other styling option
color_list = ['#550b1d', '#933b41', '#cc7878', '#ddb7b1', '#dfccce', '#e2e2e2', '#c9d9d3', '#a5bab7', '#75968f']
curdoc().clear()
p = make_bokeh_heatmap(data_long, years, countries, "Measles First Dose Coverage", color_list, 900, 400, len(color_list))
show(p)


# In[48]:


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
    figures.append(
        make_bokeh_heatmap(
            data_long,
            years,
            countries,
            "{0} Coverage {1}-{2}".format(i, years[0], years[-1]),
            color_list,
            900, 4000, len(color_list)
        )
    )
grid = gridplot([figures])
show(grid)


# Height of the color bar can be change with an additional height parameter to the ColorBar object.

# In[49]:


# Mapping geographically relevant data using bokeh and geojson

import json
from bokeh.models import GeoJSONDataSource

# Geojson file contain coordinates for each country necessary for drawing a polygon of that country geographical shape
# Here we will load the geojson file that only contain country name and polygon coordinates and modify it to include the coverage data

with open("../data/countries.geojson", "rb") as infile:
    
    geojson = json.load(infile)


# In[50]:


country_region = pd.read_csv("../data/countries.regions.csv", index_col=0)
country_region.head()


# In[51]:


country_region = country_region[country_region["region"].isin(["Asia", "Oceania"])]
country_region.index.name = "Country"
selected_countries = country_region.join(measles["M1"])
selected_countries.tail()


# In[52]:


from bokeh.palettes import viridis
color_list = viridis(20)
mapper = LinearColorMapper(palette=color_list, low=0, high=100)


# In[53]:


# looping through each countries within the geojson file and add coverage data and only include the country if we have coverage data
modded_data = []

for f in geojson["features"]:
    if f["properties"]["ADMIN"] in selected_countries.index:
        if pd.notnull(selected_countries.loc[f["properties"]["ADMIN"]][2017]):
            f["properties"]["data"] = int(selected_countries.loc[f["properties"]["ADMIN"]][2017])
            f["properties"]["alpha"] = 0.7
            modded_data.append(f)

# create a new dictionary with the modified data array
new_dict = {"type": "FeatureCollection", "features": modded_data}


# In[54]:


# create a geojsondata string that can be load by GeoJSONDataSource
geo_data = GeoJSONDataSource(geojson=json.dumps(new_dict))


# In[55]:


curdoc().clear()
output_file('M1_Map.html')
p = figure(title="Measles First Dose Coverage, 2017",x_axis_location=None, y_axis_location=None, plot_width=1200, plot_height=1000,
    tooltips=[
        ("Country", "@ADMIN"), ("Coverage", "@data%")
    ])

p.grid.grid_line_color = None
p.hover.point_policy = "follow_mouse"

p.patches('xs', 'ys', fill_color={'field': 'data', 'transform': mapper}, fill_alpha='alpha', source=geo_data, line_width=0.5, line_color="white")
cbar = ColorBar(color_mapper=mapper,
                     ticker=BasicTicker(desired_num_ticks=10),
                     formatter=PrintfTickFormatter(format="%d%%"),
                     label_standoff=6, border_line_color=None,location=(0,0))
p.add_layout(cbar, "right")
show(p)

