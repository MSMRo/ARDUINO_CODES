import os
import sys
from pathlib import Path

# Ensure project root directory is in sys.path for top-level package imports
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import streamlit as st
from frontend.controllers.api_client import api_client
from frontend.views.sidebar import render_sidebar
from frontend.views.peripheral_view import render_peripheral_view
from frontend.views.code_viewer import render_code_viewer
from frontend.views.architecture_view import render_block_diagram_view, render_mvc_system_view

# Streamlit Page Configuration
st.set_page_config(
    page_title="Arduino codes made easy - ATmega2560",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load Custom CSS
css_path = os.path.join(os.path.dirname(__file__), "static", "styles.css")
if os.path.exists(css_path):
    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def main():
    # Fetch health & peripheral metadata from Backend API
    health_info = api_client.check_health()
    peripherals = api_client.get_peripherals()

    # Top Banner / Header matching required project title
    col_head, col_badge = st.columns([3, 1])
    with col_head:
        st.markdown('<h1 class="main-title">Arduino codes made easy</h1>', unsafe_allow_html=True)
        st.markdown('<p class="sub-title">Interactive ATmega2560 Hardware Architecture & Code Learning Hub</p>', unsafe_allow_html=True)

    with col_badge:
        db_stat = health_info.get("database", {}).get("status", "unknown")
        engine_name = health_info.get("database", {}).get("engine_dialect", "sql")
        is_sq = health_info.get("database", {}).get("is_sqlite_fallback", False)
        badge_text = "PostgreSQL" if not is_sq and db_stat == "connected" else "SQLite (Fallback)"
        st.markdown(
            f"""
            <div style="text-align: right; padding-top: 8px;">
                <span class="status-pill">
                    <span style="height: 7px; width: 7px; background-color: #10B981; border-radius: 50%;"></span>
                    FastAPI + {badge_text}
                </span>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Render Sidebar navigation
    selected_slug = render_sidebar(peripherals, health_info)
    view_mode = st.session_state.get("view_mode", "Peripheral Details & Code")

    # Routing based on View Mode
    if view_mode == "ATmega2560 Block Diagram":
        render_block_diagram_view()
    elif view_mode == "System Architecture (MVC)":
        render_mvc_system_view()
    else:
        # Default Mode: Peripheral Details, Libraries, and Code Viewer
        if selected_slug:
            # Fetch detailed peripheral data via API Client Controller
            peripheral_data = api_client.get_peripheral_detail(selected_slug)
            if peripheral_data:
                # 1. Hardware Description, Specs, Registers, and Pinout
                render_peripheral_view(peripheral_data)
                
                # 2. Library Analysis & Arduino Code Examples
                render_code_viewer(peripheral_data)
            else:
                st.error(f"Could not load details for peripheral '{selected_slug}'.")
        else:
            st.info("Select a peripheral from the sidebar to begin exploring.")

    # Global Code Search Box at footer
    with st.expander("🔎 Quick Code Search across all ATmega2560 Peripherals"):
        search_query = st.text_input("Search keywords (e.g., 'Serial1', 'analogRead', 'Timer 1', 'OCR4A'):")
        if search_query:
            results = api_client.search_codes(query=search_query)
            if results:
                st.success(f"Found {len(results)} matching code example(s):")
                for r in results:
                    st.markdown(f"**{r.get('title')}** ({r.get('difficulty')} - {r.get('category')})")
                    st.code(r.get("code"), language="cpp")
                    st.markdown(f"*{r.get('description')}*")
                    st.divider()
            else:
                st.warning("No code examples matched your search query.")


if __name__ == "__main__":
    main()
