#include <stdio.h>
#include <stdbool.h>  // Required for 'bool' type
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/ledc.h"
#include "driver/touch_sensor.h"

#define LED_PIN          5
#define TOUCH_PIN        TOUCH_PAD_NUM0 // GPIO 4
#define TOUCH_THRESH     300

// Shared variables
volatile int global_duty = 0; 
volatile bool manual_override = false; // The "Switch" between Manual and Auto

// Task 1: The Sensor Specialist (Auto-Control)
void touch_sensor_task(void *pvParameters) {
    uint16_t touch_value;
    while (1) {
        // Only run this logic if the user hasn't taken manual control via UART
        if (!manual_override) {
            touch_pad_read(TOUCH_PIN, &touch_value);
            
            if (touch_value < TOUCH_THRESH) {
                if (global_duty < 1023) global_duty += 40; 
            } else {
                if (global_duty > 0) global_duty -= 20;
            }
        }
        vTaskDelay(pdMS_TO_TICKS(20));
    }
}

// Task 2: The Command Specialist (Manual-Control)
void uart_command_task(void *pvParameters) {
    char incoming_char;
    printf("\n--- ESP32 Command Center Started ---\n");
    printf("Commands: H=High, L=Low, O=Off, R=Resume Sensor\n");

    while (1) {
        incoming_char = getchar();

        if (incoming_char != EOF && incoming_char != '\n' && incoming_char != '\r') {
            
            if (incoming_char == 'H' || incoming_char == 'h') {
                global_duty = 1023;
                manual_override = true; // Block sensor
                printf(">> Manual Mode: HIGH\n");
            } 
            else if (incoming_char == 'L' || incoming_char == 'l') {
                global_duty = 150;
                manual_override = true; // Block sensor
                printf(">> Manual Mode: LOW\n");
            }
            else if (incoming_char == 'O' || incoming_char == 'o') {
                global_duty = 0;
                manual_override = true; // Block sensor
                printf(">> Manual Mode: OFF\n");
            }
            else if (incoming_char == 'R' || incoming_char == 'r') {
                manual_override = false; // Hand back to sensor
                printf(">> Mode: SENSOR CONTROL RESTORED\n");
            }
        }
        vTaskDelay(pdMS_TO_TICKS(10)); 
    }
}

// Task 3: The Light Specialist (Hardware Output)
void led_pwm_task(void *pvParameters) {
    while (1) {
        ledc_set_duty(LEDC_LOW_SPEED_MODE, LEDC_CHANNEL_0, global_duty);
        ledc_update_duty(LEDC_LOW_SPEED_MODE, LEDC_CHANNEL_0);
        vTaskDelay(pdMS_TO_TICKS(30));
    }
}

void app_main(void) {
    // 1. Hardware Setup: PWM
    ledc_timer_config_t ledc_timer = {
        .speed_mode = LEDC_LOW_SPEED_MODE, .timer_num = LEDC_TIMER_0,
        .duty_resolution = LEDC_TIMER_10_BIT, .freq_hz = 5000, .clk_cfg = LEDC_AUTO_CLK
    };
    ledc_timer_config(&ledc_timer);

    ledc_channel_config_t ledc_channel = {
        .speed_mode = LEDC_LOW_SPEED_MODE, .channel = LEDC_CHANNEL_0,
        .timer_sel = LEDC_TIMER_0, .gpio_num = LED_PIN, .duty = 0, .hpoint = 0
    };
    ledc_channel_config(&ledc_channel);

    // 2. Hardware Setup: Touch
    touch_pad_init();
    touch_pad_config(TOUCH_PIN, 0);

    // 3. Launching 3 Tasks
    xTaskCreate(touch_sensor_task, "TouchTask", 2048, NULL, 5, NULL);
    xTaskCreate(uart_command_task, "UartTask", 2048, NULL, 5, NULL);
    xTaskCreate(led_pwm_task, "LEDTask", 2048, NULL, 5, NULL);
}


