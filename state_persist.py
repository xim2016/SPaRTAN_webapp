import streamlit as st
from persist import persist, load_widget_state

PAGES = {
     "home": page_settings,
     "settings": page_home,
}


def main():
    if "tf_page" not in st.session_state:
        # Initialize session state.
        st.session_state.update({
            # Default page.
            "page": "tf_page",

            # Radio, selectbox and multiselect options.
            "options": ["Hello", "Everyone", "Happy", "Streamlit-ing"],

            # Default widget values.
            "text": "",
            "slider": 0,
            "checkbox": False,
            "radio": "Hello",
            "selectbox": "Hello",
            "multiselect": ["Hello", "Everyone"],
        })

    page = st.sidebar.radio("Select your page",("settings","home"), format_func=str.capitalize) # tuple(PAGES.keys())

    PAGES[page]()


def page_home():
    st.write(
        f"""
        Settings values
        ---------------
        - **Input**: {st.session_state.text}
        - **Slider**: `{st.session_state.slider}`
        - **Checkbox**: `{st.session_state.checkbox}`
        - **Radio**: {st.session_state.radio}
        - **Selectbox**: {st.session_state.selectbox}
        - **Multiselect**: {", ".join(st.session_state.multiselect)}
        """
    )


def page_settings():
    st.header("Change settings")

    st.text_input("Input", key=persist("text"))
    st.slider("Slider", 0, 10, key=persist("slider"))
    st.checkbox("Checkbox", key=persist("checkbox"))
    st.radio("Radio", st.session_state["options"], key=persist("radio"))
    st.selectbox("Selectbox", st.session_state["options"], key=persist("selectbox"))
    st.multiselect("Multiselect", st.session_state["options"], key=persist("multiselect"))




if __name__ == "__main__":
    load_widget_state()
    main()