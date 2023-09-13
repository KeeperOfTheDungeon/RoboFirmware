# Problems

Interrupts behave weird. An unrelative index has been behaving as an relative index,
when using a callback on the state machine (not the pio) from the main thread.

Iterrupt not thrown in case of error. Following messages are corrupted (only ones).
No reset possible.


The commands wait and irq take 'pin' not 'pins' as an argument.

The command wait takes 'pins' instead of 'pin' suggested by the documentation.

The end bit problem was solved by adding a wait for the clock signal to go to zero again.

The state machines can keep running as long as the micro controller is connected to a power source, thats why interrupts can be continuisly triggered.



The end bit is send if the message contains zeros in the more significant bits, since it keeps sending the most significant bit if not told otherwise
