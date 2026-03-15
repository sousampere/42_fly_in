# Feedback — Fly-in-2

> Analyse du projet au regard des règles **OOP**, **SOLID** et **STUPID**.  
> Date : 12 mars 2026 — Révision v5

> **Note de contexte architectural** : Les modèles Pydantic (`HubModel`, `ConnectionModel`, `MapModel`) sont des **DTOs de parsing intentionnels et transitoires**. Leur absence de comportement métier est un choix délibéré — la logique active sera portée par les objets domaine (`Node`, `Link`) en cours de scaffolding. Ce choix est pris en compte dans l'analyse.

---

## Résumé des changements depuis la v4

| Point modifié | Avant (v4) | Après (v5) |
|---|---|---|
| `exit_programm` | Typo persistante | ✅ `exit_program` corrigé |
| `exit_program()` | `os._exit(0)` dans `Controller` | ✅ `raise ControllerError` — Controller testable |
| `ControllerError` | Absent | ✅ Exception propre pour signaler la sortie |
| Injection de `RunSecurity` | Instanciée en dur dans `Controller` | ✅ Injectée via constructeur (`secure_env: Optional[RunSecurity]`) |
| `src/__init__.py` | Exportait `Controller` | ✅ Exporte `Controller` et `ControllerError` |
| `_check_dependencies` | `_` protégé, incohérent | ✅ `__check_dependencies` (privé, cohérent) |
| Magic number `11` | `data.pop(0)[11::]` | ✅ `data.pop(0).split(":")[1]` |
| `MapEmptyError` | Absent | ✅ Fichier vide ou 100% commentaires → `MapEmptyError` |
| Validation préfix inconnu | Partielle | ✅ `MapPrefixError` si préfixe hub/connexion inconnu |
| `MapNbDronesError` 1ère ligne | Absent | ✅ Lève `MapNbDronesError` si 1ère ligne n'est pas `nb_drones:` |
| Tests unitaires | 11 | ✅ 15 (4 nouveaux : empty, no_drone_line, invalid_hub_type, invalid_prefix_connection) |

---

## 1. État général du projet

| Composant attendu (sujet) | Présent | Complet |
|---|---|---|
| Parser de la map | ✅ | ✅ Complet |
| Structure domaine (Graph, Simulation) | ✅ | ❌ Fichiers vides |
| Moteur de simulation | ❌ | — |
| Algorithme de pathfinding | ❌ | — |
| Représentation visuelle | ❌ | — |
| README.md complet | ⚠️ | ❌ Toujours vide (`# Fly-In`) |
| Tests unitaires | ✅ | ⚠️ Parser uniquement, 15 tests |

L'architecture de base est **complète et solide**. Cette itération clôt toutes les dettes techniques mineures identifiées en v4. Le prochain palier ne peut venir que de l'implémentation des fonctionnalités métier.

---

## 2. Analyse OOP

### ✅ Corrections notables

**`ControllerError` + `exit_program()` : sortie propre sans `os._exit`.**

C'est la correction structurelle majeure de cette itération. `Controller.exit_program()` lève désormais une exception :

```python
def exit_program(self) -> NoReturn:
    self.logger.info("Programm exit")
    input("\n\nPress Enter to exit...")
    raise ControllerError("Programm exit")
```

Et `main.py` l'attrape proprement :

```python
try:
    controller.process()
except ControllerError:
    pass
```

`Controller` ne dépend plus du comportement de sortie de l'OS. Il est maintenant **entièrement testable** unitairement.

**Injection de `RunSecurity` via constructeur.**

```python
def __init__(self, map_path: str, secure_env: Optional[RunSecurity] = None) -> None:
```

`RunSecurity` n'est plus instanciée en dur dans `Controller`. La dépendance est injectée depuis `main.py`, ce qui permet de tester `Controller` sans environnement réel et respecte le principe **Tell, Don't Ask** étendu.

**`__check_dependencies` : cohérence complète de l'API interne `RunSecurity`.**

Toutes les méthodes de `RunSecurity` sont maintenant `__` (double underscore). L'API publique se réduit à `check_process()`. Aucune incohérence de visibilité ne subsiste.

**Magic number `11` supprimé.**

```python
# Avant (v4)
value: str = data.pop(0)[11::]

# Après (v5)
value: str = data.pop(0).split(":")[1]
```

Le code est maintenant auto-documenté : on extrait la valeur après le séparateur `:`, sans dépendre d'un offset hardcodé.

**`MapEmptyError`, `MapPrefixError`, `MapNbDronesError` : robustesse du parser complétée.**

Tous les cas dégénérés d'entrée ont maintenant leur exception propre :
- Fichier vide ou 100% commentaires → `MapEmptyError`
- Première ligne sans `nb_drones:` → `MapNbDronesError`
- Préfixe de ligne inconnu → `MapPrefixError`

Les 15 tests couvrent l'intégralité de ces cas.

### ⚠️ Points résiduels

#### `assert` en production

```python
assert self.__map_model is not None
return self.__map_model
```
Toujours présent dans `MapParser.process()`. Désactivable avec `-O`. Remplacer par une guard explicite :

```python
if self.__map_model is None:
    raise MapError("Unexpected None map model")
return self.__map_model
```

#### `nb_drones: 0` → `ValidationError` non wrappée

`nb_drones: 0` passe la conversion `int()` mais échoue à la validation Pydantic (`ge=1`). La `ValidationError` remonte directement au lieu d'être wrappée en `MapNbDronesError`. Le test `test_zero_drone` attrape `ValidationError` directement — fuite d'abstraction intentionnellement laissée.

#### `Node.py`, `Link.py`, `drone.py` : fichiers vides

Le scaffolding est présent mais non implémenté. Ce n'est pas un défaut en soi — c'est une intention déclarée — mais l'analyse ne peut pas encore évaluer la qualité de ces couches.

#### `Controller` sans docstrings

La classe `Controller` et ses méthodes (`process`, `__read_file`, `__parse_content`) ne sont pas documentées. Toutes les autres classes (`MapParser`, `RunSecurity`, `HubModel`, etc.) ont leurs docstrings.

---

## 3. Analyse SOLID

### S — Single Responsibility Principle

| Composant | Constat |
|---|---|
| `main.py` | ✅ Bootstrap + spawn terminal uniquement |
| `Controller` | ✅ Orchestration du flux principal |
| `MapParser` | ✅ Parsing uniquement |
| `RunSecurity` | ✅ Vérification d'environnement runtime |
| `ControllerError` | ✅ Signal de sortie propre |

La séparation des responsabilités est **maximale** sur la couche infrastructure.

### O — Open/Closed Principle

- `src/graph/algorithms/` vide : signal d'ouverture à l'extension. Plusieurs algorithmes pourront être ajoutés sans modifier le graph. ✅ (intention)
- Le parsing de lignes reste ad hoc — ajouter un type de ligne impose toujours de modifier les méthodes existantes.

### L — Liskov Substitution Principle

✅ Inchangé, aucune régression. Hiérarchies d'erreurs irréprochables.

### I — Interface Segregation Principle

Toujours aucune `Protocol`/`ABC` définie. `src/graph/algorithms/` reste le lieu naturel pour introduire une `Protocol IPathfinder`. C'est maintenant le seul manque structurel en SOLID.

### D — Dependency Inversion Principle

- `Controller` ne connaît plus directement l'implémentation de `RunSecurity` — elle est injectée. ✅
- `main.py` injecte `RunSecurity()` : la composition se fait à la périphérie. ✅
- `Controller` dépend encore directement de `MapParser` (concret). Une injection supplémentaire serait possible mais non urgente.
- `MapModel` importe toujours directement les classes d'erreurs — ce couplage disparaîtra avec les objets actifs.

---

## 4. Analyse STUPID

### S — Singleton
Absent. ✅

### T — Tight Coupling (Couplage fort)

- **Terminal** : `TERMINAL: list[str] = ["gnome-terminal", "--"]` toujours hardcodé dans `main.py`. Portabilité limitée. Acceptable pour un projet d'étude mais reste un couplage.
- `os._exit(0)` a quitté `Controller`. Il reste dans `main.py` pour la gestion du processus de spawn terminal — c'est son rôle naturel. ✅

### U — Untestability

| Composant | Testabilité |
|---|---|
| `MapParser` | ✅ Entièrement testable (15 tests) |
| `RunSecurity.check_process()` | ✅ Lève `RunEnvironmentError` → mockable |
| `Controller.process()` | ✅ Lève `ControllerError` → testable unitairement |
| `main.py` | ⚠️ Spawn terminal + `os._exit(0)` non-testables (attendu) |
| `test_zero_drone` | ⚠️ Attrape `ValidationError` directement — fuite d'abstraction |

`Controller` est maintenant **entièrement testable**. C'est la correction majeure sur ce critère.

### P — Premature Optimization
Absent. ✅

### I — Indescriptive Naming

Tous les problèmes de nommage identifiés en v4 ont été corrigés :

| Symbole | Avant | Après |
|---|---|---|
| Magic number `11` | `data.pop(0)[11::]` | ✅ `data.pop(0).split(":")[1]` |
| `_check_dependencies` | `_` (protégé, incohérent) | ✅ `__check_dependencies` |
| `exit_programm` | Faute d'orthographe | ✅ `exit_program` |

Note : les messages de log contiennent encore `"Programm starting"` et `"Programm exit"` — faute dans les chaînes, non dans les symboles.

### D — Duplication
✅ Aucune duplication significative.

---

## 5. Conformité au sujet

### Parser — état final

| Validation requise | État |
|---|---|
| Format `nb_drones: <entier positif>` | ✅ |
| Première ligne obligatoirement `nb_drones:` | ✅ |
| Fichier vide ou 100% commentaires | ✅ `MapEmptyError` |
| Préfixe inconnu | ✅ `MapPrefixError` |
| `start_hub` / `end_hub` uniques | ✅ |
| Noms de hubs uniques | ✅ |
| Connexions vers hubs définis uniquement | ✅ |
| Connexions dupliquées (a-b = b-a) | ✅ |
| `max_link_capacity` entier positif | ✅ |
| `max_drones` entier positif | ⚠️ Pas de contrainte `ge=1` sur `HubModel.max_drones` |
| `nb_drones: 0` → `MapError` | ⚠️ Lève `ValidationError` Pydantic directement (non wrappée) |

### README.md
Contient uniquement `# Fly-In`. **Toutes les sections obligatoires du sujet sont absentes.**

---

## 6. Points forts consolidés

- **Architecture `src/` claire et intentionnelle** : `parsing/`, `graph/`, `simulation/`, `utils/` → séparation domaine propre.
- **`Controller`** : testable, injection propre, sortie via exception. Architecture exemplaire.
- **`RunSecurity`** : encapsulation totale, API publique réduite à `check_process()`.
- **Parser complet, robuste, testé** : 15 tests couvrant tous les cas d'erreur connus.
- **Zéro dette technique de nommage** : magic numbers, typos et incohérences de visibilité tous corrigés.
- **`MapParser` idempotent** grâce au `.copy()`.
- **Scaffolding domaine pensé** : Graph / Simulation séparés, dossier `algorithms/` prévu.
- **Docstrings, type hints, Makefile** : toujours au niveau.

---

## 7. Priorités restantes

1. **Implémenter `Node` et `Link`** — objets actifs du domaine, transfert logique depuis les DTOs Pydantic.
2. **Définir `IPathfinder` (Protocol)** dans `src/graph/algorithms/` **avant** d'implémenter les algorithmes.
3. **Implémenter le moteur de simulation** — bloquant pour l'évaluation.
4. **Implémenter un algorithme de pathfinding**.
5. **Représentation visuelle**.
6. **Écrire le README.md** — toujours obligatoire et vide.
7. **Wrapper `nb_drones: 0`** → `MapNbDronesError` au lieu de laisser remonter `ValidationError`.
8. **Ajouter `ge=1`** sur `HubModel.max_drones`.
9. **Remplacer l'`assert`** par une guard explicite dans `MapParser.process()`.
10. **Documenter `Controller`** et ses méthodes (docstrings manquantes).
11. **Corriger les chaînes de log** : `"Programm starting"` / `"Programm exit"` → `"Program"`.
