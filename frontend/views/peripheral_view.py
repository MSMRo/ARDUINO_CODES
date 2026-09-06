import streamlit as st
from typing import Dict, Any


def render_peripheral_view(peripheral: Dict[str, Any]):
    """Render peripheral information, registers, visual bitfields, and pinouts."""
    details = peripheral.get("details", {})
    if not details and "full_description" in peripheral:
        details = peripheral  # handle flat schema if any

    icon = peripheral.get("icon", "🔌")
    name = peripheral.get("name", "ATmega2560 Peripheral")
    category = peripheral.get("category", "General")
    summary = peripheral.get("summary", "")

    # Top Peripheral Title & Category
    st.markdown(
        f"""
        <div style="margin-bottom: 15px;">
            <span class="badge-category">{category}</span>
            <span class="badge-difficulty" style="background-color: #E0E7FF; color: #3730A3;">ATmega2560 Hardware Architecture</span>
            <h1 style="font-size: 1.85rem; font-weight: 800; margin: 8px 0 4px 0; color: #0F172A;">{icon} {name}</h1>
            <p style="font-size: 1.05rem; color: #475569; margin: 0;">{summary}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

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
    spec_tabs = st.tabs(["⚙️ Hardware Specifications", "📋 Hardware Registers & Bit Mapping", "📌 Mega 2560 Pinout Mapping"])

    with spec_tabs[0]:
        st.markdown(details.get("hardware_specs", "No specifications recorded."))

    with spec_tabs[1]:
        st.markdown("#### Low-Level Internal Registers, Control Bits & Bitfield Layouts")
        st.caption("Direct register manipulation bypasses Arduino core wrappers for zero-latency execution and maximum control.")
        st.markdown(hw_registers_text)

    with spec_tabs[2]:
        st.markdown("#### ATmega2560 Physical Pins vs Arduino Mega 2560 Header Board Mapping")
        st.markdown(details.get("mega2560_pins", "Pinout information not available."))

