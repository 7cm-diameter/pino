if __name__ == '__main__':
    from time import sleep

    from pino.ino import OUTPUT, Comport, Optuino

    com = Comport() \
        .set_port("/dev/ttyACM0") \
        .set_baudrate(115200) \
        .set_timeout(1.) \
        .set_warmup(2.) \
        .deploy() \
        .connect()

    ino = Optuino(com)

    LED_BUILTIN = 13
    ino.set_pinmode(LED_BUILTIN, OUTPUT)

    ino.set_pulse_params(setting_idx=0, freq=5, duration=10)
    ino.set_pulse_params(setting_idx=1, freq=10, duration=10)
    ino.set_pulse_params(setting_idx=2, freq=20, duration=10)

    for setting in ino.pulse_settings:
        print(setting)

    for idx in range(3):
        ino.pulse_on(LED_BUILTIN, idx)
        sleep(2)
        ino.pulse_off()
