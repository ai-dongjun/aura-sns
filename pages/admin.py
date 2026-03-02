import streamlit as st
import json
import os

# ══════════════════════════════════════════════════════
# PAGE CONFIG
# ══════════════════════════════════════════════════════
st.set_page_config(
    page_title="AURA Admin — 프롬프트 관리",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ══════════════════════════════════════════════════════
# CSS
# ══════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=Noto+Sans+KR:wght@300;400;500;700&family=DM+Mono:wght@400;500&display=swap');

:root {
    --bg:      #0D0D14;
    --surface: #13131E;
    --surface2:#1A1A28;
    --border:  #2A2A40;
    --border2: #3A3A55;
    --text:    #E8E8F5;
    --text2:   #8888AA;
    --text3:   #5555770;
    --rose:    #FF6B9D;
    --purple:  #C77DFF;
    --mint:    #4ECDC4;
    --yellow:  #FFD93D;
    --red:     #FF6B6B;
    --green:   #6BCB77;
}

html, body, .stApp {
    background: var(--bg) !important;
    font-family: 'Noto Sans KR', sans-serif;
    color: var(--text);
}

.main .block-container {
    padding: 2rem 3rem 4rem !important;
    max-width: 1200px;
}

/* 헤더 */
.admin-header {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 1.5rem 0 2rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 2rem;
}
.admin-logo {
    font-family: 'Playfair Display', serif;
    font-size: 1.8rem;
    font-weight: 900;
    background: linear-gradient(135deg, #FF6B9D, #C77DFF);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.admin-badge {
    background: rgba(255,107,157,0.15);
    border: 1px solid rgba(255,107,157,0.3);
    border-radius: 6px;
    padding: 0.2rem 0.7rem;
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.12em;
    color: var(--rose);
    text-transform: uppercase;
}
.admin-sub {
    margin-left: auto;
    font-size: 0.78rem;
    color: var(--text2);
}

/* 비밀번호 화면 */
.lock-screen {
    text-align: center;
    padding: 6rem 2rem;
    max-width: 400px;
    margin: 0 auto;
}
.lock-icon {
    font-size: 3rem;
    margin-bottom: 1.5rem;
}
.lock-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.8rem;
    font-weight: 700;
    color: var(--text);
    margin-bottom: 0.5rem;
}
.lock-sub {
    font-size: 0.85rem;
    color: var(--text2);
    margin-bottom: 2rem;
    line-height: 1.6;
}

/* 탭 */
.stTabs [data-baseweb="tab-list"] {
    background: var(--surface);
    border-radius: 12px;
    padding: 4px;
    gap: 3px;
    border: 1px solid var(--border);
    margin-bottom: 1.5rem;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: var(--text2) !important;
    border-radius: 8px !important;
    font-size: 0.83rem !important;
    font-weight: 500 !important;
    font-family: 'Noto Sans KR', sans-serif !important;
    padding: 0.5rem 1.2rem !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #FF6B9D, #C77DFF) !important;
    color: white !important;
}

/* 프롬프트 카드 */
.prompt-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
}
.prompt-card-header {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 1rem;
}
.prompt-title {
    font-weight: 700;
    font-size: 0.95rem;
    color: var(--text);
}
.prompt-desc {
    font-size: 0.75rem;
    color: var(--text2);
    margin-top: 0.15rem;
}
.ptag {
    font-family: 'DM Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    padding: 0.2rem 0.6rem;
    border-radius: 5px;
    margin-left: auto;
}
.ptag-insta  { background: rgba(255,107,157,0.15); color: var(--rose); }
.ptag-yt     { background: rgba(255,107,107,0.15); color: var(--red); }
.ptag-thread { background: rgba(136,136,170,0.15); color: var(--text2); }
.ptag-hash   { background: rgba(78,205,196,0.15);  color: var(--mint); }
.ptag-ctx    { background: rgba(255,217,61,0.15);  color: var(--yellow); }

/* 입력 필드 */
.stTextArea > div > div > textarea {
    background: var(--surface2) !important;
    border: 1px solid var(--border2) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.82rem !important;
    line-height: 1.7 !important;
}
.stTextArea > div > div > textarea:focus {
    border-color: var(--rose) !important;
    box-shadow: 0 0 0 2px rgba(255,107,157,0.15) !important;
}
.stTextInput > div > div > input {
    background: var(--surface2) !important;
    border: 1px solid var(--border2) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
    font-family: 'Noto Sans KR', sans-serif !important;
}
.stTextInput > div > div > input:focus {
    border-color: var(--rose) !important;
    box-shadow: 0 0 0 2px rgba(255,107,157,0.15) !important;
}
.stTextInput label, .stTextArea label {
    color: var(--text2) !important;
    font-size: 0.78rem !important;
    font-weight: 600 !important;
}

/* 버튼 */
.stButton > button {
    background: linear-gradient(135deg, #FF6B9D, #C77DFF) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    font-size: 0.88rem !important;
    padding: 0.65rem 1.5rem !important;
    font-family: 'Noto Sans KR', sans-serif !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 16px rgba(255,107,157,0.35) !important;
}

/* 초기화 버튼 */
.reset-btn > button {
    background: var(--surface2) !important;
    color: var(--text2) !important;
    border: 1px solid var(--border2) !important;
}
.reset-btn > button:hover {
    border-color: var(--red) !important;
    color: var(--red) !important;
    box-shadow: none !important;
}

/* 저장됨 배지 */
.saved-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.3rem;
    background: rgba(107,203,119,0.15);
    border: 1px solid rgba(107,203,119,0.3);
    border-radius: 6px;
    padding: 0.25rem 0.75rem;
    font-size: 0.75rem;
    color: var(--green);
    font-weight: 600;
}

/* 통계 */
.stat-row {
    display: flex;
    gap: 1rem;
    margin-bottom: 2rem;
    flex-wrap: wrap;
}
.stat-mini {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1rem 1.25rem;
    min-width: 140px;
}
.stat-mini-num {
    font-family: 'Playfair Display', serif;
    font-size: 1.6rem;
    font-weight: 900;
    color: var(--rose);
}
.stat-mini-lbl {
    font-size: 0.7rem;
    color: var(--text2);
    margin-top: 0.2rem;
}

/* 알림 */
.stAlert { border-radius: 10px !important; }

/* 구분선 */
hr { border-color: var(--border) !important; }

/* 팁 박스 */
.tip-box {
    background: rgba(255,217,61,0.08);
    border: 1px solid rgba(255,217,61,0.2);
    border-radius: 10px;
    padding: 1rem 1.25rem;
    font-size: 0.82rem;
    color: var(--yellow);
    line-height: 1.7;
    margin: 1rem 0;
}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
# 기본 프롬프트 (초기값)
# ══════════════════════════════════════════════════════
DEFAULT_PROMPTS = {
    "context": """{industry} | {tone} | {target}
무드/감성: {mood} | 브랜드: {brand}
핵심 키워드: {keywords}
주제 및 방향:
{topic}""",

    "instagram": """인스타그램 피드 콘텐츠를 아래 형식으로 작성하세요.

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
(각 15자 이내, 임팩트 있게)""",

    "youtube": """유튜브 영상 길이: {yt_type}

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
🎬 대본
━━━━━━━━━━━━━━━━━━━━━
[오프닝 — 첫 3초 후킹]

[본론]

[클로징 — 구독/좋아요 CTA]

※ 구어체, 자연스럽게 / [카메라 지시사항] 포함""",

    "threads": """스레드(Threads) 및 트위터(X) 콘텐츠를 작성하세요.

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
━━━━━━━━━━━━━━━━━━━━━""",

    "hashtags": """해시태그 언어: {hash_lang}
총 {hash_count}개, 노출성·광고 효과 최우선으로 작성하세요.

━━━━━━━━━━━━━━━━━━━━━
🔴 대형 해시태그 (게시물 100만+)
━━━━━━━━━━━━━━━━━━━━━
(각 태그 옆 예상 게시물 수 표기)

━━━━━━━━━━━━━━━━━━━━━
🟡 중형 해시태그 (10~100만)
━━━━━━━━━━━━━━━━━━━━━

━━━━━━━━━━━━━━━━━━━━━
🟢 소형 해시태그 (1~10만, 상위노출 집중)
━━━━━━━━━━━━━━━━━━━━━

━━━━━━━━━━━━━━━━━━━━━
💡 최적 조합 TOP 15 — 바로 복붙 가능하게 한 줄로
━━━━━━━━━━━━━━━━━━━━━

━━━━━━━━━━━━━━━━━━━━━
📈 이 조합 사용 시 예상 노출 효과 한 줄 요약
━━━━━━━━━━━━━━━━━━━━━"""
}

PROMPT_FILE = "prompts.json"

# ══════════════════════════════════════════════════════
# 프롬프트 저장/로드
# ══════════════════════════════════════════════════════
def load_prompts():
    if os.path.exists(PROMPT_FILE):
        try:
            with open(PROMPT_FILE, "r", encoding="utf-8") as f:
                saved = json.load(f)
            # 기본값에 없는 키는 기본값으로 채움
            result = DEFAULT_PROMPTS.copy()
            result.update(saved)
            return result
        except:
            return DEFAULT_PROMPTS.copy()
    return DEFAULT_PROMPTS.copy()

def save_prompts(prompts):
    with open(PROMPT_FILE, "w", encoding="utf-8") as f:
        json.dump(prompts, f, ensure_ascii=False, indent=2)

# ══════════════════════════════════════════════════════
# SESSION STATE
# ══════════════════════════════════════════════════════
if "admin_auth" not in st.session_state:
    st.session_state.admin_auth = False
if "prompts" not in st.session_state:
    st.session_state.prompts = load_prompts()
if "save_msg" not in st.session_state:
    st.session_state.save_msg = {}

# ══════════════════════════════════════════════════════
# 비밀번호 확인
# ══════════════════════════════════════════════════════
try:
    ADMIN_PW = st.secrets["ADMIN_PASSWORD"]
except:
    ADMIN_PW = "aura2024"  # 로컬 테스트용 기본값

if not st.session_state.admin_auth:
    st.markdown("""
    <div class="lock-screen">
        <div class="lock-icon">🔐</div>
        <div class="lock-title">Admin Only</div>
        <div class="lock-sub">관리자 전용 페이지입니다.<br>비밀번호를 입력하세요.</div>
    </div>
    """, unsafe_allow_html=True)

    _, center, _ = st.columns([1, 1.5, 1])
    with center:
        pw_input = st.text_input("비밀번호", type="password", placeholder="관리자 비밀번호 입력", label_visibility="collapsed")
        if st.button("🔓 로그인", use_container_width=True):
            if pw_input == ADMIN_PW:
                st.session_state.admin_auth = True
                st.rerun()
            else:
                st.error("❌ 비밀번호가 틀렸습니다.")
    st.stop()

# ══════════════════════════════════════════════════════
# 관리자 페이지 메인
# ══════════════════════════════════════════════════════
st.markdown("""
<div class="admin-header">
    <div class="admin-logo">✦ AURA</div>
    <div class="admin-badge">Admin</div>
    <div class="admin-sub">프롬프트 관리 시스템</div>
</div>
""", unsafe_allow_html=True)

# 통계
total_chars = sum(len(v) for v in st.session_state.prompts.values())
st.markdown(f"""
<div class="stat-row">
    <div class="stat-mini">
        <div class="stat-mini-num">5</div>
        <div class="stat-mini-lbl">관리 중인 프롬프트</div>
    </div>
    <div class="stat-mini">
        <div class="stat-mini-num">{total_chars:,}</div>
        <div class="stat-mini-lbl">총 프롬프트 글자수</div>
    </div>
    <div class="stat-mini">
        <div class="stat-mini-num" style="color:#4ECDC4;">Live</div>
        <div class="stat-mini-lbl">현재 배포 상태</div>
    </div>
</div>
""", unsafe_allow_html=True)

# 팁 박스
st.markdown("""
<div class="tip-box">
💡 <strong>사용법</strong> — 각 프롬프트를 수정하고 저장하면 메인 앱에 즉시 반영됩니다.<br>
<code>{topic}</code> <code>{industry}</code> <code>{tone}</code> <code>{target}</code> <code>{mood}</code> <code>{brand}</code> <code>{keywords}</code> 는 사용자 입력값으로 자동 치환됩니다. 삭제하지 마세요!
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
# 탭별 프롬프트 편집
# ══════════════════════════════════════════════════════
tab_ctx, tab_ig, tab_yt, tab_th, tab_hash, tab_test = st.tabs([
    "🌐 공통 컨텍스트",
    "📸 인스타그램",
    "📺 유튜브",
    "🧵 스레드/X",
    "🏷️ 해시태그",
    "🧪 테스트 미리보기"
])

def prompt_editor(tab, key, tag_class, tag_label, title, desc, height=350):
    with tab:
        st.markdown(f"""
        <div class="prompt-card">
            <div class="prompt-card-header">
                <div>
                    <div class="prompt-title">{title}</div>
                    <div class="prompt-desc">{desc}</div>
                </div>
                <span class="ptag {tag_class}">{tag_label}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        edited = st.text_area(
            "프롬프트 내용",
            value=st.session_state.prompts[key],
            height=height,
            key=f"editor_{key}",
            label_visibility="collapsed"
        )

        col1, col2, col3 = st.columns([1, 1, 3])
        with col1:
            if st.button(f"💾 저장", key=f"save_{key}", use_container_width=True):
                st.session_state.prompts[key] = edited
                save_prompts(st.session_state.prompts)
                st.session_state.save_msg[key] = True
                st.rerun()
        with col2:
            with st.container():
                st.markdown('<div class="reset-btn">', unsafe_allow_html=True)
                if st.button("↺ 초기화", key=f"reset_{key}", use_container_width=True):
                    st.session_state.prompts[key] = DEFAULT_PROMPTS[key]
                    save_prompts(st.session_state.prompts)
                    st.session_state.save_msg[key] = False
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
        with col3:
            if st.session_state.save_msg.get(key):
                st.markdown('<div style="padding-top:0.5rem"><span class="saved-badge">✓ 저장 완료 — 메인 앱에 즉시 반영됨</span></div>', unsafe_allow_html=True)

        # 글자수 & 변경 여부
        changed = edited != DEFAULT_PROMPTS[key]
        char_count = len(edited)
        color = "#FF6B9D" if changed else "#5555AA"
        status = "수정됨" if changed else "기본값"
        st.markdown(f'<div style="font-size:0.7rem;color:{color};margin-top:0.3rem;font-family:\'DM Mono\',monospace;">{char_count}자 · {status}</div>', unsafe_allow_html=True)

# 각 탭 렌더링
prompt_editor(
    tab_ctx, "context", "ptag-ctx", "CONTEXT",
    "공통 컨텍스트 (모든 프롬프트에 자동 포함)",
    "사용자 입력값을 AI에게 전달하는 기본 정보 블록입니다.",
    height=200
)
prompt_editor(
    tab_ig, "instagram", "ptag-insta", "INSTAGRAM",
    "인스타그램 피드 생성 프롬프트",
    "캡션 2버전 + 카드뉴스 5장 + 스토리 문구를 생성하는 지시문입니다.",
    height=400
)
prompt_editor(
    tab_yt, "youtube", "ptag-yt", "YOUTUBE",
    "유튜브 콘텐츠 생성 프롬프트",
    "썸네일 카피 3전략 + 영상 제목 5개 + 대본을 생성하는 지시문입니다.",
    height=400
)
prompt_editor(
    tab_th, "threads", "ptag-thread", "THREADS / X",
    "스레드 & 트위터 콘텐츠 생성 프롬프트",
    "연속 포스트 5개 + 단문 트윗 3버전 + RT 유도 문구를 생성합니다.",
    height=350
)
prompt_editor(
    tab_hash, "hashtags", "ptag-hash", "HASHTAGS",
    "해시태그 최적화 프롬프트",
    "대형/중형/소형 해시태그 분류 및 최적 조합을 생성하는 지시문입니다.",
    height=350
)

# ══════════════════════════════════════════════════════
# 테스트 미리보기 탭
# ══════════════════════════════════════════════════════
with tab_test:
    st.markdown("""
    <div style="margin-bottom:1.5rem;">
        <div style="font-size:0.78rem;color:#8888AA;margin-bottom:0.3rem;">
            실제 변수값을 입력해서 프롬프트가 어떻게 완성되는지 미리 확인하세요
        </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        t_topic    = st.text_input("주제", value="나이키 신상 운동화 리뷰")
        t_industry = st.text_input("분야", value="패션 (의류/스타일링)")
        t_tone     = st.text_input("톤앤매너", value="감성적·공감형 🌸")
    with c2:
        t_target   = st.text_input("타겟", value="20-30대 MZ세대")
        t_mood     = st.text_input("무드", value="미니멀 & 클린")
        t_brand    = st.text_input("브랜드", value="Nike")
        t_keywords = st.text_input("키워드", value="운동화, 데일리룩, 스트릿")

    preview_target = st.selectbox("미리볼 프롬프트", [
        "📸 인스타그램", "📺 유튜브", "🧵 스레드/X", "🏷️ 해시태그"
    ])

    key_map = {
        "📸 인스타그램": "instagram",
        "📺 유튜브": "youtube",
        "🧵 스레드/X": "threads",
        "🏷️ 해시태그": "hashtags"
    }

    if st.button("🔍 미리보기 생성", use_container_width=False):
        ctx_filled = st.session_state.prompts["context"].format(
            topic=t_topic, industry=t_industry, tone=t_tone,
            target=t_target, mood=t_mood, brand=t_brand or "없음",
            keywords=t_keywords or "없음"
        )
        body = st.session_state.prompts[key_map[preview_target]]
        full_prompt = ctx_filled + "\n\n" + body

        st.markdown(f"""
        <div style="background:#13131E;border:1px solid #2A2A40;border-radius:14px;
                    padding:1.5rem;margin-top:1rem;">
            <div style="font-family:'DM Mono',monospace;font-size:0.62rem;letter-spacing:0.12em;
                        color:#FF6B9D;text-transform:uppercase;margin-bottom:1rem;">
                완성된 프롬프트 미리보기
            </div>
            <pre style="white-space:pre-wrap;font-family:'DM Mono',monospace;font-size:0.78rem;
                        color:#C8C8E8;line-height:1.8;margin:0;">{full_prompt}</pre>
        </div>
        """, unsafe_allow_html=True)

        st.caption(f"총 {len(full_prompt):,}자")

# ══════════════════════════════════════════════════════
# 하단 로그아웃
# ══════════════════════════════════════════════════════
st.markdown("<br><hr>", unsafe_allow_html=True)
col_lo1, col_lo2 = st.columns([5, 1])
with col_lo2:
    if st.button("🚪 로그아웃", use_container_width=True):
        st.session_state.admin_auth = False
        st.rerun()
