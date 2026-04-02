import streamlit as st
import yfinance as yf
import ta
import warnings
from groq import Groq
import plotly.graph_objects as go
import time
warnings.filterwarnings('ignore')

st.set_page_config(page_title="ET AI Investor", page_icon="📈", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #0a0a0a 100%);
        color: #ffffff;
    }
    .stApp header, .stApp [data-testid="stHeader"] {
        background: transparent !important;
    }
    .metric-card {
        background: linear-gradient(145deg, #1e1e2e, #2a2a3e);
        border: 1px solid #333;
        border-radius: 16px;
        padding: 20px;
        text-align: center;
        margin: 5px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    }
    .metric-label { color: #888; font-size: 0.85rem; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 1px; }
    .metric-value { font-size: 1.6rem; font-weight: 700; color: #ffffff; }
    .metric-delta-up   { color: #00ff88; font-size: 0.9rem; font-weight: 600; }
    .metric-delta-down { color: #ff4444; font-size: 0.9rem; font-weight: 600; }
    .metric-delta-neutral { color: #ffaa00; font-size: 0.9rem; font-weight: 600; }
    .ai-section {
        background: linear-gradient(145deg, #1a1a2e, #16213e);
        border: 1px solid #00d4ff33;
        border-left: 4px solid #00d4ff;
        border-radius: 12px;
        padding: 25px 30px;
        margin-top: 10px;
        color: white;
        font-size: 1rem;
    }
    .chat-container {
        background: linear-gradient(145deg, #1a1a2e, #16213e);
        border: 1px solid #7b2ff733;
        border-radius: 16px;
        padding: 20px;
        margin-top: 10px;
        max-height: 400px;
        overflow-y: auto;
    }
    .chat-user {
        background: linear-gradient(90deg, #00d4ff22, #7b2ff722);
        border-radius: 12px 12px 4px 12px;
        padding: 10px 15px;
        margin: 8px 0 8px 40px;
        color: #ffffff;
        font-size: 0.95rem;
    }
    .chat-bot {
        background: rgba(255,255,255,0.05);
        border-radius: 12px 12px 12px 4px;
        padding: 10px 15px;
        margin: 8px 40px 8px 0;
        color: #dddddd;
        font-size: 0.95rem;
    }
    .stButton > button {
        background: linear-gradient(90deg, #00d4ff, #7b2ff7);
        color: white; border: none; border-radius: 10px;
        font-weight: 700; font-size: 1rem; padding: 12px 30px; width: 100%;
    }
    .stButton > button:hover { transform: translateY(-2px); box-shadow: 0 5px 20px rgba(0,212,255,0.4); }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center; padding:30px 0 8px 0;">
  <span style="font-size:3.2rem; font-weight:900;
    background:linear-gradient(90deg,#00d4ff,#7b2ff7);
    -webkit-background-clip:text;
    -webkit-text-fill-color:white;
    display:inline-block;">
    📈 ET AI Investor
  </span>
</div>
<div style="text-align:center; color:#888; font-size:1.1rem; margin-bottom:10px;">
  Smart Stock Analysis for Every Indian — Powered by AI 🤖
</div>
""", unsafe_allow_html=True)

st.divider()

STOCKS = {
    "🛢️ Reliance Industries": "RELIANCE.NS",
    "💻 TCS": "TCS.NS",
    "🖥️ Infosys": "INFY.NS",
    "🏦 HDFC Bank": "HDFCBANK.NS",
    "🚗 Tata Motors": "TATAMOTORS.NS",
    "⚙️ Wipro": "WIPRO.NS",
    "🏛️ SBI": "SBIN.NS",
    "⚓ Adani Ports": "ADANIPORTS.NS"
}

def get_stock_analysis(symbol, name):
    # Retry logic — 3 attempts
    for attempt in range(3):
        try:
            stock = yf.Ticker(symbol)
            data = stock.history(period="1y")
            if data.empty:
                time.sleep(2)
                continue
            data['RSI'] = ta.momentum.RSIIndicator(data['Close']).rsi()
            data['DMA_200'] = data['Close'].rolling(window=200).mean()
            macd = ta.trend.MACD(data['Close'])
            data['MACD'] = macd.macd()
            data['MACD_signal'] = macd.macd_signal()
            latest = data.iloc[-1]
            prev   = data.iloc[-2]
            price  = latest['Close']
            rsi    = latest['RSI']
            dma200 = latest['DMA_200']
            macd_val = latest['MACD']
            macd_sig = latest['MACD_signal']
            price_change = ((price - prev['Close']) / prev['Close']) * 100
            return {
                "name": name, "price": price, "price_change": price_change,
                "rsi": rsi, "dma200": dma200,
                "above_dma": price > dma200,
                "macd_bullish": macd_val > macd_sig,
                "data": data
            }
        except Exception as e:
            if attempt < 2:
                time.sleep(3)
                continue
            else:
                raise e
    return None

def call_groq(messages):
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        max_tokens=600
    )
    return response.choices[0].message.content

def get_ai_explanation(analysis):
    try:
        prompt = f"""
You are an expert Indian stock market advisor helping common Indians understand stocks simply.

Stock: {analysis['name']}
Current Price: Rs.{analysis['price']:.2f}
Today's Change: {analysis['price_change']:.2f}%
RSI: {analysis['rsi']:.2f}
200 Day Moving Average: Rs.{analysis['dma200']:.2f}
Price above 200 DMA: {analysis['above_dma']}
MACD Bullish: {analysis['macd_bullish']}

Respond in EXACTLY this format. Leave one blank line between each section:

WHAT IS HAPPENING
Write 2 simple sentences here.

SIGNAL
Write only one: STRONG BUY or BUY or HOLD or CAUTION or AVOID

WHY
- Reason 1
- Reason 2
- Reason 3

RISK LEVEL
Write only: Low or Medium or High

SIMPLE ADVICE
Write 1 simple line for a normal Indian investor.

Keep sections clearly separate. Simple English only.
"""
        return call_groq([{"role": "user", "content": prompt}])
    except Exception as e:
        return f"AI Analysis Error: {str(e)}"

# TABS
tab1, tab2 = st.tabs(["📊 Stock Analyzer", "🤖 AI Stock Chat"])

# TAB 1
with tab1:
    col_left, col_right = st.columns([2, 1])
    with col_left:
        selected_name = st.selectbox("🔍 Select a Stock:", list(STOCKS.keys()))
    with col_right:
        st.markdown("<br>", unsafe_allow_html=True)
        analyze_btn = st.button("🚀 Analyze Now!")

    if analyze_btn:
        try:
            with st.spinner("⏳ Fetching live NSE data..."):
                symbol     = STOCKS[selected_name]
                clean_name = selected_name.split(" ", 1)[1]
                analysis   = get_stock_analysis(symbol, clean_name)

            if analysis is None:
                st.error("Could not fetch stock data. Please try again in a moment.")
            else:
                st.markdown(f"### 📊 {clean_name} — Live Analysis")

                price_color = "metric-delta-up"   if analysis['price_change'] >= 0 else "metric-delta-down"
                price_arrow = "▲"                 if analysis['price_change'] >= 0 else "▼"
                rsi_val     = analysis['rsi']
                rsi_status  = "Overbought" if rsi_val > 70 else ("Oversold" if rsi_val < 30 else "Normal")
                rsi_color   = "metric-delta-down" if rsi_val > 70 else ("metric-delta-up" if rsi_val < 30 else "metric-delta-neutral")
                dma_status  = "Above DMA" if analysis['above_dma'] else "Below DMA"
                dma_color   = "metric-delta-up" if analysis['above_dma'] else "metric-delta-down"
                macd_status = "Bullish" if analysis['macd_bullish'] else "Bearish"
                macd_color  = "metric-delta-up" if analysis['macd_bullish'] else "metric-delta-down"

                c1, c2, c3, c4 = st.columns(4)
                with c1:
                    st.markdown(f"""<div class="metric-card">
                        <div class="metric-label">💰 Current Price</div>
                        <div class="metric-value">Rs.{analysis['price']:.2f}</div>
                        <div class="{price_color}">{price_arrow} {abs(analysis['price_change']):.2f}%</div>
                    </div>""", unsafe_allow_html=True)
                with c2:
                    st.markdown(f"""<div class="metric-card">
                        <div class="metric-label">📊 RSI</div>
                        <div class="metric-value">{rsi_val:.1f}</div>
                        <div class="{rsi_color}">{rsi_status}</div>
                    </div>""", unsafe_allow_html=True)
                with c3:
                    st.markdown(f"""<div class="metric-card">
                        <div class="metric-label">📉 200 DMA</div>
                        <div class="metric-value">Rs.{analysis['dma200']:.2f}</div>
                        <div class="{dma_color}">{dma_status}</div>
                    </div>""", unsafe_allow_html=True)
                with c4:
                    st.markdown(f"""<div class="metric-card">
                        <div class="metric-label">📈 MACD</div>
                        <div class="metric-value">Signal</div>
                        <div class="{macd_color}">{macd_status}</div>
                    </div>""", unsafe_allow_html=True)

                st.divider()

                price_min = analysis['data']['Close'].min() * 0.97
                price_max = analysis['data']['Close'].max() * 1.03
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=analysis['data'].index, y=analysis['data']['Close'],
                    name='Stock Price', line=dict(color='#00d4ff', width=2)
                ))
                fig.add_trace(go.Scatter(
                    x=analysis['data'].index, y=analysis['data']['DMA_200'],
                    name='200 Day Average', line=dict(color='#ff9500', width=2, dash='dash')
                ))
                fig.update_layout(
                    title=dict(text=f"{clean_name} — 1 Year Price Chart", font=dict(color='white', size=20)),
                    height=420, template="plotly_dark",
                    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(15,15,30,0.8)',
                    font=dict(color='white'),
                    legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(color='white', size=13)),
                    xaxis=dict(
                        title=dict(text="Date", font=dict(size=16, color='#aaaaaa')),
                        gridcolor='#333', tickfont=dict(size=13, color='white')
                    ),
                    yaxis=dict(
                        title=dict(text="Price (Rs.)", font=dict(size=16, color='#aaaaaa')),
                        gridcolor='#333', range=[price_min, price_max],
                        tickfont=dict(size=13, color='white')
                    ),
                )
                st.plotly_chart(fig, use_container_width=True)

                st.divider()
                st.markdown("### 🤖 AI Analysis — Simple English")
                with st.spinner("🧠 AI is thinking..."):
                    ai_text = get_ai_explanation(analysis)

                lines = ai_text.strip().split('\n')
                formatted = ""
                for line in lines:
                    line = line.strip()
                    if line == "":
                        formatted += "<br>"
                    else:
                        formatted += f"<p style='margin:8px 0;'>{line}</p>"
                st.markdown(f'<div class="ai-section">{formatted}</div>', unsafe_allow_html=True)

                st.divider()
                st.info("Educational purposes only. Not financial advice. Consult SEBI registered advisor before investing.")

        except Exception as e:
            st.error(f"Error fetching data. Please try again in a moment. ({str(e)[:100]})")

# TAB 2
with tab2:
    st.markdown("### 🤖 Ask Anything About Indian Stocks!")
    st.markdown("*Ask me about any stock, market trends, or investment advice in simple English*")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if st.session_state.chat_history:
        chat_html = ""
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                chat_html += f'<div class="chat-user">You: {msg["content"]}</div>'
            else:
                content = msg["content"].replace('\n', '<br>')
                chat_html += f'<div class="chat-bot">AI: {content}</div>'
        st.markdown(f'<div class="chat-container">{chat_html}</div>', unsafe_allow_html=True)

    col_inp, col_btn = st.columns([4, 1])
    with col_inp:
        user_input = st.text_input("Type your question:", placeholder="e.g. Is TCS a good stock to buy now?", label_visibility="collapsed")
    with col_btn:
        send_btn = st.button("Send 🚀")

    if send_btn and user_input.strip():
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        system_msg = {
            "role": "system",
            "content": "You are a friendly Indian stock market expert. Answer in very simple English. Keep answers short (3-5 lines). Use Rs. for prices. Never give risky advice. Always suggest consulting a SEBI advisor for big investments."
        }
        messages = [system_msg] + [{"role": m["role"], "content": m["content"]} for m in st.session_state.chat_history]
        with st.spinner("🧠 Thinking..."):
            try:
                reply = call_groq(messages)
            except Exception as e:
                reply = f"Error: {str(e)}"
        st.session_state.chat_history.append({"role": "assistant", "content": reply})
        st.rerun()

    st.markdown("**Quick Questions:**")
    q1, q2, q3 = st.columns(3)
    with q1:
        if st.button("Best stocks to buy now?"):
            st.session_state.chat_history.append({"role": "user", "content": "What are the best Indian stocks to buy right now?"})
            with st.spinner("Thinking..."):
                reply = call_groq([
                    {"role": "system", "content": "You are a friendly Indian stock market expert. Answer simply in 4-5 lines."},
                    {"role": "user", "content": "What are the best Indian stocks to buy right now?"}
                ])
            st.session_state.chat_history.append({"role": "assistant", "content": reply})
            st.rerun()
    with q2:
        if st.button("What is RSI?"):
            st.session_state.chat_history.append({"role": "user", "content": "What is RSI in stock market? Explain simply."})
            with st.spinner("Thinking..."):
                reply = call_groq([
                    {"role": "system", "content": "You are a friendly Indian stock market expert. Answer simply in 4-5 lines."},
                    {"role": "user", "content": "What is RSI in stock market? Explain simply."}
                ])
            st.session_state.chat_history.append({"role": "assistant", "content": reply})
            st.rerun()
    with q3:
        if st.button("How to start investing?"):
            st.session_state.chat_history.append({"role": "user", "content": "How can a normal Indian start investing in stocks?"})
            with st.spinner("Thinking..."):
                reply = call_groq([
                    {"role": "system", "content": "You are a friendly Indian stock market expert. Answer simply in 4-5 lines."},
                    {"role": "user", "content": "How can a normal Indian start investing in stocks?"}
                ])
            st.session_state.chat_history.append({"role": "assistant", "content": reply})
            st.rerun()

    if st.session_state.chat_history:
        if st.button("Clear Chat"):
            st.session_state.chat_history = []
            st.rerun()