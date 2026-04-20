import collections
import json
import os
from typing import Dict, List, Literal

import instructor
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel
from tqdm import tqdm

# ----------------- SCHEMATY PYDANTIC I TYPY -----------------
TagCategory = Literal[
    "Języki programowania",
    "Technologie i frameworki Web/Frontend",
    "Technologie i frameworki Backend",
    "Bazy danych i Hurtownie danych",
    "Chmura obliczeniowa (Cloud)",
    "DevOps, CI/CD i Konteneryzacja",
    "Sztuczna Inteligencja, Machine Learning i Data Science",
    "Testowanie i Quality Assurance (QA)",
    "Architektura, API i Wzorce projektowe",
    "Metodyki, Zarządzanie i Organizacja pracy",
    "Systemy klasy Enterprise (ERP / CRM / ITSM)",
    "Sieci komputerowe i Telekomunikacja",
    "Bezpieczeństwo (Cybersecurity)",
    "Narzędzia analityczne i Business Intelligence (BI)",
    "Tworzenie urządzeń mobilnych (Mobile)",
    "Systemy operacyjne platformy serwerowe",
    "Umiejętności miękkie i biznesowe (Soft Skills / Biznes)",
    "Design i UX/UI",
    "Inne/Niesklasyfikowane",
]


# Modele dla Fazy 1
class CategoryAssignment(BaseModel):
    original_tag: str
    category: TagCategory


class CategorizationResult(BaseModel):
    assignments: List[CategoryAssignment]


# Modele dla Fazy 2
class UnificationAssignment(BaseModel):
    original_tag: str
    unified_name: str


class UnificationResult(BaseModel):
    unifications: List[UnificationAssignment]


# ----------------- KLIENT DEEPINFRA -----------------
# Wczytanie zmiennych środowiskowych (np. z pliku .env)
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


# ----------------- FAZA 1: KATEGORYZACJA -----------------
def categorize_batch(
    tags_batch: List[str], model_name: str = "google/gemma-4-26B-A4B-it"
) -> List[CategoryAssignment]:
    prompt = f"""
Twoim jedynym zadaniem jest przypisanie każdemu tagowi z poniższej listy odpowiedniej kategorii IT.
Zwróć przypisania w formacie JSON z polami 'original_tag' i 'category'.

Oto tagi do przypisania:
{json.dumps(tags_batch, indent=2, ensure_ascii=False)}
"""
    try:
        response = client.chat.completions.create(
            model=model_name,
            response_model=CategorizationResult,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,
        )
        return response.assignments
    except Exception as e:
        print(f"Błąd Fazy 1 (Kategoryzacja): {e}")
        return []


# ----------------- FAZA 2: UJEDNOLICENIE -----------------
def unify_category_tags(
    category_name: str, tags: List[str], model_name: str = "google/gemma-4-26B-A4B-it"
) -> List[UnificationAssignment]:
    prompt = f"""
Otrzymujesz wszystkie tagi z kategorii: '{category_name}'.
Twoim zadaniem jest BARDZO AGRESYWNE ujednolicanie i generalizowanie tych tagów do głównych, nadrzędnych technologii.

Zasady generalizacji:
1. Dialekty i konkretne implementacje łącz w główny nurt. (np. 't-sql', 'pl/sql', 'mysql', 'postgresql', 'ms sql', 'sqlite' -> 'SQL')
2. Chmury obliczeniowe: konkretne sub-usługi łącz do nazwy dostawcy. (np. 'aws ec2', 'aws s3', 'amazon redshift' -> 'AWS'; 'azure ad', 'azure data factory' -> 'Azure')
3. Biblioteki i poboczne narzędzia łącz z głównym frameworkiem. (np. 'react hooks', 'react router', 'react.js', 'react native' -> 'React')
4. Odrzuć wersje. (np. 'java 8', 'java 11', 'java 17+' -> 'Java'; 'angular 2+', 'angular 16', 'angularjs' -> 'Angular')
5. Odmiany nazw i literówki grupuj razem (np. 'k8s', 'kubernetes', 'kubenetes' -> 'Kubernetes').
6. Zwróć mapowanie parując KAŻDY oryginalny tag podany na wejściu z jego nową, zgeneralizowaną nazwą 'unified_name'.

Oto tagi wejściowe z tej kategorii (musisz zmapować wszystkie poniższe tagi):
{json.dumps(tags, indent=2, ensure_ascii=False)}
"""
    try:
        response = client.chat.completions.create(
            model=model_name,
            response_model=UnificationResult,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,
        )
        return response.unifications
    except Exception as e:
        print(f"Błąd Fazy 2 (Ujednolicanie w kategorii {category_name}): {e}")
        return []


# ----------------- GŁÓWNY PROCES -----------------
def main():
    # 1. Wczytanie plików
    with open("unikalne_tagi.json", "r", encoding="utf-8") as f:
        #
        #
        #
        unique_tags = json.load(f)["unique_tags"]  # [:100]

    print(f"Rozpoczynam pracę na {len(unique_tags)} tagach...")

    # ------------------
    # ETAP 1: Kategoryzacja
    # ------------------
    categorized_tags = []
    # chunk_size = 100 ? # Kategorie nie wymagają kontekstu synonimów, mogą być większe paczki
    chunk_size = 20  # Ka?tegorie nie wymagają kontekstu synonimów, mogą być większe paczki

    for i in tqdm(range(0, len(unique_tags), chunk_size), desc="Faza 1: Kategoryzacja"):
        batch = unique_tags[i : i + chunk_size]
        assignments = categorize_batch(batch)
        categorized_tags.extend([a.model_dump() for a in assignments])

    # Zapis punktu kontrolnego (lista obiektów Pydantic)
    with open("tagi_faza1_raw.json", "w", encoding="utf-8") as f:
        json.dump(categorized_tags, f, ensure_ascii=False, indent=4)

    # ------------------
    # GRUPOWANIE DO ETAPU 2 (Twój format: dict[Kategoria: List[Tagi]])
    # ------------------
    grouped_by_category: Dict[str, List[str]] = collections.defaultdict(list)
    for row in categorized_tags:
        # Zabezpieczenie przed uszkodzeniem JSON i brakiem pol
        cat = row.get("category", "Inne/Niesklasyfikowane")
        tag = row.get("original_tag")
        if tag:
            grouped_by_category[cat].append(tag)

    # Zapisujemy ładnie pogrupowane wg wymogu
    with open("tagi_krok1_pogrupowane.json", "w", encoding="utf-8") as f:
        json.dump(grouped_by_category, f, ensure_ascii=False, indent=4)

    # ------------------
    # ETAP 2: Ujednolicenie
    # ------------------
    final_results = []

    for category, tags_in_cat in tqdm(
        grouped_by_category.items(), desc="Faza 2: Ujednolicanie wewnątrz kategorii"
    ):
        if not tags_in_cat:
            continue

        # Wysłanie całej sfokusowanej grupy do modelu
        unifications = unify_category_tags(category, tags_in_cat)

        for u in unifications:
            final_results.append(
                {"original_tag": u.original_tag, "unified_name": u.unified_name, "category": category}
            )

    # Zmiana końcowa
    with open("tagi_finalne.json", "w", encoding="utf-8") as f:
        json.dump({"mappings": final_results}, f, ensure_ascii=False, indent=4)

    print("PROCES ZAKOŃCZONY SUKCESEM! Wyniki w 'tagi_finalne.json'")


if __name__ == "__main__":
    main()
