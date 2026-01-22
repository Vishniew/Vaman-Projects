

#include <stdio.h>
#include "driver/ledc.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"

#define LEDC_GPIO              (2)   // Your onboard Blue LED
#define LEDC_MODE              LEDC_LOW_SPEED_MODE
#define LEDC_TIMER             LEDC_TIMER_0
#define LEDC_DUTY_RES          LEDC_TIMER_10_BIT // 2^10 = 1024 levels of brightness
#define LEDC_FREQUENCY         (5000) // 5 kHz frequency

void app_main(void)
{
    // 1. Setup the Timer
    ledc_timer_config_t ledc_timer = {
        .speed_mode       = LEDC_MODE,
        .timer_num        = LEDC_TIMER,
        .duty_resolution  = LEDC_DUTY_RES,
        .freq_hz          = LEDC_FREQUENCY,
        .clk_cfg          = LEDC_AUTO_CLK
    };
    ledc_timer_config(&ledc_timer);

    // 2. Setup the Channel
    ledc_channel_config_t ledc_channel = {
        .speed_mode     = LEDC_MODE,
        .channel        = LEDC_CHANNEL_0,
        .timer_sel      = LEDC_TIMER,
        .intr_type      = LEDC_INTR_DISABLE,
        .gpio_num       = LEDC_GPIO,
        .duty           = 0, // Start with LED OFF
        .hpoint         = 0
    };
    ledc_channel_config(&ledc_channel);

    printf("PWM Initialized! Starting Fade Loop...\n");

    while (1) {
        // Fade Up
        for (int i = 0; i < 1024; i++) {
            ledc_set_duty(LEDC_MODE, LEDC_CHANNEL_0, i);
            ledc_update_duty(LEDC_MODE, LEDC_CHANNEL_0);
            vTaskDelay(pdMS_TO_TICKS(2)); // Wait 2ms per step
        }
        // Fade Down
        for (int i = 1023; i >= 0; i--) {
            ledc_set_duty(LEDC_MODE, LEDC_CHANNEL_0, i);
            ledc_update_duty(LEDC_MODE, LEDC_CHANNEL_0);
            vTaskDelay(pdMS_TO_TICKS(2));
        }
    }
}

