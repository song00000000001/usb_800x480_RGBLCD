set(src_dirs
            LED
            LCD
            MYIIC
            ES8388
            MYI2S
            XL9555)

set(include_dirs
            LED
            LCD
            MYIIC
            ES8388
            MYI2S
            XL9555)

set(requires
            driver
            esp_lcd
            esp_common
            esp_driver_gpio
            esp_driver_i2s
            esp_driver_i2c
            esp_mm
)

idf_component_register(SRC_DIRS ${src_dirs} INCLUDE_DIRS ${include_dirs} REQUIRES ${requires})

component_compile_options(-ffast-math -O3 -Wno-error=format=-Wno-format)