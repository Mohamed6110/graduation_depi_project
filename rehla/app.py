import os
import uuid
import time
import streamlit as st

# ================================================================
# AGENT IMPORT — guarded so the UI loads even if agent is offline
# ================================================================
try:
    from agent import root_agent
    AGENT_AVAILABLE = True
    AGENT_ERROR = ""
except Exception as _e:
    AGENT_AVAILABLE = False
    AGENT_ERROR = str(_e)
    root_agent = None

# ================================================================
# PAGE CONFIG
# ================================================================
st.set_page_config(
    page_title="Rehla — AI Travel Assistant",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ================================================================
# CUSTOM CSS  — Rehla ocean palette
# ================================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@300;400;500;700&family=Sora:wght@300;400;600;700&display=swap');

/* ── Design tokens ─────────────────────────────────────── */
:root {
    --navy:     #0F2535;
    --primary:  #1A3C5E;
    --teal:     #0D9488;
    --teal-lt:  #14B8A6;
    --ice:      #E8F4F2;
    --mid:      #B2D8D8;
    --white:    #FFFFFF;
    --off-wh:   #F7FAFA;
    --gray:     #64748B;
    --slate:    #334155;
    --border:   #CBD5E1;
    --amber:    #D97706;
    --amber-lt: #FEF3C7;
    --text:     #1E293B;
    --muted:    #94A3B8;
    --surface:  #F1F5F9;
}

/* ── Global reset ──────────────────────────────────────── */
html, body,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
[data-testid="block-container"] {
    background-color: var(--off-wh) !important;
    font-family: 'Sora', 'Tajawal', sans-serif;
    color: var(--text);
}

/* ── Sidebar ───────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background-color: var(--navy) !important;
    border-right: 1px solid rgba(255,255,255,0.08);
}
[data-testid="stSidebar"] * { color: var(--white) !important; }
[data-testid="stSidebar"] .stMarkdown p,
[data-testid="stSidebar"] .stMarkdown span { color: var(--mid) !important; }

/* ── Top nav strip ─────────────────────────────────────── */
.rehla-nav {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 14px 24px;
    background: var(--primary);
    border-radius: 12px;
    margin-bottom: 24px;
    box-shadow: 0 2px 12px rgba(15,37,53,0.12);
}
.rehla-logo {
    font-size: 1.6rem;
    font-weight: 700;
    letter-spacing: 2px;
    color: var(--white);
}
.rehla-logo span { color: var(--teal); }
.rehla-tagline {
    font-size: 0.75rem;
    color: var(--mid);
    letter-spacing: 0.5px;
    margin-top: 2px;
}
.rehla-arabic {
    font-size: 0.95rem;
    color: var(--mid);
    font-family: 'Tajawal', sans-serif;
    font-weight: 500;
}

/* ── Status bar ────────────────────────────────────────── */
.status-bar {
    display: flex;
    gap: 12px;
    flex-wrap: wrap;
    margin: 0 0 20px 0;
}
.status-chip {
    display: flex;
    align-items: center;
    gap: 6px;
    background: var(--white);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 4px 12px;
    font-size: 0.72rem;
    color: var(--slate);
    font-weight: 500;
}
.dot { width: 7px; height: 7px; border-radius: 50%; flex-shrink: 0; }
.dot-active  { background: #22C55E; box-shadow: 0 0 6px #22C55E; animation: pulse 2s infinite; }
.dot-idle    { background: var(--muted); }
@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.35} }

/* ── Welcome screen ────────────────────────────────────── */
.welcome-wrap {
    text-align: center;
    padding: 56px 0 40px 0;
}
.welcome-plane {
    font-size: 3.2rem;
    margin-bottom: 16px;
    display: block;
}
.welcome-title {
    font-size: 1.45rem;
    font-weight: 700;
    color: var(--primary);
    margin-bottom: 8px;
}
.welcome-sub {
    font-size: 0.88rem;
    color: var(--gray);
    margin-bottom: 28px;
    max-width: 480px;
    margin-left: auto;
    margin-right: auto;
    line-height: 1.6;
}
.prompt-chips {
    display: flex;
    gap: 10px;
    justify-content: center;
    flex-wrap: wrap;
    margin-top: 4px;
}
.prompt-chip {
    background: var(--white);
    border: 1.5px solid var(--border);
    color: var(--slate);
    padding: 8px 16px;
    border-radius: 22px;
    font-size: 0.78rem;
    cursor: pointer;
    transition: border-color 0.2s, color 0.2s;
}
.prompt-chip:hover {
    border-color: var(--teal);
    color: var(--teal);
}

/* ── Chat messages ─────────────────────────────────────── */
.msg-user {
    display: flex;
    justify-content: flex-end;
    margin: 14px 0;
}
.msg-user .bubble {
    background: linear-gradient(135deg, var(--primary), #2D5F8A);
    color: var(--white);
    padding: 12px 18px;
    border-radius: 18px 18px 4px 18px;
    max-width: 68%;
    font-size: 0.92rem;
    line-height: 1.65;
    box-shadow: 0 4px 16px rgba(15,37,53,0.18);
}

.msg-assistant {
    display: flex;
    justify-content: flex-start;
    margin: 14px 0;
    gap: 10px;
    align-items: flex-start;
}
.msg-assistant .avatar {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    background: linear-gradient(135deg, var(--teal), var(--teal-lt));
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.05rem;
    flex-shrink: 0;
    margin-top: 2px;
    box-shadow: 0 2px 8px rgba(13,148,136,0.3);
}
.msg-assistant .bubble {
    background: var(--white);
    border: 1px solid var(--border);
    color: var(--text);
    padding: 14px 18px;
    border-radius: 4px 18px 18px 18px;
    max-width: 74%;
    font-size: 0.92rem;
    line-height: 1.72;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

/* ── Agent badge ───────────────────────────────────────── */
.agent-badge {
    display: inline-block;
    font-size: 0.66rem;
    font-weight: 600;
    padding: 2px 8px;
    border-radius: 4px;
    margin-bottom: 7px;
    letter-spacing: 0.3px;
    text-transform: uppercase;
}
.badge-rehla      { background: rgba(13,148,136,0.12); color: var(--teal); border: 1px solid rgba(13,148,136,0.3); }
.badge-flight     { background: rgba(26,60,94,0.1);    color: var(--primary); border: 1px solid rgba(26,60,94,0.25); }
.badge-hotel      { background: rgba(217,119,6,0.12);  color: var(--amber); border: 1px solid rgba(217,119,6,0.3); }
.badge-activity   { background: rgba(34,197,94,0.12);  color: #16A34A; border: 1px solid rgba(34,197,94,0.3); }
.badge-compliance { background: rgba(239,68,68,0.1);   color: #DC2626; border: 1px solid rgba(239,68,68,0.25); }

/* ── Thinking indicator ────────────────────────────────── */
.thinking {
    display: flex;
    align-items: center;
    gap: 10px;
    color: var(--gray);
    font-size: 0.82rem;
    padding: 12px 0;
}
.thinking-dots span {
    display: inline-block;
    width: 5px; height: 5px;
    border-radius: 50%;
    background: var(--teal);
    animation: bounce 1.2s infinite;
    margin: 0 2px;
}
.thinking-dots span:nth-child(2) { animation-delay: 0.2s; }
.thinking-dots span:nth-child(3) { animation-delay: 0.4s; }
@keyframes bounce {
    0%,80%,100% { transform:translateY(0); }
    40%         { transform:translateY(-6px); }
}

/* ── Timestamp ─────────────────────────────────────────── */
.msg-time {
    font-size: 0.66rem;
    color: var(--muted);
    margin-top: 5px;
    padding-left: 2px;
}

/* ── Metric cards (sidebar) ────────────────────────────── */
.metric-card {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 10px;
    padding: 12px 14px;
    text-align: center;
}
.metric-val   { font-size: 1.55rem; font-weight: 700; color: var(--teal-lt); }
.metric-label { font-size: 0.68rem; color: var(--mid); margin-top: 2px; }

/* ── Session items (sidebar) ───────────────────────────── */
.session-item {
    padding: 9px 12px;
    border-radius: 8px;
    border: 1px solid rgba(255,255,255,0.08);
    margin-bottom: 5px;
    font-size: 0.8rem;
    color: var(--mid);
}
.session-active {
    border-color: var(--teal) !important;
    background: rgba(13,148,136,0.12) !important;
    color: var(--white) !important;
}

/* ── Agent status rows (sidebar) ───────────────────────── */
.agent-row {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 7px 10px;
    border-radius: 7px;
    margin-bottom: 4px;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.06);
    font-size: 0.78rem;
    color: var(--mid);
}

/* ── Chat input ────────────────────────────────────────── */
[data-testid="stChatInput"] textarea {
    background: var(--white) !important;
    border: 1.5px solid var(--border) !important;
    color: var(--text) !important;
    border-radius: 14px !important;
    font-family: 'Sora', sans-serif !important;
    font-size: 0.92rem !important;
}
[data-testid="stChatInput"] textarea:focus {
    border-color: var(--teal) !important;
    box-shadow: 0 0 0 3px rgba(13,148,136,0.15) !important;
}
[data-testid="stChatInput"] button {
    background: var(--teal) !important;
    border-radius: 10px !important;
}

/* ── Buttons ───────────────────────────────────────────── */
.stButton > button {
    background: rgba(13,148,136,0.15) !important;
    color: var(--teal-lt) !important;
    border: 1px solid rgba(13,148,136,0.35) !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 0.82rem !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    background: var(--teal) !important;
    color: var(--white) !important;
    border-color: var(--teal) !important;
}

/* ── Error banner ──────────────────────────────────────── */
.agent-offline {
    background: #FEF2F2;
    border: 1px solid #FECACA;
    border-radius: 10px;
    padding: 12px 16px;
    font-size: 0.84rem;
    color: #991B1B;
    margin-bottom: 20px;
}

/* ── Divider & chrome ──────────────────────────────────── */
hr { border-color: rgba(255,255,255,0.08) !important; margin: 14px 0 !important; }
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stToolbar"] { display: none; }
</style>
""", unsafe_allow_html=True)


# ================================================================
# SESSION STATE INIT
# ================================================================
if "sessions" not in st.session_state:
    sid = str(uuid.uuid4())[:8]
    st.session_state.sessions = {sid: {"name": "Trip 1", "messages": []}}
    st.session_state.active_session = sid

if "is_thinking" not in st.session_state:
    st.session_state.is_thinking = False

if "total_queries" not in st.session_state:
    st.session_state.total_queries = 0


# ================================================================
# HELPERS
# ================================================================
def get_active_messages() -> list:
    return st.session_state.sessions[st.session_state.active_session]["messages"]


def add_message(role: str, content: str, agent: str = None):
    get_active_messages().append({
        "role":    role,
        "content": content,
        "agent":   agent,
        "time":    time.strftime("%H:%M"),
    })


def new_session():
    sid  = str(uuid.uuid4())[:8]
    n    = len(st.session_state.sessions) + 1
    st.session_state.sessions[sid] = {"name": f"Trip {n}", "messages": []}
    st.session_state.active_session = sid


def clear_session():
    st.session_state.sessions[st.session_state.active_session]["messages"] = []


def render_message(msg: dict):
    """Render a single chat message bubble."""
    if msg["role"] == "user":
        st.markdown(f"""
        <div class="msg-user">
            <div class="bubble">{msg['content']}</div>
        </div>""", unsafe_allow_html=True)
    else:
        agent = msg.get("agent", "rehla")
        # Map agent key → badge class + display label
        AGENT_META = {
            "rehla":      ("badge-rehla",      "✈️ Rehla"),
            "flight":     ("badge-flight",     "✈️ Transporter"),
            "hotel":      ("badge-hotel",      "🏨 In-Sider"),
            "activity":   ("badge-activity",   "🗺️ Explorer"),
            "compliance": ("badge-compliance", "🛂 Compliance"),
            "concierge":  ("badge-rehla",      "🎩 Concierge"),
        }
        badge_cls, label = AGENT_META.get(agent, ("badge-rehla", "🎩 Rehla"))

        st.markdown(f"""
        <div class="msg-assistant">
            <div class="avatar">✈</div>
            <div>
                <span class="agent-badge {badge_cls}">{label}</span>
                <div class="bubble">{msg['content']}</div>
                <div class="msg-time">{msg.get('time', '')}</div>
            </div>
        </div>""", unsafe_allow_html=True)


# ================================================================
# AGENT QUERY
# ================================================================
def query_agent(user_input: str) -> str:
    """
    Invoke root_agent with conversation history prepended.
    Returns the final text response.
    """
    if not AGENT_AVAILABLE:
        return f"⚠️ Agent unavailable: {AGENT_ERROR}\n\nMake sure Ollama is running and `agent.py` is in the same directory."

    # Build conversation context
    history = get_active_messages()
    history_text = ""
    for msg in history[:-1]:  # exclude the latest user message (already sent)
        role = "User" if msg["role"] == "user" else "Assistant"
        history_text += f"{role}: {msg['content']}\n\n"

    full_query = user_input
    if history_text:
        full_query = f"Previous conversation:\n{history_text}\nCurrent question: {user_input}"

    thread_id = f"rehla_{st.session_state.active_session}"
    config    = {"configurable": {"thread_id": thread_id}}

    try:
        result   = root_agent.invoke(
            {"messages": [("user", full_query)]},
            config=config,
        )
        messages = result.get("messages", [])
        # Walk backwards, skip tool-call messages, return first real text
        for msg in reversed(messages):
            if hasattr(msg, "content") and msg.content:
                if not hasattr(msg, "tool_calls") or not msg.tool_calls:
                    content = msg.content
                    # Handle list content blocks (Anthropic/Gemini style)
                    if isinstance(content, list):
                        return "".join(
                            b.get("text", str(b)) if isinstance(b, dict) else str(b)
                            for b in content
                        )
                    return str(content)
    except Exception as e:
        return f"⚠️ Error communicating with agent:\n\n`{str(e)}`\n\n💡 Make sure Ollama is running and the model is downloaded."

    return "I could not generate a response. Please try again."


# ================================================================
# SIDEBAR
# ================================================================
with st.sidebar:

    # ── Logo ──────────────────────────────────────────────────────
    st.markdown("""
    <div style="padding: 20px 4px 12px 4px;">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 220 72" width="100%" height="auto">
            <!-- Teal accent bar -->
            <rect x="0" y="0" width="4" height="72" fill="#0D9488" rx="2"/>
            <!-- Globe lines -->
            <g transform="translate(38,36)" opacity="0.18">
                <circle cx="0" cy="0" r="26" fill="none" stroke="#B2D8D8" stroke-width="2"/>
                <ellipse cx="0" cy="0" rx="11" ry="26" fill="none" stroke="#B2D8D8" stroke-width="1.5"/>
                <line x1="-26" y1="0" x2="26" y2="0" stroke="#B2D8D8" stroke-width="1.5"/>
            </g>
            <!-- Wordmark -->
            <text x="68" y="43" font-family="'Arial Black',Impact,sans-serif"
                  font-weight="900" font-size="32" letter-spacing="3">
                <tspan fill="#FFFFFF">REH</tspan><tspan fill="#0D9488">LA</tspan>
            </text>
            <!-- Arabic & tagline -->
            <text x="68" y="62" font-family="'Tajawal',sans-serif"
                  font-size="11" fill="#B2D8D8" letter-spacing="0.5">رحلة · AI Travel Assistant</text>
        </svg>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    # ── New trip button ───────────────────────────────────────────
    if st.button("＋  New Trip", use_container_width=True):
        new_session()
        st.rerun()

    # ── Session list ──────────────────────────────────────────────
    st.markdown(
        "<div style='font-size:0.68rem;color:#64748B;margin:10px 0 6px 0;"
        "text-transform:uppercase;letter-spacing:1px;'>Trips</div>",
        unsafe_allow_html=True,
    )
    for sid, sdata in st.session_state.sessions.items():
        is_active = sid == st.session_state.active_session
        n_pairs   = len(sdata["messages"]) // 2
        label     = f"{sdata['name']}  ·  {n_pairs} msg{'s' if n_pairs != 1 else ''}"
        cls       = "session-item session-active" if is_active else "session-item"
        st.markdown(f'<div class="{cls}">{label}</div>', unsafe_allow_html=True)
        if st.button(sdata["name"], key=f"btn_{sid}", use_container_width=True,
                     help="Switch to this trip"):
            st.session_state.active_session = sid
            st.rerun()

    st.markdown("<hr>", unsafe_allow_html=True)

    # ── Agent roster ──────────────────────────────────────────────
    st.markdown(
        "<div style='font-size:0.68rem;color:#64748B;margin-bottom:8px;"
        "text-transform:uppercase;letter-spacing:1px;'>Agents</div>",
        unsafe_allow_html=True,
    )
    agents_list = [
        ("🎩", "Concierge",    "#0D9488"),
        ("✈️", "Transporter",  "#1A3C5E"),
        ("🏨", "In-Sider",     "#D97706"),
        ("🗺️", "Explorer",     "#16A34A"),
        ("🛂", "Compliance",   "#DC2626"),
        ("💰", "Accountant",   "#7C3AED"),
        ("🔔", "Support",      "#0891B2"),
    ]
    dot_color = "#22C55E" if AGENT_AVAILABLE else "#94A3B8"
    for icon, name, color in agents_list:
        st.markdown(f"""
        <div class="agent-row">
            <div class="dot" style="background:{dot_color};{'box-shadow:0 0 5px '+dot_color+';animation:pulse 2s infinite;' if AGENT_AVAILABLE else ''}"></div>
            <span style="font-size:1rem;">{icon}</span>
            <span style="color:#E2E8F0;font-size:0.78rem;">{name}</span>
        </div>""", unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    # ── Stats ─────────────────────────────────────────────────────
    msgs      = get_active_messages()
    user_msgs = [m for m in msgs if m["role"] == "user"]
    c1, c2    = st.columns(2)
    with c1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-val">{len(user_msgs)}</div>
            <div class="metric-label">Queries</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-val">{len(st.session_state.sessions)}</div>
            <div class="metric-label">Trips</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    if st.button("🗑️  Clear Trip", use_container_width=True):
        clear_session()
        st.rerun()


# ================================================================
# MAIN AREA
# ================================================================

# ── Top nav bar ──────────────────────────────────────────────────
st.markdown("""
<div class="rehla-nav">
    <div>
        <div class="rehla-logo">REH<span>LA</span></div>
        <div class="rehla-tagline">رحلة · AI-Powered Travel Planning</div>
    </div>
    <div class="rehla-arabic">✈ خطط رحلتك مع الذكاء الاصطناعي</div>
</div>
""", unsafe_allow_html=True)

# ── Agent status chips ───────────────────────────────────────────
dot_cls   = "dot-active" if AGENT_AVAILABLE else "dot-idle"
status_lbl = "Online" if AGENT_AVAILABLE else "Offline — check Ollama"
st.markdown(f"""
<div class="status-bar">
    <div class="status-chip"><div class="dot {dot_cls}"></div>Rehla Agent · {status_lbl}</div>
    <div class="status-chip"><div class="dot dot-idle"></div>9 Specialists Ready</div>
    <div class="status-chip"><div class="dot dot-idle"></div>Live Search · Tavily + Nowah</div>
</div>
""", unsafe_allow_html=True)

# ── Agent offline warning ────────────────────────────────────────
if not AGENT_AVAILABLE:
    st.markdown(f"""
    <div class="agent-offline">
        ⚠️ <strong>Agent unavailable:</strong> {AGENT_ERROR or 'Could not import agent.py'}
        <br><small>Make sure Ollama is running (<code>ollama serve</code>) and <code>agent.py</code> is in the same directory.</small>
    </div>
    """, unsafe_allow_html=True)

# ── Chat history ─────────────────────────────────────────────────
messages = get_active_messages()

if not messages:
    st.markdown("""
    <div class="welcome-wrap">
        <span class="welcome-plane">✈️</span>
        <div class="welcome-title">Where would you like to go?</div>
        <div class="welcome-sub">
            Tell Rehla your destination, dates, and budget — the AI will plan
            flights, hotels, activities, dining, and compliance in one conversation.
        </div>
        <div class="prompt-chips">
            <span class="prompt-chip">✈️ 7 nights in Tokyo, $3 000 budget</span>
            <span class="prompt-chip">🏨 Best hotels in Istanbul under $150/night</span>
            <span class="prompt-chip">🛂 Do Egyptians need a visa for France?</span>
            <span class="prompt-chip">🍽️ Hidden restaurants in Rome</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    for msg in messages:
        render_message(msg)

# ── Thinking indicator placeholder ──────────────────────────────
thinking_ph = st.empty()

# ── Chat input — MUST be at top-level (not inside any container) ─
user_input = st.chat_input("Plan my trip... e.g. '7 nights in Bali for 2, budget $2 500'")

if user_input:
    # Persist user message
    add_message("user", user_input)
    st.session_state.total_queries += 1

    # Show thinking animation
    with thinking_ph:
        st.markdown("""
        <div class="thinking">
            ✈ Routing to the right agents
            <span class="thinking-dots">
                <span></span><span></span><span></span>
            </span>
        </div>""", unsafe_allow_html=True)

    # Query agent (blocking — response comes back fully)
    response = query_agent(user_input)

    # Clear thinking
    thinking_ph.empty()

    # Stream response character-by-character in the UI
    stream_ph = st.empty()
    displayed = ""
    for char in response:
        displayed += char
        stream_ph.markdown(f"""
        <div class="msg-assistant">
            <div class="avatar">✈</div>
            <div>
                <span class="agent-badge badge-rehla">🎩 Concierge</span>
                <div class="bubble">{displayed}▌</div>
            </div>
        </div>""", unsafe_allow_html=True)
        time.sleep(0.006)

    # Final render without cursor
    stream_ph.markdown(f"""
    <div class="msg-assistant">
        <div class="avatar">✈</div>
        <div>
            <span class="agent-badge badge-rehla">🎩 Concierge</span>
            <div class="bubble">{displayed}</div>
            <div class="msg-time">{time.strftime('%H:%M')}</div>
        </div>
    </div>""", unsafe_allow_html=True)

    # Save to history and rerun to render properly
    add_message("assistant", response, agent="concierge")
    st.rerun()
