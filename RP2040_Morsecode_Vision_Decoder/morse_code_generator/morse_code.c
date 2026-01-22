#include <stdio.h>
#include <ctype.h>
#include "pico/stdlib.h"

// Define the LED pin
#define LED_PIN 4

// Timing in milliseconds
const uint32_t DOT_TIME = 200;
const uint32_t DASH_TIME = DOT_TIME * 3;
const uint32_t GAP_ELEMENT = DOT_TIME;
const uint32_t GAP_LETTER = DOT_TIME * 3;
const uint32_t GAP_WORD = DOT_TIME * 7;

// Function to blink a single dot or dash
void blink(uint32_t duration) {
    gpio_put(LED_PIN, 1);
    sleep_ms(duration);
    gpio_put(LED_PIN, 0);
    sleep_ms(GAP_ELEMENT);
}

// Function to process Morse patterns
void play_morse(const char* pattern) {
    for (int i = 0; pattern[i] != '\0'; i++) {
        if (pattern[i] == '.') blink(DOT_TIME);
        else if (pattern[i] == '-') blink(DASH_TIME);
    }
}

// Morse Code Dictionary Lookup
void output_morse(char c) {
    switch (toupper(c)) {
        case 'A': play_morse(".-"); break;
        case 'B': play_morse("-..."); break;
        case 'C': play_morse("-.-."); break;
        case 'D': play_morse("-.."); break;
        case 'E': play_morse("."); break;
        case 'F': play_morse("..-."); break;
        case 'G': play_morse("--."); break;
        case 'H': play_morse("...."); break;
        case 'I': play_morse(".."); break;
        case 'J': play_morse(".---"); break;
        case 'K': play_morse("-.-"); break;
        case 'L': play_morse(".-.."); break;
        case 'M': play_morse("--"); break;
        case 'N': play_morse("-."); break;
        case 'O': play_morse("---"); break;
        case 'P': play_morse(".--."); break;
        case 'Q': play_morse("--.-"); break;        
        case 'R': play_morse(".-."); break;
        case 'S': play_morse("..."); break;
        case 'T': play_morse("-"); break;
        case 'U': play_morse("..-"); break;
        case 'V': play_morse("...-"); break;
        case 'W': play_morse(".--"); break;
        case 'X': play_morse("-..-"); break;
        case 'Y': play_morse("-.--"); break;
        case 'Z': play_morse("--.."); break;
        case ' ': sleep_ms(GAP_WORD); break;
        default: break; // Ignore unknown characters
    }
    sleep_ms(GAP_LETTER);
}

int main() {
    // Initialize standard I/O for Serial Communication
    stdio_init_all();

    // Initialize the GPIO Pin
    gpio_init(LED_PIN);
    gpio_set_dir(LED_PIN, GPIO_OUT);

    printf("Pico Morse Code Terminal Ready!\n");
    printf("Type something and press Enter:\n");

    while (true) {
        int c = getchar_timeout_us(0); // Check if a character is sent from laptop
        if (c != PICO_ERROR_TIMEOUT) {
            putchar(c); // Echo character back to terminal
            output_morse((char)c);
        }
    }
}