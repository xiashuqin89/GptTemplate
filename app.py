import time
import random
import string
from typing import Dict

import streamlit as st
from streamlit_chat import message

from api import get_answer


class GptModel:
    def __init__(self):
        if 'generated' not in st.session_state:
            st.session_state['generated'] = []
        if 'past' not in st.session_state:
            st.session_state['past'] = []

    def _set_menu(self):
        st.set_page_config(
            page_title='BKCHAT GPT',
            initial_sidebar_state="expanded",
            menu_items={
                'Get Help': 'https://bkchat.woa.com',
                'Report a bug': 'https://bkchat.woa.com',
                'About': 'https://bkchat.woa.com'
            }
        )
        st.markdown("## BKCHAT GPT")
        hide_footer()

    def _render_bar(self):
        self._set_menu()
        st.sidebar.subheader("Config")
        model = st.sidebar.selectbox('model', ('chat', 'ko2cn'))

        max_tokens = st.sidebar.slider("max_tokens", min_value=0, max_value=5000, value=2500)
        temperature = st.sidebar.number_input("temperature", min_value=0.0, max_value=1.0, value=0.9, step=0.1)
        top_p = st.sidebar.number_input("top_p", min_value=0.0, max_value=1.0, value=0.95, step=0.01)

        frequency_penalty = st.sidebar.number_input("frequency_penalty", min_value=0.0, max_value=1.0, value=0.0, step=0.01)
        presence_penalty = st.sidebar.number_input("presence_penalty", min_value=0.0, max_value=1.0, value=0.6, step=0.01)

        stop = st.sidebar.text_input('stop', 'prompt_split_token')

        return {
            'model': model,
            'temperature': temperature,
            'max_tokens': max_tokens,
            'top_p': top_p,
            'frequency_penalty': frequency_penalty,
            'presence_penalty': presence_penalty,
            'stop': [stop]
        }

    @staticmethod
    def _render_main(config: Dict):
        is_session = st.checkbox('Enable session')
        if is_session:
            session = st.text_input('session', generate_str())
        else:
            session = ''

        content = st.text_input("Please input", max_chars=512)
        col1, col2, *col = st.columns([1, 1, 6])
        with col1:
            submit = st.button("Submit")
        with col2:
            clear = st.button("Clear")

        if clear:
            st.session_state['past'] = []
            st.session_state['generated'] = []

        if submit:
            st.session_state.past.append(content)
            start_message = st.empty()
            start_message.write("Parsing...")
            start_time = time.time()
            answer = get_answer(input_text=content, session_id=session, model_config=config)
            if answer:
                st.session_state.generated.append(answer.get('result'))
            else:
                st.session_state.generated.append('parse error...')
            end_time = time.time()
            start_message.write(f"Parse finished，it take {end_time - start_time}s")
        else:
            st.stop()

        if st.session_state['generated']:
            for i in range(len(st.session_state['generated']) - 1, -1, -1):
                message(st.session_state["generated"][i], key=str(i))
                message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')

    def render(self):
        config = self._render_bar()
        self._render_main(config)


def generate_str(num: int = 16) -> str:
    return ''.join(random.sample(string.ascii_letters + string.digits, num))


def hide_footer():
    hide_footer_style = """
                <style>
                footer {visibility: hidden;}
                </style>
                """
    st.markdown(hide_footer_style, unsafe_allow_html=True)


if __name__ == '__main__':
    GptModel().render()
