from datetime import datetime, date
import sys

class Szoba:
    def __init__(self, szobaszam: int, ar: int):
        self.szobaszam = szobaszam
        self.ar = ar

    def get_ar(self):
        return self.ar

    def get_szobaszam(self):
        return self.szobaszam

class EgyagyasSzoba(Szoba):
    pass

class KetagyasSzoba(Szoba):
    pass

class HaromagyasSzoba(Szoba):
    pass

class Foglalas:
    def __init__(self, szoba: Szoba, datum: date, foglalo_nev: str):
        self.szoba = szoba
        self.datum = datum
        self.foglalo_nev = foglalo_nev

    def get_szoba(self):
        return self.szoba

    def get_datum(self):
        return self.datum

    def get_foglalo_nev(self):
        return self.foglalo_nev

class Szalloda:
    def __init__(self, nev: str):
        self.nev = nev
        self.szobak = []
        self.foglalasok = []

    def add_szoba(self, szoba: Szoba):
        self.szobak.append(szoba)

    def lemond_foglalas(self, szobaszam: int, datum: date):
        for foglalas in self.foglalasok:
            if foglalas.get_szoba().get_szobaszam() == szobaszam and foglalas.get_datum() == datum:
                self.foglalasok.remove(foglalas)
                return True
        return False

    def foglal_szoba(self, szobaszam: int, datum: date, foglalo_nev: str):
        for foglalas in self.foglalasok:
            if foglalas.get_szoba().get_szobaszam() == szobaszam and foglalas.get_datum() == datum:
                raise ValueError("A szoba ezen a napon már foglalt.")
        for szoba in self.szobak:
            if szoba.get_szobaszam() == szobaszam:
                new_foglalas = Foglalas(szoba, datum, foglalo_nev)
                self.foglalasok.append(new_foglalas)
                return szoba.get_ar()
        raise ValueError("Nincs ilyen számú szoba a szállodában.")

    def listaz_foglalasok(self):
        if not self.foglalasok:
            print("Nincsenek jelenleg foglalások.")
            return
        print("Foglalások listája:")
        for foglalas in self.foglalasok:
            print(f"Szobaszám: {foglalas.get_szoba().get_szobaszam()}, Dátum: {foglalas.get_datum()}, Foglaló neve: {foglalas.get_foglalo_nev()}, Ár: {foglalas.get_szoba().get_ar()} Ft")

class SzallodaInterface:
    def __init__(self):
        self.szalloda = Szalloda("Grand Tokaj")
        self.szalloda.add_szoba(EgyagyasSzoba(1, 20000))
        self.szalloda.add_szoba(KetagyasSzoba(2, 30000))
        self.szalloda.add_szoba(KetagyasSzoba(3, 35000))

    def start(self):
        while True:
            print("\nGrand Tokaj")
            print("Válassz egy opciót:")
            print("1. Foglalás")
            print("2. Lemondás")
            print("3. Listázás")
            print("4. Kilépés")
            choice = input("Opció: ")
            if choice == "1":
                self.handle_reservation()
            elif choice == "2":
                self.handle_cancellation()
            elif choice == "3":
                self.szalloda.listaz_foglalasok()
            elif choice == "4":
                print("Kilépés...")
                sys.exit()
            else:
                print("Érvénytelen opció.")

    def handle_reservation(self):
        try:
            room_number = int(input("Add meg a szobaszámot (1: Egyágyas szoba, 2: Kétágyas szoba, 3: Háromágyas szoba): "))
            if room_number not in [1, 2, 3]:
                print("Nincs ilyen számú szoba.")
                return
            date_str = input("Add meg a dátumot (yyyy-mm-dd): ")
            datum = datetime.strptime(date_str, '%Y-%m-%d').date()
            if datum < date.today():
                print("A dátum nem lehet a múltban!")
                return
            reserver_name = input("Add meg a foglaló nevét: ")
            price = self.szalloda.foglal_szoba(room_number, datum, reserver_name)
            print(f"Foglalás sikeres. Ár: {price} Ft")
        except ValueError as e:
            print(str(e))
        except Exception as e:
            print("Hiba történt:", str(e))

    def handle_cancellation(self):
        try:
            room_number = int(input("Add meg a szobaszámot: "))
            date_str = input("Add meg a dátumot (yyyy-mm-dd): ")
            datum = datetime.strptime(date_str, '%Y-%m-%d').date()
            if self.szalloda.lemond_foglalas(room_number, datum):
                print("Lemondás sikeres.")
            else:
                print("Nincs ilyen foglalás.")
        except Exception as e:
            print("Hiba történt:", str(e))

if __name__ == "__main__":
    interface = SzallodaInterface()
    interface.start()
