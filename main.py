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
    # genre 열에서 세로막대(|) 기호가 있는 경우 첫 번째 장르만 추출 후 공백 제거
    df['genre'] = df['genre'].fillna('미분류').astype(str).apply(lambda x: x.split('|')[0].strip())
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


    # ==========================================
    # 세 번째 그래프: 총 관객수 분포 (히스토그램)
    # ==========================================
    st.header("📈 3. 영화별 총 관객수 분포 및 최다 흥행작")
    
    # 히스토그램 생성
    fig3 = px.histogram(
        df, 
        x='total_audi',
        nbins=30, # 구간 수 설정
        title="영화별 총 관객수 빈도 분포",
        labels={'total_audi': '총 관객수', 'count': '영화 수'},
        color_discrete_sequence=['#4A90E2']
    )
    
    # 레이아웃 수정 및 Y축 라벨 표기 고정
    fig3.update_layout(
        yaxis_title="영화 수",
        showlegend=False
    )
    
    # 호버 템플릿 설정
    fig3.update_traces(
        hovertemplate="관객수 구간: %{x}<br>영화 수: %{y}편<extra></extra>"
    )
    
    st.plotly_chart(fig3, use_container_width=True)
    
    # 데이터 자동 분석 및 변수 추출
    max_movie_idx = df['total_audi'].idxmax()
    max_movie_name = df.loc[max_movie_idx, 'movieNm']
    max_movie_audi = df.loc[max_movie_idx, 'total_audi']
    threshold_audi = df['total_audi'].quantile(0.7)
    most_dense_count = df[df['total_audi'] <= threshold_audi].shape[0]
    
    # 그래프 설명 구역 및 동적 안내 문구 추가
    st.markdown("---")
    st.subheader("💡 이 그래프로 알 수 있는 것")
    st.write(
        f"📊 분석 결과, 이 기간에 개봉한 영화 중 대부분({most_dense_count}편)이 "
        f"**총 관객수 {threshold_audi/10000:.0f}만 명 이하**의 낮은 관객수 구간에 밀집해 있는 전형적인 롱테일 분포를 보입니다."
    )
    st.write(
        f"🏆 한편, 가장 많은 관객을 동원한 최고의 흥행 영화는 "
        f"**'{max_movie_name}'**이며, 총 **{max_movie_audi:,}명**의 압도적인 스코어를 기록했습니다."
    )
    st.markdown("---")


    # ==========================================
    # 네 번째 그래프: 개봉일 스크린수 vs 총 관객수 (산점도)
    # ==========================================
    st.header("🎯 4. 개봉일 스크린수와 총 관객수의 상관관계")
    
    # 산점도 차트 생성
    fig4 = px.scatter(
        df,
        x='first_scrn',
        y='total_audi',
        color='genre',  # 장르별 점 색상 다르게 설정
        hover_name='movieNm',  # 호버 시 가장 위에 영화명 노출
        title="개봉일 스크린수 대비 총 관객수 분포 (색상: 장르)",
        labels={'first_scrn': '개봉일 스크린수 (개)', 'total_audi': '총 관객수 (명)', 'genre': '장르'}
    )
    
    # 마우스 올렸을 때 서식 정돈 (천 단위 쉼표 포함)
    fig4.update_traces(
        hovertemplate="<b>%{hovertext}</b><br>스크린수: %{x:,}개<br>총 관객수: %{y:,}명<extra></extra>"
    )
    
    st.plotly_chart(fig4, use_container_width=True)
    
    # 그래프 설명 구역
    st.markdown("---")
    st.subheader("💡 이 그래프로 알 수 있는 것")
    st.write("여기에 네 번째 그래프를 통해 분석할 수 있는 인사이트 한 문장을 입력하세요.")
    st.markdown("---")


    # ==========================================
    # 다섯 번째 그래프: 주요 장르별 총 관객수 (박스플롯)
    # ==========================================
    st.header("📦 5. 주요 장르별 총 관객수 분포 비교")
    
    # 영화가 10편 이상인 장르 필터링
    genre_counts_series = df['genre'].value_counts()
    major_genres = genre_counts_series[genre_counts_series >= 10].index.tolist()
    df_filtered = df[df['genre'].isin(major_genres)]
    
    # 박스플롯 차트 생성
    fig5 = px.box(
        df_filtered,
        x='genre',
        y='total_audi',
        color='genre',  # 장르별 색상 다르게
        hover_name='movieNm',  # 마우스 올렸을 때 상자 외부 점(이상치)에 영화명 노출
        title="영화 10편 이상 장르의 관객수 분포 (이상치 점 마우스 오버 시 영화명 확인)",
        labels={'genre': '장르', 'total_audi': '총 관객수 (명)'}
    )
    
    # 호버 템플릿 설정 (이상치 및 데이터 포인트 정보 포맷팅)
    fig5.update_traces(
        hovertemplate="<b>%{hovertext}</b><br>총 관객수: %{y:,}명<extra></extra>"
    )
    
    st.plotly_chart(fig5, use_container_width=True)
    
    # 그래프 설명 구역
    st.markdown("---")
    st.subheader("💡 이 그래프로 알 수 있는 것")
    st.write("여기에 다섯 번째 그래프를 통해 분석할 수 있는 인사이트 한 문장을 입력하세요.")
    st.markdown("---")

except Exception as e:
    st.error(f"데이터를 불러오거나 시각화하는 중 오류가 발생했습니다: {e}")

