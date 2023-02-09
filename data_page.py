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



path = "./data"
protein_names = pd.read_csv(Path(path)/"protein_names.csv", index_col=0).T
celltype_names = pd.read_csv(Path(path)/"celltype_names.csv", index_col=0).T
dataset_info = pd.read_csv(Path(path)/"dataset_info.csv", index_col=0)

cell_count = pd.read_csv( Path(path)/"cell_count.csv")
cell_count.index.name = None

# get the gene names of mRNA violin plot
path_mRNA = ("./data/mRNA_data/violinPlot")

gene_list = [x.split(".")[0][11:] for x in os.listdir(path_mRNA)]

def data_page(path_data):
    
    spartan_data = pd.read_csv(
    Path(path_data)/"celltype_info.csv", index_col=0)
    spartan_data.dropna(inplace=True)
    if "RNArate" in spartan_data.columns:
        spartan_data['RNArate'] = spartan_data['RNArate'] .round(decimals=1).astype(object)
        
    # spartan_data.iloc[:,1:] = spartan_data.iloc[:,1:].astype(int)



    selected = option_menu(None, ["Overview", "Protein", "mRNA", "SPaRTAN data"],
                           icons=["clipboard", "hdd-fill", "hdd-stack", "clipboard-plus"],
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

    elif selected == "Protein":

        selected_sub = option_menu(None, ["by Protein", "by Patient"],
                        #    icons=["clipboard", "hdd-fill", "hdd-stack", "clipboard-plus"],
                           menu_icon="cast", default_index=0, orientation="horizontal",
                           styles={
        "container": {"padding": "5!important", "background-color": "#eee"},
        # "icon": {"color": "orange", "font-size": "14px"},
        "nav-link": {"font-size": "18px", "text-align": "center", "margin": "0px", "--hover-color": "#fafafa"},
        "nav-link-selected": {"background-color": "#80adcc"},
        # "separator":"."
                            }
                        )
        #858d83
        if selected_sub == "by Protein":
       
            path_ADT = Path("./data/ADT_data/violinPlot")
            c1,c2 = st.columns(2)
            pro_selected = c1.selectbox(
                    'Protein',
                    list(protein_names.loc['x',:]),
                    0
                )

            imgfile = str(path_ADT / f"ViolinPlot_CLR2_{pro_selected}.TotalSeqC.png"
                )
            
            st.image(imgfile)

        elif selected_sub == "by Patient":
       
            path_ADT = Path("./data/ADT_data/heatmap")
            # c3,c4 = st.columns(2)
            pat_selected = st.selectbox(
                    'Patient',
                    dataset_info.index.tolist(),
                    0
                )

            imgfile = str(path_ADT / f"{pat_selected} CLR margin=2 ADT mean.png"
                )
            
            st.image(imgfile)


    elif selected == "mRNA":

        selected_sub2 = option_menu(None, ["Violin plot", "Heatmap"],
                        #    icons=["clipboard", "hdd-fill", "hdd-stack", "clipboard-plus"],
                           menu_icon="cast", default_index=0, orientation="horizontal",
                           styles={
        "container": {"padding": "5!important", "background-color": "#eee"},
        # "icon": {"color": "orange", "font-size": "14px"},
        "nav-link": {"font-size": "18px", "text-align": "center", "margin": "0px", "--hover-color": "#fafafa"},
        "nav-link-selected": {"background-color": "#80adcc"},
        # "separator":"."
                            }
                        )
        #858d83
        if selected_sub2 == "Violin plot":
       
            path_gene = Path("./data/mRNA_data/violinPlot")
            c1,c2 = st.columns(2)
            gene_selected = c1.selectbox(
                    'Gene',
                    gene_list,
                    0
                )

            imgfile = str(path_gene / f"ViolinPlot_{gene_selected}.png"
                )
            
            st.image(imgfile)
        elif selected_sub2 == "Heatmap":
            path_plot = Path("./data/mRNA_data/heatmap")

            c3,c4 = st.columns(2)
            list3 = ["Cytoskeleton",  "CytokineReceptor", "IRFGene","InterestingGene","ImmuneGene","ImmuneCheckpoint"]
            list4 = ["AllCellType", "ImmuneCellType", "NonImmuneCellType"]
            sel_3 = c3.selectbox(
                    'Gene type',
                    list3,
                    0
                ) 
            sel_4 = c4.selectbox(
                    'Cell type',
                    list4,
                    0
                )
            
            imgfile = str(path_plot / f"OutComplexHeatmap_Mesothelioma_{sel_3}_{sel_4}_SCTNormalExp_Reorder.pdf")

            # image = Image.open(imgfile)
            # show_pdf(imgfile) 
            # st.image(image)

    elif selected == "SPaRTAN data":
        # st.info("SPaRTAN moodule was trained on dataset per donor per cell type. We selected genes by intersecting genes in TF-target gene prior matrix and filtered the genes that have to be expressed in 30\% cells in all donors in a single cell type. Not every cell type has cells(or enough cells) for every donor to run SPaRTAN module. We specify each module dataset has minimal 50 cells")

        st.dataframe(spartan_data.style.format({'RNArate': '{:.1f}'}), use_container_width=True)
        # from st_aggrid import AgGrid
        # AgGrid(spartan_data, height=500, fit_columns_on_grid_load=True)