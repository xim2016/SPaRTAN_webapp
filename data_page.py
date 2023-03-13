from pathlib import Path
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
from utils import hide_table_index, hide_dataframe_index
import os
from PIL import Image




# def show_pdf(file_path):
#     with open(file_path,"rb") as f:
#         base64_pdf = base64.b64encode(f.read()).decode('utf-8')
#     pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="950" height="800" type="application/pdf"></iframe>'
#     st.markdown(pdf_display, unsafe_allow_html=True)


page_style = """
        <style>
        #MainMenu {visibility: hidden;}  
        footer  {visibility: hidden;}  
        div.css-1vq4p4l.e1fqkh3o4{padding: 2rem 1rem 1.5rem;}
        div.block-container{padding-top:3rem;}
        </style>
        """


# set_page_container_style(75)


path = "./data"
protein_names = pd.read_csv(Path(path)/"protein_names.csv", index_col=0).T
celltype_names = pd.read_csv(Path(path)/"celltype_names.csv", index_col=0).T
dataset_info = pd.read_csv(Path(path)/"donor_info.csv", index_col=0)

cell_count = pd.read_csv(Path(path)/"cell_count.csv")
cell_count.index.name = None



def data_page(path_data):

    spartan_data = pd.read_csv(
        Path(path_data)/"celltype_info.csv", index_col=0)

    spartan_data.dropna(inplace=True)
    # if "RNArate" in spartan_data.columns:
    #     spartan_data['RNArate'] = spartan_data['RNArate'] .round(
    #         decimals=1).astype(object)
    

    selected = option_menu(None, ["Overview",  "SPaRTAN data"],
                           icons=["clipboard", "clipboard-plus"],
                           menu_icon="cast", default_index=0, orientation="horizontal",
                           styles={
        "container": {"padding": "5!important", "background-color": "#eee"},
        "icon": {"color": "orange", "font-size": "22px"},
        "nav-link": {"font-size": "18px", "text-align": "center", "margin": "0px", "--hover-color": "#fafafa"},
        "nav-link-selected": {"background-color": "#FD5816"},
        # "separator":"."
    })

    if selected == "Overview":

        hide_dataframe_index()
        # st.write("Donors (4):")
        st.markdown('''###### Donors (4):''')
        st.dataframe(dataset_info)

        hide_table_index()
        # st.write("Cell types (24):")
        st.markdown('''###### Cell types (24):''')
        st.table(celltype_names)

        # write_text("Proteins (52):", fontsize=10)
        # st.write("")
        st.markdown('''###### Proteins (52):''')
        st.table(protein_names)

        # show_dataframe_index()
        st.markdown('''###### Cell count:''')
        st.table(cell_count)

    elif selected == "SPaRTAN data":
        # st.info("SPaRTAN moodule was trained on dataset per donor per cell type. We selected genes by intersecting genes in TF-target gene prior matrix and filtered the genes that have to be expressed in 30\% cells in all donors in a single cell type. Not every cell type has cells(or enough cells) for every donor to run SPaRTAN module. We specify each module dataset has minimal 50 cells")

        st.dataframe(spartan_data.style.format(
            {'RNArate': '{:.2f}', 'Number of genes': '{:.0f}', 'Number of TFs': '{:.0f}', 'Number of proteins': '{:.0f}' }), use_container_width=True)
        # from st_aggrid import AgGrid
        # AgGrid(spartan_data, height=500, fit_columns_on_grid_load=True)
