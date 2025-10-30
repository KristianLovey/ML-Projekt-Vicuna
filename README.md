# ML-Projekt-Vicuna
Ovaj projekt izrađen je kao dio selekcijskog zadatka za Vicuna d.o.o. Cilj je bio razviti model koji na temelju povijesnih satnih podataka o cijeni Bitcoina predviđa budući smjer kretanja cijene pomoću tehničkih indikatora i algoritama strojnog učenja. Prema tome pitanje koje ćemo riješavati ovim modelom glasi: "Može li se pomoću prediktivnog modela na temelju povijesnih podataka predvidjeti vrijednost budućih cijena?"

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

1. Što ste odlučili napraviti sa null vrijednostima i zašto? 

Nakon učitavanja podataka morali smo ukloniti null vrijednosti jer radimo sa podacima u vremenskoj seriji raspoređenim po satima. Zbog toga serija mora biti potpuna te su zbog korištenja značajki nastali navedeni null podaci. Te smo vrijednosti uklonili kao i duplikate i neželjene vrijednosti.

2. Koje feature-e ste kreirali i zašto? Jeste li testirali njihovu informativnost? 

Sve koje je Vicuna tim predložio. Informativnost značajki smo provjeravali vizualno (korelacijske matrice i grafove) i promatranjem koliko pojedine značajke variraju s cijenom.
Neke značajke su pokazale jaku korelaciju s trendom cijene, dok su vremenske značajke imale manju, ali stabilnu informativnost.

3. Ako ste izrađivali vizualizaciju, opišite zašto ste to radili i kako vam je to doprinijelo razumijevanju podataka. 

Vizualizaciju smo radili kako bismo stekli uvid u osnovna svojstva vremenske serije i odnose između značajki.
Prikazali smo linijske grafove cijene (Close) i volumena (Volume) kako bismo vidjeli trendove i volatilnost kroz vrijeme. Također smo prikazali korelacijsku matricu između značajki kako bismo uočili međusobne odnose.
Vizualna analiza nam je pomogla da razumijemo sezonalne obrasce (npr. razlike po danima u tjednu) i prepoznamo periode povećane aktivnosti tržišta.

4. Koju metodu unakrsne validacije ste koristili? Kako ste pripremili skup podataka za sljedeći korak?

Nismo koristili unakrsnu validaciju nego smo podatke podijelili vremenski, prvih 80% se koristi za treniranje, a preostalih 20% za testiranje modela. Time smo osigurali da model uči samo iz prošlih podataka i da se evaluira na kasnijem razdoblju.


## 2. Modeliranje i evaluacija
Nakon što smo bili zadovoljni kvalitetom i reprezentativnošću skupa podataka, pristupili smo izradi i pripremi modela strojnog učenja za predviđanje budućih promjena cijene Bitcoina. Cilj modela nije bio savršeno predvidjeti apsolutnu vrijednost cijene, već smjer promjene (rast ili pad) na osnovi razvijenih tehničkih značajki.

U obzir smo uzeli više vrsta modela (linearne, stabla odluke, klasifikacijske i neuronske mreže), no fokusirali smo se na klasifikacijski pristup zbog prirode ciljne varijable.

1. Jeste li koristili regresijski ili klasifikacijski model? 

    Koristili smo klasifikacijski model. Model je treniran da predvidi binarni ishod — hoće li se cijena u sljedećem satu povećati ili smanjiti (1 = rast, 0 = pad). Takav pristup bolje odgovara problemu trgovinskog odlučivanja (kupiti ili prodati) nego predviđanje same numeričke vrijednosti.

2. Koju ste ciljnu varijablu koristili? 

    Ciljna varijabla bila je target_cls, definirana kao:

        target_cls = 
        - 1 → ako je logaritamski povrat veći od +0.1 %
        - 0 → ako je manji od -0.1 %
        - NaN → ako je promjena između -0.1 % i +0.1 %

    Na ovaj način izbacili smo slučajeve u kojima se cijena gotovo nije promijenila, čime smo smanjili šum u podacima.

3. Koje ste modele isprobali i koji se pokazao najboljim? 

    Ispitali smo nekoliko modela:
    • Logističku regresiju (kao jednostavnu baznu varijantu)
    • Random Forest, koji kombinira više stabala odluke
    • Linearne regresijske pristupe za usporedbu

    Najbolje se pokazao Random Forest, jer može uhvatiti nelinearne odnose između značajki i ne pati od problema koje linearni modeli imaju kad su podaci kompleksni. Osim toga, stabilan je i ne traži kompliciranu pripremu podataka.

4. Kako ste procjenjivali performanse? 

    Performanse modela smo procjenjivali pomoću točnosti pogodaka (HIT rate) – koliko puta model točno predvidi smjer kretanja cijene. Podatke smo podijelili vremenski: prvih 80 % koristili smo za treniranje, a zadnjih 20 % za testiranje. Tako smo osigurali da model uči samo iz prošlosti i da se testira na budućem razdoblju. Kako bismo dodatno provjerili stabilnost, napravili smo i rolling evaluaciju – model smo pomicali kroz više vremenskih prozora i gledali kako mu se točnost mijenja kroz vrijeme. Prosječna točnost bila je oko 0.52, što znači da model ima malu, ali stvarnu prednost u odnosu na slučajno pogađanje (0.50).

5. Kako biste znali da vaš model nije samo overfit na povijest? 

    Da bismo izbjegli overfitting, pazili smo da se model nikada ne trenira i testira na istim vremenskim periodima.
    Koristili smo vremenski odvojene skupove i testirali ga samo na budućim podacima.
    Također, sve značajke (poput RSI-a, SMA-a, MACD-a i volatilnosti) izračunavali smo samo iz prošlih vrijednosti, tako da model ne može “vidjeti u budućnost”. Osim toga, rezultat nije previsok, što je zapravo dobar znak jer pokazuje da model ne pamti povijest nego stvarno generalizira obrasce iz podataka.

6. Kako biste primijenili model u realnom vremenu (on-line predikcija)?

    Model se lako može koristiti u realnom vremenu. Zamišljamo to tako da svakih sat vremena stigne novi podatak o cijeni, iz njega se izračunaju svi tehnički indikatori, i onda se ti podaci pošalju kroz model. Model vraća 0 ako očekuje pad ili 1 ako očekuje rast. Cijeli proces je automatiziran kroz Pipeline, koji samostalno radi imputaciju, skaliranje i predikciju. Trenirani model spremili smo pomoću joblib, tako da ga kasnije možemo jednostavno učitati i koristiti u API-ju.

        import joblib
        joblib.dump(pipe, "btc_direction_model_docker.pkl")

        model = joblib.load("btc_direction_model_docker.pkl")
        pred = model.predict(new_data)

Zaključno, model se pokazao kao solidan temelj za razumijevanje odnosa između tehničkih indikatora i promjena cijene. Iako ne daje visoku točnost, uspješno prepoznaje obrasce i može se nadograđivati složenijim metodama poput neuronskih mreža ili kombiniranih modela.

## 3. Izgradnja i kontejnerizacija API-a

Nakon što smo trenirali i spremili model (btc_direction_model_docker.pkl), izradili smo REST API koji omogućuje predikciju smjera kretanja cijene Bitcoina u stvarnom vremenu. API je implementiran pomoću FastAPI frameworka i pokreće se unutar Docker kontejnera, čime se postiže jednostavno pokretanje i prenosivost između sustava.

API ima dvije pristupne točke (endpointa):
    • GET /info – vraća osnovne informacije o modelu i njegovoj namjeni
    • POST /predict – prima nove OHLCTV podatke i vraća predviđeni smjer cijene (0 = pad, 1 = rast)

1. U kojem formatu vaš API prima podatke?

    API prima podatke u JSON formatu, u obliku:

            {
            "Open": 26800.5,
            "High": 26920.1,
            "Low": 26750.0,
            "Close": 26890.7,
            "Trades": 1254,
            "Volume": 512.6
            }

    API zatim iz tih vrijednosti računa tehničke indikatore koje je model koristio tijekom treniranja (npr. omjere cijena, momentum, vrijeme u danu, RSI i dr.) te model vraća predikciju (npr. {"prediction": 1}).

2. Što se događa ako korisnik pošalje neispravne ili nepotpune podatke?

    Ako korisnik pošalje neispravan JSON ili mu nedostaju obavezna polja (Open, High, Low, Close, Trades, Volume), FastAPI automatski vraća HTTP grešku "400 – Bad Request" s detaljnim opisom problema (npr. koji parametar nedostaje ili nije u očekivanom formatu).
    Ovaj mehanizam dolazi ugrađen u Pydantic model koji validira sve ulazne podatke.

3. Kako ste integrirali model unutar kontejnera?

    Model je spremljen pomoću biblioteke joblib, a u Docker kontejneru ga učitavamo u trenutku pokretanja aplikacije. Struktura direktorija unutar kontejnera. U Dockerfileu definirali smo instalaciju svih potrebnih Python paketa i naredbu za pokretanje API-ja. Model i kod se zajedno kopiraju u /app direktorij, a FastAPI se pokreće unutar kontejnera pomoću Uvicorna.

4. Koje su prednosti Docker-izacije?

    Docker omogućuje da se cijela aplikacija (uključujući model, ovisnosti i Python okruženje) pokrene bilo gdje, bez potrebe za ponovnom instalacijom paketa ili konfiguracijom sustava.
    Prednosti:
        • Jednostavno pokretanje: jedan docker run pokreće sve.
        • Prenosivost: radi identično na Windows, Linux i macOS sustavima.
        • Izolacija: Python paketi i ovisnosti su odvojeni od glavnog sustava.
        • Reproducibilnost: svatko tko preuzme Docker image dobit će identične rezultate modela.


### Pokretanje API-ja

Za pokretanje lokalno:
        uvicorn app:app --reload

Za pokretanje unutar Dockera:
        docker build -t btc_api .
        docker run -p 8000:8000 btc_api
API će biti dostupan na http://127.0.0.1:8000/docs

U slučaju potencijalnih nepravilnosti kod korištenja pip komande u folderu se takošer nalazi lokalna datoteka za preuzimanje pipa.

Projekt pokazuje kako se na temelju povijesnih financijskih podataka i tehničkih indikatora može razviti prediktivni model za smjer kretanja cijene Bitcoina.
Model, iako jednostavan, može poslužiti kao temelj za složenije pristupe (npr. neuronske mreže ili kombinirane sustave).
API i Docker omogućuju jednostavno pokretanje modela i daljnju integraciju u aplikacije u stvarnom vremenu.
