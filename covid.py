#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime


# In[2]:


covid_df=pd.read_csv("covid_19_india.csv")


# In[3]:


covid_df.head(10)


# In[4]:


covid_df.info()


# In[5]:


covid_df.describe()


# In[7]:


vaccine_df=pd.read_csv("covid_vaccine_statewise.csv")


# In[8]:


vaccine_df.head(7)


# In[9]:


covid_df.drop(["Sno","Time" ,"ConfirmedIndianNational", "ConfirmedForeignNational"], inplace=True ,axis=1)


# In[10]:


covid_df.head()


# In[11]:


covid_df['Date']=pd.to_datetime(covid_df['Date'], format= '%Y-%m-%d')


# In[12]:


covid_df.head()


# In[19]:


#Active cases

covid_df['Active_cases']=covid_df['Confirmed']-(covid_df['Cured'] + covid_df['Deaths'])
covid_df.head()


# In[21]:


statewise=pd.pivot_table(covid_df , values=["Confirmed", "Deaths", "Cured"], index="State/UnionTerritory",aggfunc=max)


# In[22]:


statewise["Recovery Rate"]=statewise["Cured"]*100/statewise["Confirmed"]


# In[23]:


statewise["Mortality Rate"]=statewise["Deaths"]*100/statewise["Confirmed"]


# In[24]:


statewise=statewise.sort_values(by="Confirmed",ascending=False)


# In[26]:


statewise.style.background_gradient(cmap="cubehelix")


# In[27]:


#Top10 active cases states

top_10_active_cases=covid_df.groupby(by ='State/UnionTerritory').max()[['Active_Cases', 'Date']].sort_values(by=['Active_Cases'],ascending=False).reset_index()


# In[28]:


fig=plt.figure(figsize=(16,9))


# In[29]:


plt.title("Top 10 states with most active cases in India",size=25)


# In[33]:


ax=sns.barplot(data=top_10_active_cases.iloc[:10],y= "Active_Cases", x="State/UnionTerritory", linewidth=2, edgecolor='pink')
            


# In[35]:


#Complete code for top 10 active cases
top_10_active_cases=covid_df.groupby(by ='State/UnionTerritory').max()[['Active_Cases', 'Date']].sort_values(by=['Active_Cases'],ascending=False).reset_index()
fig=plt.figure(figsize=(16,9))
plt.title("Top 10 states with most active cases in India",size=25)
ax=sns.barplot(data=top_10_active_cases.iloc[:10],y= "Active_Cases", x="State/UnionTerritory", linewidth=2, edgecolor='pink')
            
plt.xlabel("States")
plt.ylabel("Total Active Cases")
plt.show


# In[36]:


#Top states with highest deaths
top_10_deaths=covid_df.groupby(by ='State/UnionTerritory').max()[['Deaths', 'Date']].sort_values(by=['Deaths'],ascending=False).reset_index()
fig=plt.figure(figsize=(18,5))
plt.title("Top 10 states with most deaths cases in India",size=25)
ax=sns.barplot(data=top_10_deaths.iloc[:12],y= "Deaths", x="State/UnionTerritory", linewidth=2, edgecolor='purple')
            
plt.xlabel("States")
plt.ylabel("Total Death Cases")
plt.show


# In[51]:


#Growth thrend
fig=plt.figure(figsize=(12,6))

ax = sns.lineplot(covid_df[covid_df['State/UnionTerritory'].isin(['Maharashtra', 'Karnataka', 'Tamil Nadu', 'Delhi', 'Uttar Pradesh'])], x = 'Date', y= 'Active_cases', hue = 'State/UnionTerritory')
plt.title("Top 5 affected states in India", size = 16)
plt.xlabel("Date")
plt.ylabel("Active_cases")
plt.show()


# In[53]:


vaccine_df.rename(columns={'Updated On': 'Vaccine_Date'},inplace=True)


# In[54]:


vaccine_df.head(10)


# In[55]:


vaccine_df.info()


# In[56]:


vaccine_df.isnull().sum()


# In[64]:


vaccination=vaccine_df.drop(columns=['Sputnik V (Doses Administered)','AEFI','18-44 Years (Doses Administered)','45-60 Years (Doses Administered)','60+ Years (Doses Administered)'],axis=1)


# In[65]:


vaccination.head()


# In[71]:


males = vaccination['Male (Doses Administered)'].sum() 
females = vaccination['Female (Doses Administered)'].sum()
#Males vs Females vaccinated
px.pie(names = ['males', 'females'], values = [males, females], title = 'Males vs Females vaccinated')


# In[76]:


#Removing Invalid State
vaccine = vaccine_df[vaccine_df['State'] != 'India']
vaccine


# In[77]:


vaccine.rename(columns={'Total Individuals Vaccinated':'Total'}, inplace=True)
vaccine.head()


# In[78]:


#Most vaccinated state
max_vac=vaccine.groupby('State')['Total'].sum().to_frame('Total')
max_vac=max_vac.sort_values('Total',ascending=False)[:5]
max_vac


# In[81]:


#Top 5 vaccinated states in India

fig = plt.figure(figsize = (10,5))
plt.title("Top 5 vaccinated states in India", size = 25)
x = sns.barplot(data=max_vac.iloc[:10], x = max_vac.index, y = max_vac.Total, linewidth = 2, edgecolor = 'red')
plt.xlabel("States")
plt.ylabel("Total Vaccination")
plt.show()


# In[ ]:




