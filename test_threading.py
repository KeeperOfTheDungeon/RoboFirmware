from utime import sleep
from _thread import start_new_thread
from rp2 import StateMachine, asm_pio, PIO
from machine import Pin


@asm_pio(set_init=PIO.OUT_LOW)
def blinker():
    wrap_target()

    wait(1, pins, 25)
    set(pins, 1)
    set(x, 7)
    in_(x, 8)
    push()
    wait(0, pins, 25)
    set(pins, 0)
    set(x, 0)
    in_(x, 8)
    push()
    
    wrap()

def thread_func():
    sm = StateMachine(0, blinker, freq=1000000, set_base=Pin(0))
    sm.active(1)
    while True:
        x = sm.get()
        print(x)

def main() -> None:
    start_new_thread(thread_func, ())
    led = Pin(25, Pin.OUT)
    while True:
        #led.value(1)
        print('HI')
        sleep(1.25)
        #led.value(0)
        print('HI')
        sleep(1.25)


if __name__ == '__main__':
    main()
