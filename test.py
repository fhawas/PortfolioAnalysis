# -*- coding: utf-8 -*-
"""
Created on Thu Oct  7 17:41:20 2021

@author: Francisco
"""

import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px

click = st.button('Run')
data_file = st.file_uploader('Upload File', type="xlsx")

if click:
    index_data = pd.read_excel(data_file,sheet_name='Index')
    portfolio_data = pd.read_excel(data_file,sheet_name='Portfolio')
    log_index = np.log(index_data.loc[:,index_data.columns != 'Fecha'].values.T)
    portfolio = portfolio_data.values
    return_index = log_index[:,1:] - log_index[:,:-1]
    cov_matrix = np.cov(return_index)*30
    variance = np.matmul(portfolio,np.matmul(cov_matrix,portfolio.T))
    std = variance**.5
    variance_decomposition = portfolio.T*np.matmul(cov_matrix,portfolio.T)
    variance_decomposition_percentage = variance_decomposition/variance
    
    data = {'Index':portfolio_data.columns,'RiskShare':np.squeeze(variance_decomposition_percentage)*100}
    data = pd.DataFrame(data)
    fig = px.bar(data[data['RiskShare']!=0], x='Index', y='RiskShare')
    st.plotly_chart(fig)
    st.write('Monthly Standard Deviation: '+str(np.round(std[0][0]*100,2)))
    #st.table(data['RiskShare'].sum())