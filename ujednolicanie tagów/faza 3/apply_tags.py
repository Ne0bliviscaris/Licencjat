import csv
import json
import os


def main():
    # Ścieżki przestrzeni roboczej
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    mapping_file = os.path.join(base_dir, "tagi_globalnie_zmergeowane.json")
    input_csv = os.path.join(base_dir, "2. Dataset oczyszczony.csv")
    output_csv = os.path.join(base_dir, "faza 3", "3. Dataset zunifikowany.csv")

    # Budowa płaskiego słownika mapującego oryginalny tag -> tag zunifikowany
    print("Wczytywanie zunifikowanych mapowań...")
    tag_mapping = {}
    try:
        with open(mapping_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            for category_container in data.get("category", []):
                for cat_name, mapped_dict in category_container.items():
                    for unified_tag, original_tags_list in mapped_dict.items():
                        for orig_tag in original_tags_list:
                            # Mapujemy ZAWSZE do wersji w lowercase i strip, żeby zniwelować różnice w plikach CSV
                            tag_mapping[orig_tag.lower().strip()] = unified_tag
    except FileNotFoundError:
        print(f"Nie znaleziono pliku mapowań: {mapping_file}")
        return

    print("Przetwarzanie pliku CSV...")
    # Przetwarzanie i mapowanie CSV
    with (
        open(input_csv, "r", encoding="utf-8") as infile,
        open(output_csv, "w", encoding="utf-8", newline="") as outfile,
    ):
        reader = csv.reader(infile, delimiter=";")
        writer = csv.writer(outfile, delimiter=";", quoting=csv.QUOTE_MINIMAL)

        # Nagłówki
        header = next(reader, None)
        if header:
            writer.writerow(header)

        processed_rows = 0
        for row in reader:
            if len(row) < 2:
                continue

            row_id = row[0]
            tags_str = row[1]

            # Odczyt tagów z formatu JSON-string (wewnątrz CSV)
            try:
                original_tags = json.loads(tags_str)
            except json.JSONDecodeError:
                original_tags = []

            # Ujednolicenie i deduplikacja (używamy set, by w wierszu ten sam zunifikowany tag nie wystąpił dwa razy)
            unified_tags = set()
            for tag in original_tags:
                clean_orig_tag = tag.lower().strip()
                # Zamieniamy na ujednoliconą wersję (jeśli nie istnieje w słowniku, zostawiamy oryginał clean)
                unified_tag = tag_mapping.get(clean_orig_tag, tag)
                unified_tags.add(unified_tag)

            # Konwersja z powrotem do zrzuconego JSON i zapis do pliku wynikowego
            new_tags_str = json.dumps(sorted(list(unified_tags)), ensure_ascii=False)
            writer.writerow([row_id, new_tags_str])
            processed_rows += 1

    print(f"Zakończono! Przetworzono {processed_rows} wierszy.")
    print(f"Plik wynikowy został zapisany jako: {output_csv}")


if __name__ == "__main__":
    main()
