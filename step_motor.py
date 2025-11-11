import utime
from machine import Pin

class StepMotor:
    def __init__(self, pin_id1, pin_id2, pin_id3, pin_id4):
        self.IN1 = Pin(pin_id1, Pin.OUT)
        self.IN2 = Pin(pin_id2, Pin.OUT)
        self.IN3 = Pin(pin_id3, Pin.OUT)
        self.IN4 = Pin(pin_id4, Pin.OUT)

        self.step_index = 0
        self._stepper_pins = [self.IN1, self.IN2, self.IN3, self.IN4]


        # full-step con 2 bobbine attive per ogni step
        # due bobbine accese per ogni step -> più coppia
        #il valore (0=spento, 1=acceso) da dare a quel pin nel passo corrente.
        self._step_sequence = [
            [1, 0, 0, 1], 
            [1, 1, 0, 0], 
            [0, 1, 1, 0], 
            [0, 0, 1, 1], 
        ]
        
        #la half-step corrispondente (8 stati) è questa:
        # Half-step (mezzo passo): alterna 1 bobina e 2 bobine
        self._step_sequence_half = [
            [1,0,0,0],
            [1,0,0,1],
            [0,0,0,1],
            [0,0,1,1],
            [0,0,1,0],
            [0,1,1,0],
            [0,1,0,0],
            [1,1,0,0],
        ]


    #direction = +1 (antiorario), -1 (orario)
    #steps = numero di passi da eseguire. max 2048
    #delay = tempo tra un passo e l'altro. tra 0.1, 0.01 e 0.005
    #step_index tiene traccia della posizione corrente nella sequenza di attivazione (fase) del motore.
    
    def step(self, direction, steps, delay):
        step_sequence = self._step_sequence
        stepper_pins = self._stepper_pins
        step_index = self.step_index

        for i in range(steps):
            # l'operatore % garantisce che step_index rimanga all'interno dell'intervallo valido (in questo caso [0-3]),
            # assicurando che la sequenza dei passi venga ripetuta ciclicamente.
            # indica la riga quindi quale passo
            step_index = (step_index + direction) % len(step_sequence) # se la sequenza ha 4 stati è come fare mod 4
    
            #pin_index determina la colonna (quindi la bobbina)
            for pin_index in range(len(stepper_pins)):
                #Esempio: se step_index = 2, la sequenza è [0, 1, 1, 0]
                # Se pin_index = 0 → pin_value = 0
                # Se pin_index = 1 → pin_value = 1
                # Se pin_index = 2 → pin_value = 1
                # Se pin_index = 3 → pin_value = 0
                pin_value = step_sequence[step_index][pin_index]
                #Scrive il valore sul pin fisico, accendendo o spegnendo la bobina
                stepper_pins[pin_index].value(pin_value)
    
            #Aspetta il tempo delay prima di passare al prossimo passo.
            #Pausa più corta → motore più veloce. Pausa più lunga → motore più lento.
            utime.sleep(delay)
