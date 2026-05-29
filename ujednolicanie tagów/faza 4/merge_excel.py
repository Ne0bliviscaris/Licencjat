import os

import pandas as pd


def main():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    xlsx_path = os.path.join(base_dir, "faza 1", "2. Dataset oczyszczony.xlsx")
    csv_path = os.path.join(base_dir, "faza 3", "3. Dataset zunifikowany.csv")
    output_path = os.path.join(base_dir, "faza 4", "4. Dataset gotowy.xlsx")

    print("Wczytywanie pliku Excel...")
    df_excel = pd.read_excel(xlsx_path)

    print("Wczytywanie pliku CSV z nowymi tagami...")
    df_csv = pd.read_csv(csv_path, sep=";")

    # Tworzymy mapowanie ID -> Tagi z CSV
    # Pozwoli to uniknąć duplikatów kolumn po merge() i bezpiecznie podmienić wartość
    tags_mapping = dict(zip(df_csv["id"], df_csv["tags"]))

    print("Podmienianie tagów...")
    # Aktualizowanie kolumny 'tags' na podstawie mapowania z CSV
    # Dla ID, których nie ma w CSV, zachowujemy oryginalne tagi
    df_excel["tags"] = df_excel["id"].map(tags_mapping).fillna(df_excel["tags"])

    print("Zapisywanie wynikowego pliku Excel...")
    df_excel.to_excel(output_path, index=False)

    print(f"\nGotowe! Połączono pliki i zapisano wynik jako: '{output_path}'")


if __name__ == "__main__":
    main()
