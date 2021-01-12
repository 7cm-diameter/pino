if __name__ == '__main__':
    from time import sleep

    from pino.ino import HIGH, LOW, OUTPUT, Arduino, Comport

    com1 = Comport() \
        .set_port("/dev/ttyACM0") \
        .set_baudrate(115200) \
        .set_timeout(1.) \
        .set_warmup(2.) \
        .deploy() \
        .connect()

    com2 = Comport() \
        .set_port("/dev/ttyACM1") \
        .set_baudrate(115200) \
        .set_timeout(1.) \
        .set_warmup(2.) \
        .deploy() \
        .connect()

    ino1 = Arduino(com1)
    ino2 = Arduino(com2)

    LED_BUILTIN = 13

    ino1.set_pinmode(LED_BUILTIN, OUTPUT)
    ino2.set_pinmode(LED_BUILTIN, OUTPUT)

    for _ in range(10):
        ino1.digital_write(LED_BUILTIN, HIGH)
        ino2.digital_write(LED_BUILTIN, LOW)
        sleep(1)
        ino1.digital_write(LED_BUILTIN, LOW)
        ino2.digital_write(LED_BUILTIN, HIGH)
        sleep(1)

    ino2.digital_write(LED_BUILTIN, LOW)
