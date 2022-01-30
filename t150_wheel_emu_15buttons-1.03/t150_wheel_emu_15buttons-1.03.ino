/*
Ver. 1.03 - 2020-03-28

Changelog:
1.03 - 2020-03-28 - Inner while loop fix. Added && condition to exit if SS became HIGH (prevent infinite loop).
1.02 - 2020-03-22 - Wiring simplified, Orange wire (SS = SlaveSelect) goes to Arduino Nano Pin D10 only. Button 2 (Gear Up) moved to Pin2.
1.01 - 2020-03-20 - Got myself a T150 Pro set. Arduino emulation works now!
1.00 - 2019-07-25 - Based on tmx_wheel_emu_16buttons.ino - for beta testers (this sketch doesn't work with T150 and must be debugged)

This sketch emulates Thrustmaster T150 / T150 Pro stock steering wheel
It allows to connect Arduino Nano (or Uno) to T150 wheelbase via 5 wires
and to emulate 15 buttons (because stock T150 wheel has 11 buttons + 4 for D-Pad)

Only for ATMega328/AtMega16x based boards - Arduino Nano / Uno / Pro Mini
Sketch must be flashed yvia external programmer or via Arduino as ISP,
because we need to get rid of arduino bootloader, that takes 2 seconds to boot.

If you just flash this sketch into Arduino via USB cable - T150 wheelbase won't recognize
it (because there is 2 seconds power on delay caused by arduino bootloader). Use external programmer or ArduinoISP!
In Arduino IDE use "Sketch" menu -> "Upload using programmer".

Arduino as ISP - refer to
https://www.arduino.cc/en/Tutorial/ArduinoISP
"Start your Arduino instantly - no boot time without bootloader" https://www.youtube.com/watch?v=lsa5h2tVM9w
http://www.martyncurrey.com/arduino-nano-as-an-isp-programmer/

Thrustmaster T150 Wheelbase cable pinout (5264 2.54mm 6-Pin female connector)
1 - Green    - not used (in stock steering rim it's connected to GND via 100k resistor)
2 - Blue     - GND (ground)
3 - White    - MISO (master in, slave out - to read the data from the wheel)
4 - Orange   - SS (slave select, or PL - parallel load, set it to 0 when you want to read the data)
5 - Red      - CLK (clock impulses)
6 - Black    - +VCC (+3.3 volts! if you have Arduino 5V version - use external +3.3V power or use the wheelbase power!!!)

Arduino Nano pins -> T150 wheelbase cable pins

Arduino GND                      -> T150 Blue wire (2)
Arduino pin 12 (MISO)            -> T150 White wire (3) (data from wheel to base)
Arduino pins 10 (SS)             -> T150 Orange wire pin (4)
Arduino pin 13 (SCK)             -> T150 Red wire (5)
Arduino +5V                      -> T150 Black wire (6) (wheelbase provides 3.3V, but it must be connected into +5V socket on arduino side)

T150 PS wheel button mapping is absolutely the same as T300 PS wheel.
We send 8 bytes to wheelbase, only 3 first bytes matter, only 15 bits are used for buttons:

Byte 1 (constant)
  1 - not used
  1 - n/u
  0 - n/u
  1 - n/u
  0 - n/u
  0 - n/u
  0 - n/u
  1 – n/u

Byte 2
  1 – n/u
  1 – Cross (button 6)            ->   pin 6 (portD bit6)
  1 – Circle (button 5)           ->   pin 5 (portD bit5)
  1 – Square (button 4)           ->   pin 4 (portD bit4)
  1 – Options (Start, button 8)   ->   pin 3 (portD bit3)
  1 – R1 (Gear Up, button 2)      ->   pin 2 (portD bit2)
  1 – Triangle (button 3)         ->   pin 1 (TX1) (portD bit1) - if you don't use serial debug (UART TX1)
  1 – R2 (button 9)               ->   pin 0 (RX0) (portD bit0) - if you don't use serial debug (UART RX0)

Byte 3
  1 – Share (Select, button 7)    ->   pin 9 (portB bit1)
  1 – PS (Menu, button 13)        ->   pin 8 (portB bit0)
  1 – D-Pad Down                  ->   pin A5 (portC bit5)
  1 – L1 (Gear Down, button 1)    ->   pin A4 (portC bit4)
  1 – D-Pad Right                 ->   pin A3 (portC bit3)
  1 - D-Pad Left                  ->   pin A2 (portC bit2)
  1 - D-Pad Up                    ->   pin A1 (portC bit1)
  1 - L2 (button 10)              ->   pin A0 (portC bit0)

Each push button has 2 pins - you connect one to Arduino, another to the Ground :)
Pressed button gives you "0" (grounded signal), released = "1" (pulled-up to +VCC)

Feel free to modify and use for your needs.
This sketch and the documentation above provided "AS IS" under the BSD New license.
http://opensource.org/licenses/BSD-3-Clause

(c) Taras Ivaniukovich (blog@rr-m.org)
https://rr-m.org/blog/

Credits:
Virág I. for Pin Change Interrupt idea (move external interrupt from Pin 2 to Pin 10)
Matt R. for reading his T150 wheel and testing
Giuseppe for reading his T150 wheel and testing
Lukas K. for reading his T150 wheel and testing
Alexander L. for beta testing
Chris B. for heavy beta testing
Lukasz S. for beta testing
Ben C. for beta testing
*/

byte wheelState [8]; // push-buttons state saved here
volatile byte next_byte;
volatile byte next_byte_idx;

void setup (void) {
  DDRB  &= B11111000; // digital pins 8,9 used as inputs. 10 - SS also input
  PORTB |= B00000011; // 8,9 - pull-up to +VCC via internal 100k resistors.

  DDRC  &= B11000000; // pins 14-19 (A0 - A5) also used as digital inputs
  PORTC |= B00111111; // pulled-up to +VCC via internal 100k resistors

  DDRD  &= B00000000; // digital pins 0-7 are inputs
  PORTD |= B11111111; // pulled-up to +VCC via internal 100k resistors

  wheelState[0] = B11010001; // T150 wheel first data byte - constant
  wheelState[1] = B11111111; // second data byte - buttons
  wheelState[2] = B11111111; // third data byte - buttons
  wheelState[3] = B11111111; // this and below - not used, but wheelbase reads all 8 bytes...
  wheelState[4] = B11111111;
  wheelState[5] = B11111111;
  wheelState[6] = B11111111;
  wheelState[7] = B11111111;

  SPDR = wheelState[0]; // load first byte into SPI data register
  next_byte_idx = 1;
  next_byte = wheelState[next_byte_idx];

  pinMode(MISO, OUTPUT); // Arduino acts as SPI Slave device, data from Arduino to Wheelbase goes via MISO line
  SPCR |= _BV(SPE);      // Enables SPI when 1

  /* Pin change interrupt - remap external interrupt0 (PCINT0) from pin 2 to pin 10 (same as SS pin).
   * We use pin 10 (SS) to identify when SPI transfer starts (wheelbase sets it to LOW)
   * and when it ends (wheelbase sets it to HIGH and we reset next_byte_idx + prepare SPDR for next transfer)
   * Here we enable external interrupt on pin 10 - via Pin Change Interrupt.
   *
   * https://www.teachmemicro.com/arduino-interrupt-tutorial/
   * Pin Change Interrupt services
   * PCICR = x x x x x PCIE2 PCIE1 PCIE0 - enable PCINT group. PCIE0 = PORTB pins group (PCINT0-PCINT7 = PB0-PB7 = pins 8-13 + XTAL), PCIE1 = PORTC group, PCIE2 = PORTD group.
   * 
   * PCMSK0 = PCINT7 PCINT6 PCINT5 PCINT4 PCINT3 PCINT2 PCINT1 PCINT0 - those are PORTB PB0-PB7 (digital pins 8 - 13, XTAL1, XTAL2)
   * PCMSK1 = x PCINT14 PCINT13 PCINT12 PCINT11 PCINT10 PCINT9 PCINT8 - those are PORTC PC0-PC6 (A0-A5, Reset)
   * PCMSK2 = PCINT23 PCINT22 PCINT21 PCINT20 PCINT19 PCINT18 PCINT17 PCINT16 - those are PORTD PD0-PD7 (digital pins 0 - 7) */
  PCMSK0 = B00000100;     // Only react to PCINT2 = PB2 = D10 (SS pin) (when signal on this pin changes 0->1 OR 1->0 - interrupt happens)
  PCIFR  = B00000000;     // clear all interrupt flags
  PCICR  = B00000001;     // Enable PCIE0 = PORTB group (PCINT0 - PCINT7 = digital pins 8-13) interrupt
}

// PCINT0_vect runs on each SS line change 0->1 or 1->0. Here we transfer 8 bytes to wheelbase - really quick.
ISR(PCINT0_vect) {
  while(!(PINB & B00000100)) { // SS line is LOW - wheelbase wants to read 8 bytes of data.
    while(!(SPSR & _BV(SPIF)) && !(PINB & B00000100)) {} // wait until byte is fully transferred

    SPDR = next_byte;
    next_byte = wheelState[++next_byte_idx];
  }

  // SS line became HIGH - SPI transfer complete
  SPDR = wheelState[0];
  next_byte_idx = 1;
  next_byte = wheelState[next_byte_idx];
}

// Read buttons infinitely, store results to wheelState[]
void loop() {
  // wheelState[0] - always constant for T150 wheel
  wheelState[1] = B10000000 | PIND; // read 7 buttons from PORTD
  wheelState[2] = ((PINB & B00000011) << 6) | (PINC & B00111111); // take bits 0,1 from PORTB + bits 0-5 from PORTC
}
