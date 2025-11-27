1. Il Circuito di Potenza (Batteria e Pompa)
Questo è il circuito che fa girare effettivamente l'acqua. Qui passa la corrente alta.

Usa le 3 viti (morsetti) del relè. Ignora "NC" (Normally Closed), useremo "NO" (Normally Open) perché vuoi che la pompa stia spenta finché non dai il comando.

    Batteria (+) [Positivo]: Collegalo al morsetto centrale COM del relè.

    Relè NO [Normally Open]: Collega qui il filo ROSSO del motore.

    Batteria (-) [Negativo]: Collega qui direttamente il filo NERO del motore.

Cosa succede fisicamente: La corrente parte dalla batteria, arriva al morsetto COM, si ferma perché l'interruttore è aperto. Quando il relè scatta, il contatto si chiude verso NO, la corrente fluisce nel filo rosso, attraversa il motore e torna alla batteria col filo nero.

2. Il Circuito di Controllo (I 3 Pin)

Qui è dove rischi di fare danni se non sai cosa stai facendo. Questi tre pin servono per dire al relè "accenditi".

    VCC: Qui devi dare l'alimentazione per la bobina del relè.

        Attenzione: Leggi cosa c'è scritto sul relè (es. 5V o 12V). Se il relè è da 5V e gli dai 12V dalla batteria della pompa, lo bruci. Se il relè è da 12V e la batteria è da 12V, puoi collegarlo al positivo della batteria.

    GND: Va al negativo (Ground) della batteria o del microcontrollore.

    IN: Questo è il segnale. Per accendere la pompa, questo pin deve ricevere un segnale (solitamente 5V o 3.3V se usi Arduino, oppure collegato a GND o VCC a seconda se il relè è "Low Trigger" o "High Trigger").
