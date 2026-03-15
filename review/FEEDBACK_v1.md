# Feedback — Fly-in

> Analyse du projet au regard des règles **OOP**, **SOLID** et **STUPID**.  
> Date : 13 mars 2026 — Révision v1

> **Note de contexte architectural** : Cette premièrHe révision évalue l'état initial du projet. Un parser de base est en cours de développement. Les modèles domaine (Hub, Connection) commencent à prendre forme avec des enums structurantes. L'ensemble des composants majeurs (simulation, pathfinding, visualisation) reste à scaffolder.

---

## Résumé de l'état v1

| Point clé | État | Remarque |
|---|---|---|
| Parser de map | ⚠️ Partiel | Fonctions de parsing écrites, pas d'intégration complète |
| Modèles domaine | ✅ Commencés | Enums complètes, classe `Hub` esquissée, pas de `Connection` ni `Graph` |
| Exceptions | ✅ Initiées | `ParserError`, `ZoneConfigurationError` — bonne direction |
| Tests unitaires | ❌ Absent | Aucun test |
| README/Docs | ❌ Absent | Fichier vide |
| Simulation | ❌ Absent | À scaffolder |
| Pathfinding | ❌ Absent | À scaffolder |
| Visualisation | ❌ Absent | À scaffolder |

---

## 1. État général du projet

| Composant attendu (sujet) | Présent | Complet |
|---|---|---|
| Parser de la map | ⚠️ | ⚠️ Partiellement implémenté |
| Modèles domaine (Hub, Connection, Zone) | ✅ | ⚠️ Esquisse, logique absente |
| Moteur de simulation | ❌ | — |
| Algorithme de pathfinding | ❌ | — |
| Représentation visuelle | ❌ | — |
| README.md complet | ❌ | ❌ Vide (`# Fly-In`) |
| Tests unitaires | ❌ | — |
| Gestion des exceptions | ✅ | ⚠️ Exceptions spécialisées commencées |

L'architecture initiale émerge. Le parser et les modèles sont en phase active de construction. Les composants critiques (simulation, pathfinding, visualisation) restent à scaffolder.

---

## 2. Analyse OOP

### ✅ Points forts

**Enumérations bien structurées.**

Les enums `Color`, `ZoneType` offrent un début de **type-safety** pour les concepts métier. C'est une bonne pratique OOP.

```python
class Color(Enum):
    GREEN = 'green'
    YELLOW = 'yellow'
    RED = 'red'
    BLUE = 'blue'
    GRAY = 'gray'

class ZoneType(Enum):
    RESTRICTED = 'restricted'
    NORMAL = 'normal'
    BLOCKED = 'blocked'
    PRIORITY = 'priority'
```

**Exceptions spécialisées.**

`ParserError`, `ZoneConfigurationError`, `ConnectionConfigurationError` permettent une gestion granulaire des erreurs. Bonne direction.

**Classe `Hub` : début d'encapsulation domaine.**

La classe `Hub` commence à porter la logique métier (position, restrictions, capacité). C'est le noyau d'une bonne architecture OOP.

### ⚠️ Domaines à vigilance

**Encapsulation partiellement absente.**

Le parser contient beaucoup de logique procédurale et de parsing "ad hoc". Les fonctions `get_nb_drones()`, `get_start_hub()`, etc. explorent la ligne manuellement plutôt que de déléguer à des classes responsables.

**Pas de classe Connection.**

Les connexions sont absentes du modèle. Elles doivent être une classe à part entière portant sa propre logique (capacité, bidirectionnalité).

**Pas de classe Graph.**

Le graphe qui relie les hubs n'existe pas encore. C'est une carence structurelle majeure pour OOP.

**Polymorphisme absent.**

Aucune hiérarchie de classe, aucune stratégie pour pathfinding/visualisation.

---

## 3. Analyse SOLID

### S — Single Responsibility ⚠️

Le parser mélange responsabilités : parsing, validation, instanciation d'objets métier. Les fonctions `get_*` ont des responsabilités superposées (extraction, validation, transformation).

`Hub` commence bien mais reste incomplet (pas de méthodes métier).

**Score : 2/4**

### O — Open/Closed ❌

Le parser n'est **pas** ouvert à l'extension. Les préfixes hardcodés (`start_hub:`, `hub:`, `connection:`) exigent une modification du code pour ajouter de nouveaux types. Pas de registre ou de stratégie.

**Score : 1/4**

### L — Liskov Substitution ⚠️

Pas encore de hiérarchie claire à évaluer. Mais l'absence de `Connection` comme classe indépendante rend difficile toute substitution future.

**Score : 2/4**

### I — Interface Segregation ❌

Aucune `Protocol` ou `ABC`. Les contrats implicites entre composants (parser, modèles, simulation) ne sont pas formalisés.

**Score : 0/4**

### D — Dependency Inversion ⚠️

Le `main.py` appelle directement `parse()`. Le `Hub` accède directement aux enums. Pas d'injection de dépendances visible.

**Score : 1/4**

**Sous-total SOLID : 6 / 20**

---

## 4. Analyse STUPID

| Anti-pattern | Pénalité | Justification |
|---|---|---|
| Tight Coupling | Parser fortement couplé à `Hub` ; `main.py` → `parse()` direct | `-2` |
| Untestability | Pas de tests ; `parse()` effectue I/O sans abstraction | `-2` |
| Indescriptive Naming | Noms clairs (`get_nb_drones`, `HubType`) mais logique implicite | `-1` |
| Duplication | `get_start_hub()` et `get_normal_hub()` dupliquent massivement le parsing | `-2` |
| Singleton | Absent | `0` |
| Premature Optimization | Absent | `0` |

**Pénalités cumulées : -7**

---

## 5. Conformité technique

| Critère | Score | Justification |
|---|---|---|
| Type hints | 2/5 | Enums typées, mais parsing sans type hints (beaucoup de `str`, `int` non explicites) |
| Docstrings (PEP 257) | 1/5 | Classe `Hub` a une docstring ; fonctions de parsing aucune |
| Tests unitaires (pytest) | 0/5 | Aucun test |
| Makefile | 3/5 | Présent mais incomplet (besoin de test, lint) |
| `pyproject.toml` | 2/5 | Minimal, pas de dependencies déclarées |
| Gestion des exceptions | 2/5 | Exceptions spécialisées, mais beaucoup de `try-except` génériques |

**Sous-total technique : 10/30**

---

## Récapitulatif

| Catégorie | v1 | Pondération | Score |
|---|---|---|---|
| A — Conformité sujet (Parser partiel) | 2 | / 80 | 3% |
| B — Qualité OOP | 12 | / 20 | 60% |
| C — Principes SOLID | 6 | / 20 | 30% |
| D — Violations STUPID | -7 | / 0 | -7 |
| E — Conformité technique | 10 | / 30 | 33% |
| **TOTAL** | **23** | **/ 150** | **15%** |

---

## Recommandations pour la v2

1. **Compléter le parser** : intégrer correctement les fonctions existantes, générer un objet `Map` structuré
2. **Créer une classe `Connection`** : modéliser les arêtes du graphe
3. **Créer une classe `Graph`** : structurer le réseau complet
4. **Réduire la duplication** : merger `get_start_hub()` et `get_normal_hub()`
5. **Ajouter type hints partout** : passer de 2/5 à 5/5
6. **Écrire des tests** : au moins coverage du parser
7. **Définir des `Protocol` ou `ABC`** : Interface Segregation

---

## Note finale

$$\text{Note v1} = \frac{23}{150} \times 100 \approx \mathbf{15\%}$$

**Appréciation** : **Chantier en cours**. L'architecture est au stade des fondations. Les éléments structurants (enums, exceptions) sont présents, mais l'intégration complète du parser, l'absence de classes `Connection` et `Graph`, et la quasi-absence de conformité technique (tests, type hints, docs) placent ce projet à un stade très précoce. C'est normal pour une v1 active — le code avance clairement, et les prochaines itérations doivent consolider l'architecture OOP et SOLID.
