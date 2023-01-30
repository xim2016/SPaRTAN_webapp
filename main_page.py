
import streamlit as st
from PIL import Image
from streamlit_option_menu import option_menu

from correlation_page import correlation_page
from data_page import data_page
from TF_page import TF_page

from pathlib import Path
Image.MAX_IMAGE_PIXELS = None

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


def set_page_container_style(prcnt_width: int = 75):
    max_width_str = f"max-width: {prcnt_width}%;"
    st.markdown(page_style, unsafe_allow_html=True)
    st.markdown(f"""
                <style> 
                
                .appview-container .main .block-container{{{max_width_str}}}
                </style>    
                """,
                unsafe_allow_html=True,
                )


set_page_container_style(75)

def main_page(setting=1):

    path_data = Path(f"./data/set{setting}") 

    with st.sidebar:
        choose = option_menu(f"Setting{setting}", ["Data Info", "TF Analyses", "Protein-TF Correlation"],
                            icons=['clipboard-data',
                                    'lightning-charge', 'bar-chart-line'],
                            menu_icon="arrow-return-right", default_index=0,
                            styles={
            "container": {"padding": "5!important", "background-color": "#fafafa"},
            "icon": {"color": "orange", "font-size": "18px"},
            "nav-link": {"font-size": "14px", "text-align": "left", "margin": "0px", "--hover-color": "#eee"},
            "nav-link-selected": {"background-color": "orange"},
        }
        )

    if choose == "Protein-TF Correlation":
        a=1
        correlation_page(path_data)

    elif choose == "TF Analyses":
        a=1
        TF_page(path_data)
    elif choose == "Data Info":
        a=1
        data_page(path_data)
