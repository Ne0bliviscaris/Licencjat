import json
from collections import defaultdict


def main():
    # Wczytanie obecnych tagów
    with open("tagi_finalne.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    # Struktura: kategoria -> tag_ujednolicony -> lista tagów oryginalnych
    grouped = defaultdict(lambda: defaultdict(list))

    for item in data.get("mappings", []):
        cat = item["category"]
        unified = item["unified_name"]
        orig = item["original_tag"]

        grouped[cat][unified].append(orig)

    # Formatowanie do oczekiwanej struktury
    result = {"category": []}
    for cat, unif_dict in grouped.items():
        # Upewniamy się, że mamy unikalne tagi oryginalne w listach (na wszelki wypadek)
        clean_unif_dict = {k: list(set(v)) for k, v in unif_dict.items()}
        result["category"].append({cat: clean_unif_dict})

    # Zapis
    with open("tagi_pogrupowane_kategorie.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=4)

    print("Zapisano pogrupowane tagi do tagi_pogrupowane_kategorie.json")


if __name__ == "__main__":
    main()
