import os
import streamlit as st
from typing import Dict


def _render_target_architecture(mcu: Dict[str, str]) -> None:
    st.markdown("### Target-specific block diagram")
    st.caption("A compact datasheet-style view of the selected AVR's CPU, memory, buses, and peripheral blocks.")

    with st.container(border=True):
        st.markdown(f"#### {mcu.get('display_name', 'AVR')} internal architecture")
        top_left, top_center, top_right = st.columns(3)
        with top_left:
            st.markdown("**Program memory**")
            st.info(f"Flash\n\n{mcu.get('flash', 'Target-specific')}")
        with top_center:
            st.markdown("**AVR CPU core**")
            st.success("8-bit RISC core\n\n32 working registers")
        with top_right:
            st.markdown("**Data memory**")
            st.warning(f"SRAM\n\n{mcu.get('sram', 'Target-specific')}\n\nEEPROM {mcu.get('eeprom', 'Target-specific')}")

        st.markdown("**System bus and control**")
        st.code("CPU core  <->  data bus  <->  peripheral registers", language="text")

        peripheral_cols = st.columns(4)
        blocks = [
            ("Serial", mcu.get("serial", "Target-specific USART")),
            ("Timers / PWM", f"{mcu.get('timer_summary', 'Target-specific timers')}\n{mcu.get('pwm_summary', 'Target-specific PWM')}"),
            ("ADC", mcu.get("adc_summary", "Target-specific ADC")),
            ("I/O and interrupts", f"{mcu.get('gpio_summary', 'Target-specific GPIO')}\n{mcu.get('interrupt_summary', 'Target-specific interrupts')}"),
        ]
        for column, (title, value) in zip(peripheral_cols, blocks):
            with column:
                st.markdown(f"**{title}**")
                st.container(border=True).write(value)

        st.markdown(f"**Buses**: SPI on {mcu.get('spi_pins', 'target-specific pins')} | I2C/TWI on {mcu.get('i2c_pins', 'target-specific pins')}")


def render_block_diagram_view(mcu: Dict[str, str]):
    """Render the selected MCU architecture and subsystem tour."""
    mcu_name = mcu.get("display_name", "ATmega2560")
    st.markdown(f"## 📐 {mcu_name} Microcontroller Architecture")
    st.markdown(mcu.get("description", "Target-specific AVR architecture overview."))

    image_path = "assets/atmega2560_architecture.jpg"
    if mcu_name == "ATmega2560" and os.path.exists(image_path):
        st.image(image_path, caption="ATmega2560 Microcontroller Architecture Technical Block Diagram", use_container_width=True)
    elif mcu_name != "ATmega2560":
        _render_target_architecture(mcu)
    else:
        st.warning("Architecture diagram image not found in assets/ folder.")

    st.markdown("### 🧩 Subsystem Architecture Overview")
    col1, col2 = st.columns(2)

    with col1:
        with st.expander("📡 Serial Communication Block", expanded=True):
            st.markdown(
                f"- **Serial hardware**: {mcu.get('serial', 'Target-specific USART configuration')}.\n"
                f"- **SPI Port**: High-speed synchronous bus on {mcu.get('spi_pins', 'target-specific SPI pins')}.\n"
                f"- **TWI / I2C**: Philips compatible 2-wire bus on {mcu.get('i2c_pins', 'target-specific SDA/SCL pins')}."
            )

        with st.expander("⏱️ Timers/Counters & PWM Channels", expanded=True):
            st.markdown(
                f"- **Timers/Counters**: {mcu.get('timer_summary', 'Target-specific timers')}.\n"
                f"- **PWM**: {mcu.get('pwm_summary', 'Target-specific PWM channels')}."
            )

        with st.expander("📊 Analog-to-Digital Converter (ADC)", expanded=True):
            st.markdown(
                f"- **Analog inputs**: {mcu.get('adc_summary', 'Target-specific ADC channels')}.\n"
                "- **10-bit Resolution**: 1024 discrete steps (0 - 1023).\n"
                "- **On-chip References**: 5V AVCC, 1.1V bandgap, 2.56V precision reference, and external AREF."
            )

    with col2:
        with st.expander("🎛️ Digital I/O Ports", expanded=True):
            st.markdown(
                f"- **Digital I/O**: {mcu.get('gpio_summary', 'Target-specific digital I/O')}.\n"
                "- **Direct Port Access**: 1 clock cycle (62.5ns) single-instruction port toggling via `PINx` and `PORTx`."
            )

        with st.expander("🧠 AVR CPU Core & Memories", expanded=True):
            st.markdown(
                f"- **CPU**: 8-bit RISC AVR core.\n"
                "- **32 Working Registers**: Single-cycle ALU execution.\n"
                f"- **Flash Memory**: {mcu.get('flash', 'Target-specific')} for program code.\n"
                f"- **SRAM**: {mcu.get('sram', 'Target-specific')} for runtime variables and call stack.\n"
                f"- **EEPROM**: {mcu.get('eeprom', 'Target-specific')} non-volatile memory."
            )

        with st.expander("🛡️ Supporting Circuits", expanded=True):
            st.markdown(
                "- **Clock Generation**: 16 MHz external quartz crystal oscillator.\n"
                "- **Watchdog Timer**: Dedicated 128 kHz RC oscillator for system freeze recovery.\n"
                "- **Power Supervision**: Power-On Reset (POR) and Brown-out Detector (BOD)."
            )


def render_mvc_system_view():
    """Render MVC full-stack system architecture and C4 diagram summary."""
    st.markdown("## 🏗️ System Architecture & MVC Design Pattern")
    st.markdown(
        "This project is engineered using a strict **Model-View-Controller (MVC)** design pattern, "
        "separating the visual interface, business logic/routing, and persistent database entities."
    )

    col1, col2 = st.columns(2)
    with col1:
        if os.path.exists("assets/ui_wireframe.png"):
            st.image("assets/ui_wireframe.png", caption="Handwritten UI Wireframe Layout", use_container_width=True)
    with col2:
        if os.path.exists("assets/mvc_sketch.png"):
            st.image("assets/mvc_sketch.png", caption="Handwritten MVC & Database Architecture Sketch", use_container_width=True)

    st.markdown("### 🏛️ MVC Layer Implementation")
    st.markdown(
        """
        | MVC Layer | Component | Technology | Responsibility |
        |---|---|---|---|
        | **View** | Frontend UI (`frontend/views/`) | **Streamlit** + Custom CSS | Renders interactive sidebar, peripheral details, tabs, and syntax-highlighted code viewers. |
        | **Controller** | API Client + Backend Endpoints | **FastAPI** (`backend/app/controllers/`) | Validates requests, serves REST endpoints (`/api/v1/peripherals`, `/api/v1/codes`), and coordinates data transfer. |
        | **Model** | Database & Schemas | **PostgreSQL** + **SQLAlchemy** + **Pydantic** | Relational schema holding 4 normalized tables: `peripherals`, `peripheral_details`, `code_examples`, and `libraries`. |
        """
    )
