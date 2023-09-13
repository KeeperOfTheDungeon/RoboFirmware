from rp2 import PIO, asm_pio, StateMachine
from machine import Pin
from time import sleep
#from decorators import own_decorator
from micropython import const

SPECIAL_PIN = const(0)

@asm_pio()
def waiter():
    wrap_target()
    wait(0, pins, SPECIAL_PIN)
    irq(block, rel(0))
    wrap()
    

def main() -> None:
    PIO(0).remove_program()
    Pin(0, Pin.IN, Pin.PULL_UP)
    print(help(waiter))
    sm = StateMachine(0, waiter, freq=10000)
    sm.irq(lambda x: {print('button pushed')})
    sm.active(1)
    sleep(4)
    sm.active(0)

if __name__ == '__main__':
    main()
