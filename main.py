import streamlit as st
import pandas as pd
import plotly.express as px

# 1. 페이지 설정 및 제목
st.set_page_config(page_title="영화 데이터 그래프 도감 2", layout="wide")
st.title("🎬 영화 데이터 그래프 도감 2 - 분포와 관계")

# 2. 데이터 불러오기 및 전처리
DATA_URL = "https://githubusercontent.com"

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)
    # genre 열에서 세로막대(|) 기호가 있는 경우 첫 번째 장르만 추출
    df['genre'] = df['genre'].fillna('미분류').astype(str).apply(lambda x: x.split('|')[0])
    return df

try:
    df = load_data()

    # ==========================================
    # 첫 번째 그래프: 장르별 영화 편수 (도넛 그래프)
    # ==========================================
    st.header("📊 1. 장르별 영화 편수 분포")
    
    # 장르별 데이터 집계
    genre_counts = df['genre'].value_counts().reset_index()
    genre_counts.columns = ['장르', '영화 편수']
    
    # 파이/도넛 차트 생성
    fig1 = px.pie(
        genre_counts, 
        values='영화 편수', 
        names='장르', 
        hole=0.5,  # 도넛 형태 지정
        title="전체 영화의 장르별 비율",
        labels={'영화 편수': '편수', '장르': '장르'}
    )
    
    # 호버(마우스 올림) 시 편수와 비율이 보이도록 설정
    fig1.update_traces(
        textposition='inside', 
        textinfo='percent+label',
        hovertemplate="<b>%{label}</b><br>편수: %{value}편<br>비율: %{percent}<extra></extra>"
    )
    
    st.plotly_chart(fig1, use_container_width=True)
    
    # 그래프 설명 구역
    st.markdown("---")
    st.subheader("💡 이 그래프로 알 수 있는 것")
    st.write("여기에 첫 번째 그래프를 통해 분석할 수 있는 인사이트 한 문장을 입력하세요.")
    st.markdown("---")


    # ==========================================
    # 두 번째 그래프: 장르 내 영화 총 관객수 (트리맵)
    # ==========================================
    st.header("🧱 2. 장르별 영화 총 관객수 규모")
    
    # 트리맵 차트 생성 (장르 -> 영화명 계층 구조)
    fig2 = px.treemap(
        df,
        path=[px.Constant("전체 영화"), 'genre', 'movieNm'],
        values='total_audi',
        title="장르 및 영화별 총 관객수 분포 (칸 크기: 총 관객수)",
        labels={'total_audi': '총 관객수', 'genre': '장르', 'movieNm': '영화명'}
    )
    
    # 호버(마우스 올림) 설정 및 텍스트 서식 (관객수 숫자 포맷팅)
    fig2.update_traces(
        hovertemplate="<b>%{label}</b><br>총 관객수: %{value:,}명<extra></extra>"
    )
    
    st.plotly_chart(fig2, use_container_width=True)
    
    # 그래프 설명 구역
    st.markdown("---")
    st.subheader("💡 이 그래프로 알 수 있는 것")
    st.write("여기에 두 번째 그래프를 통해 분석할 수 있는 인사이트 한 문장을 입력하세요.")
    st.markdown("---")

except Exception as e:
    st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")

