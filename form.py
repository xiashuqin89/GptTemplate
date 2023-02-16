import time
import random
import string
from typing import Dict

import streamlit as st

from api import get_answer


class GptModel:
    @staticmethod
    def _render_bar():
        st.markdown(
            """
            ## BKCHAT GPT
            """
        )
        st.sidebar.subheader("Config")
        model = st.sidebar.selectbox('model', ('text-davinci-003', 'text-davinci-002'))

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
        session = st.text_input('session', generate_str())
        content = st.text_area("Please input", max_chars=512)
        if st.button("Submit"):
            start_message = st.empty()
            start_message.write("Parsing...")
            start_time = time.time()
            answer = get_answer(text=content)
            end_time = time.time()
            start_message.write(f"Parse finished，it take{end_time - start_time}s")
            st.text_input("Answer", answer)
        else:
            st.stop()

    def render(self):
        config = self._render_bar()
        self._render_main(config)


def generate_str(num: int = 16) -> str:
    return ''.join(random.sample(string.ascii_letters + string.digits, num))


if __name__ == '__main__':
    GptModel().render()
