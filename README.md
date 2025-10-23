# ML-Projekt-Vicuna
Selekcijski projekt za posao u Vicuna d.o.o. Projekt izvodi prediktivni model koji na temelju povijesnih podataka predviđa sljedeću vrijednost cijene (ili povrata). Prema tome pitanje koje ćemo riješavati ovim modelom glasi: "Može li se pomoću prediktivnog modela na temelju povijesnih podataka predvidjeti vrijednost budućih cijena?"

Projekt ćemo provesti u nekoliko segmenata: "Analiza i priprema podataka", "Modeliranje i evaluacija" te "Izgradnja i kontejnerizacija API-a".

## 1. Analiza i priprema podataka
Prvi korak bio je dobavljanje podataka iz dataseta kojeg smo dobili od firme. Nakon preuzimanja dataseta i analize podataka ustanovili smo da su dani podaci raspoređeni po stupcima; Date, Open, High, Low, Close, Trades, Volume:

    1. Date - Datum  koji  označava sat  u kojem su izmjereni podaci. 
    2. Open - Početna cijena sata 
    3. High - Najviša cijena sata 
    4. Low - Najniža cijena sata 
    5. Close - Završna cijena sata 
    6. Trades - Ukupan broj transakcija u satu 
    7. Volume - Ukupan broj trade-anih jedinica instrumenta u satu

Nakon toga moramo sirove podatke ("raw") pretvoriti u informativnije varijable pomoću kojih ćemo trenirati model strojnog učenja. Da bismo to napravili moramo iz njih izvesti nove značajke:

    • Lagged returns: npr. return_t-1, return_t-5, return_t-10 
    • Volatilnost: standardna devijacija povrata kroz prozor od n dana 
    • Moving averages: SMA(5), SMA(20), EMA(10) 
    • Volume indicators: omjer trenutnog volumena i prosječnog volumena zadnjih 10 dana 
    • Price ratios: High/Low, Close/Open 
    • Momentum: razlika Close_t - Close_t-5 
    • RSI, MACD, Bollinger bands (ako žele uključiti tehničke indikatore) 
    • Time-based features: dan u tjednu, mjesec, sezonski efekti 

Time ćemo moći prepoznati uzorke, rizik, brzinu promijene, volumen trgovanja te ponavljanje uzoraka kroz vrijeme. Nakon što smo napravili sve značajke morat ćemo testirati sve i spremiti dobivene podatke jednom kada budemo zadovoljni s njima.

## 2. Modeliranje i evaluacija

## 3. Izgradnja i kontejnerizacija API-a
