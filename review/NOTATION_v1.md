# Notation — Fly-in

> Grille d'évaluation basée sur les critères du sujet, les principes **OOP**, **SOLID** et **STUPID**.  
> Date : 13 mars 2026 — Révision v1

---

## Grille de notation par critère

### A. Conformité au sujet

| Critère | Pondération | Score | Justification |
|---|---|---|---|
| Parser conforme au format d'entrée | 10 pts | **2/10** | Fonctions de parsing écrites mais pas intégrées. Pas d'objet `Map` généré |
| Moteur de simulation | 20 pts | **0/20** | Non implémenté |
| Algorithme de pathfinding | 20 pts | **0/20** | Non implémenté |
| Respect des contraintes (capacités, tours, blocage) | 10 pts | **0/10** | Non implémenté |
| Représentation visuelle (couleurs terminal ou GUI) | 10 pts | **0/10** | Non implémentée |
| Format de sortie de simulation | 5 pts | **0/5** | Non implémenté |
| README.md complet | 5 pts | **0/5** | Fichier vide (`# Fly-In`) |

**Sous-total A : 2 / 80** *(3%)*

---

### B. Qualité du code — OOP

| Critère | Pondération | Score | Justification |
|---|---|---|---|
| Code entièrement orienté objet | 10 pts | **6/10** | Enums bien structurées, classe `Hub` esquissée. Parser reste procédural, pas de `Connection` ni `Graph` |
| Encapsulation et responsabilités bien délimitées | 5 pts | **2/5** | Parser mélange responsabilités (extraction, validation, transformation) |
| Polymorphisme / héritage utilisés correctement | 5 pts | **0/5** | Absent ; pas de hiérarchie, pas de stratégies |

**Sous-total B : 8 / 20** *(40%)*

---

### C. Respect des principes SOLID

| Principe | Pondération | Score | Justification |
|---|---|---|---|
| **S** — Single Responsibility | 4 pts | **2/4** | Parser mélange responsabilités ; `Hub` incomplet |
| **O** — Open/Closed | 4 pts | **1/4** | Préfixes hardcodés, pas de registre générique |
| **L** — Liskov Substitution | 4 pts | **2/4** | Pas de hiérarchie à évaluer ; absence de `Connection` problématique |
| **I** — Interface Segregation | 4 pts | **0/4** | Aucune `Protocol` ou `ABC` |
| **D** — Dependency Inversion | 4 pts | **1/4** | Pas d'injection, couplage direct |

**Sous-total C : 6 / 20** *(30%)*

---

### D. Violations STUPID

| Anti-pattern | Pondération | Pénalité | Justification |
|---|---|---|---|
| Tight Coupling | -4 pts | **-2** | Parser couplé à `Hub` ; `main.py` → `parse()` direct |
| Untestability | -4 pts | **-2** | Pas de tests, I/O sans abstraction |
| Indescriptive Naming | -4 pts | **-1** | Noms clairs mais logique implicite |
| Duplication | -4 pts | **-2** | `get_start_hub()` / `get_normal_hub()` dupliquent massivement |
| Singleton | -4 pts | **0** | Absent |
| Premature Optimization | -4 pts | **0** | Absent |

**Sous-total D (pénalités) : -7 / 0**

---

### E. Conformité technique (règles communes)

| Critère | Pondération | Score | Justification |
|---|---|---|---|
| Type hints complets | 5 pts | **2/5** | Enums typées, parsing sans type hints |
| Docstrings (PEP 257) | 5 pts | **1/5** | `Hub` documentée, fonctions de parsing non |
| Tests unitaires (pytest) | 5 pts | **0/5** | Aucun test |
| Makefile complet et fonctionnel | 5 pts | **3/5** | Présent mais incomplet |
| `pyproject.toml` / dépendances | 5 pts | **2/5** | Minimal, dépendances manquantes |
| Gestion des exceptions | 5 pts | **2/5** | Exceptions spécialisées, mais beaucoup de `try-except` génériques |

**Sous-total E : 10 / 30** *(33%)*

---

## Récapitulatif par catégorie

| Catégorie | Pondération | v1 | % |
|---|---|---|---|
| A — Conformité au sujet | 80 pts | 2 | 3% |
| B — Qualité OOP | 20 pts | 8 | 40% |
| C — Principes SOLID | 20 pts | 6 | 30% |
| D — Violations STUPID | 0 pts | -7 | -7 |
| E — Conformité technique | 30 pts | 10 | 33% |
| **TOTAL** | **150 pts** | **23** | **15%** |

---

## Tableau de progression (v1 = baseline)

| Catégorie | v1 |
|---|---|
| A — Conformité sujet | 2 / 80 |
| B — Qualité OOP | 8 / 20 |
| C — Principes SOLID | 6 / 20 |
| D — Violations STUPID | -7 |
| E — Conformité technique | 10 / 30 |
| **TOTAL** | **23 / 150** |

---

## Analyse détaillée par section

### A. Conformité au sujet (2/80)

**Réalisé :**
- ⚠️ Parser : fonctions écrites mais non intégrées
- ⚠️ Enums pour zones et couleurs
- ❌ Pas d'objet `Map` généré
- ❌ Pas de fichier chargé en entier

**Manquant :**
- ❌ Simulation et tour by tour
- ❌ Pathfinding (multi-chemin, optimisation)
- ❌ Respect des contraintes de capacité (zones et connections)
- ❌ Visualisation terminal ou graphique
- ❌ Format de sortie de simulation
- ❌ README documenté

**Impact** : Le parser est en chantier mais inachevé. Aucune des étapes suivantes n'est possible. L'absence complète représente ~75 points perdus sur 80.

---

### B. Qualité OOP (8/20)

**Excellences :**
- Enums `Color` et `ZoneType` bien structurées
- Exceptions spécialisées (`ParserError`, `ZoneConfigurationError`)
- Classe `Hub` commence à modéliser le domaine

**Points faibles :**
- Parser reste largement procédural
- Pas de classe `Connection`
- Pas de classe `Graph`
- Pas de polymorphisme
- Mélanges de responsabilités dans `get_*`

---

### C. Principes SOLID (6/20)

| Principe | État |
|---|---|
| **S** ⚠️ | Parser mélange extraction/validation/instanciation |
| **O** ❌ | Préfixes hardcodés, pas extensible |
| **L** ⚠️ | Pas de violation évidente, mais structure incomplète |
| **I** ❌ | Pas de contrats d'interface |
| **D** ❌ | Couplage direct, pas d'injection |

---

### D. Violations STUPID (-7)

| Anti-pattern | État | Sévérité |
|---|---|---|
| Tight Coupling | `-2` (Parser ↔ Hub, main ↔ parse) | Majeure |
| Untestability | `-2` (Pas de tests, I/O directe) | Majeure |
| Indescriptive Naming | `-1` (Noms OK, logique implicite) | Mineure |
| Duplication | `-2` (`get_start_hub` / `get_normal_hub`) | Majeure |
| Singleton | `0` | Absent |
| Premature Optimization | `0` | Absent |

---

### E. Conformité technique (10/30)

| Critère | État | Raison |
|---|---|---|
| Type hints | 2/5 | Enums typées, parsing sans (`str`, `int` implicites) |
| Docstrings | 1/5 | Seule la classe `Hub` documentée |
| Tests | 0/5 | Aucun test écrit |
| Makefile | 3/5 | Basique, manquent `lint`, `test` |
| `pyproject.toml` | 2/5 | Minimal, dépendances incomplètes |
| Exceptions | 2/5 | Exceptions propres, `try-except` génériques subsistent |

---

## Note finale

$$\text{Note v1} = \frac{23}{150} \times 100 \approx \mathbf{15\%}$$

| Niveau | Fourchette | Appréciation |
|---|---|---|
| Excellent | 85–100 | — |
| Bon | 70–84 | — |
| Satisfaisant | 55–69 | — |
| Insatisfaisant | 40–54 | — |
| Faible | < 40 | ✅ **v1 (15%)** — Chantier en cours |

---

## Priorités pour la v2

1. **Intégrer complètement le parser** — générer objet `Map` avec hubs et connexions — gain : **+15 pts**
2. **Créer classe `Connection`** — modéliser arêtes du graphe — gain : **+3 pts**
3. **Créer classe `Graph`** — structurer le réseau — gain : **+3 pts**
4. **Ajouter type hints partout** — passer 2/5 → 5/5 — gain : **+3 pts**
5. **Écrire tests du parser** — couverture basique — gain : **+3 pts**
6. **Réduire duplication** — merger `get_start_hub()` / `get_normal_hub()` — gain : **+2 pts**
7. **Compléter Makefile** — `lint`, `test` rules — gain : **+2 pts**

**Cible v2** : ~55 / 150 (37%)

---

## Contexte de version

Cette v1 représente un état **très précoce** mais **actif**. Le code avance clairement (parser, enums, exceptions), les fondations structurantes sont présentes. Les trois prochains jalons critiques sont :
1. **v1.5** : Parser intégré et fonctionnel
2. **v2** : Classes domaine complètes (`Connection`, `Graph`)
3. **v3** : Simulation et pathfinding
