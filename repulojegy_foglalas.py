# Készítette: Tadjer Ábrahám Tamás
# Neptun kód: EWOUOG
# Projekt: Repülőjegy foglalási rendszer

from abc import ABC, abstractmethod
from datetime import datetime, date
from typing import List


class Jarat(ABC):
    def __init__(self, jaratszam: str, celallomas: str, jegyar: int) -> None:
        if not jaratszam.strip():
            raise ValueError("A járatszám nem lehet üres.")
        if not celallomas.strip():
            raise ValueError("A célállomás nem lehet üres.")
        if jegyar <= 0:
            raise ValueError("A jegyárnak pozitív számnak kell lennie.")

        self._jaratszam = jaratszam.strip().upper()
        self._celallomas = celallomas.strip()
        self._jegyar = jegyar

    @property
    def jaratszam(self) -> str:
        return self._jaratszam

    @property
    def celallomas(self) -> str:
        return self._celallomas

    @property
    def jegyar(self) -> int:
        return self._jegyar

    @abstractmethod
    def jarat_tipus(self) -> str:
        pass

    def __str__(self) -> str:
        return f"{self._jaratszam} | {self.jarat_tipus()} | {self._celallomas} | {self._jegyar} Ft"


class BelfoldiJarat(Jarat):
    def jarat_tipus(self) -> str:
        return "Belföldi járat"


class NemzetkoziJarat(Jarat):
    def jarat_tipus(self) -> str:
        return "Nemzetközi járat"


class JegyFoglalas:
    _kovetkezo_azonosito = 1

    def __init__(self, utas_nev: str, jarat: Jarat, utazasi_datum: str) -> None:
        if not utas_nev.strip():
            raise ValueError("Az utas neve nem lehet üres.")

        self._foglalas_azonosito = JegyFoglalas._kovetkezo_azonosito
        self._utas_nev = utas_nev.strip()
        self._jarat = jarat
        self._utazasi_datum = self._ervenyes_datum(utazasi_datum)

        JegyFoglalas._kovetkezo_azonosito += 1

    @staticmethod
    def _ervenyes_datum(datum_szoveg: str) -> date:
        try:
            datum = datetime.strptime(datum_szoveg.strip(), "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("Hibás dátumformátum. Helyes forma: ÉÉÉÉ-HH-NN")

        if datum < date.today():
            raise ValueError("Múltbeli dátumra nem lehet foglalni.")

        return datum

    @property
    def foglalas_azonosito(self) -> int:
        return self._foglalas_azonosito

    @property
    def utas_nev(self) -> str:
        return self._utas_nev

    @property
    def jarat(self) -> Jarat:
        return self._jarat

    @property
    def utazasi_datum(self) -> date:
        return self._utazasi_datum

    def __str__(self) -> str:
        return (
            f"Azonosító: {self._foglalas_azonosito} | "
            f"Utas: {self._utas_nev} | "
            f"Járat: {self._jarat.jaratszam} | "
            f"Célállomás: {self._jarat.celallomas} | "
            f"Dátum: {self._utazasi_datum} | "
            f"Ár: {self._jarat.jegyar} Ft"
        )


class LegiTarsasag:
    def __init__(self, nev: str) -> None:
        if not nev.strip():
            raise ValueError("A légitársaság neve nem lehet üres.")

        self._nev = nev.strip()
        self._jaratok: List[Jarat] = []
        self._foglalasok: List[JegyFoglalas] = []

    @property
    def nev(self) -> str:
        return self._nev

    def jarat_hozzaadasa(self, jarat: Jarat) -> None:
        for aktualis_jarat in self._jaratok:
            if aktualis_jarat.jaratszam == jarat.jaratszam:
                raise ValueError("Ilyen járatszám már létezik.")

        self._jaratok.append(jarat)

    def jaratok_listazasa(self) -> None:
        print("\n--- Elérhető járatok ---")

        if not self._jaratok:
            print("Nincs rögzített járat.")
            return

        for jarat in self._jaratok:
            print(jarat)

    def _jarat_keresese(self, jaratszam: str) -> Jarat:
        keresett_jaratszam = jaratszam.strip().upper()

        for jarat in self._jaratok:
            if jarat.jaratszam == keresett_jaratszam:
                return jarat

        raise ValueError("Nem található ilyen járatszámú járat.")

    def jegy_foglalasa(self, utas_nev: str, jaratszam: str, utazasi_datum: str) -> int:
        jarat = self._jarat_keresese(jaratszam)

        for foglalas in self._foglalasok:
            ugyanaz_a_jarat = foglalas.jarat.jaratszam == jarat.jaratszam
            ugyanaz_a_datum = str(foglalas.utazasi_datum) == utazasi_datum.strip()
            ugyanaz_az_utas = foglalas.utas_nev.lower() == utas_nev.strip().lower()

            if ugyanaz_a_jarat and ugyanaz_a_datum and ugyanaz_az_utas:
                raise ValueError("Ez a foglalás már létezik.")

        foglalas = JegyFoglalas(utas_nev, jarat, utazasi_datum)
        self._foglalasok.append(foglalas)

        return jarat.jegyar

    def foglalas_lemondasa(self, foglalas_azonosito: int) -> None:
        for index, foglalas in enumerate(self._foglalasok):
            if foglalas.foglalas_azonosito == foglalas_azonosito:
                del self._foglalasok[index]
                return

        raise ValueError("Nem létezik ilyen azonosítójú foglalás.")

    def foglalasok_listazasa(self) -> None:
        print("\n--- Aktív foglalások ---")

        if not self._foglalasok:
            print("Jelenleg nincs aktív foglalás.")
            return

        for foglalas in self._foglalasok:
            print(foglalas)

    def elokeszites(self) -> None:
        self.jarat_hozzaadasa(BelfoldiJarat("B101", "Debrecen", 15000))
        self.jarat_hozzaadasa(BelfoldiJarat("B202", "Pécs", 12000))
        self.jarat_hozzaadasa(NemzetkoziJarat("N303", "Berlin", 45000))

        kezdo_foglalasok = [
            ("Kiss Anna", "B101", "2026-06-20"),
            ("Nagy Péter", "B202", "2026-06-21"),
            ("Tóth Júlia", "N303", "2026-06-22"),
            ("Szabó Márk", "B101", "2026-06-23"),
            ("Varga Éva", "N303", "2026-06-24"),
            ("Kovács Dániel", "B202", "2026-06-25"),
        ]

        for utas_nev, jaratszam, datum in kezdo_foglalasok:
            self.jegy_foglalasa(utas_nev, jaratszam, datum)


def menu() -> None:
    legitarsasag = LegiTarsasag("SkyLine Airways")
    legitarsasag.elokeszites()

    while True:
        print(f"\n--- {legitarsasag.nev} repülőjegy foglalási rendszer ---")
        print("1 - Járatok listázása")
        print("2 - Jegy foglalása")
        print("3 - Foglalás lemondása")
        print("4 - Foglalások listázása")
        print("0 - Kilépés")

        valasztas = input("Választás: ").strip()

        try:
            if valasztas == "1":
                legitarsasag.jaratok_listazasa()

            elif valasztas == "2":
                legitarsasag.jaratok_listazasa()

                utas_nev = input("\nUtas neve: ")
                jaratszam = input("Járatszám: ")
                utazasi_datum = input("Utazási dátum (ÉÉÉÉ-HH-NN): ")

                ar = legitarsasag.jegy_foglalasa(utas_nev, jaratszam, utazasi_datum)
                print(f"Sikeres foglalás. Fizetendő ár: {ar} Ft")

            elif valasztas == "3":
                legitarsasag.foglalasok_listazasa()

                azonosito = input("\nLemondandó foglalás azonosítója: ").strip()

                if not azonosito.isdigit():
                    raise ValueError("Az azonosítónak pozitív egész számnak kell lennie.")

                legitarsasag.foglalas_lemondasa(int(azonosito))
                print("A foglalás sikeresen lemondva.")

            elif valasztas == "4":
                legitarsasag.foglalasok_listazasa()

            elif valasztas == "0":
                print("Kilépés...")
                break

            else:
                print("Érvénytelen menüpont.")

        except ValueError as hiba:
            print(f"Hiba: {hiba}")

        except Exception as hiba:
            print(f"Váratlan hiba történt: {hiba}")


if __name__ == "__main__":
    menu()