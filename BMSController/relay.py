import lgpio
import time


class Relay:
    def __init__(self, pin_num: int) -> None:
        print(f"Relay: using pin={pin_num}")
        self.pin_num = pin_num
        self.gpio_handler = None

    def __enter__(self):
        print("ENTER")
        self.gpio_handler = lgpio.gpiochip_open(0)
        return self

    def __exit__(self, exc_type, exc, tb):
        print("GPIO Cleanup")
        self.off()
        lgpio.gpiochip_close(self.gpio_handler)

    def on(self):
        print("Set ON")
        lgpio.gpio_claim_output(self.gpio_handler, self.pin_num)
        lgpio.gpio_write(self.gpio_handler, self.pin_num, 1)

    def off(self):
        print("Set OFF")
        lgpio.gpio_claim_input(self.gpio_handler, self.pin_num)


if __name__ == "__main__":
    with Relay(pin_num=17) as re:

        while True:
            re.on()
            time.sleep(2)
            re.off()
            time.sleep(2)
