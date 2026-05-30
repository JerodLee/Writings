from pathlib import Path

import pandas as pd
import streamlit as st
from dotenv import load_dotenv

from modules.screener import run_screener

load_dotenv()

st.set_page_config(page_title="US Momentum Surge Scanner", layout="wide")
st.title("US Momentum Surge Scanner - Phase 1 MVP")

base_dir = Path(__file__).resolve().parent

if st.button("오늘 스캔 실행", type="primary"):
    df, asof_date = run_screener(base_dir)
    st.caption(f"기준일(US/Eastern): {asof_date}")
    if df.empty:
        st.info("오늘은 강한 후보 없음")
    else:
        view_cols = {
            "ticker": "티커",
            "name": "종목명",
            "type": "유형(TYPE A~F)",
            "grade": "등급(A+/A/B/C)",
            "score": "Score",
            "confidence": "Confidence",
            "regime": "Regime",
            "regime_multiplier": "Regime Multiplier",
            "kill_switch": "Kill-Switch 결과",
            "data_quality_flags": "데이터 품질 경고",
            "premarket_gap": "프리마켓 갭",
            "volume_velocity": "거래량 Velocity",
            "float_rotation": "Float Rotation",
            "news_summary": "뉴스 요약",
            "entry_ban_reason": "진입 금지 사유",
        }
        existing = [k for k in view_cols if k in df.columns]
        view = df[existing].rename(columns=view_cols)
        st.dataframe(view, use_container_width=True)
        st.download_button("CSV 다운로드", df.to_csv(index=False).encode("utf-8-sig"), file_name="candidates.csv")
else:
    st.write("버튼을 눌러 오늘 후보를 계산하세요.")
