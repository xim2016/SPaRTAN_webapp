import pandas as pd
import streamlit as st
from pathlib import Path
from utils import img2buf, violin_plot, convert_df_to_csv, load_data




def correlation_page(path_data,last_select=""):

    
    
    @st.cache
    def load_corrall(datafile):
        return(pd.read_csv(datafile, index_col=0))
        
    df_corrall = load_corrall(str(path_data / "protein_TF_abs_highCorr_inAllExistSamples_cutoff0.3.csv"))

    celltypes = sorted(set(df_corrall['Celltype']))

    celltype2protein = {}
    celltype2Nsample = {}
    celltypes2 = []
    for celltype in celltypes:
        proteins = sorted(df_corrall.loc[df_corrall["Celltype"]==celltype, "Protein"])
        Nsamples = list(df_corrall.loc[df_corrall["Celltype"]==celltype, "Num of Samples"])[0]
        if Nsamples < 2: continue
        celltypes2.append(celltype)
        celltype2protein[celltype] = proteins
        celltype2Nsample[celltype] = Nsamples

    celltypes = celltypes2

    st.markdown("### Correlation betwen surface protein and Transcription Factor(TF)", True)
    st.info('Explore the sample mean of protein-TF correlations for each cell type and protein. The protein-TF pairs with lower correlation (abs<0.3) in all samples of each cell type have been removed. Cell types having less than 2 samples are not included in the list.')
 
    c_celltype, c_protein = st.columns(2)

    s_celltype = c_celltype.selectbox(f'Cell Type ({len(celltypes)})', celltypes, 2, format_func=lambda x: x + " (Num of samples: " + str(celltype2Nsample[x]) + ")")
    
    proteins = celltype2protein[s_celltype]
   
    # Check if session state object exists
    if "selected_protein" not in st.session_state:
        st.session_state['selected_protein'] = proteins[0]
    if 'old_protein' not in st.session_state:
        st.session_state['old_protein'] = ""   


    # Check if value exists in the new options list. if it does retain the selection, else reset
    if st.session_state["selected_protein"] not in proteins:
        st.session_state["selected_protein"] = proteins[0]

    prev_num = st.session_state["selected_protein"]


    def number_callback():
        st.session_state["old_protein"] = st.session_state["selected_protein"]
        st.session_state["selected_protein"] = st.session_state.new_protein
        

    st.session_state["selected_protein"] = c_protein.selectbox(
                f'Protein ({len(proteins)})',
                proteins,
                index=proteins.index(st.session_state["selected_protein"]),
                key = 'new_protein',
                on_change = number_callback
            )


    selected_protein = st.session_state["selected_protein"]
    imgfile_input = str(path_data / "protein-TF_correlation/figure"/f"{s_celltype}_{selected_protein}.png")
    
    datafile_input = str(path_data / "protein-TF_correlation"/f"{s_celltype}_{selected_protein}.csv")


    imgfile_output = "heatmap_corr_" + f"{s_celltype}~{selected_protein}.png" 
    datafile_output = "corr_" + f"{s_celltype}~{selected_protein}.csv"
    
    st.write("")
    st.image(imgfile_input)
    
    ################################################################
    # show table and download data
    corr_data = load_data(datafile_input)

    c_checkbox ,_,c_dwdata, c_dwimg = st.columns([3,5,3,3])

    cb = c_checkbox.checkbox("Show data", key="corr_checkbox")

    btn_img = c_dwimg.download_button(
        label='📥 '+"Download Image",
        data = img2buf(imgfile_input),
        file_name = imgfile_output
    )

    btn_data = c_dwdata.download_button(
        label='📩 '+"Download Data",
        data = convert_df_to_csv(corr_data),
        file_name=datafile_output,
        mime = "text/csv",
        key = 'download-csv',
        disabled= not cb
    )

    if cb:
        st.dataframe(corr_data, use_container_width=True)
        
    
    