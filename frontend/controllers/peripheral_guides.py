from typing import Any, Dict, List


REGISTER_GUIDES: Dict[str, Dict[str, Any]] = {
    "usart": {
        "title": "USART register map and operating modes",
        "registers": [
            {"register": "UBRRnH / UBRRnL", "purpose": "Baud-rate divider", "bits": "16-bit value; UBRR = F_CPU / (16 x baud) - 1"},
            {"register": "UCSRnA", "purpose": "Status and speed", "bits": "RXCn | TXCn | UDREn | FEn | DORn | UPEn | U2Xn | MPCMn"},
            {"register": "UCSRnB", "purpose": "Enable and interrupts", "bits": "RXCIEn | TXCIEn | UDRIEn | RXENn | TXENn | UCSZn2 | RXB8n | TXB8n"},
            {"register": "UCSRnC", "purpose": "Frame format", "bits": "UMSELn | UPMn1:0 | USBSn | UCSZn1:0 | UCPOLn"},
            {"register": "UDRn", "purpose": "Transmit / receive buffer", "bits": "8-bit data, read to receive or write to transmit"},
        ],
        "modes": [
            {"mode": "Asynchronous normal", "configuration": "U2Xn = 0", "use": "Standard UART communication with maximum compatibility."},
            {"mode": "Asynchronous double speed", "configuration": "U2Xn = 1", "use": "Higher baud-rate precision or reduced baud error."},
            {"mode": "Synchronous master", "configuration": "UMSELn1:0 = 01", "use": "USART supplies the clock on XCKn."},
            {"mode": "Frame formats", "configuration": "UCSZn, UPMn, USBSn", "use": "Select 5-9 data bits, parity, and one or two stop bits."},
        ],
    },
    "spi": {
        "title": "SPI register map and operating modes",
        "registers": [
            {"register": "SPCR", "purpose": "SPI control", "bits": "SPIE | SPE | DORD | MSTR | CPOL | CPHA | SPR1:0"},
            {"register": "SPSR", "purpose": "SPI status", "bits": "SPIF | WCOL | SPI2X"},
            {"register": "SPDR", "purpose": "SPI data", "bits": "8-bit shift data register"},
        ],
        "modes": [
            {"mode": "Master", "configuration": "MSTR = 1", "use": "AVR generates SCK and controls slave select."},
            {"mode": "Slave", "configuration": "MSTR = 0", "use": "AVR receives SCK from an external master."},
            {"mode": "SPI mode 0-3", "configuration": "CPOL / CPHA", "use": "Match clock polarity and sampling phase to the peripheral."},
            {"mode": "Double speed", "configuration": "SPI2X = 1", "use": "Doubles the SPI clock when the selected prescaler allows it."},
        ],
    },
    "twi": {
        "title": "TWI / I2C register map and operating modes",
        "registers": [
            {"register": "TWBR", "purpose": "Bit-rate generator", "bits": "SCL frequency divider"},
            {"register": "TWSR", "purpose": "Status and prescaler", "bits": "TWS7:3 status code | TWPS1:0 prescaler"},
            {"register": "TWCR", "purpose": "Control and flags", "bits": "TWINT | TWEA | TWSTA | TWSTO | TWWC | TWEN | TWIE"},
            {"register": "TWDR", "purpose": "Data register", "bits": "8-bit data byte transmitted or received"},
            {"register": "TWAR / TWAMR", "purpose": "Address and mask", "bits": "Own slave address and address-match mask"},
        ],
        "modes": [
            {"mode": "Master transmitter", "configuration": "START -> SLA+W -> data -> STOP", "use": "Write registers or commands to a slave."},
            {"mode": "Master receiver", "configuration": "START -> SLA+R -> data -> NACK", "use": "Read bytes from a slave device."},
            {"mode": "Slave receiver", "configuration": "TWAR + TWEN + TWEA", "use": "Respond to a matching address from an external master."},
            {"mode": "Bus arbitration", "configuration": "TWSR status codes", "use": "Detect ACK, NACK, arbitration loss, and bus errors."},
        ],
    },
    "timers": {
        "title": "Timer / counter register map and operating modes",
        "registers": [
            {"register": "TCCRnA", "purpose": "Waveform and output compare", "bits": "COMnA/B/C | WGMn1:0"},
            {"register": "TCCRnB", "purpose": "Clock and waveform", "bits": "ICNCn | ICESn | WGMn3:2 | CSn2:0"},
            {"register": "TCNTn", "purpose": "Counter value", "bits": "Current 8-bit or 16-bit timer count"},
            {"register": "OCRnA/B/C", "purpose": "Compare values", "bits": "Output compare match and PWM duty value"},
            {"register": "TIMSKn / TIFRn", "purpose": "Interrupt enable and flags", "bits": "Overflow, compare-match, and input-capture events"},
        ],
        "modes": [
            {"mode": "Normal", "configuration": "WGM = 0", "use": "Free-running counter with overflow interrupt."},
            {"mode": "CTC", "configuration": "WGM selects OCRnA as TOP", "use": "Accurate periodic interrupts or output toggling."},
            {"mode": "Fast PWM", "configuration": "Fast PWM WGM mode", "use": "High-frequency PWM with adjustable duty cycle."},
            {"mode": "Phase-correct PWM", "configuration": "Phase-correct WGM mode", "use": "Symmetric PWM for motor and power-control applications."},
            {"mode": "Input capture", "configuration": "ICESn + ICFn", "use": "Timestamp an external edge in ICRn."},
        ],
    },
    "pwm": {
        "title": "PWM register map and operating modes",
        "registers": [
            {"register": "TCCRnA / TCCRnB", "purpose": "PWM waveform setup", "bits": "COMnA/B/C output mode | WGM waveform mode | CS prescaler"},
            {"register": "OCRnA/B/C", "purpose": "Duty-cycle compare", "bits": "Compare value controls output duty cycle"},
            {"register": "ICRn / OCRnA", "purpose": "TOP value", "bits": "Sets PWM period in programmable TOP modes"},
            {"register": "TIMSKn / TIFRn", "purpose": "PWM interrupts", "bits": "Overflow and compare-match enable/flags"},
        ],
        "modes": [
            {"mode": "Fast PWM", "configuration": "WGM fast mode", "use": "Fast edge-aligned PWM for LEDs, motors, and switching."},
            {"mode": "Phase-correct PWM", "configuration": "WGM phase-correct mode", "use": "Center-aligned PWM with reduced harmonic asymmetry."},
            {"mode": "Non-inverting output", "configuration": "COMnA1:0 = 10", "use": "Duty increases as OCRn increases."},
            {"mode": "Inverting output", "configuration": "COMnA1:0 = 11", "use": "Duty is inverted for active-low drive stages."},
        ],
    },
    "adc": {
        "title": "ADC register map and operating modes",
        "registers": [
            {"register": "ADMUX", "purpose": "Reference and channel", "bits": "REFS1:0 | ADLAR | MUX bits"},
            {"register": "ADCSRA", "purpose": "ADC control", "bits": "ADEN | ADSC | ADATE | ADIF | ADIE | ADPS2:0"},
            {"register": "ADCSRB", "purpose": "Trigger and channel extension", "bits": "ADTS2:0 and device-specific MUX extension"},
            {"register": "ADCL / ADCH", "purpose": "Conversion result", "bits": "10-bit result, left or right adjusted"},
            {"register": "DIDR0 / DIDR1", "purpose": "Digital input disable", "bits": "Disconnects digital input buffers from ADC pins"},
        ],
        "modes": [
            {"mode": "Single conversion", "configuration": "ADSC = 1", "use": "Start and read one conversion when needed."},
            {"mode": "Free running", "configuration": "ADATE + ADTS = 000", "use": "Continuously sample at the ADC clock rate."},
            {"mode": "Auto-triggered", "configuration": "ADATE + ADTS source", "use": "Synchronize conversions to timers, interrupts, or external events."},
            {"mode": "Sleep noise reduction", "configuration": "ADC Noise Reduction sleep", "use": "Reduce digital switching noise during conversion."},
        ],
    },
    "interrupts": {
        "title": "External interrupt register map and operating modes",
        "registers": [
            {"register": "EICRA / EICRB", "purpose": "External interrupt sense", "bits": "ISCn1:0 selects low, change, falling, or rising edge"},
            {"register": "EIMSK", "purpose": "Interrupt enable", "bits": "INTn enable bits"},
            {"register": "EIFR", "purpose": "Interrupt flags", "bits": "INTFn flags cleared by writing one"},
            {"register": "PCICR / PCIFR", "purpose": "Pin-change interrupts", "bits": "PCIE groups and PCIF flags"},
            {"register": "PCMSKx", "purpose": "Pin-change mask", "bits": "Selects pins within each pin-change group"},
        ],
        "modes": [
            {"mode": "Low level", "configuration": "ISCn1:0 = 00", "use": "Interrupt remains active while the input is low."},
            {"mode": "Any logical change", "configuration": "ISCn1:0 = 01", "use": "Respond to both rising and falling transitions."},
            {"mode": "Falling edge", "configuration": "ISCn1:0 = 10", "use": "Respond only when the signal falls."},
            {"mode": "Rising edge", "configuration": "ISCn1:0 = 11", "use": "Respond only when the signal rises."},
        ],
    },
    "gpio": {
        "title": "GPIO register map and operating modes",
        "registers": [
            {"register": "DDRx", "purpose": "Data direction", "bits": "1 = output, 0 = input"},
            {"register": "PORTx", "purpose": "Output or pull-up", "bits": "Output level when output; pull-up enable when input"},
            {"register": "PINx", "purpose": "Input read and toggle", "bits": "Read pin state; write one to toggle output latch"},
            {"register": "MCUCR / port control", "purpose": "Global port behavior", "bits": "Device-specific pull-up and alternate-function controls"},
        ],
        "modes": [
            {"mode": "Push-pull output", "configuration": "DDRx bit = 1", "use": "Drive a digital signal high or low."},
            {"mode": "Floating input", "configuration": "DDRx = 0, PORTx = 0", "use": "Read an externally biased signal."},
            {"mode": "Input with pull-up", "configuration": "DDRx = 0, PORTx = 1", "use": "Read switches without an external pull-up resistor."},
            {"mode": "Peripheral alternate function", "configuration": "Peripheral owns the pin", "use": "Connect timers, USART, SPI, or ADC to the physical pin."},
        ],
    },
    "watchdog": {
        "title": "Watchdog register map and operating modes",
        "registers": [
            {"register": "WDTCSR", "purpose": "Watchdog control", "bits": "WDIF | WDIE | WDP3:0 | WDE | WDCE"},
            {"register": "MCUSR", "purpose": "Reset cause", "bits": "WDRF indicates watchdog reset"},
            {"register": "WDTCR", "purpose": "ATmega8 control name", "bits": "Equivalent watchdog control register on ATmega8"},
        ],
        "modes": [
            {"mode": "System reset", "configuration": "WDE = 1", "use": "Reset the CPU if firmware fails to service the watchdog."},
            {"mode": "Interrupt", "configuration": "WDIE = 1, WDE = 0", "use": "Run a recovery or periodic interrupt routine."},
            {"mode": "Interrupt then reset", "configuration": "WDIE = 1, WDE = 1", "use": "Attempt recovery, then reset if firmware remains stuck."},
            {"mode": "Prescaler", "configuration": "WDP3:0", "use": "Select watchdog timeout interval."},
        ],
    },
    "memory": {
        "title": "Memory register map and operating modes",
        "registers": [
            {"register": "EEARH / EEARL", "purpose": "EEPROM address", "bits": "EEPROM byte address"},
            {"register": "EEDR", "purpose": "EEPROM data", "bits": "Data byte read or written"},
            {"register": "EECR", "purpose": "EEPROM control", "bits": "EERE | EEPE | EEMPE | EERIE"},
            {"register": "SPMCSR", "purpose": "Self-programming", "bits": "Flash page erase, write, and boot-loader controls"},
        ],
        "modes": [
            {"mode": "EEPROM read", "configuration": "Address -> EERE", "use": "Read persistent configuration data."},
            {"mode": "EEPROM write", "configuration": "EEMPE -> EEPE", "use": "Commit a byte after the timed write sequence."},
            {"mode": "Flash page write", "configuration": "SPMCSR + SPM", "use": "Bootloader self-programming from the boot section."},
            {"mode": "Power-save storage", "configuration": "EEPROM endurance rules", "use": "Store values across reset and power loss."},
        ],
    },
}


def get_register_guide(slug: str, mcu: Dict[str, str]) -> Dict[str, Any]:
    guide = REGISTER_GUIDES.get(slug, {"title": "Register map", "registers": [], "modes": []})
    if slug != "usart":
        return guide

    adapted = {**guide, "registers": [dict(row) for row in guide["registers"]]}
    if mcu.get("display_name") == "ATmega8":
        replacements = {"UBRRnH / UBRRnL": "UBRRH / UBRRL", "UCSRnA": "UCSRA", "UCSRnB": "UCSRB", "UCSRnC": "UCSRC", "UDRn": "UDR"}
    elif mcu.get("display_name") == "ATmega32U4":
        replacements = {"UBRRnH / UBRRnL": "UBRR1H / UBRR1L", "UCSRnA": "UCSR1A", "UCSRnB": "UCSR1B", "UCSRnC": "UCSR1C", "UDRn": "UDR1"}
    else:
        replacements = {"UBRRnH / UBRRnL": "UBRR0H / UBRR0L", "UCSRnA": "UCSR0A", "UCSRnB": "UCSR0B", "UCSRnC": "UCSR0C", "UDRn": "UDR0"}
    for row in adapted["registers"]:
        row["register"] = replacements.get(row["register"], row["register"])
    return adapted
