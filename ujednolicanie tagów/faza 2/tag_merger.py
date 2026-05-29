import json
import os
from collections import defaultdict
from typing import List

import instructor
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel
from tqdm import tqdm

# ================= KONFIGURACJA =================

# Wczytanie zmiennych środowiskowych (np. z pliku .env)
load_dotenv()
api_key = os.getenv("DEEPINFRA_API_KEY")
if not api_key:
    raise ValueError(
        "Nie znaleziono zdefiniowanej zmiennej DEEPINFRA_API_KEY! Upewnij się, że plik .env jest dostępny."
    )

client = instructor.from_openai(
    OpenAI(
        base_url="https://api.deepinfra.com/v1/openai",
        api_key=api_key,
    ),
    mode=instructor.Mode.JSON,
)

# ================= MODELE PYDANTIC =================


class MergeAssignment(BaseModel):
    old_unified_tag: str
    new_unified_tag: str


class MergeResult(BaseModel):
    merges: List[MergeAssignment]


# ================= FUNKCJE LLM =================


def merge_unified_tags(
    category_name: str,
    tags: List[str],
    model_name: str = "google/gemma-4-26B-A4B-it",  # Użyty domyślny z Fazy 1 (możesz zmienić wedle uznania)
) -> List[MergeAssignment]:
    prompt = f"""
Otrzymujesz tagi z kategorii: '{category_name}'.
Twoim zadaniem jest UJEDNOLICENIE NAZW (unification), a NIE super-ogólne grupowanie odrębnych technologii.
Złącz tylko te tagi, które w rzeczywistości oznaczają dokładnie to samo narzędzie lub technologię.
Zasady:
1. Standaryzuj nazewnictwo, poprawiaj literówki i wielkość liter (np. 'node.js', 'nodejs', 'node' -> 'Node.js' ; 'postgres', 'postgresql' -> 'PostgreSQL').
2. Usuwaj numery wersji (np. 'java 11', 'java 8' -> 'Java').
3. Absolutnie NIE GRUPUJ niezależnych od siebie baz danych, języków czy chmur w jedno pojęcie. 'PostgreSQL', 'MySQL', 'Oracle' i 'SQLite' to różne technologie i muszą zostać osobnymi tagami!
4. Zwróć mapowanie parujące KAŻDY podany poniżej klucz ('old_unified_tag') z jego poprawną, wystandaryzowaną nazwą ('new_unified_tag').

Lista tagów do ujednolicenia:
{json.dumps(tags, indent=2, ensure_ascii=False)}
"""
    try:
        response = client.chat.completions.create(
            model=model_name,
            response_model=MergeResult,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,
        )
        return response.merges
    except Exception as e:
        print(f"Błąd LLM w kategorii {category_name}: {e}")
        return []


# ================= GŁÓWNY SKRYPT =================


def main():
    # Pobieramy plik roboczy, którego strukturę utworzyliśmy przed chwilą
    input_path = "faza 2\\tagi_pogrupowane_kategorie.json"

    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    final_result = {"category": []}

    # Format wejścia: "category": [ { "Bazy danych": { "SQL": ["tag1", "tag2"], ... } } ]
    for cat_dict_container in tqdm(
        data.get("category", []), desc="Faza 2: Iterowanie po kategoriach"
    ):
        # Spodziewamy się, że cat_dict_container ma format {nazwa_kat: { słownik tagów }}
        for category_name, unified_dict in cat_dict_container.items():
            old_unified_tags = list(unified_dict.keys())

            # W przypadku braku tagów ujednoliconych dla kategorii, przepisz ją bez zmian.
            if not old_unified_tags:
                final_result["category"].append({category_name: {}})
                continue

            # Wysłanie zbioru starych unifikacji do LLMa celem przypisania nowych
            merges = merge_unified_tags(category_name, old_unified_tags)

            # Budowa szybkiego mapowania starego->nowego dla łatwego dostępu
            merge_map = {m.old_unified_tag: m.new_unified_tag for m in merges}

            # Przebudowa struktury pod nową unifikację, agregujemy listy klasycznych tagów
            new_unified_dict = defaultdict(list)
            for old_tag, original_tags_list in unified_dict.items():
                new_tag = merge_map.get(
                    old_tag, old_tag
                )  # Jeżeli LLM pominął mapowanie, trzymamy starą nazwę
                new_unified_dict[new_tag].extend(original_tags_list)

            # Upewniamy się, że zredukowalismy duplikujące się nazwy z łączonych list i odpięliśmy defaultdic
            clean_new_unified_dict = {
                k: list(set(v)) for k, v in new_unified_dict.items()
            }

            # Dodajemy gotową, zdeduplikowanką kategorię do wyniku
            final_result["category"].append({category_name: clean_new_unified_dict})

    output_path = "tagi_finalnie_zmergeowane.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(final_result, f, ensure_ascii=False, indent=4)

    print(f"\nPROCES ZAKOŃCZONY SUKCESEM! Wyniki po de-duplikacji w: '{output_path}'")


if __name__ == "__main__":
    main()
