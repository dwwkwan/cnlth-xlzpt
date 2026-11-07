import streamlit as st
import time
from datetime import datetime, timedelta

# 페이지 설정
st.set_page_config(
    page_title="공연 취소표 타이머 & 모니터링 가이드",
    page_icon="⏰",
    layout="wide"
)

st.title("🎫 취소표(취켓팅) 골든타임 알리미 & 가이드")
st.write("주요 예매처별 취소표 풀리는 시간을 확인하고, 실전 알림 타이머를 세팅할 수 있는 앱입니다.")

# 세션 상태 초기화
if "timer_running" not in st.session_state:
    st.session_state["timer_running"] = False

# 사이드바: 예매처 정보 및 타겟 설정
st.sidebar.header("⚙️ 취켓팅 타겟 설정")
selected_site = st.sidebar.selectbox(
    "예매처 선택",
    ["예스24 티켓 (자정 직후)", "멜론티켓 / 티켓링크 (12시 10분 이후)", "인터파크 티켓 (오전 9시 이후 순차)"]
)

concert_name = st.sidebar.text_input("공연 이름", "2026 샘스미스 내한 공연")
target_date = st.sidebar.date_input("관람 희망일")

# 예매처별 골든타임 안내 딕셔너리
site_info = {
    "예스24 티켓 (자정 직후)": {
        "golden_time": "00:03 ~ 00:15",
        "tip": "무통장 입금 마감 직후인 자정 3분 뒤부터 새로고침 전쟁이 시작됩니다. 00시 02분부터 대기하세요."
    },
    "멜론티켓 / 티켓링크 (12시 10분 이후)": {
        "golden_time": "00:10 ~ 00:20",
        "tip": "시스템이 순차적으로 미입금 표를 취소 처리하므로 10분~20분 사이에 새로고침을 집중해야 합니다."
    },
    "인터파크 티켓 (오전 9시 이후 순차)": {
        "golden_time": "오전 09:00 ~",
        "tip": "새벽보다는 오전 시간대 순차 반영 및 예매대기(예대) 알림을 적극 활용하는 것이 유리합니다."
    }
}

# 메인 레이아웃
col1, col2 = st.columns(2)

with col1:
    st.subheader(f"📌 {selected_site.split(' ')[0]} 골든타임 가이드")
    info = site_info[selected_site]
    
    st.info(f"**핵심 골든타임:** {info['golden_time']}")
    st.success(f"**공략 팁:** {info['tip']}")
    
    st.divider()
    
    st.subheader("⏰ 실전 타이머 및 대기 모드")
    current_time = datetime.now()
    st.metric(
        label="현재 시간", 
        value=current_time.strftime("%Y-%m-%d %H:%M:%S")
    )
    
    if st.button("🔔 취켓팅 골든타임 대기 알람 시작", type="primary", use_container_width=True):
        st.session_state["timer_running"] = True
        st.rerun()

with col2:
    st.subheader("📋 실시간 모니터링 로그")
    log_container = st.container(border=True)
    
    with log_container:
        if st.session_state["timer_running"]:
            st.write(f"🎯 **타겟 공연:** {concert_name} ({target_date})")
            st.write(f"🏢 **예매처:** {selected_site}")
            st.warning("⏳ 골든타임 진입 대기 중... 새로고침 창을 띄워두고 준비하세요!")
            time.sleep(0.5)
            st.info("💡 F5 새로고침 간격은 IP 차단을 방지하기 위해 3~5초 간격을 유지하는 것이 안전합니다.")
        else:
            st.write("사이드바에서 예매처를 선택하고 '취켓팅 골든타임 대기 알람 시작' 버튼을 눌러주세요.")

# 하단 팁
st.markdown("---")
st.markdown("""
### 💡 취켓팅 성공 핵심 요약
1. **결제 수단은 무조건 무통장 입금**을 선택할 수 있도록 미리 연습해 두세요.
2. 새로고침을 너무 짧은 간격(0.1초 등)으로 하면 **매크로 방지 보안 문자(CAPTCHA)**나 **IP 차단**을 당할 수 있으니 주의하세요.
3. 예매처별로 표가 풀리는 타이밍이 다르므로 본인이 노리는 예매처의 시간을 정확히 숙지해야 합니다.
""")
