# US Momentum Surge Scanner (Phase 1 MVP)

미국 급등주 후보를 매일 선별하는 Streamlit MVP입니다.

## Phase 1 범위
- Gate 0 유니버스 필터 → 가격/프리마켓/뉴스 수집 → 타입 점수화(TYPE A~F) → 리스크 필터(SEC RSS Kill-Switch) → 후보 리포트 생성.
- 후보가 없으면 `오늘은 강한 후보 없음` 출력.

## Windows PowerShell 실행 가이드
1. 프로젝트 폴더 이동
2. 가상환경 생성
3. 가상환경 활성화
4. 의존성 설치
5. `.env` 구성
6. Streamlit 실행

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
streamlit run app.py
```

### ExecutionPolicy 오류 해결
PowerShell 정책 오류가 나면 현재 세션에서만 아래를 실행한 뒤 다시 활성화하세요.

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

## TODO (Phase 2 이후)
- bid-ask spread 기반 거래 가능성 필터
- 호가 공백 분석
- 실시간 Stocktwits/X SNS 분석
- 패턴 DB
- XGBoost/ML
- 자동매매
- 본격 백테스트
- delisted ticker dataset 연동
