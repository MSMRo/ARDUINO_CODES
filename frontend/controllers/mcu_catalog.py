from copy import deepcopy
from typing import Any, Dict, List


MCU_PROFILES: Dict[str, Dict[str, str]] = {
    "atmega2560": {
        "display_name": "ATmega2560",
        "board_name": "Arduino Mega 2560",
        "description": "The full reference dataset currently available in the learning hub.",
        "serial": "4 hardware USARTs (USART0-USART3)",
        "spi_pins": "50 (MISO), 51 (MOSI), 52 (SCK), 53 (SS)",
        "i2c_pins": "20 (SDA), 21 (SCL)",
        "timer_summary": "Timers 0, 1, 2, 3, 4, and 5",
        "pwm_summary": "16 hardware PWM channels",
        "adc_summary": "16 analog channels (A0-A15)",
        "interrupt_summary": "INT0-INT7 plus pin-change interrupts",
        "gpio_summary": "54 digital I/O pins",
        "flash": "256 KB",
        "sram": "8 KB",
        "eeprom": "4 KB",
        "eeprom_bytes": "4096 bytes",
    },
    "atmega8": {
        "display_name": "ATmega8",
        "board_name": "ATmega8 development board",
        "description": "Explore the shared Arduino and register-learning content while comparing a smaller AVR target.",
        "serial": "1 hardware USART (USART)",
        "spi_pins": "PB3 (MOSI), PB4 (MISO), PB5 (SCK), PB2 (SS)",
        "i2c_pins": "PC4 (SDA), PC5 (SCL)",
        "timer_summary": "Timers 0, 1, and 2",
        "pwm_summary": "3 hardware PWM channels",
        "adc_summary": "6 analog channels (ADC0-ADC5)",
        "interrupt_summary": "INT0 and INT1 plus pin-change interrupts",
        "gpio_summary": "23 general-purpose I/O pins",
        "flash": "8 KB",
        "sram": "1 KB",
        "eeprom": "512 bytes",
        "eeprom_bytes": "512 bytes",
    },
    "atmega328p": {
        "display_name": "ATmega328P",
        "board_name": "Arduino Uno / ATmega328P board",
        "description": "Explore the shared Arduino and register-learning content while comparing the Uno-class AVR target.",
        "serial": "1 hardware USART (USART0)",
        "spi_pins": "10 (SS), 11 (MOSI), 12 (MISO), 13 (SCK)",
        "i2c_pins": "A4 (SDA), A5 (SCL)",
        "timer_summary": "Timers 0, 1, and 2",
        "pwm_summary": "6 hardware PWM channels",
        "adc_summary": "6 analog channels (A0-A5)",
        "interrupt_summary": "INT0 and INT1 plus pin-change interrupts",
        "gpio_summary": "23 general-purpose I/O pins",
        "flash": "32 KB",
        "sram": "2 KB",
        "eeprom": "1 KB",
        "eeprom_bytes": "1024 bytes",
    },
    "atmega32u4": {
        "display_name": "ATmega32U4",
        "board_name": "Arduino Leonardo / Micro board",
        "description": "Explore the shared Arduino and register-learning content while comparing the USB-capable AVR target.",
        "serial": "1 hardware USART (USART1) plus native USB Serial",
        "spi_pins": "ICSP header (MISO, MOSI, SCK), with SS on the board header",
        "i2c_pins": "2 (SDA), 3 (SCL)",
        "timer_summary": "Timers 0, 1, 3, and 4",
        "pwm_summary": "7 hardware PWM channels",
        "adc_summary": "12 analog channels (board-dependent)",
        "interrupt_summary": "INT0-INT3 plus pin-change interrupts",
        "gpio_summary": "20 general-purpose I/O pins (board-dependent)",
        "flash": "32 KB",
        "sram": "2.5 KB",
        "eeprom": "1 KB",
        "eeprom_bytes": "1024 bytes",
    },
}

MCU_SLUGS: List[str] = list(MCU_PROFILES)
REFERENCE_MCU = "ATmega2560"


def get_mcu_profile(slug: str) -> Dict[str, str]:
    """Return a known MCU profile, falling back to the primary reference MCU."""
    return MCU_PROFILES.get(slug, MCU_PROFILES["atmega2560"])


def adapt_peripheral(peripheral: Dict[str, Any], mcu_slug: str) -> Dict[str, Any]:
    """Adapt the shared reference corpus to the selected AVR target."""
    profile = get_mcu_profile(mcu_slug)
    if mcu_slug == "atmega2560":
        return peripheral

    replacements = {
        "ATmega2560": profile["display_name"],
        "Arduino Mega 2560": profile["board_name"],
        "Mega 2560": profile["board_name"],
        "four independent, programmable hardware USARTs": profile["serial"],
        "Four independent hardware serial ports": profile["serial"],
        "four independent hardware serial ports": profile["serial"],
        "4 independent hardware serial channels (USART0, USART1, USART2, USART3)": profile["serial"],
        "4 independent USART channels (USART0, USART1, USART2, USART3)": profile["serial"],
        "Six hardware timers": profile["timer_summary"],
        "six hardware timers": profile["timer_summary"],
        "6 hardware timers (Two 8-bit, Four 16-bit)": profile["timer_summary"],
        "16 independent hardware PWM channels": profile["pwm_summary"],
        "16 dedicated hardware PWM pins": profile["pwm_summary"],
        "16 dedicated PWM pins": profile["pwm_summary"],
        "16-channel, 10-bit Successive Approximation ADC": profile["adc_summary"],
        "16-channel 10-bit Successive Approximation ADC": profile["adc_summary"],
        "16 single-ended channels (A0 - A15)": profile["adc_summary"],
        "8 dedicated hardware external interrupt pins": profile["interrupt_summary"],
        "8 dedicated external interrupts (INT0 to INT7)": profile["interrupt_summary"],
        "54 General Purpose I/O pins": profile["gpio_summary"],
        "54 general-purpose digital I/O pins": profile["gpio_summary"],
        "six hardware timers (two 8-bit, four 16-bit)": profile["timer_summary"],
        "six hardware timers": profile["timer_summary"],
        "Pins 50, 51, 52, and 53": profile["spi_pins"],
        "Pin 20 (SDA) and Pin 21 (SCL)": profile["i2c_pins"],
        "4096-byte EEPROM": f"{profile['eeprom_bytes']} EEPROM",
        "4096 bytes": profile["eeprom_bytes"],
    }

    if mcu_slug in {"atmega8", "atmega328p"}:
        replacements.update({
            "USART1": "USART0",
            "USART2": "USART0",
            "USART3": "USART0",
            "Serial1": "Serial",
            "Serial2": "Serial",
            "Serial3": "Serial",
            "UBRR1": "UBRR0",
            "UCSR1": "UCSR0",
            "UDR1": "UDR0",
            "USART1_RX_vect": "USART_RX_vect",
            "OCR4A": "OCR1A",
            "TCCR4A": "TCCR1A",
            "TCCR4B": "TCCR1B",
            "ICR4": "ICR1",
        })
    elif mcu_slug == "atmega32u4":
        replacements.update({
            "USART0": "USART1",
            "USART2": "USART1",
            "USART3": "USART1",
            "Serial2": "Serial1",
            "Serial3": "Serial1",
            "UCSR0": "UCSR1",
            "UDR0": "UDR1",
            "UBRR0": "UBRR1",
            "USART0_RX_vect": "USART1_RX_vect",
        })

    def replace_text(value: Any) -> Any:
        if isinstance(value, str):
            for source, target in replacements.items():
                value = value.replace(source, target)
            return value
        if isinstance(value, list):
            return [replace_text(item) for item in value]
        if isinstance(value, dict):
            return {key: replace_text(item) for key, item in value.items()}
        return value

    adapted = replace_text(deepcopy(peripheral))

    # Memory values are fields, not interchangeable text. Override the complete
    # memory peripheral so one value cannot accidentally rewrite another.
    if adapted.get("slug") == "memory":
        details = adapted.setdefault("details", {})
        adapted["summary"] = (
            f"{profile['flash']} Flash program memory, {profile['sram']} internal SRAM, "
            f"and {profile['eeprom']} non-volatile EEPROM for persistent configuration storage."
        )
        details["full_description"] = (
            f"The {profile['display_name']} features {profile['flash']} Flash, "
            f"{profile['sram']} SRAM, and {profile['eeprom']} EEPROM.\n\n"
            "### 🔑 Commonly Used Registers for EEPROM & Flash Memory\n"
            "- **`EEARH` / `EEARL`**: EEPROM address registers.\n"
            "- **`EEDR`**: EEPROM data register.\n"
            "- **`EECR`**: EEPROM control register (`EERE`, `EEPE`, `EEMPE`).\n"
            "- **`SPMCSR`**: Store Program Memory Control Register."
        )
        details["hardware_specs"] = (
            f"- **Flash**: {profile['flash']}\n"
            f"- **SRAM**: {profile['sram']}\n"
            f"- **EEPROM**: {profile['eeprom']}"
        )
        details["hardware_registers"] = details["hardware_registers"].replace(
            "Address 0 to 4095", f"Address range sized for {profile['eeprom']} EEPROM"
        )
        adapted["libraries"] = replace_text(adapted.get("libraries", []))
        adapted["code_examples"] = replace_text(adapted.get("code_examples", []))

    if adapted.get("slug") == "timers":
        adapted["summary"] = f"{profile['timer_summary']} with CTC, PWM, and input-capture modes."
        adapted["details"]["full_description"] = (
            f"The {profile['display_name']} includes {profile['timer_summary']}. "
            "These hardware counters operate independently of the CPU core and support normal, CTC, PWM, and input-capture operation."
        )
        adapted["details"]["hardware_specs"] = (
            f"- **Total Timers**: {profile['timer_summary']}\n"
            "- **Prescalers**: 1, 8, 64, 256, 1024 where supported\n"
            "- **Modes**: Normal, Clear Timer on Compare Match (CTC), Fast PWM, Phase Correct PWM"
        )

    if adapted.get("slug") == "gpio":
        adapted["summary"] = f"{profile['gpio_summary']} with direct port-register access."

    return adapted