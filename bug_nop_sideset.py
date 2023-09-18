from time import sleep

from machine import Pin
from rp2 import asm_pio, StateMachine, PIO

@asm_pio(sideset_init=PIO.OUT_LOW)
def asm():
    wrap_target()
    
    nop()	.side(1)
    nop()	.delay(7)
    nop()	.delay(7)
    nop()	.delay(7)
    nop()	.delay(7)
    nop()	.delay(7)
    nop()	.delay(7)
    nop()	.delay(7)
    nop()	.delay(7)
    nop()	.side(0)
    nop()	.delay(7)
    nop()	.delay(7)
    nop()	.delay(7)
    nop()	.delay(7)
    nop()	.delay(7)
    nop()	.delay(7)
    nop()	.delay(7)
    nop()	.delay(7)
    
    wrap()



def main():
    PIO(0).remove_program()
    
    sm = StateMachine(0, asm, freq=2000, sideset_base=Pin(25))
    sm.active(1)
    
    sleep(5)
    
    sm.active(0)
    
    print('end')
    

if __name__ == '__main__':
    main()
