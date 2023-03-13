
import streamlit as st
from PIL import Image
from streamlit_option_menu import option_menu

from correlation_page import correlation_page
from data_page import data_page
from TF_page import TF_page
# from utils import set_page_container_style

from pathlib import Path
Image.MAX_IMAGE_PIXELS = None

def set_page_container_style(prcnt_width: int = 75):
    max_width_str = f"max-width: {prcnt_width}%;"
    st.markdown(f"""
                <style> 
                
                .appview-container .main .block-container{{{max_width_str}}}
                </style>    
                """,
                unsafe_allow_html=True,
                )


page_style = """
        <style>
        #MainMenu {visibility: hidden;}  
        footer  {visibility: hidden;}  
        div.css-1vq4p4l.e1fqkh3o4{padding: 2rem 1rem 1.5rem;}
        div.block-container{padding-top:3rem;}
        </style>
        """

# st.write('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)
# st.write('<style>div.css-1vq4p4l.e1fqkh3o4{padding: 4rem 1rem 1.5rem;}</style>', unsafe_allow_html=True)



set_page_container_style(75)

mainTitle2idx = {"Data overview": 0,
                 "TF activity analysis": 1,
                 "Protein-TF Correlation": 2
                 }



def main_page(orisetting, cleanedsetting):

    pages = {
        "Data overview": data_page,
        "TF activity analysis": TF_page,
        "Protein-TF Correlation":correlation_page
    }

    path_data = Path(f"./data/{cleanedsetting}") 
    # st.write(str(path_data))
    with st.sidebar:
        default_value = st.session_state["main"] if "main" in st.session_state else 0
        # print( "main" in st.session_state)
        choose2 = option_menu(orisetting, ["Data overview", "TF activity analysis", "Protein-TF Correlation"],
                            icons=['clipboard-data',
                                    'lightning-charge', 'bar-chart-line'],
                            menu_icon="arrow-return-right", default_index=default_value,
                            styles={
            "container": {"padding": "5!important", "background-color": "#fafafa"},
            "icon": {"color": "orange", "font-size": "18px"},
            "nav-link": {"font-size": "14px", "text-align": "left", "margin": "0px", "--hover-color": "#eee"},
            "nav-link-selected": {"background-color": "orange"},
        }
        )



    # if choose2 == "Protein-TF Correlation":
        
    #     correlation_page(path_data)

    # elif choose2 == "TF Analyses":
        
    #     TF_page(path_data)
    # elif choose2 == "Data Info":
        
    #     data_page(path_data)

    pages[choose2](path_data)
   
    value = mainTitle2idx[choose2]
    st.session_state["main"] = value
    