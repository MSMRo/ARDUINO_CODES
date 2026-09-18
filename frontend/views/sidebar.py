import streamlit as st
from typing import List, Dict, Any, Optional, Tuple

from frontend.controllers.mcu_catalog import MCU_PROFILES, MCU_SLUGS, REFERENCE_MCU, get_mcu_profile


def _remember_peripheral() -> None:
    slug = st.session_state.get("peripheral_selector")
    if not slug:
        return

    recent = [item for item in st.session_state.get("recent_peripherals", []) if item != slug]
    st.session_state["recent_peripherals"] = [slug, *recent][:5]


def _select_recent_peripheral(slug: str) -> None:
    st.session_state["peripheral_selector"] = slug
    _remember_peripheral()


def render_sidebar(peripherals: List[Dict[str, Any]], health_info: Dict[str, Any]) -> Tuple[Optional[str], Dict[str, str]]:
    """
    Render sidebar navigation matching user's sketch (Image 2).
    Returns the selected peripheral slug and MCU profile.
    """
    st.session_state.setdefault("recent_peripherals", [])

    with st.sidebar:
        selected_mcu_slug = st.selectbox(
            "Select your ATmega",
            options=MCU_SLUGS,
            format_func=lambda slug: f"{MCU_PROFILES[slug]['display_name']} - {MCU_PROFILES[slug]['board_name']}",
            key="mcu_selector",
        )
        selected_mcu = get_mcu_profile(selected_mcu_slug)

        # Top Logo Header with red theme matching user drawing
        st.markdown(
            f"""
            <div class="sidebar-logo-card">
                <div style="font-size: 2.2rem; margin-bottom: 2px;">⚡</div>
                <div class="sidebar-logo-title">{selected_mcu['board_name'].upper()}</div>
                <div class="sidebar-logo-subtitle">Internal Peripheral Architecture</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        if selected_mcu_slug != "atmega2560":
            st.caption(f"Shared learning reference: {REFERENCE_MCU}")

        st.markdown("### 🔌 Peripherals")

        # Category Filter
        categories = ["All"] + sorted(list(set(p.get("category", "") for p in peripherals if p.get("category"))))
        selected_cat = st.selectbox("Filter by Subsystem:", categories, index=0)

        filtered = peripherals
        if selected_cat != "All":
            filtered = [p for p in peripherals if p.get("category") == selected_cat]

        # Options for selection
        # Keep the memory map easy to find while preserving the backend order for everything else.
        options = sorted(
            [p["slug"] for p in filtered],
            key=lambda slug: (slug != "memory", next(p.get("order_index", 0) for p in filtered if p["slug"] == slug)),
        )
        format_func = lambda slug: next((f"{p.get('icon', '🔹')} {p['name'].split('(')[0].strip()}" for p in filtered if p["slug"] == slug), slug)

        if options and st.session_state.get("peripheral_selector") not in options:
            st.session_state["peripheral_selector"] = options[0]

        selected_slug = st.radio(
            "Select Hardware Module:",
            options=options,
            format_func=format_func,
            key="peripheral_selector",
            on_change=_remember_peripheral,
            label_visibility="collapsed"
        )

        recent_slugs = [slug for slug in st.session_state["recent_peripherals"] if slug in options]
        if recent_slugs:
            st.markdown("**Recently explored**")
            for slug in recent_slugs:
                peripheral = next(p for p in filtered if p["slug"] == slug)
                st.button(
                    f"{peripheral.get('icon', '🔹')} {peripheral['name'].split('(')[0].strip()}",
                    key=f"recent_{slug}",
                    on_click=_select_recent_peripheral,
                    args=(slug,),
                    width="stretch",
                )

        st.divider()

        # System Architecture Quick Toggle
        view_mode = st.radio(
            "View Mode:",
            ["Peripheral Details & Code", "Architecture Block Diagram", "System Architecture (MVC)"],
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

    return selected_slug, selected_mcu
