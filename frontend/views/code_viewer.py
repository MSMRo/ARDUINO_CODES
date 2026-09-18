import streamlit as st
from typing import Dict, Any, List
from frontend.controllers.mcu_catalog import REFERENCE_MCU


def render_code_viewer(peripheral: Dict[str, Any], mcu: Dict[str, str]):
    """
    Render Arduino library requirements and practical Arduino code examples.
    """
    details = peripheral.get("details", {})
    if not details and "library_analysis" in peripheral:
        details = peripheral

    libraries: List[Dict[str, Any]] = peripheral.get("libraries", [])
    code_examples: List[Dict[str, Any]] = peripheral.get("code_examples", [])
    mcu_name = mcu.get("display_name", REFERENCE_MCU)

    st.divider()

    # 1. LIBRARIES SECTION
    st.markdown("### 📚 Arduino Libraries & Toolchain Requirements")

    requires_ext = details.get("requires_external_library", False)
    if not requires_ext:
        st.markdown(
            f"""
            <div class="library-box-native">
                <div style="font-weight: 700; font-size: 1.05rem;">✅ No External Library Required</div>
                <div style="font-size: 0.92rem; margin-top: 4px;">
                    This {mcu_name} peripheral is natively supported by the standard Arduino Core or the built-in AVR Libc runtime.
                    You do not need to install any external packages through the Library Manager to use this hardware feature.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            """
            <div class="library-box-external">
                <div style="font-weight: 700; font-size: 1.05rem;">📦 Third-Party / External Library Recommended</div>
                <div style="font-size: 0.92rem; margin-top: 4px;">
                    An external helper library simplifies hardware control for this peripheral.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Detailed Analysis
    analysis = details.get("library_analysis", "")
    if analysis:
        st.markdown(analysis)

    # Library Cards
    if libraries:
        st.markdown("#### Available & Recommended Libraries:")
        cols = st.columns(len(libraries) if len(libraries) <= 3 else 2)
        for i, lib in enumerate(libraries):
            col = cols[i % len(cols)]
            with col:
                builtin_badge = "🟢 Built-in" if lib.get("is_builtin", True) else "🟡 Third-party"
                st.markdown(
                    f"""
                    <div style="background-color: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 8px; padding: 12px; height: 100%;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                            <span style="font-weight: 700; font-size: 0.95rem; color: #1E293B;">{lib.get('name')}</span>
                            <span style="font-size: 0.75rem; font-weight: 600;">{builtin_badge}</span>
                        </div>
                        <code style="font-size: 0.85rem; color: #0284C7;">{lib.get('header_file')}</code>
                        <p style="font-size: 0.82rem; color: #475569; margin: 6px 0;">{lib.get('purpose')}</p>
                        <div style="font-size: 0.78rem; color: #64748B;"><b>Installation:</b> {lib.get('installation_guide')}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                if lib.get("documentation_url"):
                    st.link_button("📖 Official Documentation", lib["documentation_url"])

    st.divider()

    # 2. CODE EXAMPLES SECTION
    st.markdown("### 💻 Practical Code Examples & Firmware Implementations")
    st.caption("Explore low-level AVR register manipulation vs high-level Arduino core and library abstractions.")

    if not code_examples:
        st.info("No code examples currently loaded for this peripheral.")
        return

    # Filter selector for Code Example Category
    filter_col1, filter_col2 = st.columns([2, 3])
    with filter_col1:
        code_filter = st.radio(
            "Filter Code Approach:",
            ["Show All Examples", "⚡ Only Registers (Bare-Metal)", "📦 Only Arduino Code / Library"],
            horizontal=True,
            key=f"filter_{peripheral.get('slug', 'p')}"
        )

    # Filter examples list based on user choice
    filtered_examples = []
    for ex in code_examples:
        cat = ex.get("category", "")
        is_register = "Register" in cat or "Bare-Metal" in cat or "Direct" in cat
        if code_filter == "⚡ Only Registers (Bare-Metal)":
            if is_register:
                filtered_examples.append(ex)
        elif code_filter == "📦 Only Arduino Code / Library":
            if not is_register:
                filtered_examples.append(ex)
        else:
            filtered_examples.append(ex)

    if not filtered_examples:
        st.warning(f"No code examples match the selected filter option ('{code_filter}').")
        return

    # Create tabs for each filtered example
    tab_titles = []
    for ex in filtered_examples:
        cat = ex.get("category", "Example")
        is_register = "Register" in cat or "Bare-Metal" in cat or "Direct" in cat
        icon = "⚡ Register-Only" if is_register else "📦 Arduino Core/Lib"
        tab_titles.append(f"{icon}: {ex.get('title', 'Example')[:35]}")

    code_tabs = st.tabs(tab_titles)

    for i, ex in enumerate(filtered_examples):
        with code_tabs[i]:
            cat = ex.get("category", "Standard Arduino API")
            is_register = "Register" in cat or "Bare-Metal" in cat or "Direct" in cat
            
            col_t, col_b = st.columns([3, 1])
            with col_t:
                st.markdown(f"#### {ex.get('title')}")
                st.markdown(f"*{ex.get('description')}*")
            with col_b:
                diff = ex.get("difficulty", "Beginner")
                color = "#10B981" if diff == "Beginner" else ("#F59E0B" if diff == "Intermediate" else "#EF4444")
                type_badge = (
                    '<span style="background-color: #FEF3C7; color: #92400E; border: 1px solid #F59E0B; padding: 4px 10px; border-radius: 12px; font-weight: 700; font-size: 0.78rem; margin-right: 6px;">⚡ Direct Register</span>'
                    if is_register else
                    '<span style="background-color: #E0F2FE; color: #075985; border: 1px solid #0284C7; padding: 4px 10px; border-radius: 12px; font-weight: 700; font-size: 0.78rem; margin-right: 6px;">📦 Arduino Core / Library</span>'
                )
                st.markdown(
                    f"""
                    <div style="text-align: right;">
                        {type_badge}
                        <span style="background-color: {color}20; color: {color}; border: 1px solid {color}; padding: 4px 10px; border-radius: 12px; font-weight: 700; font-size: 0.78rem;">
                            {diff} Level
                        </span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            # Code Language Badge & Code Box
            st.caption(f"**Implementation Paradigm:** {cat}")
            st.code(ex.get("code", "// Code snippet"), language="cpp")

            # Explanation & Circuit Notes
            st.markdown("##### 🔍 Code Breakdown & Line-by-Line Analysis:")
            st.markdown(ex.get("explanation", "No breakdown available."))

            circuit = ex.get("circuit_notes")
            if circuit:
                st.info(f"**🔌 Circuit Wiring & Hardware Setup:** {circuit}")

