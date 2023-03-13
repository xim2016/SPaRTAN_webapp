
import streamlit as st
from PIL import Image
from streamlit_option_menu import option_menu

from correlation_page import correlation_page
from data_page import data_page
from TF_page import TF_page
# from utils import set_page_container_style

from pathlib import Path
Image.MAX_IMAGE_PIXELS = None



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
    