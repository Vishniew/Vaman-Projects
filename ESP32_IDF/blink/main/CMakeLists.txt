# idf_component_register(SRCS "blink_example_main.c"
#                        INCLUDE_DIRS ".")

idf_component_register(SRCS "blink_example_main.c"
                    INCLUDE_DIRS "."
                    REQUIRES driver)
