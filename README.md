# Progetto PotXII

## Interfaccia
- Dashboard NodeRED
- MQTT/Wifi
- Grafico a punti per ogni grandezza misurata
- Istogramma per indicare quante volte in un arco di tempo annaffi la pianta
- Grafico per indicare il livello dell'acqua nel tempo

## Sensori/Componenti da Utilizzare
- Pompa add immersione per acqua
- Sensore ad ultrasuoni
- Sensore per temperatura ed umidità
- Fotoresistore
- SSD1306
- Buzzer
- Led per allarme
- Power supply

## Features
- Start at boot
- Allarme serbatoio vuoto
- Allarme temperatura troppo alta
- Misurazione umidità, luminosità e temperatura
- Analisi delle grandezze misurate
    - In quanto tempo finisce il serbatoio in media?
    - Temperatura media giornaliera
    - Luminosita media giornaliera
    - Umidità media in giornaliera
    - Altre analisi??
- Pulsante di reset
- Irrigazione automatica

## OLED
- Mostrare logo all'accensione
- Mostrare schermata di caricamento durante la connessione al wifi
- Mostrare pagina di default se è tutto ok, con le grandezze misurate ora
- Mostrare errore se manca acqua, se non ci connettiamo al wifi
- Mostrare warning se c'è troppa luce, se l'acqua sta per finire, se la temperatura non è adatta
- Mostrare icona per indicare l'irrigazione in corso della pianta
- Mostrare gli ultimi valori misurati sull'OLED
