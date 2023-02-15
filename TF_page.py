import random
from pathlib import Path

import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu

from utils import convert_df_to_csv, img2buf, load_data, violin_plot, set_page_container_style

my_theme = {'txc_inactive': 'black', 'menu_background': 'white',
            'txc_active': 'white', 'option_active': 'blue'}

set_page_container_style(75)

def TF_page(path_data):


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
        snames = df_info.loc[type, "sample names"]
        if pd.isna(snames):
            continue
        snames = [x.strip() for x in snames.split(',')]
        type2ds[type] = snames

    
   

    selected = option_menu(None, ["Analysis by TF", "Analysis by cell-type", "Analysis by TF & cell-type"],
                        #    icons=["bi bi-grid-3x3", "bi bi-align-end",
                        #           "bi bi-align-bottom"],
                           menu_icon="cast", default_index=0, orientation="horizontal",
                           styles={
        "container": {"padding": "20!important", "background-color": "#eee"},
        "icon": {"color": "orange", "font-size": "22px"},
        "nav-link": {"font-size": "18px", "text-align": "center", "margin": "0px", "--hover-color": "#fafafa"},
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

    if selected == 'Analysis by TF':
        st.info('For each TF, violin plot shows its ranks across cell types. You can select multiple TFs of your interest from TFs list for comparison.')
        # violin plot for selected TFs]]
        defaults = st.session_state['1_tf'] if "1_tf" in st.session_state and set(st.session_state['1_tf']).issubset(set(tfall)) else [tfall[0]]
        TFs_selected = st.multiselect('TFs', tfall, defaults)
        st.session_state["1_tf"] = TFs_selected
        for tf in TFs_selected:
            df_ranks = df_ranks_all.loc[:, [tf, "Celltype"]]
            fig = violin_plot(tf, df_ranks, "Celltype",tf, 25, 5)
            st.pyplot(fig)
        s_TFs = "_".join(TFs_selected)
        s_TFs if len(s_TFs) <= 100 else s_TFs[:100]
        datafile_out = f"TFranks--{s_TFs}.csv"

        # imgfile =  str(path_data / "figure/commingsoon.jpg")
        # _,c,_ = st.columns([2,4,2])
        # c.image(imgfile)


        df_data = df_ranks_all[['Celltype', 'Dataset'] + TFs_selected]
        # df_data = df_data.set_index('Celltype')
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

        # _, c_celltype,_ = st.columns([0,5,0])
        default = celltypeAll.index(celltypeAll[0]) if "2_celltype" not in st.session_state else st.session_state['2_celltype']
        # st.write(default)
        s_celltype = st.selectbox(f'Cell type ({len(celltypeAll)})', celltypeAll, default,
                                  format_func=lambda x: x + " (Num of samples: " + str(len(type2ds[x])) + ")")

        st.session_state["2_celltype"] = celltypeAll.index(s_celltype)
        imgfile = str(
            path_data / f"TFrank/within_celltype/figure/heatmap_TFrank_samples_{s_celltype}.png")
        imgfile_out = f"heatmap_TFrank_within_{s_celltype}.png"

        # _, c_img, _ = st.columns([1,100,1])
        st.image(imgfile)

        datafile = str(
            path_data / f"TFrank/within_celltype/TFrank_samples_{s_celltype}.csv")
        datafile_out = f"TFranks_within_{s_celltype}.csv"

        # st.write(datafile)
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

    elif selected == "Analysis by TF & cell-type":
        c3_1, c3_2 = st.columns(2)

        defaults = st.session_state['3_tf'] if "3_tf" in st.session_state and set(st.session_state['3_tf']).issubset(set(tfall)) else [tfall[0]]
        tf3_selected = st.multiselect('TFs', tfall, defaults)

        defaults = st.session_state['3_celltype'] if "3_celltype" in st.session_state and set(st.session_state['3_celltype']).issubset(set(celltypeAll)) else [celltypeAll[0]]
        type3_selected = st.multiselect(f'Cell types', celltypeAll, defaults,
                                 format_func=lambda x: x + " (Num of samples: " + str(len(type2ds[x])) + ")")

        st.session_state["3_tf"] = tf3_selected
        st.session_state["3_celltype"] = type3_selected

        for tf in tf3_selected:
            for type in type3_selected:
                df_ranks_2 = df_ranks_all.loc[df_ranks_all['Celltype']==type, [tf, "Dataset"]]
                # group_order_donor = type2ds[type]
                fig = violin_plot(f"{tf} in {type}", df_ranks_2, "Dataset", tf, 25,5)
                st.pyplot(fig)

        s3_TFs = "_".join(tf3_selected)
        s3_types = "_".join(type3_selected)
        datafile_out = f"TFranks--{s3_TFs}--{s3_types}.csv"

        # imgfile =  str(path_data / "figure/commingsoon.jpg")
        # _,c,_ = st.columns([2,4,2])
        # c.image(imgfile)

        
        df_data = df_ranks_all.loc[df_ranks_all["Celltype"].isin(type3_selected), ['Celltype', 'Dataset'] + tf3_selected]
        # df_data = df_data.set_index('Celltype')
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
