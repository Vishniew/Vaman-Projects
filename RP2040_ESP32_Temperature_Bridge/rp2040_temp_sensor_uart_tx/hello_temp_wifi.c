#include <stdio.h>
#include "pico/stdlib.h"
#include "hardware/adc.h"
#include "hardware/uart.h"

// Use UART0 at 115200 baud
#define UART_ID uart0
#define BAUD_RATE 115200
#define UART_TX_PIN 0
#define UART_RX_PIN 1

int main() {
    stdio_init_all();

    // 1. Initialize UART
    uart_init(UART_ID, BAUD_RATE);
    gpio_set_function(UART_TX_PIN, GPIO_FUNC_UART);
    gpio_set_function(UART_RX_PIN, GPIO_FUNC_UART);

    // 2. Initialize ADC for Temperature Sensor
    adc_init();
    adc_set_temp_sensor_enabled(true);
    adc_select_input(4); // Internal temp sensor is on ADC 4

    char msg[32];

    // Inside your while(true) loop in RP2040 main.c
    while (true) {
        uint16_t raw = adc_read();
        const float conversion_factor = 3.3f / (1 << 12);
        float voltage = raw * conversion_factor;
        float temp = 27.0f - (voltage - 0.706f) / 0.001721f;

        // Change the message format here!
        // We send the full phrase including the degree symbol
        sprintf(msg, "Sent to ESP32: %.2f °C\n", temp);

        // Send it out
        uart_puts(UART_ID, msg);

        printf("Local Log: %s", msg); // This shows on your laptop
        sleep_ms(2000);
    }
}