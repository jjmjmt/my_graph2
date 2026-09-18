import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="영화 데이터 그래프 도감 2 - 분포와 관계", layout="wide")

st.title("🎬 영화 데이터 그래프 도감 2 - 분포와 관계")
st.write("박스오피스 10위권 내 개봉 영화 216편의 데이터를 시각화합니다.")


# 데이터 불러오기 및 전처리
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"
    df = pd.read_csv(url)

    # 장르 전처리: 세로막대 기호(|)로 분리되어 있는 경우 첫 번째 장르만 추출
    df["genre"] = df["genre"].fillna("미상").apply(lambda x: str(x).split("|")[0])

    return df


df = load_data()

st.divider()

# -------------------------------------------------------------------
# 첫 번째 그래프: 장르별 영화 편수 (도넛 그래프)
# -------------------------------------------------------------------
st.subheader("1. 장르별 영화 편수 비율")

# 장르별 편수 집계
genre_counts = df["genre"].value_counts().reset_index()
genre_counts.columns = ["genre", "count"]

# Plotly 도넛 차트 생성
fig_donut = px.pie(
    genre_counts,
    names="genre",
    values="count",
    hole=0.4,
    title="장르별 영화 편수 분포",
)

# 마우스 호버 시 편수와 비율 표시 설정
fig_donut.update_traces(
    hovertemplate="<b>장르: %{label}</b><br>영화 편수: %{value}편<br>비율: %{percent}<extra></extra>"
)

# Streamlit에 그래프 출력
st.plotly_chart(fig_donut, use_container_width=True)

# 그래프 해석 안내 영역
st.markdown("---")
st.markdown("💡 **이 그래프로 알 수 있는 것**")
st.info("어떤 장르의 영화가 박스오피스 상위권에 가장 많이 포함되었는지 전체적인 비중을 한눈에 파악할 수 있습니다.")
st.markdown("---")

# -------------------------------------------------------------------
# 두 번째 그래프: 장르 내 영화별 총 관객수 (트리맵)
# -------------------------------------------------------------------
st.subheader("2. 장르 및 영화별 총 관객수 분포")

# 트리맵 생성: 계층(path)은 장르 -> 영화명, 크기(values)는 총 관객수
fig_treemap = px.treemap(
    df,
    path=["genre", "movieNm"],
    values="total_audi",
    title="장르 및 영화별 총 관객수 (칸 크기 = 총 관객수)",
    color="genre",
)

# 마우스 호버 시 영화명(label)과 총 관객수(value) 표시 설정
fig_treemap.update_traces(
    hovertemplate="<b>%{label}</b><br>총 관객수: %{value:,}명<extra></extra>"
)

st.plotly_chart(fig_treemap, use_container_width=True)

st.markdown("---")
st.markdown("💡 **이 그래프로 알 수 있는 것**")
st.info("각 장르 안에서 어떤 영화가 흥행을 주도했는지, 그리고 전체 관객수에서 특정 영화가 차지하는 비중을 직관적으로 비교할 수 있습니다.")
st.markdown("---")

# -------------------------------------------------------------------
# 세 번째 그래프: 총 관객수 분포 (히스토그램)
# -------------------------------------------------------------------
st.subheader("3. 총 관객수 분포 (히스토그램)")

# 히스토그램 생성
fig_hist = px.histogram(
    df,
    x="total_audi",
    nbins=30,
    title="영화별 총 관객수 분포",
    labels={"total_audi": "총 관객수", "count": "영화 수"},
)

# 마우스 호버 시 구간과 영화 수 표시 설정
fig_hist.update_traces(
    hovertemplate="<b>관객수 구간: %{x}</b><br>영화 수: %{y}편<extra></extra>"
)

st.plotly_chart(fig_hist, use_container_width=True)

# 가장 관객 수가 많은 영화 자동 추출
top_movie = df.loc[df["total_audi"].idxmax()]
top_movie_name = top_movie["movieNm"]
top_movie_audi = top_movie["total_audi"]

st.markdown("---")
st.markdown("💡 **이 그래프로 알 수 있는 것**")
st.info(
    f"대부분의 영화는 관객수가 약 100만 명 이하의 구간에 밀집되어 있으며, "
    f"가장 관객이 많은 영화는 **'{top_movie_name}'**(총 {top_movie_audi:,}명)입니다."
)
st.markdown("---")

# -------------------------------------------------------------------
# 네 번째 그래프: 개봉일 스크린수 vs 총 관객수 (산점도)
# -------------------------------------------------------------------
st.subheader("4. 개봉일 스크린수와 총 관객수의 관계")

# 산점도 생성: x축 = 개봉일 스크린수, y축 = 총 관객수, 색상 = 장르, 호버 데이터 = 영화명
fig_scatter = px.scatter(
    df,
    x="first_scrn",
    y="total_audi",
    color="genre",
    hover_name="movieNm",
    title="개봉일 스크린수 vs 총 관객수",
    labels={"first_scrn": "개봉일 스크린수", "total_audi": "총 관객수", "genre": "장르"},
)

# 마우스 호버 시 표시 정보 설정
fig_scatter.update_traces(
    hovertemplate="<b>%{hovertext}</b><br>개봉일 스크린수: %{x:,}개<br>총 관객수: %{y:,}명<extra></extra>"
)

st.plotly_chart(fig_scatter, use_container_width=True)

st.markdown("---")
st.markdown("💡 **이 그래프로 알 수 있는 것**")
st.info("개봉일 스크린수가 많을수록 총 관객수도 증가하는 경향을 보이는지, 그리고 특정 장르가 초기 스크린 확보 및 최종 관객수 선점에 유리했는지 파악할 수 있습니다.")
st.markdown("---")

# -------------------------------------------------------------------
# 다섯 번째 그래프: 영화 10편 이상 장르의 총 관객수 분포 (박스플롯)
# -------------------------------------------------------------------
st.subheader("5. 영화 10편 이상 장르별 총 관객수 분포 (상자 그림)")

# 영화 수가 10편 이상인 장르 필터링
genre_counts_series = df["genre"].value_counts()
major_genres = genre_counts_series[genre_counts_series >= 10].index
df_filtered = df[df["genre"].isin(major_genres)]

# 박스플롯 생성: x축 = 장르, y축 = 총 관객수, 이상치/점 호버 정보 = 영화명
fig_box = px.box(
    df_filtered,
    x="genre",
    y="total_audi",
    color="genre",
    hover_name="movieNm",
    points="outliers",  # 이상치 점 표시
    title="영화 10편 이상 장르별 총 관객수 분포",
    labels={"genre": "장르", "total_audi": "총 관객수"},
)

# 마우스 호버 시 영화명 및 총 관객수 표시 설정
fig_box.update_traces(
    hovertemplate="<b>%{hovertext}</b><br>총 관객수: %{y:,}명<extra></extra>"
)

st.plotly_chart(fig_box, use_container_width=True)

st.markdown("---")
st.markdown("💡 **이 그래프로 알 수 있는 것**")
st.info(
    "영화 수가 10편 이상인 주력 장르별 관객수 중앙값과 분포 범위를 비교할 수 있으며, "
    "상자 밖 튀는 점(이상치)을 통해 동일 장르 내에서 대흥행한 특이점 영화를 식별할 수 있습니다."
)
st.markdown("---")

# -------------------------------------------------------------------
# 여섯 번째 그래프: 개봉일 스크린수 vs 총 관객수 + 첫 주 관객수 (버블 차트)
# -------------------------------------------------------------------
st.subheader("6. 개봉일 스크린수, 총 관객수, 첫 주 관객수의 관계 (버블 차트)")

# 버블 차트 생성: x축 = 개봉일 스크린수, y축 = 총 관객수, 크기 = 첫 주 관객수, 색상 = 장르
fig_bubble = px.scatter(
    df,
    x="first_scrn",
    y="total_audi",
    size="first_week_audi",
    color="genre",
    hover_name="movieNm",
    size_max=40,  # 버블 최대 크기 조절
    title="개봉일 스크린수 vs 총 관객수 (버블 크기 = 개봉 첫 주 관객수)",
    labels={
        "first_scrn": "개봉일 스크린수",
        "total_audi": "총 관객수",
        "first_week_audi": "개봉 첫 주 관객수",
        "genre": "장르",
    },
)

# 마우스 호버 시 표시 정보 설정
fig_bubble.update_traces(
    hovertemplate=(
        "<b>%{hovertext}</b><br>"
        "개봉일 스크린수: %{x:,}개<br>"
        "총 관객수: %{y:,}명<br>"
        "개봉 첫 주 관객수: %{marker.size:,}명<extra></extra>"
    )
)

st.plotly_chart(fig_bubble, use_container_width=True)

st.markdown("---")
st.markdown("💡 **이 그래프로 알 수 있는 것**")
st.info(
    "개봉일 스크린수와 총 관객수의 관계뿐만 아니라, "
    "버블의 크기를 통해 개봉 첫 주 초반 흥행 기세가 최종 관객수로 얼마나 이어졌는지 세 가지 변수를 동시에 비교할 수 있습니다."
)
st.markdown("---")

# -------------------------------------------------------------------
# 여덟 번째 그래프: 10위권 체류 기간 vs 총 관객수 (산점도)
# -------------------------------------------------------------------
st.subheader("8. 10위권 체류 기간과 총 관객수의 관계")

# 8번째 그래프 생성 (영화명 컬럼: movieNm)
fig8 = px.scatter(
    df,
    x="days_in_top10",
    y="total_audi",
    hover_name="movieNm",  # 'movie_name' -> 'movieNm' 으로 수정
    color="genre",
    title="10위권에 오래 머문 영화는 총 관객도 많은가",
    labels={"days_in_top10": "10위권 머문 날수", "total_audi": "총 관객수", "genre": "장르"},
)

# 호버 서식 지정 및 스타일 수정
fig8.update_traces(
    marker=dict(size=10, opacity=0.7),
    hovertemplate="<b>%{hovertext}</b><br>10위권 머문 날수: %{x}일<br>총 관객수: %{y:,}명<extra></extra>",
)

# Streamlit에 출력 (fig8.show() 대신 st.plotly_chart 사용)
st.plotly_chart(fig8, use_container_width=True)

st.markdown("---")
st.markdown("💡 **이 그래프로 알 수 있는 것**")
st.info(
    "박스오피스 Top 10 진입 일수가 긴 영화일수록 누적 관객 수도 큰 비례 관계를 나타내는지, "
    "혹은 단기간 흥행 후 가파르게 누적 관객을 끌어 모은 영화가 존재하는지 분석할 수 있습니다."
)
st.markdown("---")
