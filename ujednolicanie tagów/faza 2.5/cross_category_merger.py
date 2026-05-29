import json
import os
from collections import defaultdict
from typing import List

import instructor
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel

# ================= KONFIGURACJA =================
load_dotenv()
api_key = os.getenv("DEEPINFRA_API_KEY")
if not api_key:
    raise ValueError("Nie znaleziono zdefiniowanej zmiennej DEEPINFRA_API_KEY!")

client = instructor.from_openai(
    OpenAI(
        base_url="https://api.deepinfra.com/v1/openai",
        api_key=api_key,
    ),
    mode=instructor.Mode.JSON,
)


# ================= MODELE PYDANTIC =================
class MergeAssignment(BaseModel):
    old_tag: str
    new_tag: str


class MergeResult(BaseModel):
    merges: List[MergeAssignment]


# ================= FUNKCJE LLM =================
def cross_category_merge(
    tags: List[str], model_name: str = "google/gemma-4-26B-A4B-it"
) -> List[MergeAssignment]:
    prompt = f"""
Otrzymujesz wszystkie unikalne tagi, które pozostały nam po wstępnym czyszczeniu.
Część z nich może znaczyć dokładnie to samo, ale pochodzą z różnych kategorii (np. 'React' w Web i 'React.js' w Inne).
Twoim zadaniem jest GLOBALNE UJEDNOLICENIE, aby pozbyć się duplikatów oznaczających tę samą technologię.

Zasady:
1. Złącz tagi, które odzwierciedlają dokładnie ten sam byt technologiczny (np. 'AWS' i 'Amazon Web Services' -> 'AWS').
2. Standaryzuj nazewnictwo i poprawiaj literówki (np. 'C#' i 'C Sharp' -> 'C#', 'JS' i 'JavaScript' -> 'JavaScript').
3. NIE grupuj niezależnych od siebie technologii o różnych zastosowaniach w ogólne kategorie (nie rób z 'Java' i 'Python' tagu 'Backend'). Złączaj tylko synonimy.
4. Zwróć mapowanie tylko dla tych tagów, które ulegają JAKIEJKOLWIEK zmianie na nową zunifikowaną nazwę. Jeśli tag zostaje taki sam, możesz go pominąć (zostawię go bez zmian) LUB przypisać do niego tę samą nazwę 'new_tag' = 'old_tag'.

Lista tagów do globalnego ujednolicenia:
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
        print(f"Błąd LLM: {e}")
        return []


def main():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    input_path = os.path.join(base_dir, "tagi_finalnie_zmergeowane.json")

    if not os.path.exists(input_path):
        print(f"Brak pliku wejściowego: {input_path}")
        return

    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # ------------------ KROK 1: Ręczne usuwanie duplikatów ------------------
    # Zebranie tagów i oryginalnych aliasów pomijając kategorie.
    global_tags = defaultdict(list)

    for cat_dict_container in data.get("category", []):
        for category_name, unified_dict in cat_dict_container.items():
            for unified_tag, original_tags_list in unified_dict.items():
                # Ujednolicanie wielkości liter dla kluczy (żeby automatycznie złączyć "React" i "react")
                # Zapisujemy docelowy przypadek używając np. pierwszego napotkanego lub Title Case
                key_lower = unified_tag.strip().lower()

                # Zbieranie oryginałów pod jeden klucz lower-case (dla łatwego złączenia)
                global_tags[key_lower].append(
                    unified_tag
                )  # Przechowujemy też starą zunifikowaną nazwę, jako oryginał
                global_tags[key_lower].extend(original_tags_list)

    # Przywrócenie pierwotnego caseingu dla unikalnych tagów (wybieramy najczęstszą wariację wielkości liter z oryginałów lub zostawiamy title())
    step1_dict = defaultdict(list)
    for key_lower, originals in global_tags.items():
        # Znajdź najbardziej reprezentatywną formę (np. pierwszą najkrótszą z dużej litery albo po prostu pierwszą dodaną, która nie jest oryginalnym tagiem małymi literami)
        representative = sorted(
            originals, key=lambda x: (x.lower() != key_lower, len(x))
        )[0]

        # Oczyszczenie z powtórzeń na liście oryginałów
        step1_dict[representative] = list(set(originals))

    unique_tags_after_step1 = list(step1_dict.keys())
    print(
        f"Po usunięciu duplikatów exact-match i case-insensitive liczba tagów to: {len(unique_tags_after_step1)}"
    )

    # ------------------ Zapis wyników ------------------
    # Z pominięciem LLM - wynikami są bezpośrednio dane po deduplikacji ręcznej
    clean_final_global_dict = {k: list(set(v)) for k, v in step1_dict.items()}

    # Format dla skryptów faza 3 (umieszczamy wszystko w jednej uogólnionej kategorii np. "Global")
    output_data = {"category": [{"Global": clean_final_global_dict}]}

    output_path = os.path.join(base_dir, "faza 2.5", "tagi_globalnie_zmergeowane.json")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=4)

    print(f"PROCES ZAKOŃCZONY! Wyniki po globalnej de-duplikacji w: '{output_path}'")
    print(
        "Teraz możesz zmienić wejście w faza 3/apply_tags.py, by wskazywało na ten nowy plik JSON."
    )


if __name__ == "__main__":
    main()
