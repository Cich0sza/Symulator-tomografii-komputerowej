# Symulator tomografii komputerowej
Implementacja aplikacji symulującej działanie tomografu komputerowego (symulacja
dwuwymiarowa). Przykład: https://www.youtube.com/watch?v=tgNP-n2z3po

## Użyte algorytmy:
  - transformacja Radona
  - odwrotna transformacja Radona
  - filtr RAMP
  - algorytm Bresenhama
  
## Wejściowy format obrazu: 
Obraz kwadratowy. Zakładamy, że badany obiekt w
całości znajduje się w okręgu wpisanym w kwadrat wyznaczony przez granice obrazu.
Pracujemy tylko na obrazach o czarno-białej (w odcieniach szarości) palecie barw. Ale nie
binarnej. Każdy piksel może mieć dowolny kolor szarości z zakresu 0-255 (przynajmniej).

## Parametry
Układ emiterów: równoległy
Możliwość konfiguracji:
  - ilość emiterów/detektorów
  - krok Δα układu emiter/detektor
  - rozpiętość układu emiter/detektor
