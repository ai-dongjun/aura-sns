import streamlit as st
import datetime
import google.generativeai as genai
from concurrent.futures import ThreadPoolExecutor
from PIL import Image
import base64
import io
import time

# ══════════════════════════════════════════════════════
# PAGE CONFIG
# ══════════════════════════════════════════════════════
st.set_page_config(
    page_title="AURA — SNS 콘텐츠 스튜디오",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ══════════════════════════════════════════════════════
# CSS — 패션/뷰티 감성 컬러풀 트렌디 테마
# ══════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,900;1,700&family=Noto+Sans+KR:wght@300;400;500;700&family=DM+Mono&display=swap');

:root {
    --rose:    #FF6B9D;
    --coral:   #FF8C69;
    --peach:   #FFB347;
    --mint:    #4ECDC4;
    --lavender:#C77DFF;
    --sky:     #74B9FF;
    --bg:      #FFF8F9;
    --surface: #FFFFFF;
    --surface2:#FFF0F4;
    --text:    #2D1B2E;
    --text2:   #7A5F7E;
    --text3:   #B8A0BC;
    --border:  #F0D9E8;
}

/* ── 배경 ── */
html, body, .stApp {
    background: var(--bg) !important;
    font-family: 'Noto Sans KR', sans-serif;
}

/* ── 메시 그라디언트 배경 효과 ── */
.stApp::before {
    content: '';
    position: fixed;
    top: -50%;
    left: -20%;
    width: 60vw;
    height: 60vw;
    background: radial-gradient(circle, rgba(255,107,157,0.08) 0%, transparent 70%);
    pointer-events: none;
    z-index: 0;
}
.stApp::after {
    content: '';
    position: fixed;
    bottom: -30%;
    right: -10%;
    width: 50vw;
    height: 50vw;
    background: radial-gradient(circle, rgba(116,185,255,0.08) 0%, transparent 70%);
    pointer-events: none;
    z-index: 0;
}

/* ── 사이드바 ── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #FFF0F8 0%, #F5F0FF 100%) !important;
    border-right: 1px solid var(--border) !important;
}
section[data-testid="stSidebar"] > div {
    padding: 1.5rem 1.2rem;
}

/* ── 메인 컨테이너 ── */
.main .block-container {
    padding: 1.5rem 2.5rem 4rem !important;
    max-width: 1150px;
    position: relative;
    z-index: 1;
}

/* ── 히어로 ── */
.hero {
    background: linear-gradient(135deg, #FF6B9D 0%, #C77DFF 50%, #74B9FF 100%);
    border-radius: 24px;
    padding: 3rem 2.5rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '✦ ✧ ✦';
    position: absolute;
    top: 1rem; right: 2rem;
    font-size: 1.2rem;
    color: rgba(255,255,255,0.3);
    letter-spacing: 0.5rem;
}
.hero::after {
    content: '';
    position: absolute;
    bottom: -30px; right: -30px;
    width: 150px; height: 150px;
    background: rgba(255,255,255,0.08);
    border-radius: 50%;
}
.hero-eyebrow {
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: rgba(255,255,255,0.7);
    margin-bottom: 0.75rem;
}
.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: 3rem;
    font-weight: 900;
    color: white;
    line-height: 1.1;
    margin: 0 0 0.75rem;
    text-shadow: 0 2px 20px rgba(0,0,0,0.1);
}
.hero-title em {
    font-style: italic;
    font-weight: 700;
}
.hero-sub {
    color: rgba(255,255,255,0.85);
    font-size: 0.95rem;
    font-weight: 300;
    line-height: 1.6;
    max-width: 520px;
}

/* ── 플랫폼 뱃지 ── */
.platform-badges {
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
    margin-top: 1.5rem;
}
.pbadge {
    background: rgba(255,255,255,0.2);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.35);
    border-radius: 20px;
    padding: 0.3rem 0.9rem;
    font-size: 0.8rem;
    color: white;
    font-weight: 500;
}

/* ── 섹션 라벨 ── */
.slabel {
    font-family: 'DM Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: var(--rose);
    margin: 1.8rem 0 0.5rem;
    display: flex;
    align-items: center;
    gap: 0.4rem;
}
.slabel::after {
    content: '';
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, var(--border), transparent);
}

/* ── 입력 필드 ── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background: var(--surface) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: 12px !important;
    color: var(--text) !important;
    font-family: 'Noto Sans KR', sans-serif !important;
    transition: all 0.25s !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: var(--rose) !important;
    box-shadow: 0 0 0 3px rgba(255,107,157,0.12) !important;
}
.stTextInput label, .stTextArea label,
.stSelectbox label, .stFileUploader label,
.stRadio label, .stSlider label,
.stMultiselect label {
    color: var(--text2) !important;
    font-size: 0.8rem !important;
    font-weight: 600 !important;
}

/* ── 셀렉트박스 ── */
.stSelectbox > div > div {
    background: var(--surface) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: 12px !important;
}

/* ── 멀티셀렉트 ── */
.stMultiselect > div > div {
    background: var(--surface) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: 12px !important;
}

/* ── 파일 업로더 ── */
.stFileUploader > div {
    background: linear-gradient(135deg, #FFF0F8, #F5F0FF) !important;
    border: 2px dashed #E8C8E8 !important;
    border-radius: 16px !important;
    transition: all 0.2s !important;
}
.stFileUploader > div:hover {
    border-color: var(--rose) !important;
    background: linear-gradient(135deg, #FFE8F4, #EDE0FF) !important;
}

/* ── 메인 버튼 ── */
.stButton > button {
    background: linear-gradient(135deg, #FF6B9D, #C77DFF) !important;
    color: white !important;
    border: none !important;
    border-radius: 14px !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    padding: 0.85rem 2rem !important;
    font-family: 'Noto Sans KR', sans-serif !important;
    letter-spacing: 0.02em !important;
    transition: all 0.3s !important;
    box-shadow: 0 4px 20px rgba(255,107,157,0.3) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 30px rgba(255,107,157,0.45) !important;
}

/* ── 다운로드 버튼 ── */
.stDownloadButton > button {
    background: var(--surface2) !important;
    color: var(--rose) !important;
    border: 1.5px solid #F0C0D8 !important;
    border-radius: 10px !important;
    font-size: 0.82rem !important;
    font-weight: 600 !important;
    transition: all 0.2s !important;
}
.stDownloadButton > button:hover {
    background: #FFE0EE !important;
    border-color: var(--rose) !important;
    transform: none !important;
    box-shadow: none !important;
}

/* ── 탭 ── */
.stTabs [data-baseweb="tab-list"] {
    background: var(--surface2);
    border-radius: 14px;
    padding: 5px;
    gap: 3px;
    border: 1px solid var(--border);
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: var(--text3) !important;
    border-radius: 10px !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
    font-family: 'Noto Sans KR', sans-serif !important;
    padding: 0.55rem 1.3rem !important;
    transition: all 0.2s !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #FF6B9D, #C77DFF) !important;
    color: white !important;
    box-shadow: 0 2px 10px rgba(255,107,157,0.3) !important;
}

/* ── 결과 카드 ── */
.rcard {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 18px;
    padding: 1.75rem;
    margin: 1rem 0;
    position: relative;
    transition: box-shadow 0.2s;
}
.rcard:hover {
    box-shadow: 0 4px 24px rgba(255,107,157,0.1);
}
.rcard-stripe {
    position: absolute;
    top: 0; left: 0;
    width: 4px;
    height: 100%;
    border-radius: 18px 0 0 18px;
}
.stripe-insta  { background: linear-gradient(180deg, #FF6B9D, #C77DFF); }
.stripe-yt     { background: linear-gradient(180deg, #FF4444, #FF8C69); }
.stripe-thread { background: linear-gradient(180deg, #2D1B2E, #7A5F7E); }
.stripe-hash   { background: linear-gradient(180deg, #4ECDC4, #74B9FF); }

.rtag {
    display: inline-block;
    font-family: 'DM Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    padding: 0.2rem 0.65rem;
    border-radius: 6px;
    margin-bottom: 1rem;
    margin-left: 0.5rem;
}
.rtag-insta  { background: #FFE8F4; color: var(--rose); }
.rtag-yt     { background: #FFE8E8; color: #FF4444; }
.rtag-thread { background: #EDE8F0; color: var(--text2); }
.rtag-hash   { background: #E8F8F7; color: var(--mint); }

.rcontent {
    white-space: pre-wrap;
    line-height: 1.9;
    color: var(--text);
    font-size: 0.88rem;
    margin-left: 0.5rem;
}

/* ── 통계 카드 ── */
.stats-row {
    display: flex;
    gap: 1rem;
    margin: 1.5rem 0;
    flex-wrap: wrap;
}
.stat-box {
    flex: 1;
    min-width: 120px;
    border-radius: 16px;
    padding: 1.2rem 1rem;
    text-align: center;
}
.stat-box.pink   { background: linear-gradient(135deg, #FFD6E7, #FFF0F8); border: 1px solid #FFCCD9; }
.stat-box.purple { background: linear-gradient(135deg, #E8D5FF, #F5EEFF); border: 1px solid #D4B8FF; }
.stat-box.mint   { background: linear-gradient(135deg, #C8F4F1, #EDFAF8); border: 1px solid #A8EAE5; }
.stat-box.peach  { background: linear-gradient(135deg, #FFE5CC, #FFF5EB); border: 1px solid #FFD1AA; }
.stat-num  { font-family: 'Playfair Display', serif; font-size: 2rem; font-weight: 900; line-height: 1; }
.stat-lbl  { font-size: 0.7rem; color: var(--text2); margin-top: 0.3rem; font-weight: 500; }
.pink   .stat-num { color: var(--rose); }
.purple .stat-num { color: var(--lavender); }
.mint   .stat-num { color: var(--mint); }
.peach  .stat-num { color: var(--coral); }

/* ── 사이드바 ── */
.sb-logo {
    font-family: 'Playfair Display', serif;
    font-size: 1.6rem;
    font-weight: 900;
    background: linear-gradient(135deg, #FF6B9D, #C77DFF);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.sb-sec {
    font-family: 'DM Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: var(--text3);
    margin: 1.5rem 0 0.5rem;
}

/* ── 알림 ── */
.stAlert { border-radius: 12px !important; }

/* ── 진행바 ── */
.stProgress > div > div {
    background: linear-gradient(90deg, #FF6B9D, #C77DFF, #74B9FF) !important;
    border-radius: 4px !important;
}

/* ── 빈 상태 ── */
.empty-state {
    text-align: center;
    padding: 5rem 2rem;
    color: var(--text3);
}
.empty-icon { font-size: 3rem; margin-bottom: 1rem; }
.empty-text { font-size: 0.9rem; line-height: 1.7; color: var(--text2); }

/* ── 샘플 라이브러리 카드 ── */
.lib-card {
    background: linear-gradient(135deg, #FFF5FB, #F5EEFF);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 0.85rem 1.1rem;
    margin: 0.4rem 0;
    font-size: 0.83rem;
    color: var(--text2);
}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
# API KEY — Streamlit Secrets에서 로드 (숨김 처리)
# ══════════════════════════════════════════════════════
try:
    gemini_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    gemini_key = None

# ══════════════════════════════════════════════════════
# SESSION STATE
# ══════════════════════════════════════════════════════
for k, v in {
    "results": {},
    "hashtags": "",
    "generated": False,
    "sample_library": [],
    "gen_count": 0,
    "last_gen_time": None,
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── 사용량 제한 설정 ──
MAX_PER_SESSION = 10      # 세션당 최대 생성 횟수
COOLDOWN_SECONDS = 20     # 연속 생성 쿨다운 (초)

# ══════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════
with st.sidebar:
    st.markdown('<div class="sb-logo">✦ AURA</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:0.72rem;color:#B8A0BC;margin-bottom:0.5rem;">SNS 콘텐츠 자동화 스튜디오</div>', unsafe_allow_html=True)

    # API 키 입력창 제거 — 서버에서 자동 로드됨
    remaining = MAX_PER_SESSION - st.session_state.gen_count
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#FFE8F4,#EDE0FF);border:1px solid #F0C0D8;
                border-radius:12px;padding:0.9rem 1rem;margin-bottom:0.5rem;">
        <div style="font-size:0.62rem;font-family:'DM Mono',monospace;letter-spacing:0.12em;
                    color:#C77DFF;text-transform:uppercase;margin-bottom:0.4rem;">이용 현황</div>
        <div style="font-size:1.4rem;font-weight:900;color:#FF6B9D;font-family:'Playfair Display',serif;">
            {remaining}<span style="font-size:0.75rem;color:#B8A0BC;font-family:'Noto Sans KR',sans-serif;"> / {MAX_PER_SESSION} 회</span>
        </div>
        <div style="font-size:0.72rem;color:#B8A0BC;margin-top:0.2rem;">남은 생성 횟수</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sb-sec">📱 플랫폼</div>', unsafe_allow_html=True)
    plat_insta   = st.checkbox("📸 인스타그램", value=True)
    plat_youtube = st.checkbox("📺 유튜브", value=True)
    plat_thread  = st.checkbox("🧵 스레드 / 트위터(X)", value=True)

    st.markdown('<div class="sb-sec">🎨 콘텐츠 설정</div>', unsafe_allow_html=True)
    industry = st.selectbox("분야", [
        "패션 (의류/스타일링)", "뷰티 (스킨케어/메이크업)",
        "패션+뷰티 통합", "음식/카페", "라이프스타일", "여행", "피트니스", "IT/기술"
    ])
    tone = st.selectbox("톤앤매너", [
        "감성적·공감형 🌸", "트렌디·자극형 ✨", "정보전달·전문형 📋",
        "고급·럭셔리 💎", "유머·가벼운 😄"
    ])
    target = st.selectbox("타겟층", [
        "10대 후반 ~ 20대 초반", "20대 여성", "20~30대 MZ세대",
        "30대 직장인", "전 연령 범용"
    ])

    st.markdown('<div class="sb-sec">🏷️ 해시태그</div>', unsafe_allow_html=True)
    hash_count = st.slider("해시태그 수", 10, 30, 20)
    hash_lang  = st.radio("언어", ["한국어+영어 혼합", "한국어만", "영어만"], horizontal=False)

    st.markdown('<div class="sb-sec">📚 샘플 라이브러리</div>', unsafe_allow_html=True)
    lib_count = len(st.session_state.sample_library)
    st.markdown(f'<div style="font-size:0.78rem;color:#C77DFF;font-weight:600;">저장된 샘플: {lib_count}개</div>', unsafe_allow_html=True)
    if lib_count >= 5:
        st.success(f"✦ {lib_count}개 샘플 확보! 이미지 없이도 스타일 생성 가능합니다.")

# ══════════════════════════════════════════════════════
# HERO HEADER
# ══════════════════════════════════════════════════════
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">✦ AI-Powered SNS Content Studio</div>
    <h1 class="hero-title">당신의 피드를<br><em>완전히 바꿀</em> AI</h1>
    <p class="hero-sub">
        사진 한 장 또는 주제 한 줄만으로 —<br>
        인스타그램, 유튜브, 스레드용 콘텐츠와 노출 최적화 해시태그를 동시에 완성합니다.
    </p>
    <div class="platform-badges">
        <span class="pbadge">📸 Instagram</span>
        <span class="pbadge">📺 YouTube</span>
        <span class="pbadge">🧵 Threads / X</span>
        <span class="pbadge">🏷️ 해시태그 최적화</span>
        <span class="pbadge">🖼️ 이미지 AI 분석</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
# INPUT SECTION
# ══════════════════════════════════════════════════════
col_left, col_right = st.columns([1.15, 1], gap="large")

with col_left:
    st.markdown('<div class="slabel">콘텐츠 정보 입력</div>', unsafe_allow_html=True)

    topic = st.text_area(
        "주제 & 방향",
        placeholder="예시:\n나이키 x 자크뮈스 문 슈즈 신제품 리뷰\n- 클래식함과 근본 있는 스타일 강조\n- MZ세대 데일리룩 연결\n- 착용감과 디자인 포인트 위주",
        height=160,
        help="구체적으로 쓸수록 퀄리티가 높아집니다."
    )

    col_kw, col_br = st.columns(2)
    with col_kw:
        keywords = st.text_input("핵심 키워드", placeholder="패션, 신발, 데일리룩")
    with col_br:
        brand = st.text_input("브랜드명 (선택)", placeholder="Nike, 올리브영 ...")

    col_mood, col_len = st.columns(2)
    with col_mood:
        mood = st.selectbox("무드/감성", [
            "미니멀 & 클린", "빈티지 레트로", "스트릿 & 엣지",
            "로맨틱 & 걸리쉬", "하이패션 & 럭셔리", "캐주얼 & 편안"
        ])
    with col_len:
        yt_type = st.selectbox("유튜브 영상 길이", [
            "쇼츠 (60초)", "미들폼 (5~10분)", "롱폼 (15분+)"
        ])

with col_right:
    st.markdown('<div class="slabel">이미지 업로드 (선택)</div>', unsafe_allow_html=True)
    uploaded = st.file_uploader(
        "이미지",
        type=["jpg","jpeg","png","webp"],
        accept_multiple_files=True,
        label_visibility="collapsed",
        help="최대 4장. AI가 이미지를 분석해 더 정확한 콘텐츠를 생성합니다."
    )

    if uploaded:
        cols = st.columns(min(len(uploaded), 2))
        for i, f in enumerate(uploaded[:4]):
            with cols[i % 2]:
                st.image(Image.open(f), use_container_width=True)
        if len(uploaded) > 4:
            st.caption(f"+ {len(uploaded)-4}장 더 업로드됨")

        # 샘플 저장 옵션
        save_sample = st.checkbox("📚 이 이미지를 샘플 라이브러리에 저장")
        if save_sample:
            sample_label = st.text_input("샘플 레이블", placeholder="예: 나이키 스포츠웨어 룩")
    else:
        st.markdown("""
        <div style="background:linear-gradient(135deg,#FFF5FB,#F5EEFF);border:1px solid #F0D9E8;
                    border-radius:14px;padding:1.5rem;text-align:center;margin-top:0.5rem;">
            <div style="font-size:1.8rem;margin-bottom:0.5rem;">🖼️</div>
            <div style="font-size:0.82rem;color:#B8A0BC;line-height:1.6;">
                이미지 없이도 생성 가능합니다<br>
                <span style="color:#C77DFF;font-weight:600;">샘플 5개 이상</span> 저장 시<br>스타일 자동 반영
            </div>
        </div>
        """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
# GENERATE BUTTON
# ══════════════════════════════════════════════════════
st.markdown("<br>", unsafe_allow_html=True)
bc1, bc2, bc3 = st.columns([1, 1.6, 1])
with bc2:
    gen_btn = st.button("🌸 콘텐츠 자동 생성하기", use_container_width=True)

# ══════════════════════════════════════════════════════
# PROMPT BUILDERS
# ══════════════════════════════════════════════════════
def ctx():
    lib_hint = ""
    if st.session_state.sample_library:
        labels = [s["label"] for s in st.session_state.sample_library[-3:]]
        lib_hint = f"\n샘플 스타일 참고: {', '.join(labels)}"
    return f"""
분야: {industry}  |  톤앤매너: {tone}  |  타겟: {target}
무드/감성: {mood}  |  브랜드: {brand or '없음'}
핵심 키워드: {keywords or '없음'}
주제 및 방향:
{topic}
{lib_hint}
"""

def p_instagram():
    return f"""{ctx()}
인스타그램 피드 콘텐츠를 아래 형식으로 작성하세요.

━━━━━━━━━━━━━━━━━━━━━
📝 캡션 버전 A — 감성/스토리텔링형
━━━━━━━━━━━━━━━━━━━━━
(첫 줄: 스크롤을 멈추는 후킹 문장)
(본문 2~3문단: 감성적 묘사, 공감 유도)
(마무리: 부드러운 CTA + 질문)

━━━━━━━━━━━━━━━━━━━━━
📝 캡션 버전 B — 정보/트렌드형
━━━━━━━━━━━━━━━━━━━━━
(첫 줄: 숫자/통계/트렌드 기반 후킹)
(본문: 핵심 정보 or 아이템 소개)
(마무리: 행동 유도 CTA)

━━━━━━━━━━━━━━━━━━━━━
🗂️ 카드뉴스 구성안 (5장)
━━━━━━━━━━━━━━━━━━━━━
1장 [표지]: 제목 / 서브텍스트 / 배경 색감 & 폰트 제안
2장 [내용1]: 핵심 텍스트 (50자 이내) + 비주얼 제안
3장 [내용2]: 핵심 텍스트 (50자 이내) + 비주얼 제안
4장 [내용3]: 핵심 텍스트 (50자 이내) + 비주얼 제안
5장 [마무리]: 마무리 멘트 + CTA + 팔로우 유도 멘트

━━━━━━━━━━━━━━━━━━━━━
💬 스토리 & 릴스용 짧은 문구 (5가지)
━━━━━━━━━━━━━━━━━━━━━
(각 15자 이내, 임팩트 있게)
"""

def p_youtube():
    length_map = {
        "쇼츠 (60초)": "60초 / 약 150자 대본",
        "미들폼 (5~10분)": "7분 분량 / 약 1400자 대본",
        "롱폼 (15분+)": "15분 분량 / 약 3000자 대본"
    }
    return f"""{ctx()}
유튜브 영상 길이: {yt_type} ({length_map.get(yt_type,'')})

━━━━━━━━━━━━━━━━━━━━━
🖼️ 썸네일 카피 — 3가지 전략
━━━━━━━━━━━━━━━━━━━━━
[전략1 · 숫자/임팩트형]
 메인 텍스트(4자 이내): 
 서브 텍스트(12자 이내): 
 이미지 연출 제안: 

[전략2 · 호기심/질문형]
 메인 텍스트: 
 서브 텍스트: 
 이미지 연출 제안: 

[전략3 · 감성/공감형]
 메인 텍스트: 
 서브 텍스트: 
 이미지 연출 제안: 

━━━━━━━━━━━━━━━━━━━━━
📋 영상 제목 추천 5개 (클릭률 이유 포함)
━━━━━━━━━━━━━━━━━━━━━

━━━━━━━━━━━━━━━━━━━━━
🎬 대본 ({yt_type})
━━━━━━━━━━━━━━━━━━━━━
[오프닝 — 첫 3초 후킹]

[본론]

[클로징 — 구독/좋아요 CTA]

※ 구어체, 자연스럽게 / [카메라 지시사항] 포함
"""

def p_threads():
    return f"""{ctx()}
스레드(Threads) 및 트위터(X) 콘텐츠를 작성하세요.

━━━━━━━━━━━━━━━━━━━━━
🧵 스레드 — 연속 포스트 (5개 연결)
━━━━━━━━━━━━━━━━━━━━━
1/ (후킹 — 반드시 읽게 만드는 첫 문장)
2/ (핵심 내용 A)
3/ (핵심 내용 B)
4/ (공감 or 팁)
5/ (마무리 + 팔로우 유도 CTA)

━━━━━━━━━━━━━━━━━━━━━
🐦 트위터(X) 단문 3가지 (280자 이내)
━━━━━━━━━━━━━━━━━━━━━
[버전A · 공감형]
[버전B · 정보형]
[버전C · 트렌디/밈형]

━━━━━━━━━━━━━━━━━━━━━
🔁 리트윗 유도 문구 3가지
━━━━━━━━━━━━━━━━━━━━━
"""

def p_hashtags():
    return f"""{ctx()}
해시태그 언어: {hash_lang}
총 {hash_count}개, 노출성·광고 효과 최우선으로 작성하세요.

━━━━━━━━━━━━━━━━━━━━━
🔴 대형 해시태그 (게시물 100만+)  · {round(hash_count*0.3)}개
━━━━━━━━━━━━━━━━━━━━━
(각 태그 옆 예상 게시물 수 표기)

━━━━━━━━━━━━━━━━━━━━━
🟡 중형 해시태그 (10~100만)  · {round(hash_count*0.5)}개
━━━━━━━━━━━━━━━━━━━━━

━━━━━━━━━━━━━━━━━━━━━
🟢 소형 해시태그 (1~10만, 상위노출 집중)  · {round(hash_count*0.2)}개
━━━━━━━━━━━━━━━━━━━━━

━━━━━━━━━━━━━━━━━━━━━
💡 최적 조합 TOP 15 — 바로 복붙 가능하게 한 줄로
━━━━━━━━━━━━━━━━━━━━━

━━━━━━━━━━━━━━━━━━━━━
📈 이 조합 사용 시 예상 노출 효과 한 줄 요약
━━━━━━━━━━━━━━━━━━━━━
"""

# ══════════════════════════════════════════════════════
# GENERATION
# ══════════════════════════════════════════════════════
if gen_btn:
    active = [p for p, c in [
        ("📸 인스타그램", plat_insta),
        ("📺 유튜브",     plat_youtube),
        ("🧵 스레드/X",  plat_thread)
    ] if c]

    if not gemini_key:
        st.error("⚙️ 서버 설정 오류입니다. 관리자에게 문의해 주세요.")
        st.stop()
    elif not gemini_key.startswith("AIza"):
        st.error("⚙️ API 키 설정이 올바르지 않습니다. 관리자에게 문의해 주세요.")
        st.stop()
    elif st.session_state.gen_count >= MAX_PER_SESSION:
        st.error(f"🚫 세션당 최대 {MAX_PER_SESSION}회까지 사용 가능합니다. 브라우저를 새로 열어주세요.")
        st.stop()
    elif st.session_state.last_gen_time and \
         (datetime.datetime.now() - st.session_state.last_gen_time).seconds < COOLDOWN_SECONDS:
        left = COOLDOWN_SECONDS - (datetime.datetime.now() - st.session_state.last_gen_time).seconds
        st.warning(f"⏳ {left}초 후에 다시 생성할 수 있습니다.")
        st.stop()
    elif not topic.strip():
        st.warning("✏️ 주제 & 방향을 입력해 주세요.")
    elif not active:
        st.warning("📱 플랫폼을 최소 1개 선택해 주세요.")
    else:
        genai.configure(api_key=gemini_key)
        model = genai.GenerativeModel("gemini-2.0-flash")

        # 이미지 파트 준비
        image_parts = []
        if uploaded:
            for f in uploaded[:4]:
                try:
                    f.seek(0)
                    img = Image.open(f)
                    buf = io.BytesIO()
                    img.save(buf, format="PNG")
                    buf.seek(0)
                    image_parts.append({
                        "mime_type": "image/png",
                        "data": base64.b64encode(buf.read()).decode()
                    })
                except:
                    pass

        def generate(prompt_text):
            if image_parts:
                contents = [{"inline_data": p} for p in image_parts] + [prompt_text]
                return model.generate_content(contents).text
            return model.generate_content(prompt_text).text

        progress = st.progress(0, text="✨ 생성 준비 중...")
        total = len(active) + 1

        try:
            prompt_map = {}
            if "📸 인스타그램" in active: prompt_map["📸 인스타그램"] = p_instagram()
            if "📺 유튜브"     in active: prompt_map["📺 유튜브"]     = p_youtube()
            if "🧵 스레드/X"  in active: prompt_map["🧵 스레드/X"]  = p_threads()

            with ThreadPoolExecutor(max_workers=4) as ex:
                futures = {n: ex.submit(generate, p) for n, p in prompt_map.items()}
                hash_f  = ex.submit(generate, p_hashtags())

                results = {}
                done = 0
                for name, fut in futures.items():
                    results[name] = fut.result()
                    done += 1
                    progress.progress(int(done / total * 88),
                                      text=f"✦ {name} 완성!")

                hashtags = hash_f.result()
                progress.progress(100, text="🌸 완료!")

            time.sleep(0.5)
            progress.empty()

            st.session_state.results   = results
            st.session_state.hashtags  = hashtags
            st.session_state.generated = True
            st.session_state.gen_count += 1
            st.session_state.last_gen_time = datetime.datetime.now()

            # 샘플 저장
            if uploaded and 'save_sample' in dir() and save_sample:
                label = sample_label if 'sample_label' in dir() and sample_label else f"{industry} 샘플"
                st.session_state.sample_library.append({
                    "label": label,
                    "topic": topic[:30],
                    "industry": industry,
                    "mood": mood,
                    "count": len(uploaded)
                })

            st.success(f"✦ 콘텐츠 생성 완료! {len(results)}개 플랫폼 + 해시태그가 준비됐어요 🌸")

        except Exception as e:
            progress.empty()
            err = str(e)
            if "429" in err or "quota" in err.lower():
                st.error("⏱️ API 할당량을 초과했습니다. 잠시 후 다시 시도하거나, Google AI Studio에서 새 API 키를 발급받으세요.")
            else:
                st.error(f"오류: {e}")

# ══════════════════════════════════════════════════════
# RESULTS
# ══════════════════════════════════════════════════════
if st.session_state.generated and st.session_state.results:
    st.markdown("<br>", unsafe_allow_html=True)

    # 통계 배지
    n_plat = len(st.session_state.results)
    n_img  = len(uploaded) if uploaded else 0
    n_samp = len(st.session_state.sample_library)
    st.markdown(f"""
    <div class="stats-row">
        <div class="stat-box pink">
            <div class="stat-num">{n_plat}</div>
            <div class="stat-lbl">생성된 플랫폼</div>
        </div>
        <div class="stat-box purple">
            <div class="stat-num">{hash_count}</div>
            <div class="stat-lbl">최적화 해시태그</div>
        </div>
        <div class="stat-box mint">
            <div class="stat-num">{n_img}</div>
            <div class="stat-lbl">분석 이미지</div>
        </div>
        <div class="stat-box peach">
            <div class="stat-num">{n_samp}</div>
            <div class="stat-lbl">샘플 라이브러리</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 탭
    tab_names = list(st.session_state.results.keys()) + ["🏷️ 해시태그"]
    tabs = st.tabs(tab_names)

    stripe_map = {
        "📸 인스타그램": ("stripe-insta", "rtag-insta"),
        "📺 유튜브":     ("stripe-yt",    "rtag-yt"),
        "🧵 스레드/X":  ("stripe-thread","rtag-thread"),
    }

    for i, (name, content) in enumerate(st.session_state.results.items()):
        with tabs[i]:
            sc, tc = stripe_map.get(name, ("stripe-insta","rtag-insta"))
            st.markdown(f"""
            <div class="rcard">
                <div class="rcard-stripe {sc}"></div>
                <span class="rtag {tc}">{name}</span>
                <div class="rcontent">{content}</div>
            </div>
            """, unsafe_allow_html=True)

            d1, d2 = st.columns([1, 3])
            with d1:
                short = name.replace("📸","").replace("📺","").replace("🧵","").strip()
                st.download_button(
                    f"⬇ {short} 저장",
                    data=content,
                    file_name=f"{short}_{topic[:10].replace(' ','_')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )

    # 해시태그 탭
    with tabs[-1]:
        st.markdown(f"""
        <div class="rcard">
            <div class="rcard-stripe stripe-hash"></div>
            <span class="rtag rtag-hash">🏷️ 해시태그 최적화</span>
            <div class="rcontent">{st.session_state.hashtags}</div>
        </div>
        """, unsafe_allow_html=True)

        h1, h2 = st.columns([1, 2])
        with h1:
            st.download_button(
                "⬇ 해시태그 저장",
                data=st.session_state.hashtags,
                file_name=f"hashtags_{topic[:10].replace(' ','_')}.txt",
                mime="text/plain",
                use_container_width=True
            )
        with h2:
            all_txt = "\n\n".join(
                [f"{'='*40}\n{n}\n{'='*40}\n\n{c}"
                 for n, c in st.session_state.results.items()]
            ) + f"\n\n{'='*40}\n해시태그\n{'='*40}\n\n{st.session_state.hashtags}"
            st.download_button(
                "⬇ 전체 합본 다운로드",
                data=all_txt,
                file_name=f"AURA_전체_{topic[:10].replace(' ','_')}.txt",
                mime="text/plain",
                use_container_width=True
            )

    # 샘플 라이브러리
    if st.session_state.sample_library:
        st.markdown('<div class="slabel">📚 샘플 라이브러리</div>', unsafe_allow_html=True)
        cols = st.columns(min(len(st.session_state.sample_library), 3))
        for i, s in enumerate(st.session_state.sample_library):
            with cols[i % 3]:
                st.markdown(f"""
                <div class="lib-card">
                    <div style="font-weight:700;color:#C77DFF;font-size:0.85rem;">{s['label']}</div>
                    <div style="font-size:0.75rem;color:#B8A0BC;margin-top:0.2rem;">{s['industry']} · {s['mood']}</div>
                    <div style="font-size:0.72rem;color:#D4B8FF;margin-top:0.2rem;">이미지 {s['count']}장</div>
                </div>
                """, unsafe_allow_html=True)

        if len(st.session_state.sample_library) >= 5:
            st.info("💡 샘플 5개 이상 확보! 이제 이미지 없이 주제만 입력해도 스타일이 자동 반영됩니다.")

    # 초기화
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("↺ 새 콘텐츠 만들기"):
        st.session_state.results   = {}
        st.session_state.hashtags  = ""
        st.session_state.generated = False
        st.rerun()

else:
    st.markdown("""
    <div class="empty-state">
        <div class="empty-icon">🌸</div>
        <div class="empty-text">
            위에서 주제를 입력하고 생성 버튼을 눌러주세요<br>
            <span style="color:#C77DFF;font-weight:600;">이미지가 없어도 괜찮아요</span> —
            텍스트만으로도 완성도 높은 콘텐츠가 만들어집니다
        </div>
    </div>
    """, unsafe_allow_html=True)
