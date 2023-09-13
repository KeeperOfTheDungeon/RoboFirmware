from time import sleep
from _thread import allocate_lock

from machine import Pin
from rp2 import asm_pio, PIO, StateMachine

@asm_pio(set_init=PIO.OUT_LOW)
def noblock():
    irq(block, rel(0))
    
    wrap_target()
    set(pins, 1)[31]
    nop()[31]
    nop()[31]
    nop()[31]
    nop()[31]
    set(pins, 0)[31]
    nop()[31]
    nop()[31]
    nop()[31]
    nop()[31]
    wrap()
    

def callback(anyLock):
    if not anyLock.locked():
        anyLock.acquire()
        input('Press anykey and enter to continue.')
        anyLock.release()
    else:
        pass
    

def main():
    PIO(0).remove_program()
    myLock = allocate_lock()
    sm = StateMachine(0, noblock, freq=2000, set_base=Pin(25))
    sm.irq(callback, myLock)

    sm.active(1)
    sleep(5.125)
    sm.active(0)

if __name__ == '__main__':
    main()
