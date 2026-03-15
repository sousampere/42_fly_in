# Notation — Fly-in-2

> Grille d'évaluation basée sur les critères du sujet, les principes **OOP**, **SOLID** et **STUPID**.  
> Date : 12 mars 2026 — Révision v5

---

## Grille de notation par critère

### A. Conformité au sujet

| Critère | Pondération | Score | Justification |
|---|---|---|---|
| Parser conforme au format d'entrée | 10 pts | **9/10** | Complet. `max_drones ge=1` absent, `nb_drones: 0` non wrappé en `MapError` |
| Moteur de simulation | 20 pts | **0/20** | Non implémenté (scaffolding uniquement) |
| Algorithme de pathfinding | 20 pts | **0/20** | Non implémenté (`algorithms/` vide) |
| Respect des contraintes (capacités, tours, blocage) | 10 pts | **0/10** | Non implémenté |
| Représentation visuelle (couleurs terminal ou GUI) | 10 pts | **0/10** | Non implémentée |
| Format de sortie de simulation | 5 pts | **0/5** | Non implémenté |
| README.md complet | 5 pts | **0/5** | Fichier vide (`# Fly-In`) |

**Sous-total A : 9 / 80** *(stable vs v4)*

---

### B. Qualité du code — OOP

| Critère | Pondération | Score | Justification |
|---|---|---|---|
| Code entièrement orienté objet | 10 pts | **10/10** | `Controller`, `MapParser`, `RunSecurity` sont de vraies classes OOP. `Controller` testable via `ControllerError` ✅. `os._exit` sorti du domaine. DTOs Pydantic intentionnels. `Node`/`Link` en scaffolding |
| Encapsulation et responsabilités bien délimitées | 5 pts | **5/5** | Chaque classe a une responsabilité claire. `__` cohérent dans `RunSecurity` et `Controller` ✅. `RunSecurity` injecté, pas instancié ✅ |
| Polymorphisme / héritage utilisés correctement | 5 pts | **5/5** | Hiérarchies d'erreurs complètes. `ControllerError` propre. `NoReturn` typé sur `exit_program` ✅ |

**Sous-total B : 20 / 20** *(+1 vs v4)*

---

### C. Respect des principes SOLID

| Principe | Pondération | Score | Justification |
|---|---|---|---|
| **S** — Single Responsibility | 4 pts | **4/4** | `main.py`, `Controller`, `MapParser`, `RunSecurity`, `ControllerError` ont chacun une responsabilité unique et claire ✅ |
| **O** — Open/Closed | 4 pts | **3/4** | `algorithms/` prévu pour l'extension ✅. Parsing de lignes toujours ad hoc |
| **L** — Liskov Substitution | 4 pts | **4/4** | Irréprochable ✅ |
| **I** — Interface Segregation | 4 pts | **1/4** | Toujours aucune `Protocol`/`ABC` définie — le seul manque structurel SOLID restant |
| **D** — Dependency Inversion | 4 pts | **3/4** | `RunSecurity` injectée dans `Controller` ✅. `main.py` → `Controller` uniquement ✅. `Controller` → `MapParser` concret direct |

**Sous-total C : 15 / 20** *(+1 vs v4)*

---

### D. Violations STUPID

| Anti-pattern | Pondération | Pénalité | Justification |
|---|---|---|---|
| Tight Coupling | -4 pts | **-1** | Terminal hardcodé dans `main.py`. `os._exit` sorti de `Controller` ✅ |
| Untestability | -4 pts | **0** | `Controller.process()` testable via `ControllerError` ✅. `MapParser` et `RunSecurity` testables ✅. `test_zero_drone` : fuite `ValidationError` (qualité de test, non de production) |
| Indescriptive Naming | -4 pts | **0** | Magic number `11` corrigé ✅. `__check_dependencies` ✅. `exit_program` ✅. Faute résiduelle dans les chaînes de log uniquement |
| Duplication | -4 pts | **0** | Absent ✅ |
| Singleton | -4 pts | **0** | Absent ✅ |
| Premature Optimization | -4 pts | **0** | Absent ✅ |

**Sous-total D (pénalités) : -1 / 0** *(+3 vs v4)*

---

### E. Conformité technique (règles communes)

| Critère | Pondération | Score | Justification |
|---|---|---|---|
| Type hints complets | 5 pts | **5/5** | Présents partout, `NoReturn` correct ✅ |
| Docstrings (PEP 257) | 5 pts | **3/5** | `MapParser` et `RunSecurity` documentés. `Controller` et ses méthodes non documentés. Modèles sans docstrings |
| Tests unitaires (pytest) | 5 pts | **4/5** | 15 tests. 14 robustes et bien structurés. `test_zero_drone` attrape `ValidationError` directement (fuite d'abstraction non corrigée) |
| Makefile complet et fonctionnel | 5 pts | **5/5** | Toujours excellent ✅ |
| `pyproject.toml` / dépendances | 5 pts | **5/5** | Propre ✅ |
| Gestion des exceptions | 5 pts | **4/5** | `ControllerError` propre ✅. `RunEnvironmentError` ✅. `assert` dans `MapParser.process()` et `nb_drones: 0` → `ValidationError` subsistent |

**Sous-total E : 26 / 30** *(stable vs v4)*

---

## Récapitulatif

| Catégorie | v1 | v2 | v3 | v4 | v5 | Δ v4→v5 |
|---|---|---|---|---|---|---|
| A — Conformité sujet | 6 / 80 | 8 / 80 | 9 / 80 | 9 / 80 | **9 / 80** | = |
| B — Qualité OOP | 11 / 20 | 14 / 20 | 17 / 20 | 19 / 20 | **20 / 20** | +1 |
| C — Principes SOLID | 10 / 20 | 10 / 20 | 12 / 20 | 14 / 20 | **15 / 20** | +1 |
| D — Violations STUPID | -9 | -7 | -4 | -4 | **-1** | +3 |
| E — Conformité technique | 21 / 30 | 23 / 30 | 26 / 30 | 26 / 30 | **26 / 30** | = |
| **TOTAL** | **39 / 150** | **48 / 150** | **60 / 150** | **64 / 150** | **69 / 150** | **+5** |

---

## Note finale

$$\text{Note v5} = \frac{69}{150} \times 100 \approx \mathbf{46\%}$$

| Niveau | Fourchette | Appréciation |
|---|---|---|
| Insuffisant | < 40% | ❌ |
| Passable | 40–55% | ⚠️ |
| Correct | 55–70% | 🟡 |
| Bien | 70–85% | 🟢 |
| Très bien | > 85% | ✅ |

> **Appréciation : ⚠️ Passable — 46%** *(+30 pts depuis v1)*

---

## Lecture de la progression

```
v1 : 39/150 — 26%  ❌  Parser procédural, 3 tests
v2 : 48/150 — 32%  ❌  MapParser OOP, validators, 5 tests
v3 : 60/150 — 40%  ⚠️  src/ layout, RunSecurity OOP, hiérarchie erreurs, 11 tests
v4 : 64/150 — 43%  ⚠️  Controller, scaffolding domaine, .copy(), cohérence visibilité
v5 : 69/150 — 46%  ⚠️  ControllerError, injection RunSecurity, magic number, 15 tests
```

La progression sur la **qualité de conception** est excellente et constante. B+C passent de 21/40 en v1 à **35/40 en v5** — c'est une progression de **+67%** sur la qualité OOP/SOLID. Les violations STUPID sont quasi éliminées (-9 → -1). Le palier suivant en note ne peut venir que de l'implémentation des fonctionnalités.

---

## Diagnostic du plafonnement

La catégorie A (conformité sujet) représente **53% de la note totale** (80/150). Avec 9/80 acquis, toute la progression sur les 4 autres catégories ne peut structurellement dépasser ~50% sans implémenter la simulation et le pathfinding.

$$\text{Plafond sans fonctionnalités} = \frac{9 + 20 + 15 + (-1) + 26}{150} \approx 46\%$$

---

## Projection après implémentation des parties manquantes

| Composant | Gain estimé |
|---|---|
| `Node` et `Link` actifs (logique métier) | +3 pts |
| `IPathfinder` Protocol + 1 algorithme fonctionnel | +25 pts |
| Moteur de simulation complet | +25 pts |
| Représentation visuelle (terminal coloré) | +8 pts |
| README.md conforme (toutes sections) | +4 pts |
| Corrections mineures restantes (`assert`, `ge=1`, docstrings `Controller`) | +1 pt |
| **Total gain potentiel** | **+66 pts → 135/150 ≈ 90%** ✅ |
