import os
import streamlit as st


def render_block_diagram_view():
    """Render ATmega2560 hardware architecture diagram and subsystem tour."""
    st.markdown("## 📐 ATmega2560 Microcontroller Architecture")
    st.markdown(
        "Technical block diagram showing internal peripherals, buses, and memory spaces of the ATmega2560."
    )

    image_path = "assets/atmega2560_architecture.jpg"
    if os.path.exists(image_path):
        st.image(image_path, caption="ATmega2560 Microcontroller Architecture Technical Block Diagram", use_container_width=True)
    else:
        st.warning("Architecture diagram image not found in assets/ folder.")

    st.markdown("### 🧩 Subsystem Architecture Overview")
    col1, col2 = st.columns(2)

    with col1:
        with st.expander("📡 Serial Communication Block", expanded=True):
            st.markdown(
                "- **4 Independent USARTs**: USART0 (USB/Pins 0-1), USART1 (19-18), USART2 (17-16), USART3 (15-14).\n"
                "- **1 SPI Port**: High-speed synchronous bus on Pins 50 (MISO), 51 (MOSI), 52 (SCK), 53 (SS).\n"
                "- **1 TWI / I2C**: Philips compatible 2-wire bus on Pins 20 (SDA) and 21 (SCL)."
            )

        with st.expander("⏱️ Timers/Counters & PWM Channels", expanded=True):
            st.markdown(
                "- **Two 8-bit Timers**: Timer 0 (millis timebase) and Timer 2 (asynchronous RTC crystal support).\n"
                "- **Four 16-bit Timers**: Timers 1, 3, 4, 5 with CTC and Input Capture.\n"
                "- **16 Hardware PWM Channels**: Pins 2-13 and 44-46."
            )

        with st.expander("📊 Analog-to-Digital Converter (ADC)", expanded=True):
            st.markdown(
                "- **16 Multiplexed Channels**: Pins A0 to A15 (Ports F and K).\n"
                "- **10-bit Resolution**: 1024 discrete steps (0 - 1023).\n"
                "- **On-chip References**: 5V AVCC, 1.1V bandgap, 2.56V precision reference, and external AREF."
            )

    with col2:
        with st.expander("🎛️ Digital I/O Ports", expanded=True):
            st.markdown(
                "- **54 Digital I/O Pins**: Grouped into 11 8-bit ports (A, B, C, D, E, F, G, H, J, K, L).\n"
                "- **Direct Port Access**: 1 clock cycle (62.5ns) single-instruction port toggling via `PINx` and `PORTx`."
            )

        with st.expander("🧠 AVR CPU Core & Memories", expanded=True):
            st.markdown(
                "- **CPU**: 8-bit RISC AVR core operating at 16 MHz (16 MIPS).\n"
                "- **32 Working Registers**: Single-cycle ALU execution.\n"
                "- **Flash Memory**: 256 KB for program code.\n"
                "- **SRAM**: 8 KB for runtime variables and call stack.\n"
                "- **EEPROM**: 4 KB non-volatile memory."
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
