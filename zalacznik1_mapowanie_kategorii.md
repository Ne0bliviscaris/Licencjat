# Ujednolicenie kategorii dla stacji źródłowych

Poniższy dokument przedstawia mapowanie źródłowych kategorii ogłoszeń o pracę, pochodzących z różnych portali (scraperów), na jedną wspólną, ujednoliconą klasyfikację. Dzięki tym mapowaniom możliwe jest spójne przetwarzanie i analiza danych zebranych z wielu źródeł w zestawie danych.

## Źródła danych
1. **InhireIO**
2. **theprotocol.it**

## Tabela mapowania

| Zunifikowana kategoria w systemie | Oryginalne kategorie: InhireIO | Oryginalne kategorie: theprotocol.it |
| :--- | :--- | :--- |
| **`frontend`** | `frontend_developer`, `ux_designer`, `full_stack_developer`, `mobile_developer` | `frontend`, `fullstack`, `mobile` |
| **`backend`** | `backend_developer`, `devops_engineer`, `full_stack_developer`, `etl_developer`, `database_developer`, `architect` | `backend`, `fullstack`, `architecture` |
| **`game_dev`** | `game_developer` | `gamedev` |
| **`data_ai`** | `data_science`, `machine_learning_engineer`, `big_data`, `database_administrator`, `etl_developer`, `database_developer`, `bi` | `big-data-science`, `ai-ml`, `data-analytics-and-bi` |
| **`devops_cloud`** | `devops_engineer` | `devops` |
| **`qa_testing`** | `testing` | `testing` |
| **`security`** | `security_engineer` | `security` |
| **`it_admin_support`** | `it_administration`, `helpdesk`, `network_engineer`, `network_administrator` | `helpdesk`, `it-admin` |
| **`ux_ui`** | `ux_designer` | `ux-ui` |
| **`management_analytics`** | `project_manager`, `product_owner`, `business_analyst`, `bi`, `architect`, `team_leader`, `sap`, `scrum_master` | `project-management`, `data-analytics-and-bi`, `business-analytics`, `agile`, `product-management`, `sap-erp`, `system-analytics` |
| **`other`** | `other`, `embedded_developer`, `blockchain_engineer`, `mobile_developer` | `embedded`, `mobile` |

## Uwagi do mapowań:
* Role mieszane (np. `fullstack`, `mobile`) mogą pojawiać się jako źródło dla więcej niż jednej kategorii nadrzędnej, ze względu na nakładające się na siebie obowiązki, np. `full_stack_developer` z InhireIO trafia zarówno do grupy `frontend` jak i `backend`. To samo tyczy się ról `mobile` i analitycznych.
