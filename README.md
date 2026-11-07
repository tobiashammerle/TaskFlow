# TaskFlow

Ein Python-Backend-Projekt zur professionellen Aufgabenverwaltung

TaskFlow ist eine Aufgabenverwaltungsanwendung, die im Rahmen eines praxisorientierten Python-Software-Engineering-Lehrgangs entwickelt wurde.

Ziel des Projekts ist es, wichtige Prinzipien professioneller Backend-Entwicklung praktisch umzusetzen: saubere Architektur, automatisierte Tests, Datenbankzugriff, Sicherheit, Versionsverwaltung, Containerisierung, CI/CD und Monitoring.

Funktionen

- Aufgaben erstellen, anzeigen, bearbeiten und löschen
- Aufgaben als erledigt markieren
- Aufgaben suchen, filtern und sortieren
- Prioritäten und Fälligkeitstermine verwalten
- Benutzerbezogene Aufgabenverwaltung
- Authentifizierung und geschützte API-Endpunkte
- Anzahl offener Aufgaben abrufen
- Asynchrone Datenbankzugriffe

Technologien

Bereich| Technologie
Programmiersprache| Python 3.12+
Webframework| FastAPI
ASGI-Server| Uvicorn
Datenbankzugriff| SQLAlchemy, aiosqlite
Datenbankmigrationen| Alembic
Authentifizierung| PyJWT, Argon2
Tests| pytest, pytest-asyncio, pytest-cov
Codequalität| Ruff, mypy, pre-commit
Versionsverwaltung| Git, GitHub
Containerisierung| Docker
Orchestrierung| Kubernetes
Deployment-Verwaltung| Helm
CI/CD| GitHub Actions
Monitoring| Prometheus, Grafana

Architektur

TaskFlow orientiert sich an den Prinzipien der Clean Architecture.

Die Anwendung trennt verschiedene Verantwortlichkeiten:

- Domain: Fachliche Modelle und Geschäftsregeln
- Application / Use Cases: Anwendungsfälle und Geschäftsabläufe
- Repositories: Abstraktion des Datenzugriffs
- Infrastructure: Technische Implementierungen, beispielsweise SQLAlchemy
- API / Router: HTTP-Endpunkte und Verarbeitung von Anfragen
- Dependency Injection: Bereitstellung austauschbarer Abhängigkeiten

Diese Trennung erleichtert die Wartung, Erweiterung und automatisierte Überprüfung der Anwendung.

Installation

Voraussetzungen:

- Python 3.12 oder neuer
- Git
- Optional: Docker

Repository klonen:

git clone <REPOSITORY-URL>
cd TaskFlow

Virtuelle Umgebung erstellen und aktivieren:

python -m venv .venv
.\.venv\Scripts\Activate.ps1

Projekt einschließlich Entwicklungswerkzeugen installieren:

python -m pip install -e ".[dev]"

Konfiguration

Die Datei ".env.example" enthält eine Beispielkonfiguration:

LOG_LEVEL=INFO

Für die lokale Entwicklung kann daraus eine ".env"-Datei erstellt werden:

Copy-Item .env.example .env

Weitere erforderliche Einstellungen hängen von der verwendeten Datenbank- und Deployment-Konfiguration ab.

Geheime Zugangsdaten gehören nicht ins Git-Repository.

Backend starten

Die FastAPI-Anwendung befindet sich in "src/taskflow/api.py".

Lokaler Entwicklungsstart:

uvicorn taskflow.api:app --reload

Standardadresse:

"http://127.0.0.1:8000"

Interaktive API-Dokumentation:

"http://127.0.0.1:8000/docs"

Alternative OpenAPI-Dokumentation:

"http://127.0.0.1:8000/redoc"

Der Parameter "--reload" ist für die lokale Entwicklung vorgesehen, nicht für den Produktivbetrieb.

Tests

Alle automatisierten Tests ausführen:

pytest -q

Testabdeckung prüfen:

pytest --cov=taskflow --cov-report=term-missing

Beim abschließenden Testlauf des Lehrgangs wurden 270 Tests erfolgreich ausgeführt.

Codequalität

Ruff:

ruff check .

mypy:

mypy src

pre-commit:

pre-commit run --all-files

Die automatisierten Prüfungen unterstützen eine konsistente und wartbare Codebasis.

Docker

Das Projekt enthält ein "Dockerfile" und eine "compose.yaml".

Container-Image erstellen:

docker build -t taskflow:local .

Die konkrete Ausführung mit Docker Compose richtet sich nach den konfigurierten Diensten und Umgebungsvariablen.

Kubernetes und Helm

TaskFlow enthält Kubernetes-Konfigurationen im Verzeichnis "k8s/" und ein Helm-Chart unter "taskflow-chart/".

Kubernetes verwaltet die Bereitstellung und den Betrieb containerisierter Anwendungen.

Helm erleichtert die wiederholbare Installation und Konfiguration der Kubernetes-Ressourcen.

CI/CD

TaskFlow verwendet GitHub Actions zur Automatisierung wichtiger Entwicklungsschritte.

Die Pipeline umfasst:

1. Automatisierte Tes
[12:48, 7.11.2026] Tobias Hammerle: TaskFlow

Ein Python-Backend-Projekt zur professionellen Aufgabenverwaltung

TaskFlow ist eine Aufgabenverwaltungsanwendung, die im Rahmen eines praxisorientierten Python-Software-Engineering-Lehrgangs entwickelt wurde.

Ziel des Projekts ist es, wichtige Prinzipien professioneller Backend-Entwicklung praktisch umzusetzen: saubere Architektur, automatisierte Tests, Datenbankzugriff, Sicherheit, Versionsverwaltung, Containerisierung, CI/CD und Monitoring.

Funktionen

- Aufgaben erstellen, anzeigen, bearbeiten und löschen
- Aufgaben als erledigt markieren
- Aufgaben suchen, filtern und sortieren
- Prioritäten und Fälligkeitstermine verwalten
- Benutzerbezogene Aufgabenverwaltung
- Authentifizierung und geschützte API-Endpunkte
- Anzahl offener Aufgaben abrufen
- Asyn…
[12:50, 7.11.2026] Tobias Hammerle: Kubernetes und Helm
TaskFlow enthält Kubernetes-Konfigurationen im Verzeichnis k8s/ und ein Helm-Chart unter taskflow-chart/.
Kubernetes verwaltet die Bereitstellung und den Betrieb containerisierter Anwendungen.
Helm erleichtert die wiederholbare Installation und Konfiguration der Kubernetes-Ressourcen.
CI/CD
TaskFlow verwendet GitHub Actions zur Automatisierung wichtiger Entwicklungsschritte.
Die Pipeline umfasst:
Automatisierte Tests und Qualitätsprüfungen
Erstellung eines Docker-Images
Deployment in die konfigurierte Zielumgebung
Ziel ist es, Änderungen reproduzierbar zu prüfen und bereitzustellen.
Monitoring
TaskFlow verwendet Prometheus-Instrumentierung zur Erfassung technischer Messwerte.
Prometheus dient der Sammlung und Speicherung von Metriken.
Grafana ermöglicht deren grafische Darstellung und Auswertung.
Dadurch lassen sich beispielsweise Antwortzeiten, Anfragen und Fehler während des Betriebs beobachten.
Projektstatus
Version: 0.1.0
Status: Lernprojekt mit implementierter Backend-Architektur, automatisierten Tests und DevOps-Infrastruktur.
Das Projekt dient als Grundlage für weitere praktische Lernschritte, beispielsweise die Entwicklung eines Frontends und dessen Anbindung an die FastAPI-Schnittstelle.
Hintergrund
TaskFlow wurde entwickelt, um den gesamten Lebenszyklus einer Backend-Anwendung kennenzulernen: von der Planung über die Implementierung und Qualitätssicherung bis zur automatisierten Bereitstellung und Überwachung.
Im Mittelpunkt stehen verständlicher Code, klare Verantwortlichkeiten, Testbarkeit und professionelle Entwicklungsabläufe.