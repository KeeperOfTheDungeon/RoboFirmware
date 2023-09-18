from time import sleep

from machine import Pin
from rp2 import asm_pio, StateMachine, PIO

@asm_pio(set_init=PIO.OUT_LOW)
def asm():
    wrap_target()
    
    wait(1, pin, 0)
    set(pins, 1)
    wait(0, pin, 0)
    set(pins, 0)
    
    wrap()



def main():
    PIO(0).remove_program()
    
    trigger = Pin(1, Pin.OUT)
    sm = StateMachine(0, asm, freq=2000, set_base=Pin(25), in_base=Pin(1))
    sm.active(1)
    
    sleep(1)
    print('Starting program.')
    trigger.value(1)
    print('trigger set')
    sleep(2)
    trigger.value(0)
    sleep(0.125)
    print('trigger done')
    
    sm.active(0)
    

if __name__ == '__main__':
    main()