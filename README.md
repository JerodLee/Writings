# dual_edge_signal_bot

Beginner-friendly Python signal bot that watches:
- **Bitget futures** (public API)
- **Bithumb KRW spot** (public API)

It generates alerts for:
1. **M1 Break-Retest**
2. **Spring Reversal**

> ✅ This bot **does not place orders**. It only sends Telegram alerts and writes signals to CSV.

---

## 1) Features

- Real-time style processing with:
  - Bitget WebSocket trade stream (for approximate CVD)
  - REST polling fallback every 10-30 seconds (default: 15)
- In-memory candle storage via `pandas.DataFrame`
- Indicators:
  - VWAP
  - RSI(14)
  - CCI(14)
  - Volume MA(20)
  - ATR(14)
  - Box High/Low over 30 candles
  - OI delta
  - Approximate CVD from trade direction
- Risk output for each signal:
  - entry candidate
  - invalidation stop
  - target1 = 2R
  - target2 = 3R
  - signal grade (A+, A, B, reject)
- Logging + error recovery + reconnect loop

---

## 2) Project Structure

```text
dual_edge_signal_bot/
├─ main.py
├─ config.py
├─ requirements.txt
├─ README.md
├─ exchanges/
│  ├─ bitget.py
│  └─ bithumb.py
├─ strategy/
│  ├─ indicators.py
│  ├─ m1.py
│  └─ spring.py
├─ notifier/
│  └─ telegram.py
└─ storage/
   └─ signal_log.csv
```

---

## 3) Environment Variables

Create a `.env` file in project root:

```env
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_chat_id
BITGET_BASE_URL=https://api.bitget.com
BITHUMB_BASE_URL=https://api.bithumb.com
```

No private trading keys are needed.

---

## 4) Local Setup (Windows + VS Code)

1. Install Python 3.11+.
2. Open this folder in VS Code.
3. Open terminal in VS Code and run:

```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

4. Create `.env` with your Telegram values.
5. Run:

```bash
python main.py
```

You should see logs in terminal and alerts in Telegram when strategy conditions pass.

---

## 5) Render Deployment

1. Push this project to GitHub.
2. In Render, create a **Background Worker**.
3. Connect your repo.
4. Use:
   - Build command: `pip install -r requirements.txt`
   - Start command: `python main.py`
5. Add environment variables in Render dashboard:
   - `TELEGRAM_BOT_TOKEN`
   - `TELEGRAM_CHAT_ID`
   - `BITGET_BASE_URL`
   - `BITHUMB_BASE_URL`
6. Deploy.

---

## 6) Safety Notes

- This is an **alert bot**, not an execution bot.
- It does **not** call any private trading endpoint.
- Candle/ticker endpoint formats may evolve by exchange; adjust parsing if API response shape changes.
- Always paper-test before relying on any strategy.

---

## 7) Customization Tips

- Change symbols in `config.py`.
- Tune thresholds in `strategy/m1.py` and `strategy/spring.py`.
- Increase/decrease polling speed in `config.py` (`poll_interval_seconds`).
