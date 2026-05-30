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

## 무료 배포 가이드 (권장: Streamlit Community Cloud)
> 무료 + Streamlit 네이티브라서 MVP 배포에 가장 간단합니다.

### 1) GitHub 저장소 준비
- `us_momentum_scanner/` 폴더가 포함된 브랜치를 GitHub에 push.
- 메인 엔트리 파일은 `us_momentum_scanner/app.py`.

### 2) Streamlit Cloud에 앱 생성
1. https://share.streamlit.io 접속 후 로그인
2. **New app** 클릭
3. Repository: 본 저장소 선택
4. Branch: 배포 브랜치 선택
5. Main file path: `us_momentum_scanner/app.py`
6. Deploy 클릭

### 3) 배포 환경변수(Secrets) 설정
앱 설정의 **Secrets**에 아래 항목을 등록:

```toml
FINNHUB_API_KEY=""
ALPHA_VANTAGE_API_KEY=""
SEC_USER_AGENT="YourName your_email@example.com"
```

### 4) 배포 확인
- 앱 URL 접속
- `오늘 스캔 실행` 버튼 클릭
- 후보 테이블 혹은 `오늘은 강한 후보 없음` 메시지 출력 확인

## 대안 무료 배포 (Hugging Face Spaces)
- Space 생성 시 SDK를 **Streamlit**으로 선택.
- Root를 `us_momentum_scanner/` 기준으로 맞추고 `app.py`를 엔트리로 지정.
- `requirements.txt`, `runtime.txt`, `.streamlit/config.toml`을 그대로 사용.

## TODO (Phase 2 이후)
- bid-ask spread 기반 거래 가능성 필터
- 호가 공백 분석
- 실시간 Stocktwits/X SNS 분석
- 패턴 DB
- XGBoost/ML
- 자동매매
- 본격 백테스트
- delisted ticker dataset 연동
