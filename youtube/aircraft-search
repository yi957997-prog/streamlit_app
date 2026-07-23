import streamlit as st
import pandas as pd
import plotly.express as px

from aircraft_data import aircraft

st.set_page_config(
    page_title="항공기 기종 검색기",
    page_icon="✈️",
    layout="wide"
)

st.title("✈️ 항공기 기종 검색기")

names = list(aircraft.keys())

selected = st.selectbox(
    "기종 선택",
    names
)

plane = aircraft[selected]

col1, col2 = st.columns([1,2])

with col1:

    st.image(plane["image"], use_container_width=True)

with col2:

    st.subheader(selected)

    st.write(f"**제조사** : {plane['manufacturer']}")
    st.write(f"**항공기 종류** : {plane['type']}")
    st.write(f"**좌석수** : {plane['seats']}석")
    st.write(f"**항속거리** : {plane['range']} km")
    st.write(f"**순항속도** : {plane['speed']} km/h")
    st.write(f"**MTOW** : {plane['mtow']} kg")
    st.write(f"**엔진** : {plane['engine']}")
    st.write(f"**최초비행** : {plane['first_flight']}")

st.divider()

df = pd.DataFrame({
    "항목":["좌석수","항속거리","속도"],
    "값":[
        plane["seats"],
        plane["range"],
        plane["speed"]
    ]
})

fig = px.bar(
    df,
    x="항목",
    y="값",
    text="값",
    title="기종 성능"
)

st.plotly_chart(fig,use_container_width=True)
