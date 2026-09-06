"""
Seed data generator for ATmega2560 Peripherals, Registers, Specifications, Libraries, and Arduino Codes.
Derived directly from the official Microchip ATmega2560 Datasheet and Arduino Mega 2560 Hardware Design.
Includes comprehensive Register-Only (Bare-Metal AVR C++) and Arduino Core/Library code examples,
along with visual register bitfield mappings and public datasheet diagrams.
"""

PERIPHERALS_DATA = [
    {
        "slug": "usart",
        "name": "USART (Universal Synchronous/Asynchronous Receiver Transmitter)",
        "category": "Serial Communication",
        "icon": "📡",
        "summary": "Four independent hardware serial ports (USART0 to USART3) supporting full-duplex UART communication, multi-processor mode, and hardware baud rate generation.",
        "order_index": 1,
        "details": {
            "full_description": (
                "The ATmega2560 microcontroller features **four independent, programmable hardware USARTs** "
                "(USART0, USART1, USART2, and USART3). Each channel contains an independent baud rate generator, "
                "a double-buffered receiver, and a double-buffered transmitter.\n\n"
                "### 🔑 Commonly Used Registers for USART\n"
                "When programming USART at the hardware register level, you work directly with:\n"
                "- **`UBRRnH` / `UBRRnL`**: 16-bit Baud Rate Register setting the clock divider.\n"
                "- **`UCSRnA`**: USART Control & Status Register A (Status flags like `RXCn`, `TXCn`, `UDREn`).\n"
                "- **`UCSRnB`**: USART Control & Status Register B (Enable bits `RXENn`, `TXENn`, `RXCIEn`, `TXCIEn`).\n"
                "- **`UCSRnC`**: USART Control & Status Register C (Framing configuration: 8N1, parity, stop bits).\n"
                "- **`UDRn`**: USART I/O Data Register (Transmit/Receive data buffer).\n\n"
                "![USART Functional Block Diagram](https://upload.wikimedia.org/wikipedia/commons/thumb/1/1d/UART_block_diagram.svg/640px-UART_block_diagram.svg.png)\n"
                "*Figure 1: Hardware UART Functional Architecture Block Diagram showing TX/RX shift registers and clock divider.*"
            ),
            "architecture_role": "Connects the AVR CPU Core to external serial devices (GPS, Bluetooth, GSM, Nextion displays, PC USB communication via ATmega16U2).",
            "hardware_specs": (
                "- **Channels**: 4 independent USART channels (USART0, USART1, USART2, USART3)\n"
                "- **Operation**: Full Duplex (Independent Serial Receive and Transmit Registers)\n"
                "- **Clock Modes**: Asynchronous or Synchronous Master/Slave\n"
                "- **Baud Rates**: Up to 2 Mbps at 16 MHz system clock\n"
                "- **Buffering**: Double-buffered UART receiver buffer (`UDRn`)\n"
                "- **Data Framing**: 5, 6, 7, 8, or 9 data bits with 1 or 2 stop bits; Even/Odd/No Parity\n"
                "- **Interrupts**: TX Complete (`TXCn`), TX Data Register Empty (`UDREn`), RX Complete (`RXCn`)"
            ),
            "hardware_registers": (
                "### 📋 USART Register & Bitfield Reference\n\n"
                "#### 1. UCSRnA — Control and Status Register A\n"
                "| Bit 7 | Bit 6 | Bit 5 | Bit 4 | Bit 3 | Bit 2 | Bit 1 | Bit 0 |\n"
                "|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|\n"
                "| `RXCn` | `TXCn` | `UDREn` | `FEn` | `DORn` | `UPEn` | `U2Xn` | `MPCMn` |\n\n"
                "- `RXCn`: Receive Complete (Set when unread data exists in UDRn).\n"
                "- `UDREn`: USART Data Register Empty (Set when UDRn is ready to accept new transmit data).\n"
                "- `U2Xn`: Double the USART Transmission Speed bit (Divides clock by 8 instead of 16).\n\n"
                "#### 2. UCSRnB — Control and Status Register B\n"
                "| Bit 7 | Bit 6 | Bit 5 | Bit 4 | Bit 3 | Bit 2 | Bit 1 | Bit 0 |\n"
                "|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|\n"
                "| `RXCIEn` | `TXCIEn` | `UDRIEn` | `RXENn` | `TXENn` | `UCSZn2` | `RXB8n` | `TXB8n` |\n\n"
                "- `RXENn`: Receiver Enable.\n"
                "- `TXENn`: Transmitter Enable.\n"
                "- `RXCIEn`: RX Complete Interrupt Enable (`ISR(USARTn_RX_vect)`).\n\n"
                "#### 3. Register Summary Table\n"
                "| Register | Address | Function Description |\n"
                "|---|---|---|\n"
                "| `UDR0` | `0xC6` | USART0 Data Register (Read RX / Write TX buffer) |\n"
                "| `UCSR0A` | `0xC0` | Status Flags (`RXC0`, `TXC0`, `UDRE0`, `U2X0`) |\n"
                "| `UCSR0B` | `0xC1` | Control Bits (`RXEN0`, `TXEN0`, `RXCIE0`) |\n"
                "| `UCSR0C` | `0xC2` | Mode, Parity, Stop Bit, & Character Size |\n"
                "| `UBRR0H/L` | `0xC5/C4` | 16-bit Baud Rate Divider: `UBRR = (F_CPU / (16 * Baud)) - 1` |"
            ),
            "mega2560_pins": (
                "| Port | Mega 2560 Digital Pins | Hardware AVR Pins | Arduino Serial Object |\n"
                "|---|---|---|---|\n"
                "| **USART0** | Pin 0 (RX0), Pin 1 (TX0) | PE0 (RXD0), PE1 (TXD0) | `Serial` (Connected to USB) |\n"
                "| **USART1** | Pin 19 (RX1), Pin 18 (TX1) | PD2 (RXD1), PD3 (TXD1) | `Serial1` |\n"
                "| **USART2** | Pin 17 (RX2), Pin 16 (TX2) | PH0 (RXD2), PH1 (TXD2) | `Serial2` |\n"
                "| **USART3** | Pin 15 (RX3), Pin 14 (TX3) | PJ0 (RXD3), PJ1 (TXD3) | `Serial3` |"
            ),
            "requires_external_library": False,
            "library_analysis": (
                "### Is an external library required?\n"
                "**No external library is required.** The official Arduino core includes the built-in `HardwareSerial` class, "
                "which automatically instantiates `Serial`, `Serial1`, `Serial2`, and `Serial3` on the Mega 2560.\n\n"
                "**When to use low-level registers instead of `Serial`:**\n"
                "- High-throughput data streaming where the standard 64-byte ring buffer causes buffer overrun.\n"
                "- Custom baud rates non-standard to standard tables.\n"
                "- Zero-latency ISR execution bypassing the Arduino background interrupt handler."
            )
        },
        "libraries": [
            {
                "name": "HardwareSerial (Core)",
                "is_builtin": True,
                "header_file": "<Arduino.h>",
                "purpose": "Built-in serial communication interface providing ring-buffered async serial I/O for Serial, Serial1, Serial2, and Serial3.",
                "installation_guide": "Pre-installed in Arduino IDE / Arduino Core. No installation needed.",
                "documentation_url": "https://www.arduino.cc/reference/en/language/functions/communication/serial/"
            }
        ],
        "code_examples": [
            {
                "title": "Dual-Port Hardware Serial Bridge",
                "category": "Standard Arduino API",
                "difficulty": "Beginner",
                "description": "Forward data bidirectionally between your PC (USB `Serial`) and an external device (e.g. GPS, ESP8266, Bluetooth module) on `Serial1` (Pins 18 & 19).",
                "code": (
                    "// Arduino Mega 2560 Dual-Port Hardware Serial Bridge\n"
                    "// Demonstrates simultaneous use of Serial (USB) and Serial1 (Pins 18/19)\n\n"
                    "void setup() {\n"
                    "  // Initialize primary USB Serial for debugging\n"
                    "  Serial.begin(115200);\n"
                    "  while (!Serial) { ; }\n\n"
                    "  // Initialize Serial1 for external peripheral at 9600 baud\n"
                    "  Serial1.begin(9600);\n\n"
                    "  Serial.println(F(\"--- ATmega2560 Dual Serial Bridge Ready ---\"));\n"
                    "  Serial.println(F(\"Forwarding data between USB and Serial1...\"));\n"
                    "}\n\n"
                    "void loop() {\n"
                    "  // Forward any character received from Serial1 to PC USB Serial\n"
                    "  if (Serial1.available() > 0) {\n"
                    "    char inChar = (char)Serial1.read();\n"
                    "    Serial.write(inChar);\n"
                    "  }\n\n"
                    "  // Forward any user input from PC Serial Monitor to Serial1\n"
                    "  if (Serial.available() > 0) {\n"
                    "    char outChar = (char)Serial.read();\n"
                    "    Serial1.write(outChar);\n"
                    "  }\n"
                    "}\n"
                ),
                "explanation": (
                    "1. `Serial.begin(115200)` configures USART0 for PC communication.\n"
                    "2. `Serial1.begin(9600)` configures USART1 on Pins 18 (TX1) and 19 (RX1).\n"
                    "3. `available()` checks the hardware circular buffer, while `read()` and `write()` transfer single bytes."
                ),
                "circuit_notes": "Connect TX of external module to Mega Pin 19 (RX1). Connect RX of module to Mega Pin 18 (TX1). Ensure common ground (GND).",
                "order_index": 1
            },
            {
                "title": "Bare-Metal Direct Register USART Transmission & Interrupt RX",
                "category": "Direct Register (AVR C++)",
                "difficulty": "Advanced",
                "description": "Configure USART1 directly using ATmega2560 registers (`UBRR1`, `UCSR1B`, `UCSR1C`) and handle incoming bytes with hardware interrupt `ISR(USART1_RX_vect)`.",
                "code": (
                    "// Direct Register Manipulation for USART1 on ATmega2560\n"
                    "#include <avr/io.h>\n"
                    "#include <avr/interrupt.h>\n\n"
                    "#define FOSC 16000000UL // 16 MHz Clock\n"
                    "#define BAUD 9600\n"
                    "#define MYUBRR ((FOSC / (16UL * BAUD)) - 1)\n\n"
                    "volatile char rxBuffer = 0;\n"
                    "volatile bool newData = false;\n\n"
                    "void USART1_Init(unsigned int ubrr) {\n"
                    "  // 1. Set baud rate divisor registers (UBRR1H and UBRR1L)\n"
                    "  UBRR1H = (unsigned char)(ubrr >> 8);\n"
                    "  UBRR1L = (unsigned char)ubrr;\n\n"
                    "  // 2. Enable Receiver, Transmitter, and RX Complete Interrupt\n"
                    "  UCSR1B = (1 << RXEN1) | (1 << TXEN1) | (1 << RXCIEN1);\n\n"
                    "  // 3. Set frame format: 8 data bits, 1 stop bit, no parity (8N1)\n"
                    "  UCSR1C = (1 << UCSZ11) | (1 << UCSZ10);\n"
                    "}\n\n"
                    "void USART1_Transmit(unsigned char data) {\n"
                    "  // Wait until UDRE1 flag is set in UCSR1A\n"
                    "  while (!(UCSR1A & (1 << UDRE1)));\n"
                    "  UDR1 = data; // Load byte into data register\n"
                    "}\n\n"
                    "void USART1_SendString(const char* str) {\n"
                    "  while (*str) {\n"
                    "    USART1_Transmit(*str++);\n"
                    "  }\n"
                    "}\n\n"
                    "// Hardware Receive Interrupt Service Routine\n"
                    "ISR(USART1_RX_vect) {\n"
                    "  rxBuffer = UDR1; // Reading UDR1 clears RXC flag\n"
                    "  newData = true;\n"
                    "}\n\n"
                    "void setup() {\n"
                    "  cli();\n"
                    "  USART1_Init(MYUBRR);\n"
                    "  sei(); // Enable global interrupts\n"
                    "  USART1_SendString(\"Direct Register USART1 Active!\\r\\n\");\n"
                    "}\n\n"
                    "void loop() {\n"
                    "  if (newData) {\n"
                    "    USART1_SendString(\"Echo: \");\n"
                    "    USART1_Transmit(rxBuffer);\n"
                    "    USART1_SendString(\"\\r\\n\");\n"
                    "    newData = false;\n"
                    "  }\n"
                    "}\n"
                ),
                "explanation": (
                    "1. Baud rate divider `MYUBRR = (16,000,000 / (16 * 9600)) - 1 = 103` is loaded into `UBRR1H`/`UBRR1L`.\n"
                    "2. `UCSR1B |= (1 << RXCIEN1)` enables `ISR(USART1_RX_vect)` whenever a byte arrives on Pin 19.\n"
                    "3. Transmission polls the `UDRE1` bit in status register `UCSR1A` before writing `UDR1`."
                ),
                "circuit_notes": "Connect TX of external module to Pin 19 (RX1) and RX to Pin 18 (TX1). Probe Pin 18 with an oscilloscope to view the raw frame.",
                "order_index": 2
            }
        ]
    },
    {
        "slug": "spi",
        "name": "SPI (Serial Peripheral Interface)",
        "category": "Serial Communication",
        "icon": "⚡",
        "summary": "High-speed, synchronous 4-wire serial bus enabling fast communication between the ATmega2560 and SD cards, LCD displays, Flash memory, and sensors.",
        "order_index": 2,
        "details": {
            "full_description": (
                "The ATmega2560 features a dedicated hardware **Serial Peripheral Interface (SPI)** subsystem. "
                "SPI provides full-duplex, three-wire synchronous data transfer plus a Slave Select (SS) pin. "
                "The ATmega2560 can operate as an **SPI Master** (generating clock SCK up to 8 MHz) or as an **SPI Slave**.\n\n"
                "### 🔑 Commonly Used Registers for SPI\n"
                "- **`SPCR`**: SPI Control Register (Enables SPI, sets Master/Slave mode, clock polarity/phase, and clock rate).\n"
                "- **`SPSR`**: SPI Status Register (Contains transfer complete flag `SPIF` and 2X double speed bit `SPI2X`).\n"
                "- **`SPDR`**: SPI Data Register (8-bit read/write buffer for transmitting and receiving bytes).\n\n"
                "![SPI Bus Connection Architecture](https://upload.wikimedia.org/wikipedia/commons/thumb/f/f5/SPI_single_slave.svg/640px-SPI_single_slave.svg.png)\n"
                "*Figure 2: SPI Bus Master-Slave Topology featuring MOSI, MISO, SCK, and SS lines.*"
            ),
            "architecture_role": "High-speed synchronous interface to SD Card shields, SPI TFT/OLED displays, Ethernet controllers (W5500), and high-precision ADCs.",
            "hardware_specs": (
                "- **Speed**: Up to half the CPU clock (8 MHz at 16 MHz system clock)\n"
                "- **Bus Lines**: MOSI (Master Out Slave In), MISO (Master In Slave Out), SCK (Serial Clock), SS (Slave Select)\n"
                "- **Modes**: Supports all 4 SPI modes (CPOL = 0/1, CPHA = 0/1)\n"
                "- **Bit Ordering**: MSB First or LSB First configurable\n"
                "- **Interrupts**: SPI Serial Transfer Complete (`SPI_STC_vect`)"
            ),
            "hardware_registers": (
                "### 📋 SPI Register & Bitfield Reference\n\n"
                "#### 1. SPCR — SPI Control Register\n"
                "| Bit 7 | Bit 6 | Bit 5 | Bit 4 | Bit 3 | Bit 2 | Bit 1 | Bit 0 |\n"
                "|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|\n"
                "| `SPIE` | `SPE` | `DORD` | `MSTR` | `CPOL` | `CPHA` | `SPR1` | `SPR0` |\n\n"
                "- `SPE`: SPI Enable (Set to 1 to activate hardware SPI).\n"
                "- `MSTR`: Master/Slave Select (1 = Master mode, 0 = Slave mode).\n"
                "- `CPOL` / `CPHA`: Clock Polarity and Clock Phase select SPI Modes 0, 1, 2, or 3.\n"
                "- `SPR1:0`: Clock Rate Select (Divides F_CPU by 4, 16, 64, or 128).\n\n"
                "#### 2. SPSR — SPI Status Register\n"
                "| Bit 7 | Bit 6 | Bit 5 | Bit 4 | Bit 3 | Bit 2 | Bit 1 | Bit 0 |\n"
                "|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|\n"
                "| `SPIF` | `WCOL` | — | — | — | — | — | `SPI2X` |\n\n"
                "- `SPIF`: SPI Interrupt Flag (Set when an 8-bit serial transfer is complete).\n"
                "- `SPI2X`: Double SPI Speed Bit (Doubles SPI frequency, e.g. fck/4 becomes fck/2 = 8 MHz).\n\n"
                "#### 3. SPDR — SPI Data Register\n"
                "- Reading `SPDR` returns received byte; Writing `SPDR` initiates 8-bit hardware transmission."
            ),
            "mega2560_pins": (
                "| SPI Signal | Arduino Mega Pin | ATmega2560 Physical Pin | Notes |\n"
                "|---|---|---|---|\n"
                "| **MISO** | Pin 50 | PB3 | Master In, Slave Out |\n"
                "| **MOSI** | Pin 51 | PB2 | Master Out, Slave In |\n"
                "| **SCK** | Pin 52 | PB1 | Serial Clock |\n"
                "| **SS** | Pin 53 | PB0 | Hardware Slave Select (Must be OUTPUT in Master mode) |\n"
                "| **ICSP Header** | Pins 1, 3, 4 | MISO, SCK, MOSI | 6-pin header on board |"
            ),
            "requires_external_library": False,
            "library_analysis": (
                "### Is an external library required?\n"
                "**No external library is required.** The Arduino IDE ships with the official `<SPI.h>` library.\n\n"
                "**Important ATmega2560 Pin Caveat:**\n"
                "On the Arduino Uno, SPI is located on pins 10, 11, 12, and 13. On the **Arduino Mega 2560**, hardware SPI is routed to **Pins 50, 51, 52, and 53** (or the 6-pin ICSP header). "
                "Any Uno shield that plugs into pins 11-13 will NOT work unless it connects via the 6-pin ICSP header!"
            )
        },
        "libraries": [
            {
                "name": "SPI",
                "is_builtin": True,
                "header_file": "<SPI.h>",
                "purpose": "Standard Arduino SPI library providing fast SPI bus transactions, settings configuration, and byte transfers.",
                "installation_guide": "Built-in with Arduino IDE. Include with `#include <SPI.h>`.",
                "documentation_url": "https://www.arduino.cc/reference/en/language/functions/communication/spi/"
            }
        ],
        "code_examples": [
            {
                "title": "Standard SPI Master Transaction with SPISettings",
                "category": "Standard Arduino API",
                "difficulty": "Beginner",
                "description": "Initialize SPI on Mega 2560 and communicate with an SPI peripheral using safe `beginTransaction` and `transfer()`.",
                "code": (
                    "// ATmega2560 Hardware SPI Master Example\n"
                    "#include <SPI.h>\n\n"
                    "const int chipSelectPin = 53; // Hardware SS pin on Mega 2560\n\n"
                    "void setup() {\n"
                    "  Serial.begin(115200);\n"
                    "  \n"
                    "  // Set CS as output\n"
                    "  pinMode(chipSelectPin, OUTPUT);\n"
                    "  digitalWrite(chipSelectPin, HIGH); // De-select slave\n\n"
                    "  // Initialize SPI bus (Pins 50 MISO, 51 MOSI, 52 SCK)\n"
                    "  SPI.begin();\n"
                    "  \n"
                    "  Serial.println(F(\"Mega 2560 SPI Master Initialized.\"));\n"
                    "}\n\n"
                    "void loop() {\n"
                    "  // Configure transaction: 4MHz clock, MSB first, SPI Mode 0\n"
                    "  SPI.beginTransaction(SPISettings(4000000, MSBFIRST, SPI_MODE0));\n"
                    "  \n"
                    "  // Select peripheral (Active LOW)\n"
                    "  digitalWrite(chipSelectPin, LOW);\n"
                    "  \n"
                    "  // Transfer 1 byte and read back simultaneous response\n"
                    "  byte command = 0xAA;\n"
                    "  byte response = SPI.transfer(command);\n"
                    "  \n"
                    "  // De-select peripheral\n"
                    "  digitalWrite(chipSelectPin, HIGH);\n"
                    "  SPI.endTransaction();\n\n"
                    "  Serial.print(F(\"Sent: 0x\"));\n"
                    "  Serial.print(command, HEX);\n"
                    "  Serial.print(F(\" | Received: 0x\"));\n"
                    "  Serial.println(response, HEX);\n\n"
                    "  delay(1000);\n"
                    "}\n"
                ),
                "explanation": (
                    "1. `SPI.begin()` configures pins 51 (MOSI) and 52 (SCK) as outputs, and pin 50 (MISO) as input.\n"
                    "2. `pinMode(53, OUTPUT)` is critical on ATmega2560; if pin 53 is left as an input and driven LOW, hardware SPI reverts to Slave mode.\n"
                    "3. `SPI.beginTransaction()` applies clock and phase settings safely."
                ),
                "circuit_notes": "Connect Pin 51 -> Slave MOSI, Pin 50 -> Slave MISO, Pin 52 -> Slave SCK, Pin 53 -> Slave CS/SS.",
                "order_index": 1
            },
            {
                "title": "Direct Register SPI Master Setup at Maximum Clock (8 MHz)",
                "category": "Direct Register (AVR C++)",
                "difficulty": "Advanced",
                "description": "Configure the ATmega2560 SPI controller directly via `SPCR` and `SPSR` registers for high-speed 8 MHz data transfer.",
                "code": (
                    "// ATmega2560 Direct Register SPI Configuration (8 MHz Double-Speed)\n"
                    "#include <avr/io.h>\n\n"
                    "void SPI_MasterInit(void) {\n"
                    "  // Set MOSI (PB2), SCK (PB1), and SS (PB0) as output pins in DDRB\n"
                    "  DDRB |= (1 << DDB2) | (1 << DDB1) | (1 << DDB0);\n"
                    "  // Set MISO (PB3) as input\n"
                    "  DDRB &= ~(1 << DDB3);\n\n"
                    "  // Set SS High initially\n"
                    "  PORTB |= (1 << PORTB0);\n\n"
                    "  // Enable SPI and set as Master: SPCR = (1<<SPE) | (1<<MSTR)\n"
                    "  SPCR = (1 << SPE) | (1 << MSTR);\n\n"
                    "  // Set SPI2X bit in SPSR for double speed (16MHz / 2 = 8 MHz)\n"
                    "  SPSR |= (1 << SPI2X);\n"
                    "}\n\n"
                    "uint8_t SPI_MasterTransmit(uint8_t data) {\n"
                    "  // Start transmission by loading byte into SPDR register\n"
                    "  SPDR = data;\n\n"
                    "  // Poll SPIF flag in SPSR until byte transfer completes\n"
                    "  while (!(SPSR & (1 << SPIF)));\n\n"
                    "  // Return received byte from SPDR\n"
                    "  return SPDR;\n"
                    "}\n\n"
                    "void setup() {\n"
                    "  SPI_MasterInit();\n"
                    "}\n\n"
                    "void loop() {\n"
                    "  // Pull SS Low (PB0 / Pin 53)\n"
                    "  PORTB &= ~(1 << PORTB0);\n\n"
                    "  uint8_t result = SPI_MasterTransmit(0x55);\n\n"
                    "  // Pull SS High\n"
                    "  PORTB |= (1 << PORTB0);\n\n"
                    "  for (volatile uint32_t i = 0; i < 50000; i++);\n"
                    "}\n"
                ),
                "explanation": (
                    "1. Configures Port B direction bits directly (`DDB2`, `DDB1`, `DDB0` map to pins 51, 52, 53).\n"
                    "2. Enables the hardware SPI engine with `SPCR = (1 << SPE) | (1 << MSTR)`.\n"
                    "3. Enables `SPI2X` in `SPSR`, achieving maximum 8 Mbps throughput on a 16 MHz AVR."
                ),
                "circuit_notes": "Use short wire connections (<10 cm) to minimize capacitive crosstalk at 8 MHz.",
                "order_index": 2
            }
        ]
    },
    {
        "slug": "twi",
        "name": "TWI / I2C (Two-Wire Interface)",
        "category": "Serial Communication",
        "icon": "🔗",
        "summary": "Hardware 2-wire serial bus compatible with Philips I2C standard, supporting 100 kHz standard and 400 kHz fast mode.",
        "order_index": 3,
        "details": {
            "full_description": (
                "The **Two-Wire Serial Interface (TWI)** in the ATmega2560 is fully compatible with the Philips I2C bus standard. "
                "It uses two bidirectional open-drain lines (SDA and SCL) pulled high by resistors.\n\n"
                "### 🔑 Commonly Used Registers for TWI / I2C\n"
                "- **`TWBR`**: TWI Bit Rate Register (Controls SCL clock frequency in Master mode).\n"
                "- **`TWCR`**: TWI Control Register (Triggers START/STOP conditions, enables ACK `TWEA`, clears flag `TWINT`).\n"
                "- **`TWSR`**: TWI Status Register (Holds 5-bit status code indicating bus state e.g., START sent, ACK received).\n"
                "- **`TWDR`**: TWI Data Register (Holds next byte to send or byte received from slave).\n"
                "- **`TWAR`**: TWI Address Register (7-bit slave address when Mega acts as an I2C slave).\n\n"
                "![I2C Bus Wiring Diagram](https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/I2C.svg/640px-I2C.svg.png)\n"
                "*Figure 3: I2C Open-Drain Bus Architecture with SDA and SCL Pull-Up Resistors.*"
            ),
            "architecture_role": "Interfacing with sensors (MPU6050, BME280), Real-Time Clocks (DS3231), OLED displays (SSD1306), and EEPROMs.",
            "hardware_specs": (
                "- **Protocol**: I2C (Philips compatible) 2-wire open drain bus\n"
                "- **Clock Rates**: Standard mode (100 kHz), Fast mode (400 kHz)\n"
                "- **Addressing**: 7-bit slave addresses (up to 128 devices) and 10-bit extended addressing\n"
                "- **Slew Rate Filter**: Built-in spike suppression filter rejecting spikes shorter than 50 ns\n"
                "- **Arbitration**: Multi-master bus collision detection and arbitration"
            ),
            "hardware_registers": (
                "### 📋 TWI Register & Bitfield Reference\n\n"
                "#### 1. TWCR — TWI Control Register\n"
                "| Bit 7 | Bit 6 | Bit 5 | Bit 4 | Bit 3 | Bit 2 | Bit 1 | Bit 0 |\n"
                "|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|\n"
                "| `TWINT` | `TWEA` | `TWSTA` | `TWSTO` | `TWWC` | `TWEN` | — | `TWIE` |\n\n"
                "- `TWINT`: TWI Interrupt Flag (Write 1 to clear flag and initiate next hardware step).\n"
                "- `TWSTA`: TWI START Condition Bit (Set to 1 to transmit START bit on bus).\n"
                "- `TWSTO`: TWI STOP Condition Bit (Set to 1 to transmit STOP bit).\n"
                "- `TWEN`: TWI Enable Bit.\n\n"
                "#### 2. SCL Frequency Formula\n"
                "$$\\text{SCL Frequency} = \\frac{F\\_{\\text{CPU}}}{16 + 2 \\cdot \\text{TWBR} \\cdot \\text{Prescaler}}$$\n\n"
                "For 100 kHz SCL at 16 MHz with Prescaler 1: `TWBR = ((16MHz / 100kHz) - 16) / 2 = 72`."
            ),
            "mega2560_pins": (
                "| I2C Signal | Arduino Mega Pin | ATmega2560 Physical Pin | Notes |\n"
                "|---|---|---|---|\n"
                "| **SDA** (Data) | Pin 20 | PD1 | Open drain, requires 4.7kΩ pull-up resistor |\n"
                "| **SCL** (Clock) | Pin 21 | PD0 | Open drain, requires 4.7kΩ pull-up resistor |"
            ),
            "requires_external_library": False,
            "library_analysis": (
                "### Is an external library required?\n"
                "**No external library is required.** The Arduino Core includes `<Wire.h>` natively.\n\n"
                "**Key differences on the Mega 2560:**\n"
                "On the Uno, I2C is on pins A4/A5. On the **Mega 2560**, I2C is routed to **Pin 20 (SDA) and Pin 21 (SCL)**!"
            )
        },
        "libraries": [
            {
                "name": "Wire",
                "is_builtin": True,
                "header_file": "<Wire.h>",
                "purpose": "Provides standard I2C master and slave communication functions on SDA (20) and SCL (21).",
                "installation_guide": "Pre-installed in Arduino IDE. Include with `#include <Wire.h>`.",
                "documentation_url": "https://www.arduino.cc/reference/en/language/functions/communication/wire/"
            }
        ],
        "code_examples": [
            {
                "title": "I2C Bus Scanner for ATmega2560",
                "category": "Standard Arduino API",
                "difficulty": "Beginner",
                "description": "Scan all 127 I2C addresses on pins 20 (SDA) and 21 (SCL) to discover connected sensors and modules.",
                "code": (
                    "// ATmega2560 I2C Address Scanner (Wire Library)\n"
                    "#include <Wire.h>\n\n"
                    "void setup() {\n"
                    "  Wire.begin(); // Initialize TWI on Pins 20 & 21\n"
                    "  Wire.setClock(400000); // 400 kHz Fast I2C\n"
                    "  Serial.begin(115200);\n"
                    "  while (!Serial);\n"
                    "  Serial.println(F(\"--- ATmega2560 I2C Scanner Active ---\"));\n"
                    "}\n\n"
                    "void loop() {\n"
                    "  byte error, address;\n"
                    "  int nDevices = 0;\n"
                    "  for (address = 1; address < 127; address++) {\n"
                    "    Wire.beginTransmission(address);\n"
                    "    error = Wire.endTransmission();\n"
                    "    if (error == 0) {\n"
                    "      Serial.print(F(\"Found I2C device at 0x\"));\n"
                    "      if (address < 16) Serial.print(\"0\");\n"
                    "      Serial.print(address, HEX);\n"
                    "      Serial.println(F(\" !\"));\n"
                    "      nDevices++;\n"
                    "    }\n"
                    "  }\n"
                    "  if (nDevices == 0) Serial.println(F(\"No I2C devices found.\"));\n"
                    "  delay(5000);\n"
                    "}\n"
                ),
                "explanation": (
                    "1. `Wire.begin()` joins the I2C bus as master on Pins 20 and 21.\n"
                    "2. `Wire.setClock(400000)` modifies `TWBR` register for 400 kHz fast mode.\n"
                    "3. `Wire.endTransmission()` returns 0 when the slave acknowledges."
                ),
                "circuit_notes": "Connect SDA to Pin 20 and SCL to Pin 21. Add 4.7kΩ pull-up resistors to +5V.",
                "order_index": 1
            },
            {
                "title": "Direct Register TWI Master Start & Byte Transmit Routine",
                "category": "Direct Register (AVR C++)",
                "difficulty": "Advanced",
                "description": "Perform raw low-level TWI master communication without `<Wire.h>` by directly driving `TWCR`, `TWDR`, `TWBR`, and `TWSR` registers.",
                "code": (
                    "// ATmega2560 Direct Register TWI (I2C) Master Protocol\n"
                    "#include <avr/io.h>\n"
                    "#include <util/twi.h>\n\n"
                    "#define F_CPU 16000000UL\n"
                    "#define SCL_CLOCK 100000UL // 100 kHz\n\n"
                    "void TWI_Init(void) {\n"
                    "  // Set TWI Bit Rate Register: TWBR = ((F_CPU / SCL_CLOCK) - 16) / 2\n"
                    "  TWBR = (uint8_t)(((F_CPU / SCL_CLOCK) - 16) / 2);\n"
                    "  TWSR = 0x00; // Prescaler = 1\n"
                    "  TWCR = (1 << TWEN); // Enable TWI Hardware Engine\n"
                    "}\n\n"
                    "uint8_t TWI_Start(uint8_t address_with_rw) {\n"
                    "  // Transmit START condition: TWINT=1, TWSTA=1, TWEN=1\n"
                    "  TWCR = (1 << TWINT) | (1 << TWSTA) | (1 << TWEN);\n"
                    "  while (!(TWCR & (1 << TWINT))); // Poll TWINT until hardware finishes\n\n"
                    "  uint8_t status = TWSR & 0xF8;\n"
                    "  if ((status != 0x08) && (status != 0x10)) return 0; // Check START status\n\n"
                    "  // Load SLA+W into TWDR\n"
                    "  TWDR = address_with_rw;\n"
                    "  TWCR = (1 << TWINT) | (1 << TWEN); // Clear TWINT to transmit\n"
                    "  while (!(TWCR & (1 << TWINT)));\n\n"
                    "  return 1;\n"
                    "}\n\n"
                    "void TWI_Stop(void) {\n"
                    "  // Transmit STOP condition\n"
                    "  TWCR = (1 << TWINT) | (1 << TWSTO) | (1 << TWEN);\n"
                    "}\n\n"
                    "void setup() {\n"
                    "  TWI_Init();\n"
                    "}\n\n"
                    "void loop() {\n"
                    "  // Ping slave at address 0x68 with write bit (0x68 << 1 | 0)\n"
                    "  TWI_Start((0x68 << 1) | 0);\n"
                    "  TWI_Stop();\n"
                    "  for (volatile uint32_t i = 0; i < 100000; i++);\n"
                    "}\n"
                ),
                "explanation": (
                    "1. Configures `TWBR = 72` for 100 kHz clock at 16 MHz.\n"
                    "2. Writing `(1 << TWINT)` clears the hardware flag and executes bus operations.\n"
                    "3. Directly inspects `TWSR & 0xF8` for hardware status code verification."
                ),
                "circuit_notes": "Requires 4.7kΩ pull-up resistors on Pins 20 and 21 to avoid infinite wait on TWINT.",
                "order_index": 2
            }
        ]
    },
    {
        "slug": "timers",
        "name": "Timers & Counters (Timer 0 through Timer 5)",
        "category": "Timing & PWM",
        "icon": "⏱️",
        "summary": "Six hardware timers: two 8-bit timers (Timer 0, Timer 2) and four 16-bit timers (Timer 1, Timer 3, Timer 4, Timer 5) with CTC and Input Capture.",
        "order_index": 4,
        "details": {
            "full_description": (
                "The ATmega2560 packs **six hardware timers** (two 8-bit, four 16-bit). "
                "These hardware counters operate independently of the CPU core.\n\n"
                "### 🔑 Commonly Used Registers for Timers\n"
                "- **`TCCRnA` / `TCCRnB` / `TCCRnC`**: Timer Control Registers (Configures Waveform Generation Mode WGM, Compare Output Mode COM, and Prescaler clock select `CSn2:0`).\n"
                "- **`TCNTn` / `TCNTnH:L`**: Timer Counter Value Register (Holds live tick count).\n"
                "- **`OCRnA` / `OCRnB` / `OCRnC`**: Output Compare Registers (Target count for interrupts and PWM duty cycle).\n"
                "- **`ICRn`**: Input Capture Register (Stores tick timestamp on pin pulse or sets custom TOP value in CTC/PWM modes).\n"
                "- **`TIMSKn`**: Timer Interrupt Mask Register (Enables Overflow `TOIEn` and Compare Match `OCIEnA/B/C`).\n"
                "- **`TIFRn`**: Timer Interrupt Flag Register (Hardware status flags).\n\n"
                "![Timer Waveform Diagram](https://upload.wikimedia.org/wikipedia/commons/thumb/c/a9/PWM_Waveform.svg/640px-PWM_Waveform.svg.png)\n"
                "*Figure 4: Timer Compare Match Waveform Generation Diagram.*"
            ),
            "architecture_role": "High-precision timekeeping, frequency generation, encoder counting, audio synthesis, and non-blocking ISR task execution.",
            "hardware_specs": (
                "- **Total Timers**: 6 hardware timers (Two 8-bit, Four 16-bit)\n"
                "- **Prescalers**: 1, 8, 64, 256, 1024 independent prescaler selection\n"
                "- **Modes**: Normal, Clear Timer on Compare Match (CTC), Fast PWM, Phase Correct PWM\n"
                "- **Input Capture**: Hardware noise canceler and timestamp capture on ICP1, ICP4, ICP5 pins"
            ),
            "hardware_registers": (
                "### 📋 Timer Register & Bitfield Reference\n\n"
                "#### 1. TCCR1B — Timer 1 Control Register B (Prescaler & CTC)\n"
                "| Bit 7 | Bit 6 | Bit 5 | Bit 4 | Bit 3 | Bit 2 | Bit 1 | Bit 0 |\n"
                "|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|\n"
                "| `ICNC1` | `ICES1` | — | `WGM13` | `WGM12` | `CS12` | `CS11` | `CS10` |\n\n"
                "- `WGM12`: CTC Mode select bit.\n"
                "- `CS12:10`: Clock select prescaler (001=fck/1, 010=fck/8, 011=fck/64, 100=fck/256, 101=fck/1024).\n\n"
                "#### 2. TIMSK1 — Timer 1 Interrupt Mask Register\n"
                "| Bit 7 | Bit 6 | Bit 5 | Bit 4 | Bit 3 | Bit 2 | Bit 1 | Bit 0 |\n"
                "|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|\n"
                "| — | — | `ICIE1` | — | `OCIE1C` | `OCIE1B` | `OCIE1A` | `TOIE1` |\n\n"
                "- `OCIE1A`: Output Compare A Match Interrupt Enable (`ISR(TIMER1_COMPA_vect)`)."
            ),
            "mega2560_pins": (
                "| Timer | Counter Size | Compare Pins (OCnx) | Input Capture (ICP) |\n"
                "|---|---|---|---|\n"
                "| **Timer 0** | 8-bit | Pin 13 (OC0A), Pin 4 (OC0B) | — |\n"
                "| **Timer 1** | 16-bit | Pin 11 (OC1A), Pin 12 (OC1B), Pin 13 (OC1C) | Pin 48 (ICP1) |\n"
                "| **Timer 2** | 8-bit | Pin 10 (OC2A), Pin 9 (OC2B) | Asynch TOSC1/TOSC2 |\n"
                "| **Timer 3** | 16-bit | Pin 5 (OC3A), Pin 2 (OC3B), Pin 3 (OC3C) | — |\n"
                "| **Timer 4** | 16-bit | Pin 6 (OC4A), Pin 7 (OC4B), Pin 8 (OC4C) | Pin 49 (ICP4) |\n"
                "| **Timer 5** | 16-bit | Pin 46 (OC5A), Pin 45 (OC5B), Pin 44 (OC5C) | Pin 47 (ICP5) |"
            ),
            "requires_external_library": False,
            "library_analysis": (
                "### Is an external library required?\n"
                "Native functions `millis()` and `micros()` rely on Timer 0. For custom ISR timers, `<avr/interrupt.h>` requires no library."
            )
        },
        "libraries": [
            {
                "name": "avr/interrupt.h (AVR Libc)",
                "is_builtin": True,
                "header_file": "<avr/interrupt.h>",
                "purpose": "Standard AVR header providing sei(), cli(), and the ISR() macro.",
                "installation_guide": "Built-in with compiler toolchain.",
                "documentation_url": "https://www.nongnu.org/avr-libc/user-manual/group__avr__interrupts.html"
            }
        ],
        "code_examples": [
            {
                "title": "Exact 1 Hz Periodic ISR Using Timer 1 in CTC Mode",
                "category": "Direct Register (AVR C++)",
                "difficulty": "Intermediate",
                "description": "Configure Timer 1 (16-bit) to trigger an Interrupt Service Routine exactly once per second without using delay() or millis().",
                "code": (
                    "// ATmega2560 Precise 1Hz Heartbeat with Timer 1 CTC Mode\n"
                    "#include <avr/io.h>\n"
                    "#include <avr/interrupt.h>\n\n"
                    "const int ledPin = 13; // Built-in LED\n"
                    "volatile bool toggleState = false;\n\n"
                    "void setup() {\n"
                    "  pinMode(ledPin, OUTPUT);\n"
                    "  cli(); // Disable interrupts during setup\n\n"
                    "  TCCR1A = 0;\n"
                    "  TCCR1B = 0;\n"
                    "  TCNT1  = 0;\n\n"
                    "  // OCR1A = (16,000,000 / (1024 * 1)) - 1 = 15624\n"
                    "  OCR1A = 15624;\n"
                    "  TCCR1B |= (1 << WGM12); // CTC mode\n"
                    "  TCCR1B |= (1 << CS12) | (1 << CS10); // Prescaler 1024\n"
                    "  TIMSK1 |= (1 << OCIE1A); // Enable Compare Match A ISR\n"
                    "  sei();\n"
                    "}\n\n"
                    "ISR(TIMER1_COMPA_vect) {\n"
                    "  toggleState = !toggleState;\n"
                    "  digitalWrite(ledPin, toggleState ? HIGH : LOW);\n"
                    "}\n\n"
                    "void loop() {}\n"
                ),
                "explanation": (
                    "1. `WGM12` sets CTC mode: when `TCNT1` reaches `15624`, counter resets to 0 and fires `ISR(TIMER1_COMPA_vect)`.\n"
                    "2. Delivers zero-jitter 1.000 Hz timing."
                ),
                "circuit_notes": "Watch Pin 13 LED toggle once per second.",
                "order_index": 1
            },
            {
                "title": "Precision Non-blocking Microsecond Clock Generator",
                "category": "Standard Arduino API",
                "difficulty": "Beginner",
                "description": "Generate periodic non-blocking timing pulses using standard Arduino core timing functions `micros()` and `millis()`.",
                "code": (
                    "// Arduino Core Non-Blocking Timing Scheduler\n"
                    "const int pulsePin = 12;\n"
                    "unsigned long previousMicros = 0;\n"
                    "const unsigned long intervalMicros = 250; // 4 kHz pulse rate\n\n"
                    "void setup() {\n"
                    "  pinMode(pulsePin, OUTPUT);\n"
                    "}\n\n"
                    "void loop() {\n"
                    "  unsigned long currentMicros = micros();\n"
                    "  if (currentMicros - previousMicros >= intervalMicros) {\n"
                    "    previousMicros = currentMicros;\n"
                    "    digitalWrite(pulsePin, !digitalRead(pulsePin));\n"
                    "  }\n"
                    "}\n"
                ),
                "explanation": (
                    "1. Uses Arduino core Timer 0 tracking via `micros()`.\n"
                    "2. Avoids `delay()` to maintain non-blocking execution."
                ),
                "circuit_notes": "Connect Pin 12 to a frequency counter or oscilloscope.",
                "order_index": 2
            }
        ]
    },
    {
        "slug": "pwm",
        "name": "PWM (Pulse Width Modulation)",
        "category": "Timing & PWM",
        "icon": "🌊",
        "summary": "16 independent hardware PWM channels with 8-bit and 16-bit resolution, enabling motor speed control, LED dimming, and high-frequency switching.",
        "order_index": 5,
        "details": {
            "full_description": (
                "The ATmega2560 provides **16 dedicated hardware PWM pins**. "
                "PWM allows an analog output level to be simulated by modulating digital pulse duty cycle.\n\n"
                "### 🔑 Commonly Used Registers for PWM\n"
                "- **`TCCRnA`**: Sets Compare Output Mode (`COMnx1:0` for non-inverting/inverting PWM) and lower WGM bits.\n"
                "- **`TCCRnB`**: Sets upper WGM bits and clock prescaler.\n"
                "- **`OCRnx`**: Output Compare Register controlling duty cycle value (`Duty% = (OCRnx / TOP) * 100`).\n"
                "- **`ICRnx`**: Input Capture Register used as TOP in Mode 14 for custom PWM frequency generation.\n\n"
                "![PWM Signal Duty Cycle Diagram](https://upload.wikimedia.org/wikipedia/commons/thumb/b/b8/Duty_Cycle_Examples.png/640px-Duty_Cycle_Examples.png)\n"
                "*Figure 5: PWM Signals at 0%, 25%, 50%, 75%, and 100% Duty Cycles.*"
            ),
            "architecture_role": "Motor speed control, RGB LED color mixing, audio DAC, servo motor positioning.",
            "hardware_specs": (
                "- **Channels**: 16 dedicated PWM pins\n"
                "- **Resolution**: 8-bit default via `analogWrite()`, up to 16-bit with registers\n"
                "- **Frequencies**: Pins 4 & 13 = ~976 Hz; Pins 2, 3, 5-12, 44-46 = ~490 Hz"
            ),
            "hardware_registers": (
                "### 📋 PWM Register & Bitfield Reference\n"
                "| Register | Name | Function |\n"
                "|---|---|---|\n"
                "| `TCCR4A` | Timer 4 Control A | `COM4A1:0` (Non-inverting PWM on Pin 6) |\n"
                "| `TCCR4B` | Timer 4 Control B | `WGM43:42` & Prescaler `CS42:40` |\n"
                "| `OCR4A` | Compare Register A | Duty cycle match value for Pin 6 |\n"
                "| `ICR4` | Input Capture Register | Defines TOP value (period) in Mode 14 Fast PWM |"
            ),
            "mega2560_pins": (
                "| Arduino Mega PWM Pin | Associated Timer & Channel |\n"
                "|---|---|\n"
                "| **Pin 2, 3, 5** | Timer 3 (OC3B, OC3C, OC3A) |\n"
                "| **Pin 6, 7, 8** | Timer 4 (OC4A, OC4B, OC4C) |\n"
                "| **Pin 9, 10** | Timer 2 (OC2B, OC2A) |\n"
                "| **Pin 11, 12** | Timer 1 (OC1A, OC1B) |\n"
                "| **Pin 44, 45, 46** | Timer 5 (OC5C, OC5B, OC5A) |"
            ),
            "requires_external_library": False,
            "library_analysis": (
                "### Is an external library required?\n"
                "**No library is required** for standard `analogWrite()`. For RC servos, `<Servo.h>` is bundled."
            )
        },
        "libraries": [
            {
                "name": "Servo",
                "is_builtin": True,
                "header_file": "<Servo.h>",
                "purpose": "Standard Arduino library driving RC servo motors using hardware timers.",
                "installation_guide": "Pre-installed in Arduino IDE.",
                "documentation_url": "https://www.arduino.cc/reference/en/libraries/servo/"
            }
        ],
        "code_examples": [
            {
                "title": "Multi-Channel PWM LED Fader",
                "category": "Standard Arduino API",
                "difficulty": "Beginner",
                "description": "Smoothly fade RGB channels independently using standard `analogWrite()` on Timer 4 PWM pins 6, 7, and 8.",
                "code": (
                    "// ATmega2560 Multi-Channel PWM Fader\n"
                    "const int redPin   = 6; // OC4A\n"
                    "const int greenPin = 7; // OC4B\n"
                    "const int bluePin  = 8; // OC4C\n\n"
                    "void setup() {\n"
                    "  pinMode(redPin, OUTPUT);\n"
                    "  pinMode(greenPin, OUTPUT);\n"
                    "  pinMode(bluePin, OUTPUT);\n"
                    "}\n\n"
                    "void loop() {\n"
                    "  for (int b = 0; b <= 255; b++) {\n"
                    "    analogWrite(redPin, b);\n"
                    "    delay(5);\n"
                    "  }\n"
                    "  for (int b = 0; b <= 255; b++) {\n"
                    "    analogWrite(greenPin, b);\n"
                    "    delay(5);\n"
                    "  }\n"
                    "  analogWrite(redPin, 0);\n"
                    "  analogWrite(greenPin, 0);\n"
                    "  delay(500);\n"
                    "}\n"
                ),
                "explanation": (
                    "1. Pins 6, 7, 8 connect to ATmega2560 Timer 4.\n"
                    "2. `analogWrite()` writes duty values 0-255 into `OCR4A`, `OCR4B`, and `OCR4C`."
                ),
                "circuit_notes": "Connect LEDs with 220Ω current-limiting resistors to GND.",
                "order_index": 1
            },
            {
                "title": "Silent 25 kHz Fan PWM on Pin 6 (Timer 4 Mode 14)",
                "category": "Direct Register (AVR C++)",
                "difficulty": "Advanced",
                "description": "Configure Timer 4 Fast PWM Mode 14 with `ICR4` as TOP to generate exact 25 kHz silent fan speed control.",
                "code": (
                    "// ATmega2560 25 kHz Silent PWM Fan Controller (Pin 6 / OC4A)\n"
                    "#include <avr/io.h>\n\n"
                    "void setup() {\n"
                    "  DDRH |= (1 << DDH3); // Pin 6 (PH3) as OUTPUT\n"
                    "  TCCR4A = 0; TCCR4B = 0; TCNT4 = 0;\n\n"
                    "  // 25,000 Hz = 16,000,000 / (1 * (1 + 639)) -> ICR4 = 639\n"
                    "  ICR4 = 639;\n"
                    "  TCCR4A |= (1 << COM4A1) | (1 << WGM41);\n"
                    "  TCCR4B |= (1 << WGM43) | (1 << WGM42) | (1 << CS40); // Prescaler 1\n"
                    "  OCR4A = 320; // 50% Duty Cycle\n"
                    "}\n\n"
                    "void setFanDuty(uint8_t percent) {\n"
                    "  if (percent > 100) percent = 100;\n"
                    "  OCR4A = (uint16_t)(((uint32_t)639 * percent) / 100);\n"
                    "}\n\n"
                    "void loop() {\n"
                    "  setFanDuty(75);\n"
                    "  delay(2000);\n"
                    "}\n"
                ),
                "explanation": (
                    "1. Intel 4-wire fans require 25 kHz PWM. Standard 490 Hz produces whining noise.\n"
                    "2. Setting `ICR4 = 639` with prescaler 1 gives exact 25 kHz."
                ),
                "circuit_notes": "Connect Pin 6 to the PWM control wire of a 4-wire PC fan.",
                "order_index": 2
            }
        ]
    },
    {
        "slug": "adc",
        "name": "ADC (Analog-to-Digital Converter)",
        "category": "Analog",
        "icon": "📊",
        "summary": "16-channel 10-bit Successive Approximation ADC with internal 1.1V and 2.56V voltage references and differential gain stages.",
        "order_index": 6,
        "details": {
            "full_description": (
                "The ATmega2560 incorporates a **16-channel, 10-bit Successive Approximation ADC**. "
                "It includes single-ended analog inputs A0-A15 and differential channels with 10x and 200x gain.\n\n"
                "### 🔑 Commonly Used Registers for ADC\n"
                "- **`ADMUX`**: ADC Multiplexer Select (Reference voltage `REFS1:0`, Left adjust `ADLAR`, Channel select `MUX4:0`).\n"
                "- **`ADCSRA`**: ADC Control & Status A (`ADEN` Enable, `ADSC` Start conversion, `ADATE` Auto-trigger, `ADIE` Interrupt enable, Prescaler `ADPS2:0`).\n"
                "- **`ADCSRB`**: ADC Control & Status B (`MUX5` bit for high channels A8-A15, trigger source).\n"
                "- **`ADCH` / `ADCL`**: ADC Data Register pair holding 10-bit result.\n"
                "- **`DIDR0` / `DIDR2`**: Digital Input Disable Registers (Saves power on analog pins).\n\n"
                "![ADC Successive Approximation Diagram](https://upload.wikimedia.org/wikipedia/commons/thumb/6/61/ADC_SAR_State_Diagram.svg/640px-ADC_SAR_State_Diagram.svg.png)\n"
                "*Figure 6: Successive Approximation Register (SAR) ADC Conversion Process.*"
            ),
            "architecture_role": "Converting analog sensor voltages into digital numbers (0 to 1023).",
            "hardware_specs": (
                "- **Resolution**: 10-bit (0 to 1023)\n"
                "- **Channels**: 16 single-ended channels (A0 - A15)\n"
                "- **References**: `DEFAULT` (5V), `INTERNAL1V1` (1.1V), `INTERNAL2V56` (2.56V), `EXTERNAL` (AREF pin)"
            ),
            "hardware_registers": (
                "### 📋 ADC Register & Bitfield Reference\n"
                "| Register | Name | Function |\n"
                "|---|---|---|\n"
                "| `ADMUX` | Multiplexer Register | `REFS1:0` Reference bits, `MUX4:0` Channel bits |\n"
                "| `ADCSRA` | Control Register A | `ADEN`, `ADSC`, `ADIE`, `ADPS2:0` Prescaler |\n"
                "| `ADCSRB` | Control Register B | `MUX5` (Bit 3) enables channels A8 through A15 |\n"
                "| `ADCL/H` | Data Registers | 10-bit output value (Read `ADCL` first!) |"
            ),
            "mega2560_pins": (
                "| Mega Pin | AVR Channel | Physical Pin |\n"
                "|---|---|---|\n"
                "| **A0 - A7** | ADC0 - ADC7 | Port F (PF0 - PF7) |\n"
                "| **A8 - A15** | ADC8 - ADC15 | Port K (PK0 - PK7) |"
            ),
            "requires_external_library": False,
            "library_analysis": (
                "### Is an external library required?\n"
                "**No library is required.** Standard `analogRead()` works natively."
            )
        },
        "libraries": [
            {
                "name": "Arduino Core (analogRead)",
                "is_builtin": True,
                "header_file": "<Arduino.h>",
                "purpose": "Standard 10-bit analog conversion for pins A0-A15.",
                "installation_guide": "Built-in.",
                "documentation_url": "https://www.arduino.cc/reference/en/language/functions/analog-io/analogread/"
            }
        ],
        "code_examples": [
            {
                "title": "Precision 2.56V Internal Reference Multi-Sensor Sampling",
                "category": "Standard Arduino API",
                "difficulty": "Beginner",
                "description": "Utilize the ATmega2560's exclusive `INTERNAL2V56` reference voltage to measure small sensor voltages with 2.5mV resolution.",
                "code": (
                    "// ATmega2560 High-Precision ADC with INTERNAL2V56 Reference\n"
                    "void setup() {\n"
                    "  Serial.begin(115200);\n"
                    "  analogReference(INTERNAL2V56); // 2.56V Internal Bandgap\n"
                    "  delay(10);\n"
                    "}\n\n"
                    "void loop() {\n"
                    "  int raw = analogRead(A0);\n"
                    "  float voltage = (raw / 1023.0) * 2.56;\n"
                    "  Serial.print(F(\"A0 Raw: \")); Serial.print(raw);\n"
                    "  Serial.print(F(\" | Voltage: \")); Serial.println(voltage, 3);\n"
                    "  delay(1000);\n"
                    "}\n"
                ),
                "explanation": (
                    "1. Switches internal reference to 2.56V.\n"
                    "2. Delivers `2.56V / 1023 = 2.5mV` per count accuracy."
                ),
                "circuit_notes": "Input voltage must not exceed 2.56V in this mode.",
                "order_index": 1
            },
            {
                "title": "Free-Running Interrupt-Driven ADC (9.6 kHz Sample Rate)",
                "category": "Direct Register (AVR C++)",
                "difficulty": "Advanced",
                "description": "Configure ADC to run continuously in the background and fire `ISR(ADC_vect)` on every finished sample.",
                "code": (
                    "// High-Speed Free-Running ADC with Interrupt on ATmega2560\n"
                    "#include <avr/io.h>\n"
                    "#include <avr/interrupt.h>\n\n"
                    "volatile uint16_t latestADC = 0;\n\n"
                    "void setup() {\n"
                    "  Serial.begin(115200);\n"
                    "  cli();\n"
                    "  ADMUX = (1 << REFS0); // AVCC reference, A0 channel\n"
                    "  ADCSRB = 0; // Free running mode\n"
                    "  ADCSRA = (1 << ADEN) | (1 << ADATE) | (1 << ADIE) | (1 << ADPS2) | (1 << ADPS1) | (1 << ADPS0); // Prescaler 128\n"
                    "  DIDR0 |= (1 << ADC0D); // Disable digital input buffer\n"
                    "  ADCSRA |= (1 << ADSC); // Start first conversion\n"
                    "  sei();\n"
                    "}\n\n"
                    "ISR(ADC_vect) {\n"
                    "  uint8_t low = ADCL;\n"
                    "  uint8_t high = ADCH;\n"
                    "  latestADC = (high << 8) | low;\n"
                    "}\n\n"
                    "void loop() {\n"
                    "  Serial.print(F(\"Live A0 Value: \")); Serial.println(latestADC);\n"
                    "  delay(500);\n"
                    "}\n"
                ),
                "explanation": (
                    "1. `ADATE` enables free running auto-triggering.\n"
                    "2. `ISR(ADC_vect)` captures sample values at 9,615 Hz without CPU polling."
                ),
                "circuit_notes": "Connect potentiometer output to Pin A0.",
                "order_index": 2
            }
        ]
    },
    {
        "slug": "interrupts",
        "name": "External Interrupts (INT0 through INT7)",
        "category": "Interrupts",
        "icon": "⚡",
        "summary": "8 dedicated hardware external interrupt pins (INT0 - INT7) and 24 Pin Change Interrupts (PCINT) with low-latency edge triggers.",
        "order_index": 7,
        "details": {
            "full_description": (
                "The ATmega2560 features **8 dedicated external interrupts** (INT0 to INT7) plus 24 Pin Change Interrupts (PCINT).\n\n"
                "### 🔑 Commonly Used Registers for Interrupts\n"
                "- **`EICRA`**: External Interrupt Control Register A (Sets trigger mode for INT0-INT3: LOW level, CHANGE, FALLING, RISING).\n"
                "- **`EICRB`**: External Interrupt Control Register B (Sets trigger mode for INT4-INT7).\n"
                "- **`EIMSK`**: External Interrupt Mask Register (Enables individual interrupts `INT7:0`).\n"
                "- **`EIFR`**: External Interrupt Flag Register (Hardware flags cleared when ISR runs).\n"
                "- **`PCICR` / `PCMSKn`**: Pin Change Interrupt Control and Mask Registers."
            ),
            "architecture_role": "Immediate hardware event handling bypassing main loop delay, encoder processing, safety emergency stop.",
            "hardware_specs": (
                "- **Dedicated External Interrupts**: 8 pins (INT0 - INT7)\n"
                "- **Pin Change Interrupts**: 24 pins (PCINT0 - PCINT23)\n"
                "- **Triggers**: LOW Level, Logical CHANGE, FALLING Edge, RISING Edge"
            ),
            "hardware_registers": (
                "### 📋 External Interrupt Register Reference\n"
                "| Register | Name | Function |\n"
                "|---|---|---|\n"
                "| `EICRA` | Control Register A | `ISC31:0` through `ISC01:0` bits |\n"
                "| `EICRB` | Control Register B | `ISC71:0` through `ISC41:0` bits |\n"
                "| `EIMSK` | Mask Register | Set `INT0` through `INT7` bits to 1 to enable |\n"
                "| `EIFR` | Flag Register | Holds active pending interrupt flags |"
            ),
            "mega2560_pins": (
                "| Interrupt | Arduino Mega Pin | Physical AVR Pin |\n"
                "|---|---|---|\n"
                "| **INT0 / INT1** | Pins 21, 20 | PD0, PD1 |\n"
                "| **INT2 / INT3** | Pins 19, 18 | PD2, PD3 |\n"
                "| **INT4 / INT5** | Pins 2, 3 | PE4, PE5 |\n"
                "| **INT6 / INT7** | Headers PE6, PE7 | PE6, PE7 |"
            ),
            "requires_external_library": False,
            "library_analysis": (
                "**No external library required.** `attachInterrupt()` is built-in."
            )
        },
        "libraries": [
            {
                "name": "Arduino Core (attachInterrupt)",
                "is_builtin": True,
                "header_file": "<Arduino.h>",
                "purpose": "Attach callback handlers to interrupt pins.",
                "installation_guide": "Built-in.",
                "documentation_url": "https://www.arduino.cc/reference/en/language/functions/external-interrupts/attachinterrupt/"
            }
        ],
        "code_examples": [
            {
                "title": "Quadrature Encoder Decoder via attachInterrupt",
                "category": "Standard Arduino API",
                "difficulty": "Intermediate",
                "description": "Decode rotary encoder rotation using INT4 (Pin 2) and INT5 (Pin 3).",
                "code": (
                    "// ATmega2560 Quadrature Encoder Decoder\n"
                    "const int pinA = 2; // INT4\n"
                    "const int pinB = 3; // INT5\n"
                    "volatile long position = 0;\n\n"
                    "void setup() {\n"
                    "  Serial.begin(115200);\n"
                    "  pinMode(pinA, INPUT_PULLUP);\n"
                    "  pinMode(pinB, INPUT_PULLUP);\n"
                    "  attachInterrupt(digitalPinToInterrupt(pinA), handleEncoder, RISING);\n"
                    "}\n\n"
                    "void loop() {\n"
                    "  Serial.print(F(\"Position: \")); Serial.println(position);\n"
                    "  delay(100);\n"
                    "}\n\n"
                    "void handleEncoder() {\n"
                    "  if (digitalRead(pinB) == HIGH) position++; else position--;\n"
                    "}\n"
                ),
                "explanation": (
                    "1. Attaches `handleEncoder` callback to Pin 2.\n"
                    "2. Evaluates state of Pin 3 inside ISR to determine direction."
                ),
                "circuit_notes": "Connect Encoder Channel A -> Pin 2 and Channel B -> Pin 3.",
                "order_index": 1
            },
            {
                "title": "Bare-Metal External Interrupt INT4 (Pin 2) Setup",
                "category": "Direct Register (AVR C++)",
                "difficulty": "Advanced",
                "description": "Configure External Interrupt INT4 on Pin 2 directly via `EICRB` and `EIMSK` registers.",
                "code": (
                    "// ATmega2560 Bare-Metal External Interrupt INT4 (Pin 2 / PE4)\n"
                    "#include <avr/io.h>\n"
                    "#include <avr/interrupt.h>\n\n"
                    "volatile uint32_t pulseCount = 0;\n\n"
                    "void setup() {\n"
                    "  Serial.begin(115200);\n"
                    "  cli();\n"
                    "  DDRE &= ~(1 << DDE4); // Pin 2 (PE4) as INPUT\n"
                    "  PORTE |= (1 << PORTE4); // Enable internal pull-up\n\n"
                    "  // Set Falling Edge Trigger for INT4: ISC41=1, ISC40=0 in EICRB\n"
                    "  EICRB |= (1 << ISC41);\n"
                    "  EICRB &= ~(1 << ISC40);\n\n"
                    "  // Enable INT4 in EIMSK\n"
                    "  EIMSK |= (1 << INT4);\n"
                    "  sei();\n"
                    "}\n\n"
                    "ISR(INT4_vect) {\n"
                    "  pulseCount++;\n"
                    "}\n\n"
                    "void loop() {\n"
                    "  Serial.print(F(\"Pulses: \")); Serial.println(pulseCount);\n"
                    "  delay(500);\n"
                    "}\n"
                ),
                "explanation": (
                    "1. Configures Pin 2 (PE4) pull-up.\n"
                    "2. `EICRB |= (1 << ISC41)` sets falling edge trigger.\n"
                    "3. `EIMSK |= (1 << INT4)` enables hardware ISR execution."
                ),
                "circuit_notes": "Connect a push button between Pin 2 and GND.",
                "order_index": 2
            }
        ]
    },
    {
        "slug": "gpio",
        "name": "Digital I/O & Port Manipulation (Ports A - L)",
        "category": "Digital I/O",
        "icon": "🎛️",
        "summary": "54 General Purpose I/O pins organized into eleven 8-bit ports (A through L) with high-speed direct port manipulation.",
        "order_index": 8,
        "details": {
            "full_description": (
                "The ATmega2560 provides **54 general-purpose digital I/O pins** across eleven 8-bit ports (A to L).\n\n"
                "### 🔑 Commonly Used Registers for GPIO\n"
                "- **`DDRx`**: Data Direction Register (1 = Output, 0 = Input).\n"
                "- **`PORTx`**: Data Register (When Output: 1=HIGH, 0=LOW. When Input: 1=Enable Pull-up).\n"
                "- **`PINx`**: Input Pins Address (Reads physical logic level; writing 1 to a `PINx` bit toggles `PORTx` in 1 clock cycle!)."
            ),
            "architecture_role": "High-speed parallel bus driving, LED matrix control, fast pin toggling.",
            "hardware_specs": (
                "- **Total Digital Pins**: 54 pins\n"
                "- **Ports**: 11 ports (A through L)\n"
                "- **Speed**: 1 clock cycle (62.5 ns) for register write vs ~50 cycles for `digitalWrite()`"
            ),
            "hardware_registers": (
                "### 📋 Digital Port Register Summary\n"
                "| Register | Function |\n"
                "|---|---|\n"
                "| `DDRA` to `DDRL` | Direction Control |\n"
                "| `PORTA` to `PORTL` | Output Level / Pull-up Enable |\n"
                "| `PINA` to `PINL` | Physical Pin Read / Single-Cycle Toggle |"
            ),
            "mega2560_pins": (
                "| Port | Pins |\n"
                "|---|---|\n"
                "| **Port A** | Pins 22 - 29 |\n"
                "| **Port C** | Pins 30 - 37 |\n"
                "| **Port L** | Pins 42 - 49 |\n"
                "| **Port B** | Pins 53, 52, 51, 50, 10, 11, 12, 13 |"
            ),
            "requires_external_library": False,
            "library_analysis": (
                "**No external library required.** Native functions and registers are standard."
            )
        },
        "libraries": [
            {
                "name": "Arduino Core (Digital I/O)",
                "is_builtin": True,
                "header_file": "<Arduino.h>",
                "purpose": "Standard pinMode, digitalWrite, and digitalRead.",
                "installation_guide": "Built-in.",
                "documentation_url": "https://www.arduino.cc/reference/en/language/functions/digital-io/digitalwrite/"
            }
        ],
        "code_examples": [
            {
                "title": "8-Bit Parallel Port Write (Port A: Pins 22-29)",
                "category": "Direct Register (AVR C++)",
                "difficulty": "Intermediate",
                "description": "Output an entire 8-bit byte across pins 22-29 in a single 62.5ns instruction.",
                "code": (
                    "// ATmega2560 Port A Parallel Output (Pins 22-29)\n"
                    "#include <avr/io.h>\n\n"
                    "void setup() {\n"
                    "  DDRA = 0xFF; // Set Pins 22-29 as OUTPUTs\n"
                    "}\n\n"
                    "void loop() {\n"
                    "  for (uint8_t val = 0; val < 255; val++) {\n"
                    "    PORTA = val; // Single cycle write to all 8 pins!\n"
                    "    delay(10);\n"
                    "  }\n"
                    "}\n"
                ),
                "explanation": (
                    "1. Pins 22-29 map to `PA0-PA7`.\n"
                    "2. Writing `PORTA` updates all 8 lines simultaneously with zero skew."
                ),
                "circuit_notes": "Connect 8 LEDs to Pins 22-29 with resistor networks.",
                "order_index": 1
            },
            {
                "title": "Arduino Core Multi-Pin Blink",
                "category": "Standard Arduino API",
                "difficulty": "Beginner",
                "description": "Standard Arduino digital output using `pinMode()` and `digitalWrite()`.",
                "code": (
                    "// Arduino Core Digital Output\n"
                    "const int ledPin = 13;\n\n"
                    "void setup() {\n"
                    "  pinMode(ledPin, OUTPUT);\n"
                    "}\n\n"
                    "void loop() {\n"
                    "  digitalWrite(ledPin, HIGH);\n"
                    "  delay(500);\n"
                    "  digitalWrite(ledPin, LOW);\n"
                    "  delay(500);\n"
                    "}\n"
                ),
                "explanation": (
                    "1. `pinMode()` sets direction.\n"
                    "2. `digitalWrite()` sets pin state."
                ),
                "circuit_notes": "Uses onboard Pin 13 LED.",
                "order_index": 2
            }
        ]
    },
    {
        "slug": "watchdog",
        "name": "Watchdog Timer (WDT)",
        "category": "Supporting Circuits",
        "icon": "🐕",
        "summary": "Independent on-chip 128 kHz RC oscillator providing system hang protection, automatic reset, and low-power sleep wake-up.",
        "order_index": 9,
        "details": {
            "full_description": (
                "The **Watchdog Timer (WDT)** in the ATmega2560 runs on an independent internal 128 kHz RC oscillator.\n\n"
                "### 🔑 Commonly Used Registers for Watchdog\n"
                "- **`WDTCSR`**: Watchdog Timer Control Register (`WDIF` Interrupt Flag, `WDIE` Interrupt Enable, `WDP3:0` Timeout prescaler, `WDCE` Change Enable, `WDE` Reset Enable).\n"
                "- **`MCUSR`**: MCU Status Register (Contains `WDRF` Watchdog Reset Flag)."
            ),
            "architecture_role": "Failsafe auto-reset on freeze, low-power periodic sleep wake-up.",
            "hardware_specs": (
                "- **Oscillator**: Internal 128 kHz RC oscillator\n"
                "- **Timeouts**: 16 ms to 8.0 s"
            ),
            "hardware_registers": (
                "### 📋 Watchdog Control Register Reference\n"
                "| Register | Name | Function |\n"
                "|---|---|---|\n"
                "| `WDTCSR` | Control Register | `WDIE`, `WDE`, `WDP3:0` timeout prescaler bits |"
            ),
            "mega2560_pins": "Internal peripheral; no external pins required.",
            "requires_external_library": False,
            "library_analysis": (
                "**No external library required.** Standard `<avr/wdt.h>` is built-in."
            )
        },
        "libraries": [
            {
                "name": "avr/wdt.h",
                "is_builtin": True,
                "header_file": "<avr/wdt.h>",
                "purpose": "Provides wdt_enable(), wdt_disable(), and wdt_reset() macros.",
                "installation_guide": "Pre-installed.",
                "documentation_url": "https://www.nongnu.org/avr-libc/user-manual/group__avr__watchdog.html"
            }
        ],
        "code_examples": [
            {
                "title": "Industrial Watchdog Reset Guard (2-Second Timeout)",
                "category": "Direct Register (AVR C++)",
                "difficulty": "Intermediate",
                "description": "Protect the Arduino Mega against unexpected lockups using a 2-second watchdog timer.",
                "code": (
                    "// ATmega2560 Watchdog System Reset Guard\n"
                    "#include <avr/wdt.h>\n\n"
                    "void setup() {\n"
                    "  Serial.begin(115200);\n"
                    "  Serial.println(F(\"\\n--- System Booted ---\"));\n"
                    "  wdt_enable(WDTO_2S); // 2-second timeout\n"
                    "}\n\n"
                    "void loop() {\n"
                    "  Serial.println(F(\"Patting the dog...\"));\n"
                    "  wdt_reset(); // Pat watchdog\n"
                    "  delay(500);\n"
                    "}\n"
                ),
                "explanation": (
                    "1. `wdt_enable(WDTO_2S)` sets 2-second timeout.\n"
                    "2. Calling `wdt_reset()` resets timer."
                ),
                "circuit_notes": "Open Serial Monitor at 115200 baud.",
                "order_index": 1
            },
            {
                "title": "Low-Power Periodic Sleep & Watchdog Wakeup",
                "category": "Library Implementation",
                "difficulty": "Intermediate",
                "description": "Put ATmega2560 to sleep and wake up every 8 seconds via Watchdog Interrupt.",
                "code": (
                    "// ATmega2560 Low Power Watchdog Sleep\n"
                    "#include <avr/wdt.h>\n"
                    "#include <avr/sleep.h>\n"
                    "#include <avr/interrupt.h>\n\n"
                    "ISR(WDT_vect) {\n"
                    "  // Watchdog interrupt callback (wakes CPU from sleep)\n"
                    "}\n\n"
                    "void setup() {\n"
                    "  Serial.begin(115200);\n"
                    "  cli();\n"
                    "  WDTCSR |= (1 << WDCE) | (1 << WDE);\n"
                    "  WDTCSR = (1 << WDIE) | (1 << WDP3) | (1 << WDP0); // Interrupt mode, 8s timeout\n"
                    "  sei();\n"
                    "}\n\n"
                    "void loop() {\n"
                    "  Serial.println(F(\"Entering Sleep for 8 seconds...\"));\n"
                    "  Serial.flush();\n"
                    "  set_sleep_mode(SLEEP_MODE_PWR_DOWN);\n"
                    "  sleep_mode(); // CPU sleeps until Watchdog fires\n"
                    "  Serial.println(F(\"Woke up from sleep!\"));\n"
                    "}\n"
                ),
                "explanation": (
                    "1. Sets WDT to Interrupt Mode (`WDIE`).\n"
                    "2. `sleep_mode()` reduces current draw to microamps during sleep."
                ),
                "circuit_notes": "Measure current consumption with a multimeter in series with VIN.",
                "order_index": 2
            }
        ]
    },
    {
        "slug": "memory",
        "name": "Memory Architecture (Flash, SRAM & EEPROM)",
        "category": "Core Peripherals",
        "icon": "💾",
        "summary": "256 KB Flash program memory, 8 KB internal SRAM, and 4 KB non-volatile EEPROM for persistent configuration storage.",
        "order_index": 10,
        "details": {
            "full_description": (
                "The ATmega2560 features 256 KB Flash, 8 KB SRAM, and 4 KB EEPROM.\n\n"
                "### 🔑 Commonly Used Registers for EEPROM & Flash Memory\n"
                "- **`EEARH` / `EEARL`**: 12-bit EEPROM Address Registers (0 to 4095).\n"
                "- **`EEDR`**: EEPROM Data Register (Data byte to read or write).\n"
                "- **`EECR`**: EEPROM Control Register (`EERE` Read Enable, `EEPE` Write Enable, `EEMPE` Master Write Enable).\n"
                "- **`SPMCSR`**: Store Program Memory Control Register."
            ),
            "architecture_role": "Non-volatile settings retention and Flash constant array storage.",
            "hardware_specs": (
                "- **Flash**: 256 KB\n"
                "- **SRAM**: 8 KB\n"
                "- **EEPROM**: 4 KB (4096 bytes)"
            ),
            "hardware_registers": (
                "### 📋 EEPROM Register Reference\n"
                "| Register | Function |\n"
                "|---|---|\n"
                "| `EEARH:L` | Address 0 to 4095 |\n"
                "| `EEDR` | Data byte |\n"
                "| `EECR` | `EEMPE` Master Write Enable, `EEPE` Write Enable, `EERE` Read Enable |"
            ),
            "mega2560_pins": "Internal memory subsystem.",
            "requires_external_library": False,
            "library_analysis": (
                "**No external library required.** `<EEPROM.h>` and `<avr/pgmspace.h>` are built-in."
            )
        },
        "libraries": [
            {
                "name": "EEPROM",
                "is_builtin": True,
                "header_file": "<EEPROM.h>",
                "purpose": "Read and write to 4096-byte EEPROM.",
                "installation_guide": "Pre-installed.",
                "documentation_url": "https://www.arduino.cc/reference/en/language/functions/communication/eeprom/"
            }
        ],
        "code_examples": [
            {
                "title": "Saving Struct in EEPROM (EEPROM.put / get)",
                "category": "Standard Arduino API",
                "difficulty": "Beginner",
                "description": "Store configuration settings in EEPROM so they survive power outages.",
                "code": (
                    "// ATmega2560 EEPROM Configuration Storage\n"
                    "#include <EEPROM.h>\n\n"
                    "struct Config {\n"
                    "  char name[16];\n"
                    "  int baud;\n"
                    "  uint32_t bootCount;\n"
                    "};\n\n"
                    "void setup() {\n"
                    "  Serial.begin(115200);\n"
                    "  Config cfg;\n"
                    "  EEPROM.get(0, cfg);\n"
                    "  if (cfg.bootCount == 0xFFFFFFFF) cfg.bootCount = 0;\n"
                    "  cfg.bootCount++;\n"
                    "  EEPROM.put(0, cfg);\n"
                    "  Serial.print(F(\"Boot Count: \")); Serial.println(cfg.bootCount);\n"
                    "}\n\n"
                    "void loop() {}\n"
                ),
                "explanation": (
                    "1. `EEPROM.put()` updates non-volatile memory."
                ),
                "circuit_notes": "Power cycle board to verify boot counter persists.",
                "order_index": 1
            },
            {
                "title": "Direct Register EEPROM Byte Write & Read Routines",
                "category": "Direct Register (AVR C++)",
                "difficulty": "Advanced",
                "description": "Perform raw low-level EEPROM read and write operations using `EEAR`, `EEDR`, and `EECR` registers.",
                "code": (
                    "// ATmega2560 Direct Register EEPROM Programming\n"
                    "#include <avr/io.h>\n\n"
                    "void EEPROM_WriteByte(uint16_t address, uint8_t data) {\n"
                    "  while (EECR & (1 << EEPE)); // Wait for completion of previous write\n"
                    "  EEAR = address; // Set address\n"
                    "  EEDR = data;    // Set data\n"
                    "  EECR |= (1 << EEMPE); // Master Write Enable\n"
                    "  EECR |= (1 << EEPE);  // Start Write\n"
                    "}\n\n"
                    "uint8_t EEPROM_ReadByte(uint16_t address) {\n"
                    "  while (EECR & (1 << EEPE)); // Wait for completion\n"
                    "  EEAR = address;\n"
                    "  EECR |= (1 << EERE); // Start Read\n"
                    "  return EEDR;\n"
                    "}\n\n"
                    "void setup() {\n"
                    "  Serial.begin(115200);\n"
                    "  EEPROM_WriteByte(0x05, 0x42);\n"
                    "  uint8_t val = EEPROM_ReadByte(0x05);\n"
                    "  Serial.print(F(\"Read Register EEPROM: 0x\")); Serial.println(val, HEX);\n"
                    "}\n\n"
                    "void loop() {}\n"
                ),
                "explanation": (
                    "1. Address is written to `EEAR` (12-bit register).\n"
                    "2. Data byte is loaded into `EEDR`.\n"
                    "3. Timed safety sequence: set `EEMPE` bit first, then set `EEPE` bit within 4 clock cycles."
                ),
                "circuit_notes": "Internal EEPROM address space spans 0x000 to 0xFFF (4096 bytes).",
                "order_index": 2
            }
        ]
    }
]
