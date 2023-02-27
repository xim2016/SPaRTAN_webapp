
import streamlit as st

from streamlit_option_menu import option_menu

from main_page import main_page

from register_load_widget_state import  load_widget_state

# Image.MAX_IMAGE_PIXELS = None

# from utils import set_page_container_style
# def set_page_container_style(prcnt_width: int = 75):
max_width_str = f"max-width: 75%;"
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



# set_page_container_style(75)


with st.sidebar:
    choose1 = option_menu("Testing set", ["CLR1norm_Denoised","CLR1norm_Raw",  "CLR2norm_Raw"],
                         icons=['clipboard-data',
                                'clipboard-data',
                                'lightning-charge'],
                         menu_icon="app-indicator", default_index=0,
                         styles={
        "container": {"padding": "5!important", "background-color": "#fafafa"},
        "icon": {"color": "orange", "font-size": "22px"},
        "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "#02ab21"},
    }
    )
cleaned_setting = choose1.replace(" ","_")
load_widget_state()
main_page(choose1, cleaned_setting)
# if choose1 == "Setting_0":

#     main_page(choose1)

# elif choose1 == "Setting 1":

#     main_page(choose1)

# elif choose1 == "CLR2norm":

#     main_page(choose1)
