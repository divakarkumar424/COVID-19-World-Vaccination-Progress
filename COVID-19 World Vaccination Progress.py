#!/usr/bin/env python
# coding: utf-8

# # Working on Real Project with python
# 

# # 💉COVID-19 World Vaccination Progress Dataset
# 

# # Introduction  

# <img src="Covid-19-Vaccine-development-e1599531596297.jpg"/>

# 
# 
# ***The data contains the following information:***
# 
# **Country:**
# this is the country for which the vaccination information is provided.

# **Country ISO Code:** 
# ISO code for the country.
# 
# **Date:**
# date for the data entry; for some of the dates we have only the daily vaccinations, for others, only the (cumulative) total.
# 
# **Total number of vaccinations:**
# this is the absolute number of total immunizations in the country.
# 
# **Total number of people vaccinated:**
# a person, depending on the immunization scheme, will receive one or more (typically 2) vaccines; at a certain moment, the number of vaccination might be larger than the number of people.
# 
# **Total number of people fully vaccinated:**
# this is the number of people that received the entire set of immunization according to the immunization scheme (typically 2); at a certain moment in time, there might be a certain number of people that received one vaccine and another number (smaller) of people that received all vaccines in the scheme.
# 
# **Daily vaccinations (raw):**
# for a certain data entry, the number of vaccination for that date/country.
# 
# **Daily vaccinations:**
# for a certain data entry, the number of vaccination for that date/country.
# 
# **Total vaccinations per hundred:**
# ratio (in percent) between vaccination number and total population up to the date in the country.
# 
# **Total number of people vaccinated per hundred:**
# ratio (in percent) between population immunized and total population up to the date in the country.
# 
# **Total number of people fully vaccinated per hundred:**
# ratio (in percent) between population fully immunized and total population up to the date in the country.
# 
# **Number of vaccinations per day:**
# number of daily vaccination for that day and country.
# 
# **Daily vaccinations per million:**
# ratio (in ppm) between vaccination number and total population for the current date in the country.
# 
# **Vaccines used in the country:**
# total number of vaccines used in the country (up to date).
# 
# **Source name:**
# source of the information (national authority, international organization, local organization etc.).
# 
# **Source website:**
# website of the source of information.
# 

# # Content 
# 
# **Daily Vaccinations Per Million according to countries**
# 
# **No of people fully vaccinated according to countries**
# 
# **No of people daily vaccination according bto countries**
# 
# **Number of Countries each vaccine is being used**
# 
# **Vaccines used by specefic Country**
# 
# **Total Vaccinations per country grouped by Vaccines**
# 
# 
# ***line Graph***
# ***Bar Graph***
# ***Treemaps***
# ***Map***
# 

# In[4]:


import pandas as pd
import numpy as np
import plotly.express as px
from plotly.offline import download_plotlyjs,init_notebook_mode,plot,iplot
import plotly.graph_objects as go
import plotly.figure_factory as ff
from plotly.colors import n_colors
from wordcloud import WordCloud,ImageColorGenerator
init_notebook_mode(connected=True)
from plotly.subplots import make_subplots
get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt
import warnings
warnings.simplefilter("ignore")


# In[5]:


data = pd.read_csv(r"C:\Users\PC-1\Desktop\nano\Data Analytics\Data\archive_2\country_vaccinations.csv")


# In[6]:


data


# # Data Cleaning 
# 

# In[7]:


new_data = data.fillna({
    'iso_code':'NA',
    'total_vaccinations':0,
    'people_vaccinated':0,
    'people_fully_vaccinated':0,
    'daily_vaccinations_raw':0,
    'daily_vaccinations':0,
    'total_vaccinations_per_hundred':0,
    'people_vaccinated_per_hundred':0,
    'people_fully_vaccinated_per_hundred':0,
    'daily_vaccinations_per_million':0  
})
new_data


# In[33]:


px.line(new_data,y='daily_vaccinations_per_million',x=new_data['date'],color='country', title='Daily Vaccinations Per Million according to countries')


# In[8]:


px.line(new_data,y='people_fully_vaccinated',x=new_data['date'],color='country', title='No of people fully vaccinated according to countries')


# In[9]:


px.line(new_data,y='daily_vaccinations_raw',x=new_data['date'],color='country', title='No of people daily vaccination according to countries')


# In[12]:


new_data.shape


# In[13]:


new_data.index


# In[14]:


new_data.columns


# In[15]:


new_data.dtypes


# # .count
# It shows the total no.of non-null values in each column.
# It can be applied on a single columns as well as on whole dataframe.

# In[16]:


new_data.count()


# In[17]:


new_df = new_data.groupby(["country",'iso_code','vaccines'])['total_vaccinations','people_vaccinated','people_fully_vaccinated',
                                           'daily_vaccinations','total_vaccinations_per_hundred','people_vaccinated_per_hundred',
                                           "people_fully_vaccinated_per_hundred",'daily_vaccinations_per_million'].max().reset_index()
new_df.head()


# # Vaccines

# In[18]:


new_df['vaccines'].unique()


# In[19]:


new_df.nunique()


# # Vaccines used by specefic Country

# In[20]:


vacc = new_df["vaccines"].unique()
for i in vacc:
    c = list(new_df[new_df["vaccines"] == i]['country'])
    print(f"Vaccine: {i}\nUsed countries: {c}")
    print('-'*70)


# In[21]:


vaccine = new_df["vaccines"].value_counts().reset_index()
vaccine.columns = ['Vaccines','Number of Country']
vaccine


# In[23]:


fig = px.bar(vaccine,x='Vaccines',y='Number of Country',hover_data = '',title = 'Number of Countries each vaccine is being used')
fig.show()


# In[24]:


fig = px.choropleth(new_df,locations = 'country',locationmode = 'country names',color = 'vaccines',
                   title = 'Vaccines used by specefic Country',hover_data= ['total_vaccinations'])
fig.show()


# In[25]:


data = new_df[['country','total_vaccinations']].nlargest(30,'total_vaccinations')
fig = px.bar(data, x = 'country',y = 'total_vaccinations',title="Number of total vaccinations according to countries",)
fig.show()


# In[26]:


data = new_df[['country','people_vaccinated']].nlargest(30,'people_vaccinated')
fig = px.bar(data, x = 'country',y = 'people_vaccinated',title="Number of people vaccinated according to countries",)
fig.show()


# In[27]:


data = new_df[['country','daily_vaccinations']].nlargest(30,'daily_vaccinations')
fig = px.bar(data, x = 'country',y = 'daily_vaccinations',title="Number of people vaccinated daily according to countries",)
fig.show()


# In[28]:


data = new_df[['country','people_vaccinated_per_hundred']].nlargest(40,'people_vaccinated_per_hundred')
fig = px.bar(data, x = 'country',y = 'people_vaccinated_per_hundred',title="Highest Number of people vaccinated per hundred according to Countries")
fig.show()


# In[29]:


fig = px.treemap(new_df,names = 'country',values = 'total_vaccinations',path = ['vaccines','country'],
                 title="Total Vaccinations per country grouped by Vaccines",
                 color_discrete_sequence =px.colors.qualitative.Set2)
fig.show()


# In[30]:


my_data=new_df[['country','total_vaccinations','people_vaccinated','people_fully_vaccinated','vaccines','iso_code']].groupby(by=['country','iso_code','vaccines']).sum().reset_index()


# In[31]:


my_data.head(60)


# **The END**

# In[ ]:




