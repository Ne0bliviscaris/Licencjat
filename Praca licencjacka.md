# 1 Wstęp
Niniejsza praca dotyczy analizy eksploracyjnej datasetu utworzonego na podstawie web scrapingu ofert pracy ze stron inhire.io i theprotocol.it. Poniższa praca ma na celu objaśnienie stanu rynku ofert pracy w branży IT dla osób wchodzących na ten rynek oraz szukających nowej pracy. Zgromadzone dane obejmują informacje dotyczące m.in. poziomu wynagrodzenia, lokalizacja, wymagania technologiczne, charakter pracy oraz inne istotne cechy ofert.

Zbiór danych został poddany oczyszczeniu i transformacji, usunięto w jego ramach kolumny o niepełnych danych lub występujące tylko w jednym ze źródeł. Przeliczono wszystkie stawki na polskie złotówki i dodano stawki godzinowe. Ujednolicono tagi określające wymagane od kandydatów umiejętności oraz znajomość narzędzi.

Z charakteru niniejszej pracy oraz dostępnego zbioru danych wyodrębniono 3 tematy, które zostaną poddane analizie. Głównym celem pracy jest zbadanie zależności pomiędzy poziomem wynagrodzeń oraz dostępnością ofert pracy a wybranymi czynnikami, takimi jak lokalizacja, technologie czy forma zatrudnienia. 


# 2. Opis zbioru danych
Dane zostały pozyskane przy użyciu autorskich skryptów web scrapingowych.Zamiast standardowego parsowania struktury HTML, wykorzystano technikę bezpośredniego odpytywania interfejsów API (API Scraping) platform ogłoszeniowych (inhire.io oraz theprotocol.it), co zapewniło wyższą rzetelność i zminimalizowało ryzyko braków w danych.
Zbiór danych zawiera łącznie 18 915 oferty pracy, zebrane z dwóch źródeł: inhire.io (4303 oferty) oraz theprotocol.it (14 612 ofert). Dane zostały zebrane w okresie od października do grudnia 2025 roku. Każda oferta pracy zawiera informacje takie jak: tytuł stanowiska, lokalizacja, wymagane technologie (tagi), forma zatrudnienia, poziom wynagrodzenia oraz inne istotne cechy. Dane źródłowe zostały poddane procesowi oczyszczania i ujednolicania, w tym przeliczeniu stawek na polskie złotówki oraz na stawki miesięczne. Dodatkowo dokonano mapowania kategorii ofert pracy na ujednoliconą klasyfikację, co umożliwia spójne przetwarzanie i analizę danych z obu źródeł. Szczegółowe informacje dotyczące procesu mapowania kategorii ze stron źródłowych znajdują się w załączniku `zalacznik1_mapowanie_kategorii.md`.

# 3. Metody badawcze
W niniejszej pracy zastosowano zbiór metod badawczych opartych na pełnym cyklu przetwarzania danych – od ich pozyskania, poprzez obróbkę, aż po eksploracyjną analizę (EDA - *Exploratory Data Analysis*). Główne kroki i metody badawcze to:

1. **Gromadzenie danych (Web Scraping)**: Proces zrealizowano przy użyciu autorskich skryptów w języku Python. Zamiast standardowego parsowania struktury HTML, wykorzystano technikę bezpośredniego odpytywania interfejsów API (API Scraping) platform ogłoszeniowych (inhire.io oraz theprotocol.it), co zapewniło wyższą rzetelność i zminimalizowało ryzyko braków w danych.
2. **Przetwarzanie, czyszczenie i standaryzacja danych (Data Preprocessing)**: Surowe dane zostały poddane wieloetapowemu procesowi czyszczenia (tzw. *Data Wrangling*). Do zastosowanych technik należą:
   - unifikacja walut oraz ujednolicenie okresów rozliczeniowych (sprowadzenie ich m.in. do wymiaru miesięcznego wyrażonego w polskich złotych),
   - mapowanie i kategoryzacja różnorodnych stanowisk do jednego spójnego standardu w celu uzyskania możliwości porównywania danych z wielu portali,
   - zaawansowana obróbka i grupowanie wymagań technologicznych (tagów) poprzez ich oczyszczanie oraz przypinanie synonimów w używanych zbiorach JSON.
3. **Eksploracyjna analiza danych (EDA)**: Główna metoda statystyczna użyta w badaniu. Umożliwia identyfikację trendów i zależności w zbiorze. W pracy posłużono się metodami statystyki opisowej (takimi jak wyznaczanie średniej, mediany i percentyli stawek wynagrodzeń). Dokonano grupowania (agregacji) danych względem zadanych wymiarów: doświadczenia (seniority), lokalizacji, formy zatrudnienia i wymaganych technologii.
4. **Wizualizacja danych**: Statystyki, odkryte struktury i wzorce zostały zaprezentowane za pomocą form graficznych (wykresy rozkładów, słupkowe, pudełkowe itp.). Metoda ta pozwala dociekać i rzetelnie formować wnioski z wyabstrahowanych, zagregowanych danych opisujących kondycję i realia panujące na rynku IT.


# 15. UZASADNIENIE DOBORU METOD STATYSTYCZNYCH I ALGORYTMÓW
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