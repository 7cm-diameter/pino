if __name__ == '__main__':
    from time import sleep

    from pino.ino import HIGH, LOW, OUTPUT, Arduino, Comport

    com = Comport() \
        .set_port("/dev/ttyACM0") \
        .set_baudrate(115200) \
        .set_timeout(1.) \
        .set_warmup(2.) \
        .deploy() \
        .connect()

    ino = Arduino(com)

    LED_BUILTIN = 13
    ino.set_pinmode(LED_BUILTIN, OUTPUT)

    for _ in range(10):
        ino.digital_write(LED_BUILTIN, HIGH)
        sleep(1)
        ino.digital_write(LED_BUILTIN, LOW)
        sleep(1)

    ino.disconnect()
    com.disconnect()
