# oop-beadando
# Repülőjegy Foglalási Rendszer

Ez a projekt egy egyszerű konzolos repülőjegy foglalási rendszer Python nyelven, objektumorientált programozási szemlélettel elkészítve.

A rendszer lehetővé teszi:
- járatok listázását
- jegyek foglalását
- foglalások lemondását
- aktuális foglalások megtekintését

## Projekt célja

A projekt az Objektumorientált Programozás tantárgy kötelező beadandó feladata számára készült.  
A fejlesztés során a cél egy egyszerű, jól átlátható és működő repülőjegy foglalási rendszer létrehozása volt.

## Használt technológiák

- Python 3
- Objektumorientált programozás
- Absztrakt osztályok
- Öröklődés
- Hibakezelés
- Property-k
- Non-public attribútumok

## Főbb osztályok

### Jarat
Absztrakt alaposztály, amely a járatok közös attribútumait tartalmazza:
- járatszám
- célállomás
- jegyár

### BelfoldiJarat
A belföldi járatok megvalósítása.

### NemzetkoziJarat
A nemzetközi járatok megvalósítása.

### JegyFoglalas
Egy konkrét repülőjegy foglalást reprezentál.
Tárolja:
- utas neve
- járat
- utazási dátum
- foglalás azonosító

### LegiTarsasag
A rendszer központi osztálya.
Feladata:
- járatok kezelése
- foglalások kezelése
- foglalások törlése
- induláskori adatok betöltése

## Funkciók

- Járatok listázása
- Új jegy foglalása
- Foglalás törlése
- Foglalások listázása
- Dátumellenőrzés
- Hibakezelés
- Duplikált foglalások tiltása

## Induláskori adatok

A rendszer automatikusan betölt:
- 1 légitársaságot
- 3 járatot
- 6 előre létrehozott foglalást


## Fejlesztő

Tadjer Ábrahám Tamás


