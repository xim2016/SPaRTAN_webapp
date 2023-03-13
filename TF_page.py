import random
from pathlib import Path

import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu

from utils import convert_df_to_csv, img2buf, load_data, violin_plot
from register_load_widget_state import  persist



my_theme = {'txc_inactive': 'black', 'menu_background': 'white',
            'txc_active': 'white', 'option_active': 'blue'}


def TF_page(path_data):

    # prepare data
    files = (path_data / "TFrank/within_celltype").iterdir()
    files = [i.name.replace('TFrank_samples_', '') for i in files]
    files = list(filter(lambda x: x != "figure", files))
    celltypeAll = list([i[:-4] for i in files])

    # celltype_list_ordered = pd.read_csv(path_data/"celltype_list_ordered.csv")
    # group_order_type = list(celltype_list_ordered["Cell_type"].str.replace(" ", "."))

    @st.cache
    def load_rootdata(path_data):
        fname = str(
            path_data / "celltype_info.csv")
        df_info = pd.read_csv(fname, index_col=0)
        fname = str(path_data / "TFrank_all_celltypeAll_samples.csv")
        # df_ranks = pd.read_csv(fname)
        df_ranks_all = pd.read_parquet(path_data/"TFranks_all.parquet.gzip")
        return ((df_info, df_ranks_all))


    cached_data = load_rootdata(path_data)
    df_info = cached_data[0]
    df_ranks_all = cached_data[1]
    tfall = df_ranks_all.columns[:-2]

    type2ds = {}
    for type in list(df_info.index):
        snames = df_info.loc[type, "Donors"]
        if pd.isna(snames):
            continue
        snames = [x.strip() for x in snames.split(',')]
        type2ds[type] = snames


   
    # start menu options
    selected = option_menu(None, ["Analysis by TFs (across all cell-types)", "Analysis by TFs (cell-type specific view)", "Analysis by cell-type"],
                        #    icons=["bi bi-grid-3x3", "bi bi-align-end",
                        #           "bi bi-align-bottom"],
                           menu_icon="cast", default_index=0, orientation="horizontal",
                           styles={
        "container": {"padding": "20!important", "background-color": "#eee"},
        "icon": {"color": "orange", "font-size": "18px"},
        "nav-link": {"font-size": "16px", "text-align": "center", "margin": "0px", "--hover-color": "#fafafa"},
        "nav-link-selected": {"background-color": "#FD5816"},
        "separator": "A"
    })

    datafile = ""
    # if selected == 'TF ranks overview':

    #     st.info('The heatmap shows the sample mean of TF ranks for every TF and every cell type. TFs that rank lower than 0.5(50\%) in all cell types have been removed.')

    #     imgfile = str(
    #         path_data / "TFrank/mean/figure/heatmap_TFrank_celltypeMean_cutoff0.5.png")
    #     imgfile_out = "heatmap_TFrank_celltypeMean.png"

    #     # _, c_img, _ = st.columns([1,100,1])
    #     st.image(imgfile)
    #     datafile = str(path_data / "TFrank/mean/TFrank_celltypeMean.csv")
    #     datafile_out = "TFrank_celltypeMean.csv"

    if selected == 'Analysis by TFs (across all cell-types)':
        st.info('For each TF, violin plot shows its ranks across cell types. You can select multiple TFs of your interest from TFs list for comparison.')
        # violin plot for selected TFs]]    
        # defaults = st.session_state['1_tf'] if "1_tf" in st.session_state and set(st.session_state['1_tf']).issubset(set(tfall)) and len(set(st.session_state['1_tf']))>0 else [tfall[0]]
    
        if "tfpage_tab1_tf" in st.session_state:
            if not set(st.session_state.tfpage_tab1_tf).issubset(set(tfall)): 
                 st.session_state.tfpage_tab1_tf = list(set(st.session_state.tfpage_tab1_tf) & set(tfall))

        TFs_selected = st.multiselect('TFs', tfall,  default=tfall[0], key=persist("tfpage_tab1_tf"))
        for tf in TFs_selected:
            df_ranks = df_ranks_all.loc[:, [tf, "Celltype","Donor"]]
            patients = sorted(set(df_ranks["Donor"]))
            for p in patients:
                df_ranks_p = df_ranks.loc[df_ranks['Donor']==p,]
                fig = violin_plot(tf + " of " + p, df_ranks_p, "Celltype",tf, 25, 4)
                st.pyplot(fig)


        s_TFs = "_".join(TFs_selected)
        s_TFs if len(s_TFs) <= 100 else s_TFs[:100]
        datafile_out = f"TFranks--{s_TFs}.csv"


        df_data = df_ranks_all[['Celltype', 'Donor'] + TFs_selected]

        c_checkbox, _, c_dwdata = st.columns([3, 9, 3])
        cb = c_checkbox.checkbox("Show data", key="TFrank")


        btn_data = c_dwdata.download_button(
            label='📩 '+"Download Data",
            data=convert_df_to_csv(df_data),
            file_name=datafile_out,
            mime="text/csv",
            key='download-csv',
            disabled=not cb
        )

        if cb:
            st.dataframe(df_data.style.format(precision=0), use_container_width=True)

        
    elif selected == 'Analysis by cell-type':

        st.info('For each cell type, check the similarity and difference among samples of each TF rank. Cell types that have only one sample are not included in the dropdown list')

        s_celltype = st.selectbox(f'Cell types ({len(celltypeAll)})', celltypeAll,  key=persist("tfpage_tab2_type"),   
                                  format_func=lambda x: x + " (Num of donors: " + str(len(type2ds[x])) + ")")

       
        imgfile = str(
            path_data / f"TFrank/within_celltype/figure/heatmap_TFrank_samples_{s_celltype}.png")
        imgfile_out = f"heatmap_TFrank_within_{s_celltype}.png"

        
        st.image(imgfile)

        datafile = str(
            path_data / f"TFrank/within_celltype/TFrank_samples_{s_celltype}.csv")
        datafile_out = f"TFranks_within_{s_celltype}.csv"

        
        df_data = load_data(datafile)

        c_checkbox, _, c_dwdata, c_dwimg = st.columns([3, 5, 3, 3])

        cb = c_checkbox.checkbox("Show data", key=imgfile)

        btn_img = c_dwimg.download_button(
            label='📥 '+"Download Image",
            data=img2buf(imgfile),
            file_name=imgfile_out
        )

        btn_data = c_dwdata.download_button(
            label='📩 '+"Download Data",
            data=convert_df_to_csv(df_data),
            file_name=datafile_out,
            mime="text/csv",
            key='download-csv',
            disabled=not cb
        )

        if cb:
            st.dataframe(df_data.style.format(precision=0), use_container_width=True)

    elif selected == "Analysis by TFs (cell-type specific view)":
        c3_1, c3_2 = st.columns(2)

        if "tfpage_tab3_tf" in st.session_state:
            if not set(st.session_state.tfpage_tab3_tf).issubset(set(tfall)): 
                 st.session_state.tfpage_tab3_tf = list(set(st.session_state.tfpage_tab3_tf) & set(tfall))


        tf3_selected = st.multiselect('TFs', tfall, default=tfall[0],  key=persist("tfpage_tab3_tf"))

        type3_selected = st.multiselect(f'Cell types', celltypeAll, default=celltypeAll[0], key=persist("tfpage_tab3_type"),
                                 format_func=lambda x: x + " (Num of donors: " + str(len(type2ds[x])) + ")")


        for tf in tf3_selected:
            for type in type3_selected:
                df_ranks_2 = df_ranks_all.loc[df_ranks_all['Celltype']==type, [tf, "Donor"]]
                # pvalue = anova_test(df_ranks_2, tf)
                fig = violin_plot(f"{tf} in {type}", df_ranks_2, "Donor", tf, 25,4)
                st.pyplot(fig)

        s3_TFs = "_".join(tf3_selected)
        s3_types = "_".join(type3_selected)
        datafile_out = f"TFranks--{s3_TFs}--{s3_types}.csv"


        
        df_data = df_ranks_all.loc[df_ranks_all["Celltype"].isin(type3_selected), ['Celltype', 'Donor'] + tf3_selected]

        c_checkbox, _, c_dwdata = st.columns([3, 9, 3])
        cb = c_checkbox.checkbox("Show data", key="TFrank")

        btn_data = c_dwdata.download_button(
            label='📩 '+"Download Data",
            data=convert_df_to_csv(df_data),
            file_name=datafile_out,
            mime="text/csv",
            key='download-csv',
            disabled=not cb
        )

        if cb:
            st.dataframe(df_data.style.format(precision=0), use_container_width=True)

