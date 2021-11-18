import streamlit as st
import time
import pandas as pd
import numpy as np
import requests
import json
import nltk
# nltk.download('punkt')
import time
import requests
import math
import re
import gg_search_norank
import gdown

if "URL" not in st.session_state:
    st.session_state.URL = ""
if "response" not in st.session_state:
    st.session_state.response = ""


def download_url(URL):
    if "<Response [200]>" not in str(st.session_state.response) or URL == "":    
        gdown.download(id="1-HFzqcNs7oDJaR9moNyzqom88hg4m3AT", output="C:/Users/ASUS/Desktop/Mooc_Project/demo/Web_App_nghia/url.json")        
        with open("C:/Users/ASUS/Desktop/Mooc_Project/demo/Web_App_nghia/url.json", "r") as bf:
            URL_json = json.load(bf)
            URL = URL_json["url"]
    else: 
        URL = URL
    return URL







st.title('Question Answering Demo')
menu = ['Close domain', 'Open domain', 'Open domain ranking']
model = ['Model 74%', 'Model 78%']
choice = st.sidebar.selectbox('Choose demo type', menu, 0)
choice_model = st.sidebar.selectbox('Choose model', model, 0)
if choice:
		st.write("Your choose option is" + " " + choice)
if choice == "Close domain":
    questions = st.text_input('Question')
    contexts = st.text_area('Context',  height=50)
    button = st.button('Submit')
    if button:
        if not questions:
            st.warning("Please fill out so required question field !")
        elif not contexts:
            st.warning("Please fill out so required context field !")
        else:
            model = ''
            if choice_model=='Model 74%':
                model = 'hieu-close'
            else:
                model = 'binh-close'
            myobj = {'question': str(questions),'context':str(contexts), 'model': model}
            
            try:
                st.session_state.URL = download_url(st.session_state.URL)
                url_1 = st.session_state.URL +'/closedomain'
                my_bar = st.progress(0)
                response = requests.post(url_1, json=myobj)
                print(response)
                st.session_state.response = response
                if response.ok:
                    # print(response.ok)
                    rs = response.json()
                    # print(rs['answer'])
                    for percent_complete in range(100):
                        time.sleep(0)
                        my_bar.progress(percent_complete + 1)
                    if rs['score'] > 0.5:
                        st.success(str("Answer: "+rs['answer']))
                        st.success(str("Score: ")+str(round(rs['score'],3)))
                        st.success(str("Time predict: ")+str(round(rs['total_time'], 2))+str("s"))
                    else:
                        st.warning("Not Answer")
                
            except AssertionError as error:
                st.subheader('Error Connect to Server.')
                print(error)
elif choice == 'Open domain':
    # st.subheader("ĐANG BẢO TRÌ Ạ")
    container = st.container()
    questions_ = st.text_input('Question')
    button = st.button('Submit')
    if button:
        if not questions_:
            st.warning("Please fill out so required question field !")
        else:
            container.subheader("Google search context with 5 link web:")
            token_query = gg_search_norank.tokenize(questions_)[0]
            # print("a",token_query)
            keywords = gg_search_norank.keywords_extraction(token_query)
            # start = time.time()
            li, urls = gg_search_norank.reurl_li(questions_, keywords)
            # print(time.time()-start)
            b = gg_search_norank.reb(li)

            result = {}
            max = 0
            for i,item_b in enumerate(b):
                contexts_ = item_b.replace('_',' ')
                if contexts_:
                    container.write("URL {}: ".format(i + 1)+ urls[i])
                    container.text_area("Context {}:".format(i + 1),contexts_)
                else:
                    container.write("URL {}: ".format(i + 1)+ urls[i])
                    container.warning("Please fill out so required context {} field !".format(i+1))
            model = ''
            if choice_model=='Model 74%':
                model = 'hieu-open'
            else:
                model = 'binh-open'

            myobj = {'question': questions_, 'model': model}  
            # print(myobj)
            try:
                st.session_state.URL = download_url(st.session_state.URL)
                url_2 = st.session_state.URL + '/opendomain'
                response = requests.post(url_2, json=myobj)
                print(response)
                st.session_state.response = response
                if response.ok:
                    rs = response.json()
                    st.success(str("Final Answer: "+rs['answer']) + str(" ----- Score: ")+str(round(rs['score'],3)) + str(" ----- Time predict: ")+str(round(rs['total_time'], 2))+str("s"))
            except AssertionError as error:
                st.subheader('Error Connect to Server.')
                print(error)
           

elif choice == 'Open domain ranking':
    container = st.container()
    container.write("link và ranking nằm ở đây")
    questions_ = st.text_input('Question')
    button = st.button('Submit')
    if button:
        model = ''
        if choice_model=='Model 74%':
            model = 'hieu-open'
        else:
            model = 'binh-open'
        myobj = {'question': str(questions_)}        
        try:
            st.session_state.URL = download_url(st.session_state.URL)
            url_3 = st.session_state.URL +'/opendomainranking'
            response = requests.post(url_3, json=myobj)
            print(response)
            st.session_state.response = response
            if response.ok:
                rs = response.json()
                print(rs)
                st.success(str("Final Answer: "+rs['answer']) + str(" ----- Score: ")+str(round(rs['score'],3)) + str(" ----- Time predict: ")+str(round(rs['total_time'], 2))+str("s"))
        except AssertionError as error:
            st.subheader('Error Connect to Server.')
            print(error)
