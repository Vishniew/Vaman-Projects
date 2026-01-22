#include <string.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "freertos/event_groups.h"
#include "esp_system.h"
#include "esp_wifi.h"
#include "esp_event.h"
#include "esp_log.h"
#include "nvs_flash.h"
#include "lwip/err.h"
#include "lwip/sys.h"
#include <esp_http_server.h>
#include <driver/gpio.h>
#include <driver/uart.h> // Added for UART communication

/* WiFi Config */
#define EXAMPLE_ESP_WIFI_SSID      "YOUR_WIFI_SSID"
#define EXAMPLE_ESP_WIFI_PASS      "YOUR_WIFI_PASSWORD"
#define EXAMPLE_ESP_MAXIMUM_RETRY  CONFIG_ESP_MAXIMUM_RETRY

/* UART Config for Vaman Internal Connection */
#define UART_PORT_NUM      UART_NUM_0  // Use UART0
#define UART_BAUD_RATE     115200
#define UART_RX_BUF_SIZE   1024

/* Global Variable for Temperature */
static char current_temp_str[32] = "Waiting..."; 

static EventGroupHandle_t s_wifi_event_group;
#define WIFI_CONNECTED_BIT BIT0
#define WIFI_FAIL_BIT      BIT1
static const char *TAG = "wifi_station";
static int s_retry_num = 0;

// --- UART Task: Listens to RP2040 ---
static void uart_rx_task(void *arg) {
    uart_config_t uart_config = {
        .baud_rate = UART_BAUD_RATE,
        .data_bits = UART_DATA_8_BITS,
        .parity    = UART_PARITY_DISABLE,
        .stop_bits = UART_STOP_BITS_1,
        .flow_ctrl = UART_HW_FLOWCTRL_DISABLE,
        .source_clk = UART_SCLK_DEFAULT,
    };
    uart_param_config(UART_PORT_NUM, &uart_config);
    uart_driver_install(UART_PORT_NUM, UART_RX_BUF_SIZE * 2, 0, 0, NULL, 0);

    uint8_t* data = (uint8_t*) malloc(UART_RX_BUF_SIZE);
    while (1) {
        int len = uart_read_bytes(UART_PORT_NUM, data, UART_RX_BUF_SIZE - 1, 20 / portTICK_PERIOD_MS);
        if (len > 0) {
            data[len] = '\0';
            // Store the received temperature string
            strncpy(current_temp_str, (char*)data, sizeof(current_temp_str)-1);
            ESP_LOGI(TAG, "Received Temp from RP2040: %s", current_temp_str);
        }
    }
}

// --- Web Server Handler ---
esp_err_t hello_get_handler(httpd_req_t *req) {
    char resp_str[1024];
    
    snprintf(resp_str, sizeof(resp_str), 
             "<html>"
             "<head><meta http-equiv=\"refresh\" content=\"2\">"
             "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\"></head>"
             "<body style='font-family: Arial; text-align: center; padding-top: 50px; background-color: #f4f4f4;'>"
             "  <div style='background: white; margin: auto; width: 85%%; padding: 40px; border-radius: 20px; box-shadow: 0px 4px 10px rgba(0,0,0,0.1);'>"
             "    <h1 style='color: #2c3e50;'>Vaman IoT Gateway</h1>"
             "    <h2 style='font-size: 32px; color: #27ae60;'>%s</h2>" // This prints the RP2040 string
             "    <p style='color: #7f8c8d;'>Live UART Stream</p>"
             "  </div>"
             "</body>"
             "</html>",
             current_temp_str); // This variable now contains the full phrase from RP2040

    httpd_send(req, resp_str, strlen(resp_str));
    return ESP_OK;
}

httpd_handle_t start_webserver(void) {
    httpd_config_t config = HTTPD_DEFAULT_CONFIG();
    httpd_handle_t server = NULL;
    if (httpd_start(&server, &config) == ESP_OK) {
        httpd_uri_t hello = {
            .uri       = "/",
            .method    = HTTP_GET,
            .handler   = hello_get_handler,
            .user_ctx  = NULL
        };
        httpd_register_uri_handler(server, &hello);
        return server;
    }
    return NULL;
}

// --- WiFi Event Handler (Standard) ---
static void event_handler(void* arg, esp_event_base_t event_base, int32_t event_id, void* event_data) {
    if (event_base == WIFI_EVENT && event_id == WIFI_EVENT_STA_START) {
        esp_wifi_connect();
    } else if (event_base == WIFI_EVENT && event_id == WIFI_EVENT_STA_DISCONNECTED) {
        if (s_retry_num < EXAMPLE_ESP_MAXIMUM_RETRY) {
            esp_wifi_connect();
            s_retry_num++;
            ESP_LOGI(TAG, "retry to connect to the AP");
        } else {
            xEventGroupSetBits(s_wifi_event_group, WIFI_FAIL_BIT);
        }
    } else if (event_base == IP_EVENT && event_id == IP_EVENT_STA_GOT_IP) {
        ip_event_got_ip_t* event = (ip_event_got_ip_t*) event_data;
        ESP_LOGI(TAG, "got ip:" IPSTR, IP2STR(&event->ip_info.ip));
        s_retry_num = 0;
        xEventGroupSetBits(s_wifi_event_group, WIFI_CONNECTED_BIT);
    }
}

void wifi_init_sta(void) {
    s_wifi_event_group = xEventGroupCreate();
    ESP_ERROR_CHECK(esp_netif_init());
    ESP_ERROR_CHECK(esp_event_loop_create_default());
    esp_netif_create_default_wifi_sta();
    wifi_init_config_t cfg = WIFI_INIT_CONFIG_DEFAULT();
    ESP_ERROR_CHECK(esp_wifi_init(&cfg));
    ESP_ERROR_CHECK(esp_event_handler_instance_register(WIFI_EVENT, ESP_EVENT_ANY_ID, &event_handler, NULL, NULL));
    ESP_ERROR_CHECK(esp_event_handler_instance_register(IP_EVENT, IP_EVENT_STA_GOT_IP, &event_handler, NULL, NULL));

    wifi_config_t wifi_config = {
        .sta = {
            .ssid = EXAMPLE_ESP_WIFI_SSID,
            .password = EXAMPLE_ESP_WIFI_PASS,
        },
    };
    ESP_ERROR_CHECK(esp_wifi_set_mode(WIFI_MODE_STA) );
    ESP_ERROR_CHECK(esp_wifi_set_config(WIFI_IF_STA, &wifi_config) );
    ESP_ERROR_CHECK(esp_wifi_start() );
}

void app_main(void) {
    esp_err_t ret = nvs_flash_init();
    if (ret == ESP_ERR_NVS_NO_FREE_PAGES || ret == ESP_ERR_NVS_NEW_VERSION_FOUND) {
      ESP_ERROR_CHECK(nvs_flash_erase());
      ret = nvs_flash_init();
    }
    ESP_ERROR_CHECK(ret);

    wifi_init_sta();

    // Start UART Task to listen to RP2040
    xTaskCreate(uart_rx_task, "uart_rx_task", 4096, NULL, 10, NULL);

    // Start Web Server
    start_webserver();
}