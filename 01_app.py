import streamlit as st
import requests
import random

# ----------------------------
# API KEY
# ----------------------------
WEATHER_API_KEY = "여기에_OpenWeather_API_KEY"

# ----------------------------
# 음식 데이터
# ----------------------------
foods = {
    "hot": [
        {
            "name": "냉면",
            "image": "https://images.unsplash.com/photo-1627308595171-d1b5d67129c4",
            "calorie": "470 kcal",
            "nutrition": {
                "탄수화물": "82g",
                "단백질": "18g",
                "지방": "7g"
            }
        },
        {
            "name": "콩국수",
            "image": "https://images.unsplash.com/photo-1550547660-d9450f859349",
            "calorie": "520 kcal",
            "nutrition": {
                "탄수화물": "63g",
                "단백질": "25g",
                "지방": "18g"
            }
        },
        {
            "name": "물회",
            "image": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c",
            "calorie": "350 kcal",
            "nutrition": {
                "탄수화물": "22g",
                "단백질": "35g",
                "지방": "8g"
            }
        }
    ],

    "cold": [
        {
            "name": "김치찌개",
            "image": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c",
            "calorie": "430 kcal",
            "nutrition": {
                "탄수화물": "28g",
                "단백질": "30g",
                "지방": "19g"
            }
        },
        {
            "name": "부대찌개",
            "image": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c",
            "calorie": "650 kcal",
            "nutrition": {
                "탄수화물": "41g",
                "단백질": "36g",
                "지방": "34g"
            }
        }
    ],

    "rain": [
        {
            "name": "파전",
            "image": "https://images.unsplash.com/photo-1504674900247-0877df9cc836",
            "calorie": "620 kcal",
            "nutrition": {
                "탄수화물": "65g",
                "단백질": "16g",
                "지방": "31g"
            }
        },
        {
            "name": "칼국수",
            "image": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd",
            "calorie": "560 kcal",
            "nutrition": {
                "탄수화물": "74g",
                "단백질": "20g",
                "지방": "14g"
            }
        }
    ]
}

# ----------------------------
# 날씨 가져오기
# ----------------------------
def get_weather(city):

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"

    response = requests.get(url)

    if response.status_code != 200:
        return None

    data = response.json()

    temp = data["main"]["temp"]
    weather = data["weather"][0]["main"]

    return temp, weather


# ----------------------------
# 음식 추천
# ----------------------------
def recommend_food(temp, weather):

    if weather == "Rain":
        return random.choice(foods["rain"])

    elif temp >= 28:
        return random.choice(foods["hot"])

    elif temp <= 10:
        return random.choice(foods["cold"])

    else:
        return random.choice(foods["hot"])


# ----------------------------
# Streamlit
# ----------------------------
st.set_page_config(page_title="오늘 뭐 먹지?", page_icon="🍽")

st.title("🍽 오늘 날씨에 뭐 먹지?")

city = st.text_input("도시 입력", "Seoul")

if st.button("추천받기"):

    weather = get_weather(city)

    if weather is None:
        st.error("도시를 찾을 수 없습니다.")
    else:

        temp, weather_state = weather

        food = recommend_food(temp, weather_state)

        st.subheader("🌤 오늘의 날씨")

        st.write(f"기온 : **{temp}℃**")
        st.write(f"날씨 : **{weather_state}**")

        st.divider()

        st.subheader("🍜 추천 음식")

        st.image(food["image"], width=400)

        st.markdown(f"## {food['name']}")

        st.success(f"🔥 칼로리 : {food['calorie']}")

        st.write("### 🥗 영양성분")

        st.table(food["nutrition"])

        st.info("오늘 날씨에 잘 어울리는 음식입니다.")
