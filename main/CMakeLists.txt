idf_component_register(
    SRC_DIRS
        "."
        "APP"
        "UAC"
    INCLUDE_DIRS
        "."
        "APP"
        "UAC"
    REQUIRES)

idf_component_get_property(tusb_lib leeebo__tinyusb_src COMPONENT_LIB)
# target_link_libraries(${tusb_lib} PRIVATE "usb_device")
# target_include_directories(${tusb_lib} PUBLIC "usb_device" "uac")
target_link_libraries(${tusb_lib} PRIVATE ${COMPONENT_LIB})

# target_include_directories(${tusb_lib} PUBLIC "${COMPONENT_DIR}/usb_device")
# target_sources(${tusb_lib} PUBLIC "${COMPONENT_DIR}/usb_device/usb_descriptors.c")