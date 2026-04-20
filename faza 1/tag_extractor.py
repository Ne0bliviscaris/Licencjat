import json
from collections import Counter

import pandas as pd


def extract_unique_tags():
    # 1. Wczytanie pliku CSV (separator to średnik)
    df = pd.read_csv("2. Dataset oczyszczony.csv", sep=";")
    # df = pd.read_excel("faza 4/4. Dataset gotowy.xlsx")

    # 2. Definicja funkcji obrabiającej specyficzny string z excela
    def parse_tags(tag_str):
        if pd.isna(tag_str):
            return []
        try:
            # Excel czasami dodaje podwójne cudzysłowy i inne dziwne formatowania,
            # zazwyczaj json.loads poradzi sobie po usunięciu nadmiaru, jeśli to standard
            return json.loads(tag_str)
        except Exception:
            return []

    # Odtworzenie list z tekstów
    df["tags_list"] = df["tags"].apply(parse_tags)

    # 3. Zbieranie wszystkich tagów do jednego obiektu iterowalnego i wyliczenie unikalnych
    all_tags = [tag.lower().strip() for sublist in df["tags_list"] for tag in sublist]

    # Zliczanie częstotliwości (przydaje się żeby zobaczyć, które tagi są najważniejsze)
    tags_counted = Counter(all_tags)

    # Sortowane po popularności malejąco
    unique_tags_sorted = sorted(
        tags_counted.keys(), key=lambda x: tags_counted[x], reverse=True
    )

    # 4. Zapis do pliku JSON do przetworzenia przez LLM
    output_data = {"unique_tags": unique_tags_sorted}

    with open("unikalne_tagi.json", "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=4)

    print(f"Zakończono! Znaleziono {len(unique_tags_sorted)} unikalnych tagów.")
    print("Wynik zapisano w pliku 'unikalne_tagi.json'")


if __name__ == "__main__":
    extract_unique_tags()
