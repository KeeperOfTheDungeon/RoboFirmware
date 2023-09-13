from machine import Pin
from time import sleep
import rp2

# clear programs form pio for clean restart
rp2.PIO(0).remove_program()
rp2.PIO(1).remove_program()


@rp2.asm_pio()
def tx_finder():
    wrap_target()
    
    jmp(pin, 'high_voltage')
    
    # pin default to low voltage
    label('low_voltage')
    jmp(pin, 'end')
    jmp('low_voltage')
    
    
    # pin standard to high voltage
    label('high_voltage')
    jmp(pin, 'high_voltage')
    
    label('end')
    irq(rel(0))
    
    wrap()
    
sm_0 = rp2.StateMachine(0, tx_finder, freq=10000, in_base=Pin(0))
sm_1 = rp2.StateMachine(1, tx_finder, freq=10000, in_base=Pin(1))

sm_0.irq(lambda x: {print('Pin 0 is recieving')})
sm_1.irq(lambda x: {print('Pin 1 is recieving')})

sm_0.active(1)
sm_1.active(1)

sleep(7)

sm_1.active(0)
sm_0.active(0)