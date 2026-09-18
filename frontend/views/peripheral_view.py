import streamlit as st
from typing import Dict, Any
from frontend.controllers.mcu_catalog import REFERENCE_MCU
from frontend.controllers.peripheral_guides import get_register_guide


def _render_register_guide(
    peripheral_slug: str,
    mcu: Dict[str, str],
    include_registers: bool = True,
    include_modes: bool = True,
) -> None:
    guide = get_register_guide(peripheral_slug, mcu)
    registers = guide.get("registers", [])
    modes = guide.get("modes", [])

    st.markdown(f"#### {guide.get('title', 'Register map')}")
    st.caption("Common control registers and bit fields from the selected AVR datasheet family.")

    if include_registers and include_modes:
        register_tab, mode_tab = st.tabs(["Register map", "Operating modes"])
    else:
        register_tab = st.container() if include_registers else None
        mode_tab = st.container() if include_modes else None

    if include_registers and register_tab is not None:
        with register_tab:
            for row in registers:
                fields = [field.strip() for field in row["bits"].split("|")]
                bit_numbers = list(range(len(fields) - 1, -1, -1))
                field_cells = "".join(
                    f'<div class="datasheet-register-field">{field or "—"}</div>'
                    for field in fields
                )
                bit_cells = "".join(
                    f'<div class="datasheet-register-bit">{bit}</div>'
                    for bit in bit_numbers
                )
                st.markdown(
                    f"""
                    <div class="datasheet-register">
                        <div class="datasheet-register-heading">
                            <strong>{row['register']}</strong>
                            <span>{row['purpose']}</span>
                        </div>
                        <div class="datasheet-register-grid" style="grid-template-columns: repeat({len(fields)}, minmax(0, 1fr));">
                            {bit_cells}
                            {field_cells}
                        </div>
                        <div class="datasheet-register-note">{row['bits']}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                st.divider()

    if include_modes and mode_tab is not None:
        with mode_tab:
            for mode in modes:
                with st.container(border=True):
                    st.markdown(f"**{mode['mode']}**")
                    st.caption(f"Configuration: `{mode['configuration']}`")
                    st.write(mode["use"])


def render_peripheral_view(peripheral: Dict[str, Any], mcu: Dict[str, str]):
    """Render peripheral information, registers, visual bitfields, and pinouts."""
    details = peripheral.get("details", {})
    if not details and "full_description" in peripheral:
        details = peripheral  # handle flat schema if any

    icon = peripheral.get("icon", "🔌")
    name = peripheral.get("name", "ATmega2560 Peripheral")
    category = peripheral.get("category", "General")
    summary = peripheral.get("summary", "")
    mcu_name = mcu.get("display_name", REFERENCE_MCU)

    # Top Peripheral Title & Category
    st.markdown(
        f"""
        <div style="margin-bottom: 15px;">
            <span class="badge-category">{category}</span>
            <span class="badge-difficulty" style="background-color: #E0E7FF; color: #3730A3;">{mcu_name} Hardware Architecture</span>
            <h1 style="font-size: 1.85rem; font-weight: 800; margin: 8px 0 4px 0; color: #0F172A;">{icon} {name}</h1>
            <p style="font-size: 1.05rem; color: #475569; margin: 0;">{summary}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    if mcu_name != REFERENCE_MCU:
        st.info(f"This {mcu_name} view reuses the {REFERENCE_MCU} Arduino and register examples as a learning reference. Pin mappings and register names should be checked against the {mcu_name} datasheet before hardware use.")

    # Architecture Role Alert
    role = details.get("architecture_role", "")
    if role:
        st.info(f"**🏛️ Architecture Role:** {role}")

    # Description & Overview
    st.markdown("### 📖 Hardware Description & Architecture")
    st.markdown(details.get("full_description", "No description available."))

    # Commonly Used Registers Quick Reference Highlight Card
    hw_registers_text = details.get("hardware_registers", "")
    st.markdown(
        """
        <div style="background-color: #F8FAFC; border: 1px solid #CBD5E1; border-left: 5px solid #0284C7; padding: 14px 18px; border-radius: 8px; margin: 15px 0 20px 0;">
            <div style="display: flex; align-items: center; gap: 8px; font-weight: 700; font-size: 1.1rem; color: #0F172A;">
                <span>🔑</span> Commonly Used Registers Quick Reference
            </div>
            <div style="font-size: 0.9rem; color: #475569; margin-top: 4px;">
                These low-level AVR control, data, and status registers are directly manipulated when operating this peripheral without Arduino core abstraction layers.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Hardware Specs, Registers, and Pinout Tabs
    spec_tabs = st.tabs(["⚙️ Hardware Specifications", "📋 Hardware Registers & Bit Mapping", f"📌 {mcu.get('board_name', 'Board')} Pinout Mapping"])

    with spec_tabs[0]:
        st.markdown(details.get("hardware_specs", "No specifications recorded."))
        _render_register_guide(peripheral.get("slug", ""), mcu, include_registers=False)

    with spec_tabs[1]:
        st.markdown("#### Low-Level Internal Registers, Control Bits & Bitfield Layouts")
        st.caption("Direct register manipulation bypasses Arduino core wrappers for zero-latency execution and maximum control.")
        _render_register_guide(peripheral.get("slug", ""), mcu, include_modes=False)
        with st.expander("Datasheet notes and register address reference"):
            st.markdown(hw_registers_text)

    with spec_tabs[2]:
        st.markdown(f"#### {mcu_name} Physical Pins vs {mcu.get('board_name', 'board')} Header Board Mapping")
        st.markdown(details.get("mega2560_pins", "Pinout information not available."))

