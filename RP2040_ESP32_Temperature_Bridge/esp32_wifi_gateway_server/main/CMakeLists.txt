idf_component_register(SRCS "esp32_wifi_gateway_server.c"
                    PRIV_REQUIRES esp_wifi nvs_flash esp_http_server driver
                    INCLUDE_DIRS ".")