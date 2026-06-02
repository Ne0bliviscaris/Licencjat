# 1 Wstęp
Niniejsza praca dotyczy analizy eksploracyjnej datasetu utworzonego na podstawie web scrapingu ofert pracy ze stron inhire.io i theprotocol.it. Poniższa praca ma na celu objaśnienie stanu rynku ofert pracy w branży IT dla osób wchodzących na ten rynek oraz szukających nowej pracy. Zgromadzone dane obejmują informacje dotyczące m.in. poziomu wynagrodzenia, lokalizacja, wymagania technologiczne, charakter pracy oraz inne istotne cechy ofert.

Zbiór danych został poddany oczyszczeniu i transformacji, usunięto w jego ramach kolumny o niepełnych danych lub występujące tylko w jednym ze źródeł. Przeliczono wszystkie stawki na polskie złotówki i dodano stawki godzinowe. Ujednolicono tagi określające wymagane od kandydatów umiejętności oraz znajomość narzędzi.

Z charakteru niniejszej pracy oraz dostępnego zbioru danych wyodrębniono 3 tematy, które zostaną poddane analizie. Głównym celem pracy jest zbadanie zależności pomiędzy poziomem wynagrodzeń oraz dostępnością ofert pracy a wybranymi czynnikami, takimi jak lokalizacja, technologie czy forma zatrudnienia. 


# 2. Podstawy teoretyczno-empiryczne analizy rynku pracy w sektorze IT
## Definicje fundamentalne
### 1. Praca, rynek pracy i ekonomia ofert
W klasycznym ujęciu nauk ekonomicznych pojęcie pracy wiąże się bezpośrednio z celową aktywnością ludzką ukierunkowaną na wytwarzanie dóbr i świadczenie usług. W podręczniku akademickim pod redakcją Romana Milewskiego i Eugeniusza Kwiatkowskiego praca w sensie ekonomicznym definiowana jest następująco:

> „Praca jest to zespół świadomych i celowych czynności człowieka, dzięki którym oddziałuje on na otaczającą go przyrodę, przekształca ją” (Milewski, Kwiatkowski, 2018, s. 21).

Z punktu widzenia analizy statystycznej, aktywność ta podlega wycenie rynkowej w postaci płacy, stając się przedmiotem transakcji na specyficznym rynku, jakim jest rynek pracy. W ujęciu podręcznikowym Davida Begga, Stanleya Fischera oraz Rudigera Dornbuscha, obszar ten definiuje się poprzez konfrontację sił popytu i podaży:

> „Rynek pracy obejmuje całokształt zagadnień związanych z kształtowaniem podaży pracy i popytu na pracę. Na rynku pracy mają miejsce transakcje kupna pracy, czyli angażowania pracowników oraz transakcje sprzedaży pracy” (Begg, Fischer, Dornbusch, 2014, s. 142).  
Z perspektywy metodologii badań statystycznych, fundamentalnym łącznikiem spajającym popytową stronę rynku z potencjalnymi pracobiorcami jest oferta pracy. W ekonomii informacji (tzw. teoria sygnalizacji) oferta pracy jest traktowana jako formalny komunikat wysyłany przez przedsiębiorstwo, który określa brzegowe warunki zakupu usług pracy (Spence, 1973, s. 355). Agregacja tych danych przy użyciu technik analitycznych (takich jak web scraping) pozwala na interpretację realnego, dynamicznego stanu struktur płacowych i wymagań stawianych przez pracodawców.

### 2. Cyfryzacja i ewolucja ogłoszeń rekrutacyjnych: Przeniesienie rynku do sieci internetowej
Tradycyjne mechanizmy dystrybucji ofert pracy (np. ogłoszenia prasowe, pośrednictwo urzędów) charakteryzowały się wysokim poziomem asymetrii informacyjnej oraz generowały znaczne obciążenia ekonomiczne. George J. Stigler w swojej pionierskiej teorii ekonomii informacji wskazywał, że wyszukiwanie informacji na rynku wiąże się z istotnymi nakładami czasu i kapitału, określanymi jako koszty poszukiwania (search costs):

> „Poszukiwanie informacji to zachowanie mające na celu zniwelowanie niewiedzy o rozkładzie cen i ofert rynkowych, przy czym koszty tego procesu są funkcją czasu i liczby przeszukiwanych rynków” (Stigler, 1961, s. 213).

Przeniesienie ofert pracy do internetu doprowadziło do rewolucji strukturalnej – koszty poszukiwania po obu stronach rynku (pracodawcy i kandydata) znacząco się zmniejszyły. Współczesne portale ogłoszeniowe wyspecjalizowane w branży zaawansowanych technologii, takie jak poddane analizie inhire.io oraz theprotocol.it, funkcjonują jako tzw. dwustronne platformy cyfrowe (two-sided markets). Cyfrowy charakter współczesnych ogłoszeń zdeterminował ich nową postać statystyczną:

*   **a. Ustrukturyzowanie i unifikacja:** Ogłoszenia przestały mieć formę narracyjną. Współczesna oferta pracy to zbiór twardych zmiennych kategorycznych (np. tryb pracy: zdalny/hybrydowy) oraz dychotomicznych (zmienne zero-jedynkowe określające obecność lub brak danej technologii), co wprost umożliwia stosowanie modeli statystycznych, takich jak regresja liniowa czy lasy losowe.
*   **b. Transparentność płacowa:** Sektor IT wymusił powszechne stosowanie tzw. „widełek płacowych”. Dla analityka danych oznacza to zastąpienie deklaratywnych danych ankietowych rzeczywistym wymiarem finansowym oferowanym na rynku w danym momencie.

### 3. Uwarunkowania makroekonomiczne: Bezrobocie w okresie badawczym
Poziom absorpcji ofert pracy oraz struktura wynagrodzeń w branży IT pozostają w relacji z ogólną sytuacją makroekonomiczną. W literaturze akademickiej wskaźnik ten jest kluczowym miernikiem równowagi gospodarczej. Paul A. Samuelson oraz William D. Nordhaus definiują stopę bezrobocia jako:

> „Stosunek liczby bezrobotnych do całkowitej liczby siły roboczej, wyrażony w procentach, gdzie siła robocza obejmuje zarówno zatrudnionych, jak i poszukujących pracy” (Samuelson, Nordhaus, 2012, s. 408).

Zbiór danych poddany analizie w niniejszej pracy został zgromadzony w okresie od października do grudnia 2025 roku. Sytuacja na rynku pracy w Polsce w tym okresie charakteryzowała się stabilizacją na bardzo niskim poziomie. Według oficjalnych danych Głównego Urzędu Statystycznego (GUS), stopa bezrobocia rejestrowanego wynosiła:
Październik  oraz Listopad – 5,6 %, Grudzień – 5,7 %

**MIEJSCE NA WYKRES STOPY BEZROBOCIA**

Równolegle, stopa bezrobocia mierzona metodologią reprezentacyjną BAEL (Badanie Aktywności Ekonomicznej Ludności) dla IV kwartału 2025 roku ukształtowała się na poziomie 3,2% (GUS, 2026).

**MIEJSCE NA WYKRES STOPY BEZROBOCIA BAE**
 
#### Trend względem roku poprzedniego
W odniesieniu do analogicznego okresu roku poprzedniego (IV kwartał 2024 roku), w którym stopa bezrobocia według BAEL wynosiła 2,8% (GUS, 2026), odnotowano minimalny trend wzrostowy (o 0,4 punktu procentowego). Pomimo tego nieznacznego wzrostu wskaźnika, rynek pracy w Polsce w okresie badawczym nadal wykazywał strukturalne cechy tzw. rynku pracownika. Niski poziom bezrobocia sprawia, że przedsiębiorstwa z sektora IT zmuszone są elastycznie dopasowywać parametry swoich ofert (stawki płac, wymagania technologiczne) w celu przyciągnięcia specjalistów, co w badaniu empirycznym uzasadnia zastosowanie analizy wariancji ANOVA do badania zróżnicowania płac między grupami.

### 4. Ekonomiczne i behawioralne czynniki wyboru ofert pracy przez kandydatów
Decyzja pracownika o złożeniu aplikacji na określoną ofertę pracy w internecie jest tłumaczona na gruncie ekonomii za pomocą teorii racjonalnego wyboru oraz teorii użyteczności. Jak wskazują Daniel Kahneman i Amos Tversky w teorii perspektywy, jednostki podejmują decyzje w warunkach ryzyka i niepewności rynkowej poprzez maksymalizację subiektywnej funkcji wartości (Kahneman, Tversky, 1979, s. 263). W kontekście ofert pracy w branży IT, czynnikami determinującymi zachowania kandydatów są:

*   **a. Maksymalizacja korzyści finansowych:** Wysokość oferowanego wynagrodzenia w relacji do formy zatrudnienia. Kandydaci szacują opłacalność netto kontraktów B2B (z uwzględnieniem ryzyka gospodarczego i podatku liniowego/ryczałtu) w zestawieniu z ochroną prawną, jaką daje Umowa o Pracę (UoP).
*   **b. Lokalizacja i stopień elastyczności (Tryb pracy):** Przeniesienie rekrutacji do internetu umożliwiło upowszechnienie pracy zdalnej (remote), co zredukowało ograniczenia geograficzne. Możliwość wyboru trybu pracy (zdalna vs hybrydowa vs stacjonarna) jest obecnie jednym z podstawowych kryteriów niefinansowych, bezpośrednio wpływającym na rozkład wariancji płac w modelach statystycznych.
*   **c. Rozwój kapitału ludzkiego (Stack technologiczny):** Pracownicy sektora IT dobierają oferty pod kątem zgodności z posiadanymi kompetencjami oraz perspektywicznością danych technologii (np. Python, chmura AWS). Zbieżność „tagów” z oferty z umiejętnościami kandydata minimalizuje ryzyko utraty wartości jego kapitału ludzkiego na rynku.

Identyfikacja i statystyczny opis powiązań pomiędzy powyższymi czynnikami (widocznymi w ogłoszeniach) a poziomem oferowanych wynagrodzeń stanowi bezpośrednie uzasadnienie dla przeprowadzenia eksploracyjnej analizy danych (EDA) w niniejszej pracy licencjackiej.


# 3. Opis zbioru danych
Zbiór danych zawiera łącznie 18 915 oferty pracy, zebrane z dwóch źródeł: **inhire.io** (4303 oferty) oraz **theprotocol.it** (14 612 ofert). Dane zostały zebrane w okresie od października do grudnia 2025 roku. Każda oferta pracy zawiera informacje takie jak: tytuł stanowiska, lokalizacja, wymagane technologie (tagi), forma zatrudnienia, poziom wynagrodzenia oraz inne istotne cechy. Dane źródłowe zostały poddane procesowi oczyszczania i ujednolicania, w tym przeliczeniu stawek na polskie złotówki oraz na stawki miesięczne. Dodatkowo dokonano mapowania kategorii ofert pracy na ujednoliconą klasyfikację, co umożliwia spójne przetwarzanie i analizę danych z obu źródeł. Szczegółowe informacje dotyczące procesu mapowania kategorii ze stron źródłowych znajdują się w załączniku `zalacznik1_mapowanie_kategorii.md`.

# 4. Metody badawcze
W niniejszej pracy zastosowano zbiór metod badawczych opartych na pełnym cyklu przetwarzania danych – od ich pozyskania, poprzez obróbkę, aż po eksploracyjną analizę (EDA - *Exploratory Data Analysis*). Główne kroki i metody badawcze to:

1. **Gromadzenie danych (Web Scraping)**: Proces zrealizowano przy użyciu autorskich skryptów w języku Python. Zamiast standardowego parsowania struktury HTML, wykorzystano technikę bezpośredniego odpytywania interfejsów API platform ogłoszeniowych (inhire.io oraz theprotocol.it), co zapewniło wyższą jakość i zminimalizowało ryzyko błędów w danych.
2. **Przetwarzanie, czyszczenie i standaryzacja danych (Data Preprocessing)**: Surowe dane zostały poddane wieloetapowemu procesowi czyszczenia (tzw. *Data Wrangling*). Do zastosowanych technik należą:
   - unifikacja walut oraz ujednolicenie okresów rozliczeniowych (sprowadzenie ich m.in. do wymiaru miesięcznego wyrażonego w polskich złotych),
   - mapowanie i kategoryzacja różnorodnych stanowisk do jednego spójnego standardu w celu uzyskania możliwości porównywania danych z wielu portali,
   - zaawansowana obróbka i grupowanie wymagań technologicznych (tagów) poprzez ich uczyszczanie i ujednolicanie (np. `AWS` = `Amazon Web Services`), co pozwoliło na stworzenie spójnego zbioru cech do dalszej analizy.
3. **Eksploracyjna analiza danych (EDA)**: Główna metoda statystyczna użyta w badaniu. Umożliwia identyfikację trendów i zależności w zbiorze. W pracy posłużono się metodami statystyki opisowej (takimi jak wyznaczanie średniej, mediany i percentyli stawek wynagrodzeń). Dokonano grupowania (agregacji) danych względem zadanych wymiarów: doświadczenia (seniority), lokalizacji, formy zatrudnienia i wymaganych technologii.
4. **Wizualizacja danych**: Statystyki, odkryte struktury i wzorce zostały zaprezentowane za pomocą form graficznych (wykresy rozkładów, słupkowe, pudełkowe itp.). Metoda ta pozwala dociekać i rzetelnie formować wnioski z wyabstrahowanych, zagregowanych danych opisujących kondycję i realia panujące na rynku IT.

### 4.1. Uzasadnienie doboru metod statystycznych i algorytmów
Wybór metod analitycznych oraz modeli uczenia maszynowego został podyktowany strukturą zgromadzonego zbioru danych oraz specyfiką celów badawczych pracy:

1. **Uzasadnienie wyboru testu ANOVA (Analiza Wariancji):**
   * **Natura zmiennych:** W badaniu weryfikowany jest wpływ zmiennych kategorycznych, wieloklasowych (takich jak *poziom doświadczenia* o trzech klasach: junior, mid, senior oraz *tryb pracy*: hybrid, remote, stationary) na zmienną ciągłą (*średnie zarobki w PLN*).
   * **Kontrola błędu I rodzaju:** Tradycyjne porównywanie par za pomocą testu t-Studenta przy trzech grupach wymagałoby trzykrotnego powtórzenia procedury, co drastycznie zwiększa prawdopodobieństwo popełnienia błędu pierwszego rodzaju (fałszywego odrzucenia hipotezy zerowej). Test ANOVA bada całą wariancję międzygrupową jednocześnie.
   * **Cel akademicki:** Pozwala on na formalne i jednoznaczne udzielenie odpowiedzi na pytanie, czy obserwowane w analizie eksploracyjnej różnice w średnich zarobkach są dziełem przypadku, czy też stanowią statystycznie istotną prawidłowość na rynku pracy.

2. **Uzasadnienie wyboru Regresji Liniowej:**
   * **Rola modelu bazowego (Baseline):** W metodologii uczenia maszynowego fundamentalną zasadą jest stworzenie prostego punktu odniesienia przed wdrożeniem zaawansowanych algorytmów. Regresja liniowa – jako klasyczny model ekonometryczny – reprezentuje podejście parametryczne, zakładające liniową zależność między cechami oferty a pensją.
   * **Interpretowalność rynkowa:** Pozwala na bezpośrednią ocenę kierunku relacji (wzrost/spadek wynagrodzenia pod wpływem danej cechy).
   * **Wartość diagnostyczna:** Słabsze dopasowanie regresji liniowej stanowi istotny wniosek badawczy. Dowodzi ono, że mechanizmy płacowe w sektorze IT mają charakter silnie nieliniowy (np. premia finansowa za wejście na poziom seniora nie rośnie proporcjonalnie w stosunku do przejścia z poziomu juniora na mid-a).

3. **Uzasadnienie wyboru Lasu Losowego (Random Forest Regressor):**
   * **Kompatybilność z danymi binarnymi (One-Hot Encoded):** Proces inżynierii cech polegał na ekstrakcji słów kluczowych z tekstu ogłoszeń i przekształceniu ich w zmienne zero-jedynkowe (np. *posiada tag python = 1, brak = 0*). Struktura drzewiasta Lasu Losowego naturalnie operuje na takich podziałach, podejmując decyzje w sposób analogiczny do pytań rekrutacyjnych.
   * **Odporność na wartości skrajne (Outliers):** Dane pochodzące ze skrapingu portali pracy bywają zaszumione (np. pomyłki ludzkie w widełkach płacowych). Algorytm Lasu Losowego, dzięki agregacji (uśrednianiu) prognoz z wielu niezależnych drzew decyzyjnych, cechuje się wysoką odpornością na anomalie i zapobiega zaburzeniu wyników przez pojedyncze, nietypowe oferty.
   * **Wychwytywanie interakcji i nieliniowości:** W przeciwieństwie do modeli liniowych, Las Losowy potrafi zidentyfikować tzw. *efekt synergii*. Przykładowo, algorytm dostrzega, że obecność technologii `AWS` generuje znacznie wyższy przyrost płacy u specjalisty typu `Senior` niż u `Juniora`, co odzwierciedla realną złożoność wyceny specjalistów IT.
  
Bibliografia
Rozdział 1
1.	Begg, D., Fischer, S., Dornbusch, R. (2014). Ekonomia: Makroekonomia. Warszawa: Polskie Wydawnictwo Ekonomiczne, s. 142.
2.	Główny Urząd Statystyczny (2026). Komunikat Prezesa Głównego Urzędu Statystycznego z dnia 24 lutego 2026 r. w sprawie stopy bezrobocia w IV kwartale 2025 r. Warszawa: GUS.
3.	Kahneman, D., Tversky, A. (1979). Prospect Theory: An Analysis of Decision under Risk. Econometrica, 47(2), s. 263-291.
4.	Milewski, R., Kwiatkowski, E. (red.). (2018). Podstawy ekonomii. Warszawa: Wydawnictwo Naukowe PWN, s. 21.
5.	Samuelson, P. A., Nordhaus, W. D. (2012). Ekonomia. Warszawa: Wydawnictwo Naukowe PWN, s. 408.
6.	Spence, M. (1973). Job Market Signaling. The Quarterly Journal of Economics, 87(3), s. 355-374.
7.	Stigler, G. J. (1961). The Economics of Information. Journal of Political Economy, 69(3), s. 213-225.