import streamlit as st
from typing import List, Dict, Any, Optional


def render_sidebar(peripherals: List[Dict[str, Any]], health_info: Dict[str, Any]) -> str:
    """
    Render sidebar navigation matching user's sketch (Image 2).
    Returns the selected peripheral slug.
    """
    with st.sidebar:
        # Top Logo Header with red theme matching user drawing
        st.markdown(
            """
            <div class="sidebar-logo-card">
                <div style="font-size: 2.2rem; margin-bottom: 2px;">⚡</div>
                <div class="sidebar-logo-title">ARDUINO MEGA 2560</div>
                <div class="sidebar-logo-subtitle">Internal Peripheral Architecture</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("### 🔌 Peripherals")

        # Category Filter
        categories = ["All"] + sorted(list(set(p.get("category", "") for p in peripherals if p.get("category"))))
        selected_cat = st.selectbox("Filter by Subsystem:", categories, index=0)

        filtered = peripherals
        if selected_cat != "All":
            filtered = [p for p in peripherals if p.get("category") == selected_cat]

        # Options for selection
        options = [p["slug"] for p in filtered]
        format_func = lambda slug: next((f"{p.get('icon', '🔹')} {p['name'].split('(')[0].strip()}" for p in filtered if p["slug"] == slug), slug)

        selected_slug = st.radio(
            "Select Hardware Module:",
            options=options,
            format_func=format_func,
            index=0 if options else 0,
            label_visibility="collapsed"
        )

        st.divider()

        # System Architecture Quick Toggle
        view_mode = st.radio(
            "View Mode:",
            ["Peripheral Details & Code", "ATmega2560 Block Diagram", "System Architecture (MVC)"],
            index=0
        )
        st.session_state["view_mode"] = view_mode

        st.divider()

        # Health & Backend Status Card
        db_engine = health_info.get("database", {}).get("engine_dialect", "unknown")
        db_status = health_info.get("database", {}).get("status", "unknown")
        is_sqlite = health_info.get("database", {}).get("is_sqlite_fallback", False)
        
        status_label = "PostgreSQL Connected" if not is_sqlite and db_status == "connected" else "SQLite (Local Fallback)"
        status_color = "#10B981" if db_status == "connected" else "#F59E0B"

        st.markdown(
            f"""
            <div style="background-color: #F1F5F9; border-radius: 8px; padding: 10px 12px; font-size: 0.78rem;">
                <div style="font-weight: 700; color: #334155; margin-bottom: 4px;">SYSTEM BACKEND</div>
                <div style="display: flex; align-items: center; gap: 6px; margin-bottom: 2px;">
                    <span style="height: 8px; width: 8px; background-color: {status_color}; border-radius: 50%; display: inline-block;"></span>
                    <span style="color: #0F172A; font-weight: 600;">FastAPI:</span>
                    <span style="color: #10B981; font-weight: 600;">Online</span>
                </div>
                <div style="display: flex; align-items: center; gap: 6px;">
                    <span style="height: 8px; width: 8px; background-color: {status_color}; border-radius: 50%; display: inline-block;"></span>
                    <span style="color: #0F172A; font-weight: 600;">Database:</span>
                    <span style="color: #475569;">{status_label}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.caption("MVC Model: Streamlit + FastAPI + DB")

    return selected_slug
