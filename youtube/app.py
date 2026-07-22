import streamlit as st
import pandas as pd
import os

from youtube_api import get_video_comments
from analysis import analyze_comments
from visualization import (
    plot_sentiment,
    plot_word_frequency,
    create_wordcloud,
    plot_comment_length
)

# -------------------------------
# 페이지 설정
# -------------------------------
st.set_page_config(
    page_title="YouTube 댓글 분석기",
    page_icon="📺",
    layout="wide"
)

st.title("📺 YouTube 댓글 분석기")
st.write("유튜브 영상 URL을 입력하면 댓글을 분석합니다.")

# -------------------------------
# API KEY 불러오기
# -------------------------------
API_KEY = None

try:
    API_KEY = st.secrets["YOUTUBE_API_KEY"]
except:
    API_KEY = os.getenv("YOUTUBE_API_KEY")

if not API_KEY:
    st.error("YouTube API KEY가 설정되어 있지 않습니다.")
    st.stop()

# -------------------------------
# 입력
# -------------------------------
url = st.text_input("유튜브 URL")

max_comments = st.slider(
    "댓글 개수",
    100,
    1000,
    300,
    step=100
)

# -------------------------------
# 분석 버튼
# -------------------------------
if st.button("댓글 분석 시작"):

    if url == "":
        st.warning("유튜브 URL을 입력하세요.")
        st.stop()

    with st.spinner("댓글을 가져오는 중..."):

        df = get_video_comments(
            url,
            API_KEY,
            max_comments
        )

    if df.empty:
        st.error("댓글을 가져오지 못했습니다.")
        st.stop()

    st.success(f"{len(df)}개의 댓글을 가져왔습니다.")

    st.subheader("댓글 데이터")

    st.dataframe(df)

    csv = df.to_csv(index=False).encode("utf-8-sig")

    st.download_button(
        "CSV 다운로드",
        csv,
        "youtube_comments.csv",
        "text/csv"
    )

    # ----------------------------
    # 감성 분석
    # ----------------------------

    with st.spinner("감성 분석 중..."):

        result = analyze_comments(df)

    df = result["df"]

    st.header("감성 분석")

    plot_sentiment(df)

    # ----------------------------
    # 댓글 길이
    # ----------------------------

    st.header("댓글 길이 분포")

    plot_comment_length(df)

    # ----------------------------
    # 자주 등장 단어
    # ----------------------------

    st.header("자주 등장한 단어")

    plot_word_frequency(result["word_freq"])

    # ----------------------------
    # 워드클라우드
    # ----------------------------

    st.header("한글 워드클라우드")

    create_wordcloud(result["word_freq"])

    # ----------------------------
    # TOP 댓글
    # ----------------------------

    st.header("좋아요 TOP10 댓글")

    top = df.sort_values(
        "likes",
        ascending=False
    ).head(10)

    st.dataframe(
        top[
            [
                "likes",
                "comment"
            ]
        ]
    )
