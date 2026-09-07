import os
import time
from itertools import chain

import streamlit as st
from google import genai

import persona

st.set_page_config(page_title=persona.NAMA_BOT, page_icon="🔨", layout="centered")

MAX_RETRIES = 3
RETRY_DELAY = 2


@st.cache_resource
def get_client():
    """Bikin client Gemini sekali saja, lalu dipakai ulang selama app hidup.

    API key diambil dari environment variable GEMINI_API_KEY (lokal: file .env,
    Streamlit Cloud: menu Settings > Secrets).
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        try:
            api_key = st.secrets["GEMINI_API_KEY"]
        except Exception:
            api_key = None
    if not api_key:
        st.error("GEMINI_API_KEY belum diisi. Lihat README untuk cara mengaturnya.")
        st.stop()
    return genai.Client(api_key=api_key)


def stream_balasan(client, teks_user, previous_id):
    """Kirim pesan ke Gemini, keluarkan teksnya potong demi potong (streaming).

    Riwayat percakapan diurus server lewat previous_interaction_id, jadi kita
    tidak perlu menyusun ulang seluruh history tiap kali kirim pesan.
    """
    stream = client.interactions.create(
        model=persona.MODEL,
        system_instruction=persona.SYSTEM_INSTRUCTION,
        input=teks_user,
        previous_interaction_id=previous_id,
        stream=True,
    )
    for event in stream:
        if event.event_type == "step.delta" and event.delta.type == "text":
            yield event.delta.text
        elif event.event_type == "interaction.created":
            # Simpan ID-nya supaya pesan berikutnya nyambung dengan percakapan ini.
            st.session_state.previous_id = event.interaction.id


client = get_client()

st.title(persona.JUDUL)
st.caption(persona.SUBJUDUL)

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": persona.SAPAAN_AWAL}]
    st.session_state.previous_id = None

for pesan in st.session_state.messages:
    avatar = persona.AVATAR_USER if pesan["role"] == "user" else persona.AVATAR_BOT
    with st.chat_message(pesan["role"], avatar=avatar):
        st.markdown(pesan["content"])

if prompt := st.chat_input(persona.PLACEHOLDER_INPUT):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar=persona.AVATAR_USER):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar=persona.AVATAR_BOT):
        balasan = None
        error_terakhir = None

        for percobaan in range(1, MAX_RETRIES + 1):
            try:
                potongan = stream_balasan(client, prompt, st.session_state.previous_id)
                # Spinner tampil sampai potongan teks pertama datang,
                # setelah itu teksnya mengalir sendiri.
                with st.spinner(persona.TEKS_LOADING):
                    potongan_pertama = next(potongan, "")

                # chain() bersifat lazy: potongan berikutnya baru diambil saat
                # dibutuhkan, jadi teksnya tetap mengalir (bukan menunggu selesai).
                balasan = st.write_stream(chain([potongan_pertama], potongan))
                error_terakhir = None
                break
            except Exception as e:
                error_terakhir = e
                print(f"[stream_balasan] percobaan {percobaan}/{MAX_RETRIES} gagal: {e}")
                if percobaan < MAX_RETRIES:
                    time.sleep(RETRY_DELAY)

        if error_terakhir is not None:
            balasan = persona.TEKS_ERROR.format(error=error_terakhir)
            st.markdown(balasan)

    st.session_state.messages.append({"role": "assistant", "content": balasan})
