import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from typing import Dict, Any, Optional
import io

st.set_page_config(
    page_title="K-Career Navigator",
    page_icon="🎯",
    layout="wide",
)


def inject_css():
    """Deep Navy & Electric Blue 테마 및 카드/스텝퍼/버튼 스타일"""
    st.markdown(
        """
        <style>
        /* 전체 배경 및 기본 폰트 */
        .stApp {
            /* Deep Navy 베이스 + 보라/블루 그라디언트*/
            background: radial-gradient(circle at 0% 0%, #3b3bbf 0, #1b1b5a 35%, #050019 80%);
            color: #E6F1FF;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen,
                         Ubuntu, Cantarell, "Open Sans", "Helvetica Neue", sans-serif;
        }
        
        /* Streamlit 기본 요소 보이도록 */
        .stApp > header {
            background-color: transparent;
        }
        
        section[data-testid="stSidebar"] {
            background-color: rgba(17, 34, 64, 0.8);
        }
        
        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        
        /* 기본 Streamlit 콘텐츠 영역 보이도록 */
        .main .block-container > div {
            color: #E6F1FF;
        }
        
        /* Streamlit 기본 텍스트 */
        .element-container p, .element-container div {
            color: #E6F1FF;
        }

        /* 기본 텍스트 색상 조정 - 더 구체적으로 적용 */
        .stMarkdown p, .stMarkdown div, .stMarkdown span {
            color: #E6F1FF;
        }
        
        .main .block-container p, .main .block-container div, .main .block-container span {
            color: #E6F1FF;
        }
        
        label {
            color: #E6F1FF !important;
        }
        
        /* 입력 필드 배경 */
        .stSelectbox > div > div {
            background-color: rgba(255, 255, 255, 0.1);
            color: #E6F1FF;
        }
        
        .stRadio > label {
            color: #E6F1FF !important;
        }

        /* 헤더 타이틀 */
        .main-title {
            font-size: 2.1rem;
            font-weight: 700;
            color: #FFFFFF;
        }

        .subtitle {
            font-size: 0.95rem;
            color: #C0C8FF;
        }

        /* 스텝퍼 */
        .stepper-container {
            display: flex;
            justify-content: space-between;
            margin: 0.5rem 0 1.5rem 0;
        }
        .stepper-item {
            flex: 1;
            text-align: center;
            padding: 0.6rem 0.2rem;
            border-bottom: 2px solid #233554;
            color: #8892B0;
            font-size: 0.85rem;
        }
        .stepper-item.active {
            border-bottom: 3px solid #64FFDA;
            color: #E6F1FF;
            font-weight: 600;
        }

        /* 카드 버튼 */
        .card-button {
            border-radius: 12px;
            padding: 1.2rem 1rem;
            border: 1px solid #233554;
            background: #112240;
            cursor: pointer;
            transition: all 0.2s ease-in-out;
            text-align: left;
        }
        .card-button:hover {
            border-color: #64FFDA;
            box-shadow: 0 0 10px rgba(100, 255, 218, 0.25);
            transform: translateY(-2px);
        }
        .card-button.selected {
            border-color: #64FFDA;
            background: linear-gradient(135deg, #112240 0%, #0B253A 50%, #112240 100%);
        }
        .card-title {
            font-size: 1.0rem;
            font-weight: 600;
            color: #E6F1FF;
        }
        .card-desc {
            font-size: 0.80rem;
            color: #8892B0;
            margin-top: 0.3rem;
        }

        /* 기본 버튼 스타일 오버라이드 (하단 '계속하기' 버튼 스타일과 유사) */
        .stButton>button {
            border-radius: 999px;
            border: none;
            color: #FFFFFF;
            background: linear-gradient(135deg, #5B5CFF 0%, #7D5CFF 50%, #5B5CFF 100%);
            padding: 0.55rem 1.8rem;
            font-weight: 600;
            font-size: 0.95rem;
            letter-spacing: 0.02em;
            box-shadow: 0 8px 18px rgba(8, 12, 64, 0.65);
        }
        .stButton>button:hover {
            color: #FFFFFF;
            background: linear-gradient(135deg, #7F7FFF 0%, #9A6CFF 40%, #7F7FFF 100%);
            box-shadow: 0 10px 22px rgba(5, 10, 55, 0.9);
        }

        /* 말풍선 스타일 */
        .speech-bubble {
            position: relative;
            background: #112240;
            border-radius: 12px;
            padding: 0.9rem 1.0rem;
            margin-bottom: 0.7rem;
            border: 1px solid #233554;
            font-size: 0.85rem;
        }
        .speech-bubble:after {
            content: "";
            position: absolute;
            bottom: -15px;
            left: 20px;
            border-width: 8px 8px 0;
            border-style: solid;
            border-color: #112240 transparent;
            display: block;
            width: 0;
        }

        /* 키워드 태그 */
        .tag {
            display: inline-block;
            padding: 0.25rem 0.6rem;
            border-radius: 999px;
            border: 1px solid #64FFDA;
            color: #64FFDA;
            font-size: 0.75rem;
            margin: 0.15rem;
            background: rgba(100, 255, 218, 0.04);
        }

        /* 산업 기상도 카드 */
        .metric-card {
            background: rgba(7, 15, 53, 0.92);
            border-radius: 12px;
            padding: 0.9rem 0.9rem;
            border: 1px solid #233554;
            font-size: 0.85rem;
        }
        .metric-title {
            color: #8892B0;
            font-size: 0.78rem;
            text-transform: uppercase;
            letter-spacing: 0.06em;
        }
        .metric-value {
            font-size: 1.0rem;
            font-weight: 600;
            margin-top: 0.15rem;
        }
        .metric-sub {
            font-size: 0.78rem;
            color: #8892B0;
        }

        /* select_slider 라벨 색상 */
        .stSlider > div > div > div > div {
            color: #E6F1FF !important;
        }
        
        /* Streamlit 기본 요소 보이도록 추가 스타일 */
        h1, h2, h3, h4, h5, h6 {
            color: #E6F1FF !important;
        }
        
        /* 버튼이 보이도록 */
        .stButton > button {
            visibility: visible !important;
        }
        
        /* Expander가 보이도록 */
        .streamlit-expanderHeader {
            color: #E6F1FF !important;
        }

        /* 질문 카드 스타일 */
        .question-card {
            background: #0F2137;
            border-radius: 16px;
            padding: 1.4rem 1.6rem;
            border: 1px solid #233554;
            margin-bottom: 1.1rem;
            box-shadow: 0 10px 30px rgba(2, 12, 27, 0.7);
        }
        .question-header {
            display: flex;
            align-items: center;
            margin-bottom: 0.6rem;
        }
        .question-pill {
            background: rgba(100, 255, 218, 0.08);
            border-radius: 999px;
            padding: 0.1rem 0.55rem;
            font-size: 0.75rem;
            color: #64FFDA;
            border: 1px solid rgba(100, 255, 218, 0.4);
            margin-right: 0.5rem;
        }
        .question-title {
            font-size: 1.0rem;
            font-weight: 600;
            color: #E6F1FF;
        }
        .question-desc {
            font-size: 0.8rem;
            color: #8892B0;
            margin-bottom: 0.4rem;
        }
        .question-footer {
            font-size: 0.75rem;
            color: #55627A;
            margin-top: 0.5rem;
        }

        /* 모바일 앱 느낌의 선택형 라디오 버튼 스타일 */
        .stRadio > label {
            font-size: 0.9rem;
        }

        .stRadio > div {
            gap: 0.6rem;
        }

        .stRadio div[role="radiogroup"] {
            display: flex;
            flex-direction: column;
        }

        .stRadio div[role="radiogroup"] label {
            border-radius: 999px;
            padding: 0.65rem 1.0rem;
            border: 1px solid rgba(255, 255, 255, 0.18);
            background: rgba(10, 16, 60, 0.85);
            color: #FFFFFF;
            text-align: center;
            cursor: pointer;
            transition: all 0.18s ease-out;
            box-shadow: 0 6px 14px rgba(3, 8, 40, 0.6);
        }

        .stRadio div[role="radiogroup"] label:hover {
            border-color: rgba(255, 255, 255, 0.35);
            background: linear-gradient(135deg, rgba(108, 99, 255, 0.9), rgba(158, 116, 255, 0.9));
        }

        /* 선택된 라디오(checked) 효과 */
        .stRadio div[role="radiogroup"] input:checked + div label {
            border-color: rgba(255, 255, 255, 0.5);
            background: linear-gradient(135deg, #6C63FF, #9E74FF);
            box-shadow: 0 10px 24px rgba(5, 10, 60, 0.95);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


inject_css()


def init_session_state():
    if "current_step" not in st.session_state:
        st.session_state.current_step = 1
    if "survey" not in st.session_state:
        st.session_state.survey = {}
    if "trends" not in st.session_state:
        st.session_state.trends = None
    if "recommendation" not in st.session_state:
        st.session_state.recommendation = ""


def get_cagr(series: pd.Series) -> float:
    """연평균 성장률(CAGR) 계산 (semi.prd.md 로직 참고)"""
    valid = series.dropna()
    if len(valid) < 2:
        return float("nan")
    start_val = valid.iloc[0]
    end_val = valid.iloc[-1]
    num_years = len(valid) - 1
    if start_val > 0 and num_years > 0:
        return (end_val / start_val) ** (1 / num_years) - 1
    elif start_val == 0 and end_val > 0:
        return 1.0
    else:
        return float("nan")


def analyze_trends(df: pd.DataFrame, industry_prefix: str) -> Optional[Dict[str, Any]]:
    """2020년 이후 생산/점유율/수출/가격 CAGR 및 최근값, 가격 이름 반환"""
    df_recent = df[df.index >= 2020].copy()
    if len(df_recent) < 2:
        return None

    trends: Dict[str, Any] = {}

    prod_col = f"{industry_prefix}_생산(조원)"
    share_col = f"{industry_prefix}_시장점유율(퍼센트)"
    export_col = f"{industry_prefix}_수출(억불)"
    if industry_prefix == "반도체":
        price_col = "DRAM_가격(달러)"
        price_name = "DRAM 가격"
    else:
        price_col = "액정표시장치(LCD)_평균가격(달러)"
        price_name = "LCD 평균가격"

    if prod_col in df_recent.columns:
        trends["production_cagr"] = get_cagr(df_recent[prod_col])
        trends["production_latest"] = df_recent[prod_col].iloc[-1]
    if share_col in df_recent.columns:
        trends["share_cagr"] = get_cagr(df_recent[share_col])
        trends["share_latest"] = df_recent[share_col].iloc[-1]
    if export_col in df_recent.columns:
        trends["export_cagr"] = get_cagr(df_recent[export_col])
        trends["export_latest"] = df_recent[export_col].iloc[-1]
    if price_col in df_recent.columns:
        trends["price_cagr"] = get_cagr(df_recent[price_col])
        trends["price_latest"] = df_recent[price_col].iloc[-1]
        trends["price_name"] = price_name

    return trends


def create_dummy_data() -> pd.DataFrame:
    """CSV 업로드가 없을 경우 사용할 더미 데이터 생성"""
    years = list(range(2016, 2025))

    np.random.seed(42)
    data = {
        "연도": years,
        # 반도체
        "반도체_생산(조원)": np.linspace(250, 420, len(years))
        + np.random.normal(0, 8, len(years)),
        "반도체_시장점유율(퍼센트)": np.linspace(16, 20, len(years))
        + np.random.normal(0, 0.4, len(years)),
        "반도체_수출(억불)": np.linspace(800, 1180, len(years))
        + np.random.normal(0, 25, len(years)),
        "DRAM_가격(달러)": np.linspace(3.0, 4.5, len(years))
        + np.random.normal(0, 0.2, len(years)),
        # 디스플레이
        "디스플레이_생산(조원)": np.linspace(90, 110, len(years))
        + np.random.normal(0, 3, len(years)),
        "디스플레이_시장점유율(퍼센트)": np.linspace(30, 28, len(years))
        + np.random.normal(0, 0.3, len(years)),
        "디스플레이_수출(억불)": np.linspace(350, 320, len(years))
        + np.random.normal(0, 10, len(years)),
        "액정표시장치(LCD)_평균가격(달러)": np.linspace(1.2, 0.7, len(years))
        + np.random.normal(0, 0.05, len(years)),
    }
    df = pd.DataFrame(data).set_index("연도")
    return df


def _normalize_df(df: pd.DataFrame) -> Optional[pd.DataFrame]:
    """공통 CSV 후처리: 연도 인덱스 및 필수 컬럼 확인"""
    if "연도" not in df.columns:
        return None
    try:
        df["연도"] = pd.to_numeric(df["연도"], errors="coerce")
        df = df.dropna(subset=["연도"])
        df = df.set_index("연도")
    except Exception:
        return None

    required_any = [
        "반도체_생산(조원)",
        "디스플레이_생산(조원)",
    ]
    if not any(col in df.columns for col in required_any):
        return None
    return df


def load_data(uploaded_file) -> pd.DataFrame:
    """사용자 CSV 또는 로컬 공식 CSV / 더미 데이터 로드 (방어적으로 처리)"""
    encodings_to_try = ["utf-8", "cp949", "euc-kr"]

    # 1) 업로드된 CSV가 있다면 우선 사용
    if uploaded_file is not None:
        try:
            raw_bytes = uploaded_file.read()
        except Exception:
            st.warning("CSV 파일을 읽는 중 오류가 발생했습니다. 기본 데이터를 사용합니다.")
            raw_bytes = None

        if raw_bytes:
            for enc in encodings_to_try:
                try:
                    text = raw_bytes.decode(enc)
                    df = pd.read_csv(io.StringIO(text))
                    df_norm = _normalize_df(df)
                    if df_norm is not None:
                        return df_norm
                except UnicodeDecodeError:
                    continue
                except Exception:
                    continue
            st.warning("업로드한 CSV의 인코딩/구조를 인식하지 못했습니다. 기본 데이터를 사용합니다.")

    # 2) 업로드가 없거나 실패하면, 로컬 공식 CSV 시도
    default_path = "산업통상자원부_반도체디스플레이 산업 동향_20241231.csv"
    for enc in encodings_to_try:
        try:
            df_local = pd.read_csv(default_path, encoding=enc)
            df_norm = _normalize_df(df_local)
            if df_norm is not None:
                st.info(f"로컬 CSV 파일('{default_path}')을(를) 인코딩 {enc}로 불러왔습니다.")
                return df_norm
        except FileNotFoundError:
            break
        except UnicodeDecodeError:
            continue
        except Exception:
            continue

    # 3) 모든 시도가 실패하면 더미 데이터 사용
    st.warning("공식 CSV를 찾지 못하거나 구조를 인식하지 못해, 시뮬레이션용 더미 데이터를 사용합니다.")
    return create_dummy_data()


STATUS_TIPS: Dict[str, str] = {
    # ① 1-2학년 (전공 기초 단계)
    "입문 단계": (
        "① 1-2학년 (전공 기초 단계)  \n"
        "- 핵심 조언: \"학점이 곧 깡패\"입니다. 특히 반도체·디스플레이 직무는 전공 평점이 필터 역할을 합니다.  \n"
        "- 목표: 최소 3.8 / 4.5 이상을 노려 보세요. 전공 기초 과목에서 B0 이하가 없도록 관리하는 것이 좋습니다.  \n"
        "- 필수 과목 예시: 전자계열은 회로이론·전자기학·고체물리, 화공계열은 유기화학, 기계계열은 열역학 등 각 계열의 핵심 기초 과목입니다.  \n"
        "- 추천 활동: 아두이노·라즈베리파이 기반의 작은 HW-SW 프로젝트를 하나라도 '완성'해 보세요. 결과물의 규모보다 끝까지 마무리해 본 경험이 중요합니다."
    ),
    # ② 3-4학년 (직무 탐색 단계)
    "기본 경험 보유": (
        "② 3-4학년 (직무 탐색 단계)  \n"
        "- 핵심 조언: 이제는 \"어떤 공정/직무를 담당하고 싶은지\"를 구체화해야 하는 시기입니다.  \n"
        "- 필수 활동: 최소 6개월 이상 학부연구생 경험 또는 나노종합기술원·KANC·IDEC 등에서의 반도체 공정 실습을 권장합니다.  \n"
        "- 자격증 전략: 직무와 직접 관련 없는 기사 자격증보다, 데이터 기반 의사결정을 보여주는 ADsP(데이터분석준전문가), 6 Sigma GB 같은 자격이 실무에서 더 우대되는 편입니다.  \n"
        "- 정리 포인트: 지금까지의 프로젝트/대외활동을 지원하려는 공정·직무와 연결해 \"내가 왜 이 포지션과 잘 맞는지\"를 문장으로 정리해 두세요."
    ),
    # ③ 실무 경험 보유 / 중고신입
    "실무 경험 보유": (
        "③ 실무 경험 보유 / 중고신입  \n"
        "- 핵심 조언: 단순히 '많이 해봤다'가 아니라, 기존 경험을 새 산업/새 직무 관점에서 재해석하는 것이 중요합니다.  \n"
        "- 자소서 구조: `어떤 문제(Issue)를` → `어떤 데이터로 분석해` → `어떻게 해결(Action)했는지` → `결과(수치)` 순으로 정리하세요.  \n"
        "- 이직/지원 사유: 현재 산업의 호황/불황 국면과, 지원 기업의 CAPEX(투자 계획)를 연결해 \"왜 지금 이 회사/직무인지\" 논리를 만드는 것이 좋습니다."
    ),
    # ④ 일반 취준생 (경험 부족)
    "전공은 하나 직무 경험 부족": (
        "④ 일반 취준생 (경험 부족)  \n"
        "- 핵심 조언: 전공 지식은 있지만, 현장 용어·프로세스에 대한 이해가 부족한 상태일 가능성이 큽니다.  \n"
        "- 실행 방안: NCS 기반 직무 교육 과정이나 기업 연계 부트캠프를 통해, OCAP(Out of Control Action Plan, 이상 발생 시 조치 계획)과 같은 현장 용어를 빠르게 익히는 것을 추천합니다.  \n"
        "- 동시에, 교육 과정에서 사용하는 실제 공정/품질 리포트 포맷에 익숙해지면, 이후 인턴·신입 면접에서 큰 도움을 받을 수 있습니다."
    ),
    # 기타 상태(포트폴리오 작성 단계 등)는 기존 로직 활용
    "본격 취업 준비 중": (
        "포트폴리오·자기소개서를 본격적으로 준비하는 단계라면, 지금까지의 활동을 산업 사이클과 연결해 재구성해야 합니다. "
        "최근 3~5년간의 생산·수출·가격 데이터를 간단히 분석해, \"성장하는 영역\"과 \"구조적 어려움이 있는 영역\"을 구분하고, "
        "내 경험이 어떤 부분을 보완할 수 있는지에 초점을 맞춰 스토리를 설계해 보세요."
    ),
}


IDM_COMPANIES = [
    {
        "기업": "삼성전자 (DS부문)",
        "주력": "메모리(DRAM, NAND), 파운드리, 시스템LSI",
        "위치": "경기 화성(DSR/Line), 평택(고덕), 기흥(파운드리), 용인(남사-예정)",
        "스펙": "학점 3.5+ (전공평점 중요) / 오픽 IM2(이공), IH(인문) / GSAT 통과 필수",
        "Tip": "설비/공정은 평택 근무 가능성 높음. 메모리사업부가 채용 규모 가장 큼.",
        "링크": "https://www.samsungcareers.com/",
    },
    {
        "기업": "삼성전자 (TSP총괄)",
        "주력": "반도체 패키징 및 테스트 (후공정)",
        "위치": "충남 천안(성성동), 온양(배방읍)",
        "스펙": "패키징 공정 이해도 필수 / 기계, 재료, 화공 전공 선호 / 지방 근무 가능자",
        "Tip": "'천안/온양' 근무로, 수도권 대비 경쟁률이 소폭 낮을 수 있음. (알짜 직무)",
        "링크": "https://www.samsungcareers.com/",
    },
    {
        "기업": "SK하이닉스",
        "주력": "메모리 (DRAM 세계 2위, NAND)",
        "위치": "경기 이천(부발읍 - 본사/DRAM), 충북 청주(흥덕구 - NAND), 용인(원삼-예정)",
        "스펙": "학점 3.5+ / SKCT 난이도 최상 / '직무 면접'이 매우 깊이 있음 (전공 지식)",
        "Tip": "청주 사업장(NAND/Solution) 지원 시 경쟁률 측면에서 전략적일 수 있음.",
        "링크": "https://recruit.skhynix.com/servlet/mnus_main.view",
    },
    {
        "기업": "DB하이텍",
        "주력": "8인치 파운드리 (아날로그 반도체, PMIC)",
        "위치": "경기 부천(원미구 - 본사/Fab1), 충북 음성(감곡면 - Fab2)",
        "스펙": "학점 3.3~3.5 / 반도체 소자 및 공정 지식 / 전자공학 선호",
        "Tip": "연봉 상승률 높음. 부천 근무 선호도가 높으나 음성 공장 T/O도 많음.",
        "링크": "https://dbgroup.recruiter.co.kr/",
    },
]

FABLESS_COMPANIES = [
    {
        "기업": "LX세미콘",
        "주력": "디스플레이 구동칩(DDI) 설계 (국내 1위)",
        "위치": "서울 양재, 대전 유성구 (R&D 캠퍼스)",
        "스펙": "전자/컴공 석사 선호 / Verilog, FPGA 역량 / 학사 지원 시 프로젝트 필수",
        "링크": "https://www.lxsemicon.com/kr/company/recruitment-information/application",
    },
    {
        "기업": "텔레칩스 / 칩스앤미디어",
        "주력": "차량용 인포테인먼트(IVI) / 비디오 IP",
        "위치": "경기 성남(판교), 서울 강남",
        "스펙": "C/C++, 임베디드 SW, 디지털 논리회로 이해도 / 시스템 반도체 교육 우대",
        "링크": "https://careers.telechips.com/",
    },
]

OSAT_COMPANIES = [
    {
        "기업": "하나마이크론",
        "주력": "반도체 패키징 및 테스트 (삼성/SK 협력)",
        "위치": "충남 아산(음봉면), 경기 판교(R&D)",
        "스펙": "전기/전자/기계/재료 / 품질(QC/QA) 직무 T/O 많음",
        "링크": "https://hanamicron.recruiter.co.kr/career/home",
    },
    {
        "기업": "SFA반도체",
        "주력": "반도체 조립 및 테스트",
        "위치": "충남 천안(서북구)",
        "스펙": "학점 3.2~3.5 / 3교대 근무 가능자(엔지니어 일부) / 오픽 IM1+",
        "링크": "https://recruit.sfa.co.kr/",
    },
    {
        "기업": "네패스 (Nepes)",
        "주력": "WLP, PLP (첨단 패키징)",
        "위치": "충북 청주(오창), 괴산(청안)",
        "스펙": "화학/신소재 선호 / 차세대 패키징 기술 관심도 / 영어 독해 능력",
        "링크": "https://careers.nepes.co.kr/",
    },
]

FOREIGN_EQUIP = [
    {
        "기업": "ASML Korea",
        "주력": "EUV 노광 장비 (슈퍼을)",
        "위치": "경기 화성(동탄), 평택, 이천, 청주 (고객사 팹 내부 상주)",
        "스펙": "[필수] 영어 회화(OPIc IM3~IH) / 전자회로, 기구학 / CS는 교대 근무 있음",
        "Tip": "서류-AI역검-영어Test-면접 순. 영어 면접 대비 필수.",
        "링크": "https://midasin-asmlkorea.recruiter.co.kr/career/home",
    },
    {
        "기업": "AMAT / Lam / TEL",
        "주력": "증착/식각/트랙 장비 (세계 점유율 1~3위)",
        "위치": "경기 화성, 평택, 이천, 용인(R&D센터)",
        "스펙": "직무 관련 경험(인턴, 장비 분해조립) / 운전면허(CS) 필수",
        "Tip": "R&D 센터(용인/화성) 설립으로 석/박사 공정 엔지니어 채용 증가 중.",
        "링크": "https://www.peoplenjob.com/",
    },
]

LOCAL_EQUIP = [
    {
        "기업": "세메스 (SEMES)",
        "주력": "세정/식각/포토 장비 (삼성전자 자회사)",
        "위치": "충남 천안(직산 - 본사), 경기 화성",
        "스펙": "삼성전자 수준의 복지 / 학점 3.5+ / 기계, 전기전자, SW 전공",
        "링크": "https://www.semes.com/",
    },
    {
        "기업": "HPSP",
        "주력": "고압 수소 어닐링 장비 (세계 유일 기술)",
        "위치": "경기 화성(동탄)",
        "스펙": "최근 급성장 중 / 기계설계, 공정 엔지니어 / 외국어 가능자 우대",
        "링크": "https://thehpsp.com/ko/bbs/board.php?bo_table=career",
    },
    {
        "기업": "솔브레인 / 동진쎄미켐",
        "주력": "식각액 / 포토레지스트 (PR)",
        "위치": "경기 판교(R&D), 충남 공주(솔브레인), 경기 화성(동진)",
        "스펙": "화학공학, 신소재 전공 필수 / 위험물산업기사, 화공기사 우대",
        "링크": "https://www.soulbrain.co.kr/m64.php?tab=1",
    },
]

JOB_STRENGTH_TIPS: Dict[str, Dict[str, str]] = {
    "R&D(회로/설계)": {
        "분석적 사고": (
            "[R&D] + 데이터 분석 관점입니다.  \n"
            "- TCAD·회로 시뮬레이션 결과와 실제 계측 데이터의 **정합성(Fitting)**을 맞춰 본 경험을 강조하세요.  \n"
            "- 단순히 \"시뮬레이션을 돌려봤다\"가 아니라, 어떤 파라미터를 조정하며 오차를 줄였는지, 그 과정에서 사용한 툴과 수식을 함께 설명하면 좋습니다."
        ),
        "문제 해결": (
            "디지털·아날로그 회로 설계 프로젝트에서 발생한 버그를 어떻게 추적했는지, 구체적인 시나리오로 정리해 두세요.  \n"
            "예를 들어, 타이밍 미스나 기능 오류가 발생했을 때, 파형 분석 → RTL/테스트벤치 수정 → 재검증까지의 단계별 접근을 설명하는 것이 좋습니다."
        ),
        "수치/정확성": (
            "설계 결과를 PPA(Power, Performance, Area) 관점에서 정량적으로 비교한 경험을 어필하세요.  \n"
            "Baseline 설계와 최적화 설계의 타이밍 여유, 소비 전력, 셀 면적 등을 표로 비교하고, 어떤 트레이드오프를 선택했는지 설명할 수 있으면 좋습니다."
        ),
        "커뮤니케이션": (
            "[R&D] + 소통/협업 관점입니다.  \n"
            "연구는 혼자 하는 것이 아닙니다. 설계·검증·공정 팀 또는 석·박사 연구원과 기술 난제를 함께 해결해 본 경험이 있다면, "
            "당시 사용했던 용어·자료(블록 다이어그램, 타이밍 다이어그램 등)를 어떻게 조율했는지 중심으로 정리해 두세요."
        ),
    },
    "공정/제조/설비": {
        "분석적 사고": (
            "[공정/품질] + 데이터 분석 관점입니다.  \n"
            "수율(Yield) 개선을 위해 공정 변수(Parameter)와 불량률 간의 상관관계를 분석해 본 경험을 강조하세요. "
            "엑셀·Python·JMP·Spotfire 등을 활용해 트렌드·산점도·상관계수 등을 시각화한 사례를 준비하면 좋습니다."
        ),
        "문제 해결": (
            "[공정/품질] + 문제 해결, 그리고 [설비] + 문제 해결 관점을 함께 담습니다.  \n"
            "감이나 경험치가 아니라, Fishbone, 5 Whys 같은 RCA(Root Cause Analysis) 툴을 사용해 문제 원인을 추적하고 재발을 막은 사례를 준비하세요.  \n"
            "특히 장비 다운타임을 줄이기 위해 예지보전(PdM) 개념이나 기구학·유체역학 지식을 활용한 경험이 있다면 강하게 어필할 수 있습니다."
        ),
        "수치/정확성": (
            "Fab에서는 파라미터 1~2% 오차가 큰 손실로 이어질 수 있습니다.  \n"
            "공정 조건·레시피·체크리스트를 얼마나 꼼꼼하게 관리했는지, FMEA나 점검표를 통해 불량률을 얼마나 줄였는지 수치 중심으로 설명하세요."
        ),
        "커뮤니케이션": (
            "공정 변경·라인 이슈를 생산·품질·설비·외주사와 함께 조율한 경험이 있다면, 그 과정을 단계별로 정리해 두세요.  \n"
            "특히 OCAP(Out of Control Action Plan)와 같은 프로세스에 참여한 경험이 있다면, 어떤 역할을 했는지 구체적으로 설명하면 좋습니다."
        ),
    },
    "품질/수율(QA)": {
        "분석적 사고": (
            "[공정/품질] + 문제 해결 관점과 연결됩니다.  \n"
            "Fishbone, 5 Whys, Pareto 차트와 같은 도구를 사용해 불량 원인을 구조적으로 분석하고 재발을 막은 경험을 준비하세요."
        ),
        "수치/정확성": (
            "Cpk/PPK, 불량률, 신뢰성 시험 결과 등 품질 지표를 숫자로 관리해 본 경험을 강조하세요.  \n"
            "미세한 이상 징후를 조기에 포착해 큰 이슈를 막은 사례가 있다면 매우 설득력 있는 스토리가 됩니다."
        ),
        "문제 해결": (
            "고객사 클레임이나 내부 품질 이슈를 단순 봉합이 아닌 '재발 방지' 수준까지 끌어올린 경험이 중요합니다.  \n"
            "표준 개정, 교육, 설비 변경 등 구체적인 액션과 그 후의 지표 변화를 함께 설명해 보세요."
        ),
        "커뮤니케이션": (
            "품질 직무는 숫자와 스토리를 동시에 다룹니다.  \n"
            "8D Report, A3 Report 같은 형식을 참고해 본인의 프로젝트를 정리하고, 고객사·내부 조직에 어떻게 설명했는지 구조화해서 말할 수 있도록 준비하세요."
        ),
    },
    "경영/기획/전략": {
        "분석적 사고": (
            "산업 리포트와 기업 IR 자료를 기반으로 CAPEX·R&D 비율, ASP, 수출 지표를 분석해 본 경험을 강조하세요.  \n"
            "단순 요약이 아니라, \"그래서 어떤 전략이 필요한가?\"까지 자신의 의견을 붙이는 것이 중요합니다."
        ),
        "커뮤니케이션": (
            "전략/기획 직무는 숫자를 스토리로 바꾸는 역할입니다.  \n"
            "산업/경쟁사 분석 결과를 A4 리포트와 5장 내외의 PPT로 요약해 발표해 본 경험이 있다면, 그 구조와 피드백을 중심으로 어필하세요."
        ),
    },
    "영업/마케팅/CS": {
        "커뮤니케이션": (
            "[영업/마케팅] + 소통 관점입니다.  \n"
            "고객사(예: 모바일·서버·자동차 OEM)의 기술 로드맵을 이해하고, 자사 기술 용어를 고객의 비즈니스 언어로 번역해 전달한 경험을 강조하세요.  \n"
            "프레젠테이션, 제안서, 미팅에서 어떤 식으로 표현을 바꿨는지 구체적인 문장 예시를 준비하면 좋습니다."
        ),
        "문제 해결": (
            "CS/Field 엔지니어 관점에서, 고객사 현장에서 발생한 장애를 어떻게 진단하고 조치했는지 구체적인 사례를 준비하세요.  \n"
            "다운타임(Down-time) 감소 시간, 재방문률 감소 등 수치로 표현할 수 있다면 설득력이 크게 올라갑니다."
        ),
    },
}


def show_company_and_specs_ui():
    """반도체/디스플레이 산업 기업·스펙 지도를 설문 전에 보여주는 안내 섹션"""
    with st.expander("🗺️ K-Semicon & Display 취업 대동여지도 (기업 & 스펙 가이드)", expanded=False):
        st.markdown(
            """
            맞춤형 전략을 세우기 전에, **어떤 회사들이 어떤 지역·직무 중심으로 채용하는지** 먼저 큰 그림을 보세요.  
            각 기업명을 클릭하면 채용/회사 페이지로 이동할 수 있습니다.

            ---
            """
        )

        def render_company_block(title: str, companies: list, tier_desc: str):
            st.markdown(f"#### {title}")
            st.caption(tier_desc)
            for c in companies:
                tip = c.get("Tip", "")
                st.markdown(
                    f"- **{c['기업']}**  \n"
                    f"  - **주력**: {c['주력']}  \n"
                    f"  - **위치**: {c['위치']}  \n"
                    f"  - **스펙/우대**: {c['스펙']}  \n"
                    + (f"  - **Tip**: {tip}  \n" if tip else "")
                    + f"  - **링크**: [{c['링크']}]({c['링크']})"
                )
            st.markdown("---")

        render_company_block(
            "■ [Tier 1] 반도체 종합 기업 (IDM / 파운드리)",
            IDM_COMPANIES,
            "산업의 심장 역할을 하는 종합 반도체 기업들입니다.",
        )
        render_company_block(
            "■ [Tier 1.5] 팹리스 (설계 전문)",
            FABLESS_COMPANIES,
            "수도권 R&D 중심, 설계/임베디드 직무 비중이 높습니다.",
        )
        render_company_block(
            "■ [Tier 2] OSAT (패키징/테스트)",
            OSAT_COMPANIES,
            "충청권 중심의 후공정/패키징 알짜 기업입니다.",
        )
        render_company_block(
            "■ [Global] 외국계 장비사",
            FOREIGN_EQUIP,
            "연봉 상위권, 영어와 글로벌 커뮤니케이션 역량이 중요합니다.",
        )
        render_company_block(
            "■ [Hidden Champion] 국내 소부장 (장비/소재)",
            LOCAL_EQUIP,
            "높은 성장성과 기술력을 가진 중견 장비·소재 기업입니다.",
        )

        st.info(
            "📢 **취업 전략 힌트**  \n"
            "1) 판교·화성 등 수도권은 설계/R&D 직무 경쟁이 매우 치열합니다.  \n"
            "2) 천안·아산·청주 라인(OSAT, 소부장)은 공정/설비 엔지니어 T/O가 많아 기회가 많습니다.  \n"
            "3) 외국계 장비사는 직무 역량만큼이나 영어가 서류 통과의 핵심이 될 수 있습니다."
        )


def build_keywords(industry: str, sub_industry: str, job_role: str, strength_label: str) -> Dict[str, Any]:
    """키워드 클라우드용 추천 해시태그 생성 (semi.prd.md 로직 간략화 버전)"""
    keywords = set()
    keywords.add(industry)
    keywords.add(sub_industry.split("(")[0])
    keywords.add(job_role.split("(")[0])

    # 강점 관련
    if strength_label == "분석적 사고":
        keywords.update(["데이터 분석", "가설 검증", "근본 원인", "논리적 사고"])
    if strength_label == "문제 해결":
        keywords.update(["Trouble Shooting", "디버깅", "원인 분석", "재발 방지"])
    if strength_label == "수치/정확성":
        keywords.update(["수율(Yield)", "정량 분석", "신뢰성", "SPC"])
    if strength_label == "커뮤니케이션":
        keywords.update(["협업", "보고서", "설득력", "VOC", "B2B"])

    # 직무별
    if job_role == "R&D(회로/설계)":
        keywords.update(["EDA", "Verilog", "VLSI", "컴퓨터 구조", "PDK", "Setup/Hold"])
    if job_role == "R&D(소자/재료)":
        keywords.update(["TCAD", "고체물리", "신소자", "EUV", "GAA", "TSV"])
    if job_role == "공정/제조/설비":
        keywords.update(["8대 공정", "SPC", "FMEA", "JMP", "CapEx"])
    if job_role == "품질/수율(QA)":
        keywords.update(["불량 분석", "신뢰성", "JMP", "ISO", "VOC"])
    if job_role == "경영/기획/전략":
        keywords.update(["SCM", "시장 분석", "재무제표", "사이클 산업", "경쟁사 분석"])
    if job_role == "영업/마케팅/CS":
        keywords.update(["B2B", "기술 영업", "고객사 대응", "로드맵", "Needs 분석"])

    # 산업/트렌드
    if industry == "반도체":
        keywords.update(["HBM", "AI 반도체", "파운드리", "TSMC", "Nvidia", "CXL"])
    if industry == "디스플레이":
        keywords.update(["OLED", "XR", "전장 디스플레이", "LTPO"])

    return {"keywords": sorted(list(keywords))}


def describe_market(trends: Dict[str, Any]) -> str:
    """CAGR를 바탕으로 산업 기상도 성격 요약"""
    prod_cagr = trends.get("production_cagr", np.nan)
    price_cagr = trends.get("price_cagr", np.nan)

    if not (np.isnan(prod_cagr) or np.isnan(price_cagr)):
        if prod_cagr > 0.03 and price_cagr > 0.03:
            return "초호황기(Super Cycle)에 가까운 국면으로, 생산과 가격이 함께 상승하는 구간입니다."
        elif prod_cagr > 0.03 and price_cagr < -0.03:
            return "증설 경쟁 성격이 강한 국면으로, 생산은 늘지만 가격은 압박을 받는 상황입니다."
        elif prod_cagr < 0 and price_cagr < -0.03:
            return "다운 사이클(불황기)에 가까운 구간으로, 구조조정·효율화와 차세대 기술 준비가 병행되는 시기입니다."
        elif abs(prod_cagr) < 0.03 and abs(price_cagr) < 0.03:
            return "안정/정체 국면으로, 대규모 확장보다는 기술 고도화·효율화 중심의 채용이 이뤄집니다."
        else:
            return "변동성이 큰 구간으로, 생산과 가격 지표의 방향성이 엇갈리고 있습니다."
    return "데이터가 충분하지 않아 산업 기상도를 정교하게 판단하기 어렵습니다."


def generate_recommendation(trends: Dict[str, Any], survey: Dict[str, Any]) -> Dict[str, Any]:
    """산업 데이터 + 설문 응답 기반 종합 가이드 생성"""
    industry = survey.get("industry")
    sub_industry = survey.get("sub_industry")
    status = survey.get("status")
    job_role = survey.get("job_role")
    major = survey.get("major")
    strength = survey.get("strength")
    environment = survey.get("environment")
    biz_talk = survey.get("biz_talk")
    theory_level = survey.get("theory_level")

    result: Dict[str, Any] = {}

    # 1) 산업 기상도 설명
    result["market_summary"] = describe_market(trends)

    # 2) 상태 진단 기반 시기 조언
    status_key = status or ""
    if "입문" in status_key:
        status_tip = STATUS_TIPS["입문 단계"]
    elif "전공 공부" in status_key:
        status_tip = STATUS_TIPS["전공은 하나 직무 경험 부족"]
    elif "기본 경험" in status_key:
        status_tip = STATUS_TIPS["기본 경험 보유"]
    elif "포트폴리오" in status_key:
        status_tip = STATUS_TIPS["본격 취업 준비 중"]
    elif "인턴/계약직" in status_key or "실무 경험" in status_key:
        status_tip = STATUS_TIPS["실무 경험 보유"]
    else:
        status_tip = "현재 상황에 맞는 구체적인 목표와 타임라인을 먼저 정의해 보세요."
    result["status_tip"] = status_tip

    # 3) 직무 + 강점 기반 심층 조언
    strength_label = None
    if strength:
        if "분석적 사고력" in strength:
            strength_label = "분석적 사고"
        elif "문제 해결 능력" in strength:
            strength_label = "문제 해결"
        elif "수치감각/정확성" in strength:
            strength_label = "수치/정확성"
        elif "커뮤니케이션" in strength:
            strength_label = "커뮤니케이션"

    core_advice = ""
    job_dict = JOB_STRENGTH_TIPS.get(job_role or "", {})
    if strength_label:
        core_advice = job_dict.get(strength_label, "")
    result["core_advice"] = core_advice

    # 4) 전공/전문성 보완 조언 (Q4, Q5, Q7 조건 기반)
    complement_tips = []
    # Q5 = R&D 이면서 Q7 = "하"
    if job_role and job_role.startswith("R&D") and theory_level == "하":
        complement_tips.append(
            "석사 수준 전공지식이 요구됩니다. 핵심 과목(소자, 공정, VLSI)을 전공서 기준으로 다시 정리하는 것이 필수입니다."
        )
    # Q4 = 상경/인문계열 이면서 Q5 = 기술 직무(공정/품질/소자)
    if major == "상경/인문계열" and job_role in ["공정/제조/설비", "품질/수율(QA)", "R&D(소자/재료)"]:
        complement_tips.append(
            "8대 공정, 반도체/디스플레이 기본 구조 등 기술 기초 교육(K-MOOC 등)을 반드시 이수하는 것을 추천합니다."
        )
    # Q5 = 영업/마케팅/CS 또는 경영/기획/전략 이면서 Biz Talk = 불가능
    if job_role in ["영업/마케팅/CS", "경영/기획/전략"] and biz_talk == "불가능":
        complement_tips.append(
            "B2B 회화 능력이 중요합니다. OPIc IH 또는 토익스피킹 고득점을 목표로 별도의 말하기 학습 플랜을 세워야 합니다."
        )
    result["complement_tips"] = complement_tips

    # 5) 예상 면접 질문 (최신 기술 트렌드 기반)
    interview_questions = []

    # ① 반도체 - 메모리 (DRAM/NAND)
    if industry == "반도체" and ("메모리" in (sub_industry or "") or "DRAM" in (sub_industry or "") or "NAND" in (sub_industry or "")):
        interview_questions.extend(
            [
                "DRAM 커패시터 용량을 확보하기 위해 사용되는 공정/소자 기술 3가지는 무엇인가요? (예: High-K 물질, 3D 구조, HARC Etch 등)",
                "NAND의 적층 수(Layer)가 높아짐에 따라 Channel Hole Etch 난이도가 왜 증가하는지, 그리고 이를 해결하기 위한 공정/장비 측면의 대응 방안을 설명해 보세요.",
            ]
        )
        if job_role == "R&D(회로/설계)":
            interview_questions.append(
                "HBM의 핵심인 TSV(Through Silicon Via) 기술의 주요 이슈(열 방출, 휨 현상 등)와 본딩 기술(MR-MUF 등)에 대해 아는 대로 설명해 보세요."
            )

    # ② 반도체 - 파운드리/시스템
    if industry == "반도체" and ("시스템 반도체" in (sub_industry or "") or "파운드리" in (sub_industry or "")):
        interview_questions.extend(
            [
                "FinFET과 GAA(Gate-All-Around) 구조의 차이점은 무엇이며, 미세 공정에서 GAA가 필수적인 이유(SCE 제어 등)는 무엇인가요?",
                "EUV(극자외선) 공정이 도입되면서 PR(포토레지스트), 펠리클 등 소재 기술에는 어떤 변화와 요구 사항이 생겼는지 설명해 보세요.",
            ]
        )
        if job_role == "R&D(회로/설계)":
            interview_questions.append(
                "PDK(Process Design Kit)의 구성 요소는 무엇이며, 설계 엔지니어 입장에서 이를 어떻게 활용하는지 설명해 보세요."
            )

    # ③ 디스플레이 - OLED/모바일
    if industry == "디스플레이":
        interview_questions.extend(
            [
                "OLED의 청색 소자(Blue) 수명이 유독 짧은 물리적 이유와, 이를 개선하기 위한 최신 기술(Tandem 구조, 인광 소재 등)에 대해 설명해 보세요.",
                "LTPO TFT 기술이 모바일 기기의 전력 소모 감소에 어떻게 기여하는지, 가변 주사율과 연관 지어 설명해 보세요.",
                "대형 QD-OLED와 WOLED의 발광 구조 차이와 각각의 장단점을 비교해 보세요.",
            ]
        )

    # ④ 공통 / 소부장 / 설비
    interview_questions.extend(
        [
            "반도체 공정에서 '진공(Vacuum)'이 필요한 이유는 무엇이며, 진공 펌프(Cryo Pump, Turbo Pump 등)의 기본 원리를 설명해 보세요.",
            "플라즈마 식각 공정에서 이방성(Anisotropic) 식각과 등방성(Isotropic) 식각의 차이점과, 각각 어떤 공정 상황에서 적용되는지 설명해 보세요.",
        ]
    )
    result["interview_questions"] = interview_questions

    # 6) 키워드 클라우드
    kw = build_keywords(
        industry=industry or "",
        sub_industry=sub_industry or "",
        job_role=job_role or "",
        strength_label=strength_label or "",
    )
    result.update(kw)

    return result

def render_stepper(current_step: int):
    steps = [
        "1. 타겟 설정",
        "2. 상태 진단",
        "3. 직무 적합도",
        "4. 전문성 체크",
        "5. 결과 대시보드",
    ]
    st.markdown('<div class="stepper-container">', unsafe_allow_html=True)
    for idx, label in enumerate(steps, start=1):
        css_class = "stepper-item active" if idx == current_step else "stepper-item"
        st.markdown(
            f'<div class="{css_class}">{label}</div>',
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)


def card_button(label: str, desc: str, key: str, selected: bool) -> bool:
    """카드형 버튼 (columns 내에서 사용)"""
    selected_class = "selected" if selected else ""
    html = f"""
    <div class="card-button {selected_class}" id="{key}">
        <div class="card-title">{label}</div>
        <div class="card-desc">{desc}</div>
    </div>
    """
    clicked = st.markdown(html, unsafe_allow_html=True)
    return bool(clicked)


def radar_chart_for_strength(selected_strength: str):
    categories = ["분석적 사고", "문제 해결", "수치/정확성", "커뮤니케이션"]
    base = 2
    high = 5
    values = []
    for c in categories:
        if c in selected_strength:
            values.append(high)
        else:
            values.append(base)
    values.append(values[0])
    categories_closed = categories + [categories[0]]

    fig = go.Figure()
    fig.add_trace(
        go.Scatterpolar(
            r=values,
            theta=categories_closed,
            fill="toself",
            name="강점 프로파일",
            line=dict(color="#64FFDA"),
        )
    )
    fig.update_layout(
        polar=dict(
            bgcolor="#0A192F",
            radialaxis=dict(
                visible=True,
                range=[0, 5],
                gridcolor="#233554",
                linecolor="#233554",
                tickfont=dict(color="#8892B0"),
            ),
            angularaxis=dict(
                tickfont=dict(color="#E6F1FF"),
            ),
        ),
        showlegend=False,
        paper_bgcolor="#0A192F",
        plot_bgcolor="#0A192F",
        margin=dict(l=40, r=40, t=40, b=40),
    )
    st.plotly_chart(fig, use_container_width=True)


def step1_target_setting(df: pd.DataFrame):
    st.subheader("Step 1. 산업·세부 분야 타겟 설정")
    st.caption("먼저 \"어떤 산업의 어떤 영역\"을 노릴지부터 또렷하게 정리해 볼게요.")

    show_company_and_specs_ui()

    st.markdown(
        """
        <div class="question-card">
          <div class="question-header">
            <div class="question-pill">Q1</div>
            <div class="question-title">어떤 산업에서 커리어를 시작하고 싶나요?</div>
          </div>
          <div class="question-desc">
            반도체와 디스플레이 중, 본인이 더 흥미를 느끼거나 앞으로 성장성이 크다고 생각하는 산업을 골라주세요.
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    industry = st.radio(
        "관심 산업을 선택하세요.",
        options=["반도체", "디스플레이"],
        index=0,
        key="industry_radio",
        horizontal=True,
    )

    st.markdown(
        """
        <div class="question-card">
          <div class="question-header">
            <div class="question-pill">Q2</div>
            <div class="question-title">그 산업 안에서 특히 어떤 세부 분야가 끌리나요?</div>
          </div>
          <div class="question-desc">
            특정 기술(예: HBM, OLED) 또는 비즈니스 구조(파운드리, 팹리스)에 관심이 있다면 그에 맞는 세부 분야를 골라주세요.
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if industry == "반도체":
        sub = st.selectbox(
            "반도체 세부 분야를 선택하세요.",
            [
                "메모리(HBM,DRAM)",
                "시스템 반도체(파운드리,팹리스)",
                "소자/재료/장비",
            ],
            key="sub_industry_select",
        )
    else:
        sub = st.selectbox(
            "디스플레이 세부 분야를 선택하세요.",
            [
                "대형 패널(TV)",
                "중소형 패널(모바일,IT,XR)",
                "소자/재료/장비",
            ],
            key="sub_industry_select_display",
        )

    st.session_state.survey["industry"] = industry
    st.session_state.survey["sub_industry"] = sub
    st.session_state.survey["industry_prefix"] = industry

    # 선택한 산업 기준 최신 통계치 카드 표시
    st.markdown("---")
    st.markdown("**선택한 산업의 최신 통계 요약**")

    try:
        latest_year = int(df.index.max())
        row = df.loc[latest_year]

        prod_col = f"{industry}_생산(조원)"
        export_col = f"{industry}_수출(억불)"
        share_col = f"{industry}_시장점유율(퍼센트)"
        if industry == "반도체":
            price_col = "DRAM_가격(달러)"
            price_label = "DRAM 가격"
        else:
            price_col = "액정표시장치(LCD)_평균가격(달러)"
            price_label = "LCD 평균가격"

        c1, c2, c3, c4 = st.columns(4)

        def fmt(val, suffix=""):
            try:
                return f"{float(val):,.1f}{suffix}"
            except Exception:
                return "N/A"

        with c1:
            if prod_col in df.columns:
                st.markdown(
                    f"""
                    <div class="metric-card">
                        <div class="metric-title">생산 ({latest_year}년)</div>
                        <div class="metric-value">{fmt(row.get(prod_col, np.nan), ' 조원')}</div>
                        <div class="metric-sub">{industry} 연간 생산 규모</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        with c2:
            if export_col in df.columns:
                st.markdown(
                    f"""
                    <div class="metric-card">
                        <div class="metric-title">수출 ({latest_year}년)</div>
                        <div class="metric-value">{fmt(row.get(export_col, np.nan), ' 억불')}</div>
                        <div class="metric-sub">{industry} 연간 수출 실적</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        with c3:
            if share_col in df.columns:
                st.markdown(
                    f"""
                    <div class="metric-card">
                        <div class="metric-title">시장 점유율 ({latest_year}년)</div>
                        <div class="metric-value">{fmt(row.get(share_col, np.nan), ' %')}</div>
                        <div class="metric-sub">글로벌 시장 내 비중</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        with c4:
            if price_col in df.columns:
                st.markdown(
                    f"""
                    <div class="metric-card">
                        <div class="metric-title">{price_label} ({latest_year}년)</div>
                        <div class="metric-value">{fmt(row.get(price_col, np.nan), ' 달러')}</div>
                        <div class="metric-sub">산업 수익성에 직결되는 가격 지표</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
    except Exception:
        pass

    left, mid, right = st.columns([1, 2, 1])
    with mid:
        st.markdown("####")
        if st.button("다음 질문으로 ⮕"):
            st.session_state.current_step = 2


def step2_status_diagnosis():
    st.subheader("Step 2. 현재 준비 상태 진단")
    st.caption("지금 나의 출발선을 솔직하게 그려야, 현실적인 플랜이 나옵니다.")

    st.markdown(
        """
        <div class="question-card">
          <div class="question-header">
            <div class="question-pill">Q3</div>
            <div class="question-title">현재 취업 준비는 어느 정도 단계인가요?</div>
          </div>
          <div class="question-desc">
            이력서/자소서, 프로젝트, 인턴 경험 등을 기준으로 본인의 준비 수준을 가장 잘 설명하는 단계를 골라주세요.
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    status = st.selectbox(
        "현재 취업 준비 상태를 선택하세요.",
        [
            "이제 정보를 모으기 시작하는 단계이다. (입문 단계)",
            "전공 공부는 하고 있지만 직무 준비는 아직 부족하다.",
            "프로젝트·대외활동 등 기본 경험은 있다.",
            "포트폴리오·자기소개서 등 취업 준비를 본격적으로 하고 있다.",
            "인턴/계약직/실무 경험이 있어 실전 준비가 되어 있다.",
        ],
    )

    st.markdown(
        """
        <div class="question-card">
          <div class="question-header">
            <div class="question-pill">Q4</div>
            <div class="question-title">전공과 외국어 역량은 어느 정도인가요?</div>
          </div>
          <div class="question-desc">
            지원 직무와의 전공 적합도, 글로벌 커뮤니케이션 역량을 함께 고려해 볼게요.
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)
    with col1:
        major = st.selectbox(
            "전공 계열을 선택하세요.",
            [
                "전자공학",
                "재료/화학공학",
                "컴퓨터공학/SW",
                "기계공학",
                "산업공학",
                "상경/인문계열",
            ],
        )
    with col2:
        st.markdown("**외국어 능력**")
        toeic = st.selectbox("TOEIC 점수", ["800+", "700+", "600-"])
        opic = st.selectbox("OPIc 등급", ["IM2+", "IL", "NH", "없음"])
        biz_talk = st.radio("비즈니스 회화 가능 여부", ["가능", "불가능"], horizontal=True)

    st.session_state.survey["status"] = status
    st.session_state.survey["major"] = major
    st.session_state.survey["toeic"] = toeic
    st.session_state.survey["opic"] = opic
    st.session_state.survey["biz_talk"] = biz_talk

    prev_col, next_col = st.columns(2)
    with prev_col:
        if st.button("⟵ 이전 질문"):
            st.session_state.current_step = 1
    with next_col:
        if st.button("다음 질문으로 ⮕"):
            st.session_state.current_step = 3


def step3_job_fit():
    st.subheader("Step 3. 직무 적합도 & 강점 선택")
    st.caption("내가 잘할 수 있는 역할과 강점을 정리해, 기업이 기억하기 쉬운 포지션을 만들어 봅니다.")

    st.markdown(
        """
        <div class="question-card">
          <div class="question-header">
            <div class="question-pill">Q5</div>
            <div class="question-title">어떤 직무에서 가장 나다운 퍼포먼스를 낼 수 있을 것 같나요?</div>
          </div>
          <div class="question-desc">
            전공 지식, 프로젝트 경험, 성향을 모두 떠올리면서 가장 잘 맞는 직무를 골라주세요.
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    job_role = st.selectbox(
        "희망 직무를 선택하세요.",
        [
            "R&D(회로/설계)",
            "R&D(소자/재료)",
            "공정/제조/설비",
            "품질/수율(QA)",
            "경영/기획/전략",
            "영업/마케팅/CS",
        ],
    )

    st.markdown(
        """
        <div class="question-card">
          <div class="question-header">
            <div class="question-pill">Q6</div>
            <div class="question-title">이 직무에서 남들보다 강하다고 느끼는 나만의 무기는 무엇인가요?</div>
          </div>
          <div class="question-desc">
            면접에서 실제 에피소드로 풀어낼 수 있는 한 가지 강점을 고르고, 아래 레이더 차트를 통해 시각적으로 확인해 보세요.
          </div>
          <div class="question-footer">
            * 강점 선택에 따라 레이더 차트에서 해당 축이 강조됩니다.
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns([2, 1])
    with col1:
        strength = st.radio(
            "본인의 핵심 강점을 선택하세요.",
            [
                "분석적 사고력 (R&D/공정)",
                "문제 해결 능력 (장비/엔지니어)",
                "수치감각/정확성 (품질·수율)",
                "커뮤니케이션 (마케팅/전략/CS)",
            ],
        )

    with col2:
        st.markdown("**나의 강점 레이더 차트**")
        radar_chart_for_strength(strength)

    st.session_state.survey["job_role"] = job_role
    st.session_state.survey["strength"] = strength

    prev_col, next_col = st.columns(2)
    with prev_col:
        if st.button("⟵ 이전 질문", key="prev3"):
            st.session_state.current_step = 2
    with next_col:
        if st.button("다음 질문으로 ⮕", key="next3"):
            st.session_state.current_step = 4


def step4_expertise_check():
    st.subheader("Step 4. 전공 이해도 & 전문성 체크")
    st.caption("지원 직무에서 요구하는 전공 깊이와 지금 나의 이해 수준을 가볍게 체크해 봅니다.")

    st.markdown(
        """
        <div class="question-card">
          <div class="question-header">
            <div class="question-pill">Q7</div>
            <div class="question-title">핵심 개념(공정·장비·소자)에 대한 이해 수준은 어느 정도인가요?</div>
          </div>
          <div class="question-desc">
            예를 들어 반도체 공정 플로우, MOSFET 동작 원리, CVD·ALD, 빛의 파장/밴드갭 등 개념을
            친구에게 설명해 줄 수 있을 정도인지 떠올리면서 선택해 보세요.
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    theory_level = st.select_slider(
        "핵심 개념 이해도 수준을 선택하세요.",
        options=["하", "중", "상"],
        value="중",
    )
    st.session_state.survey["theory_level"] = theory_level

    st.markdown("---")
    st.write("모든 설문 입력이 완료되었다면, 아래 버튼을 눌러 맞춤형 대시보드를 확인해 보세요.")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("⟵ 이전 질문", key="prev4"):
            st.session_state.current_step = 3
    with col2:
        if st.button("결과 대시보드 보기 ⮕", key="to_result"):
            st.session_state.current_step = 5


def result_dashboard(df: pd.DataFrame):
    survey = st.session_state.survey

    industry = survey.get("industry", "반도체")
    trends = analyze_trends(df, survey.get("industry_prefix", industry))
    if not trends:
        st.error("최근(2020년 이후) 데이터가 충분하지 않아 분석이 어렵습니다.")
        return

    result = generate_recommendation(trends, survey)
    st.session_state.trends = trends
    st.session_state.recommendation = result

    st.subheader("Result. 맞춤형 취업 전략 대시보드")
    st.caption("산업 데이터와 설문 응답을 결합해, 당신만을 위한 K-산업 취업 전략을 제안합니다.")

    st.markdown("### 산업 기상도")
    col1, col2, col3, col4 = st.columns(4)

    prod_cagr = trends.get("production_cagr", np.nan)
    share_cagr = trends.get("share_cagr", np.nan)
    export_cagr = trends.get("export_cagr", np.nan)
    price_cagr = trends.get("price_cagr", np.nan)
    price_name = trends.get("price_name", "핵심 가격")

    def format_cagr(val: float) -> str:
        if np.isnan(val):
            return "N/A"
        arrow = "▲" if val > 0 else "▼" if val < 0 else "→"
        return f"{arrow} {val*100:.1f}%"

    with col1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">생산 규모</div>
                <div class="metric-value">{format_cagr(prod_cagr)}</div>
                <div class="metric-sub">{industry} 생산 CAGR</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">시장 점유율</div>
                <div class="metric-value">{format_cagr(share_cagr)}</div>
                <div class="metric-sub">글로벌 점유율 추세</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col3:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">수출 실적</div>
                <div class="metric-value">{format_cagr(export_cagr)}</div>
                <div class="metric-sub">{industry} 수출 CAGR</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col4:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">{price_name}</div>
                <div class="metric-value">{format_cagr(price_cagr)}</div>
                <div class="metric-sub">산업 수익성 지표</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        f"""
        <div class="speech-bubble">
            <b>[산업 해석]</b><br/>
            {result.get("market_summary", "")}
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### 직무·강점 기반 맞춤 가이드")
    col_left, col_right = st.columns([2, 1])

    with col_left:
        st.markdown(
            f"""
            <div class="speech-bubble">
                <b>[시기 조언]</b><br/>
                {result.get("status_tip", "")}
            </div>
            """,
            unsafe_allow_html=True,
        )
        if result.get("core_advice"):
            st.markdown(
                f"""
                <div class="speech-bubble">
                    <b>[직무·강점 전략]</b><br/>
                    {result.get("core_advice", "")}
                </div>
                """,
                unsafe_allow_html=True,
            )
        for tip in result.get("complement_tips", []):
            st.markdown(
                f"""
                <div class="speech-bubble">
                    <b>[보완 포인트]</b><br/>
                    {tip}
                </div>
                """,
                unsafe_allow_html=True,
            )

    with col_right:
        st.markdown("**예상 면접 질문**")
        for q in result.get("interview_questions", []):
            st.markdown(
                f"""
                <div class="speech-bubble">
                    {q}
                </div>
                """,
                unsafe_allow_html=True,
            )


    st.markdown("### 키워드 클라우드 (면접/자소서 해시태그)")
    tags_html = "".join(
        [f'<span class="tag">#{kw}</span>' for kw in result.get("keywords", [])]
    )
    st.markdown(tags_html, unsafe_allow_html=True)

    st.markdown("---")
    if st.button("⟵ 설문 다시 수정하기"):
        st.session_state.current_step = 1


def main():
    init_session_state()
    
    # CSS 재적용 (매 페이지 로드시)
    inject_css()
    
    # 기본 텍스트 표시 (디버깅용)
    st.write("")  # 빈 줄로 공간 확보

    st.markdown(
        '<div class="main-title">K-Career Navigator</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="subtitle">반도체·디스플레이 산업 데이터를 기반으로, 당신에게 최적화된 취업 전략을 설계합니다.</div>',
        unsafe_allow_html=True,
    )
    st.markdown("")

    with st.expander("📂 산업통상자원부 CSV 업로드 (선택 사항)", expanded=False):
        st.write(
            "공식 통계 CSV를 업로드하면 해당 데이터를 기반으로 산업 기상도를 분석합니다. "
            "업로드하지 않으면 시뮬레이션용 더미 데이터를 사용합니다."
        )
        uploaded = st.file_uploader("CSV 파일 선택", type=["csv"])

    df = load_data(uploaded)

    render_stepper(st.session_state.current_step)

    if st.session_state.current_step == 1:
        step1_target_setting(df)
    elif st.session_state.current_step == 2:
        step2_status_diagnosis()
    elif st.session_state.current_step == 3:
        step3_job_fit()
    elif st.session_state.current_step == 4:
        step4_expertise_check()
    elif st.session_state.current_step == 5:
        result_dashboard(df)


if __name__ == "__main__":
    main()
