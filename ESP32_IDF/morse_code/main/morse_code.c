/*
 * Morse Code Blinker
 * 
 * This program reads characters from UART input and blinks an LED
 * connected to GPIO2 in Morse code representation of the input text.
 * 
 * Each letter is translated into Morse code using a lookup table.
 * Dots and dashes are represented by short and long LED blinks respectively.
 * Spaces between letters and words are handled with appropriate delays.
 */
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "freertos/queue.h"
#include "driver/gpio.h"

// Hardware Definition
#define LED_PIN 2
#define DOT_TIME 200 // Base unit: 200ms

// Morse lookup table (Index 0=A, 1=B, etc.)
const char* morse_table[] = {
    ".-",   "-...", "-.-.", "-..",  ".",    "..-.", "--.",  "....", "..",   ".---", // A-J
    "-.-",  ".-..", "--",   "-.",   "---",  ".--.", "--.-", ".-.",  "...",  "-",    // K-T
    "..-",  "...-", ".--",  "-..-", "-.--", "--.."                          // U-Z
};

QueueHandle_t morseQueue;

// Helper: Blinks a single dot or dash
void blink_unit(int duration) {
    gpio_set_level(LED_PIN, 1);
    vTaskDelay(pdMS_TO_TICKS(duration));
    gpio_set_level(LED_PIN, 0);
    vTaskDelay(pdMS_TO_TICKS(DOT_TIME)); // Gap between symbols in same letter
}

// Logic: Translates letter into a sequence of blinks
void process_letter(char c) {
    c = toupper(c);
    
    // Handle spaces between words
    if (c == ' ') {
        printf("[Space]\n");
        vTaskDelay(pdMS_TO_TICKS(DOT_TIME * 4)); 
        return;
    }

    // Filter only A-Z
    if (c < 'A' || c > 'Z') return;

    // The Lookup: 'c - A' gives the index (e.g., 'B' - 'A' = 1)
    const char* pattern = morse_table[c - 'A'];
    printf("Blinking %c: %s\n", c, pattern);

    for (int i = 0; i < strlen(pattern); i++) {
        if (pattern[i] == '.') {
            blink_unit(DOT_TIME);
        } else if (pattern[i] == '-') {
            blink_unit(DOT_TIME * 3);
        }
    }
    vTaskDelay(pdMS_TO_TICKS(DOT_TIME * 2)); // Gap between different letters
}

// Task 1: Receiver (UART)
void uart_task(void *pvParameters) {
    char incoming;
    printf("\n--- Morse Code System Ready ---\n");
    printf("Type words and press Enter to blink the LED...\n");

    while (1) {
        incoming = getchar();
        if (incoming != EOF && incoming != '\n' && incoming != '\r') {
            // Push letter to queue
            xQueueSend(morseQueue, &incoming, 0);
        }
        vTaskDelay(pdMS_TO_TICKS(50));
    }
}

// Task 2: Executer (LED)
void morse_led_task(void *pvParameters) {
    char letter;
    while (1) {
        // Sleep until a letter arrives
        if (xQueueReceive(morseQueue, &letter, portMAX_DELAY)) {
            process_letter(letter);
        }
    }
}

void app_main(void) {
    // --- LED CONFIGURATION STARTS HERE ---
    gpio_reset_pin(LED_PIN);                       // Clear any previous settings
    gpio_set_direction(LED_PIN, GPIO_MODE_OUTPUT); // Set Pin 2 as Output
    // --- LED CONFIGURATION ENDS HERE ---

    // Create a Queue for 32 characters
    morseQueue = xQueueCreate(32, sizeof(char));

    if (morseQueue != NULL) {
        // Start the workers
        xTaskCreate(uart_task, "UART_Reader", 2048, NULL, 5, NULL);
        xTaskCreate(morse_led_task, "Morse_Blinker", 2048, NULL, 5, NULL);
    } else {
        printf("Queue creation failed!\n");
    }
}