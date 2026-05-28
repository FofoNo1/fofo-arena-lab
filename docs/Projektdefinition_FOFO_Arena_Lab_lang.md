FOFO Arena Lab

Replay Intelligence by Kapautz

FOFO Arena Lab ist ein Projekt zur kontextbezogenen Analyse von Rocket-League-Replays.

Das Ziel ist es, .replay-Dateien einzulesen, die enthaltenen Spieldaten strukturiert auszuwerten und daraus eine verständliche Analyse des Matches zu erzeugen.

Der Kern des Projekts ist nicht die reine Ausgabe von Statistiken, sondern die Bewertung von Spielsituationen im Kontext.

Viele bestehende Analyse-Tools bewerten einzelne Werte isoliert, zum Beispiel Geschwindigkeit, Boostverbrauch, Positionierung oder Ballkontakte. FOFO Arena Lab soll stattdessen untersuchen, warum ein Spieler in einer bestimmten Situation so gehandelt hat und ob diese Entscheidung unter den gegebenen Umständen sinnvoll, riskant, schlecht oder sogar besonders gut war.

Eine Aktion soll also nicht pauschal bewertet werden, sondern immer im Zusammenhang mit der Spielsituation:

Was war mit dem Ball?
Wo standen die Teammates?
Wo standen die Gegner?
Wie hoch war der Druck?
Wie war der Booststand?
Welche Optionen gab es?
Wie war der Spielstand?
Welche Folge hatte die Entscheidung?

Das Projekt startet mit dem Fokus auf 2v2-Replays, soll aber langfristig so aufgebaut werden, dass auch 3v3-Analysen möglich sind.

Ein wichtiger Bestandteil ist außerdem, nicht nur Fehler oder Schwächen hervorzuheben. FOFO Arena Lab soll auch positive Entscheidungen erkennen und sichtbar machen, damit die Analyse nicht nur kritisiert, sondern auch zeigt, welche Spielzüge, Entscheidungen oder Verhaltensweisen beibehalten werden sollten.

Der grundlegende Ablauf des Projekts lautet:

.replay-Datei
→ Replay parsen
→ verfügbare Daten verstehen
→ eigene stabile Datenstruktur ableiten
→ Spielsituationen erkennen
→ Kontext bewerten
→ Analyse ausgeben

Dabei soll das Projekt bewusst schrittweise entstehen. Welche Datenstrukturen, Klassen, Typen und Analyse-Module benötigt werden, wird erst entschieden, nachdem echte Replay-Daten geparsed und untersucht wurden.

Das Projekt folgt daher dem Prinzip:

Erst Daten verstehen.
Dann Struktur bauen.
Dann Analyse entwickeln.
Dann visualisieren und erweitern.

FOFO Arena Lab soll langfristig ein Werkzeug werden, das aus Replay-Daten echte spielerische Erkenntnisse ableitet: nicht nur „was ist passiert“, sondern vor allem „warum war es relevant“.