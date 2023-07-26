import pygame

class Plansza():
    def __init__(self,wzor = "#OO\nO*O\nOO#"):
        temp = wzor.split()
        self.wysokosc = len(temp)
        self.szerokosc = len(temp[0])
        self.tablica = []
        self.lista_kulek = []
        self.stos_cofnij = []
        for line in temp:
            to_append = []
            for character in line:
                nowa_kulka = Kulka(character)
                to_append.append(nowa_kulka)
                self.lista_kulek.append(nowa_kulka)
            self.tablica.append(to_append)
        self.wybrana = 0
        self.aktualizuj()

    def rysuj(self):
        for i, line in enumerate(self.tablica):
            for j, kulka in enumerate(line):
                y_kulki = (i+1)*(WYS/(self.wysokosc+1))
                x_kulki = (j+1)*(SZER/(self.szerokosc+1))
                if kulka.czy_wybrana:
                    pygame.draw.circle(screen, kulka.kolor_wybrana, (x_kulki, y_kulki), kulka.rozmiar+kulka.zaznaczenie, 0)
                pygame.draw.circle(screen, kulka.kolor, (x_kulki,y_kulki),kulka.rozmiar,0)

    def wybierz(self, kierunek):
        self.lista_kulek[self.wybrana].czy_wybrana = False
        self.wybrana = (self.wybrana+kierunek+len(self.lista_kulek))%len(self.lista_kulek)
        counter = self.szerokosc * self.wysokosc
        while not self.lista_kulek[self.wybrana].czy_mozna_wybrac and counter>0:
            counter -= 1
            self.wybrana = (self.wybrana + kierunek + len(self.lista_kulek)) % len(self.lista_kulek)
        if counter>0:
            self.lista_kulek[self.wybrana].czy_wybrana=True
        else:
            self.wybrana = -1

    def aktualizuj(self):
        for i, line in enumerate(self.tablica):
            for j, kulka in enumerate(line):
                kulka.czy_mozna_wybrac = False
                kulka.ruchy = []
                if kulka.czy_kulka:
                    if i>1:
                        if self.tablica[i-1][j].czy_kulka and self.tablica[i-2][j].czy_wolne:
                            kulka.czy_mozna_wybrac = True
                            kulka.ruchy.append(UP)
                    if i<self.wysokosc-2:
                        if self.tablica[i+1][j].czy_kulka and self.tablica[i+2][j].czy_wolne:
                            kulka.czy_mozna_wybrac = True
                            kulka.ruchy.append(DOWN)
                    if j>1:
                        if self.tablica[i][j-1].czy_kulka and self.tablica[i][j-2].czy_wolne:
                            kulka.czy_mozna_wybrac = True
                            kulka.ruchy.append(LEFT)
                    if j<self.szerokosc-2:
                        if self.tablica[i][j+1].czy_kulka and self.tablica[i][j+2].czy_wolne:
                            kulka.czy_mozna_wybrac = True
                            kulka.ruchy.append(RIGHT)
        self.wybierz(1)

    def ruch(self):
        if self.wybrana == -1:
            return
        kulka = self.lista_kulek[self.wybrana]
        do_polozenia = None
        do_podniesienia = None
        if len(kulka.ruchy) == 1:
            ruch = kulka.ruchy[0]
        else:
            stary_kolor = kulka.kolor
            nowy_kolor = pygame.Color(100,100,250)
            kulka.kolor = nowy_kolor
            self.rysuj()
            pygame.display.update()
            kulka.kolor = stary_kolor
            stop = False
            while not stop:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        quit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key in (pygame.K_LEFT, pygame.K_a):
                            ruch = LEFT
                            stop = True
                        elif event.key in (pygame.K_RIGHT, pygame.K_d):
                            ruch = RIGHT
                            stop = True
                        elif event.key in (pygame.K_UP, pygame.K_w):
                            ruch = UP
                            stop = True
                        elif event.key in (pygame.K_DOWN, pygame.K_s):
                            ruch = DOWN
                            stop = True

        if ruch == UP:
            do_polozenia = self.lista_kulek[self.wybrana-self.szerokosc*2]
            do_podniesienia = self.lista_kulek[self.wybrana-self.szerokosc]
        if ruch == DOWN:
            do_polozenia = self.lista_kulek[self.wybrana + self.szerokosc * 2]
            do_podniesienia = self.lista_kulek[self.wybrana + self.szerokosc]
        if ruch == LEFT:
            do_polozenia = self.lista_kulek[self.wybrana - 2]
            do_podniesienia = self.lista_kulek[self.wybrana - 1]
        if ruch == RIGHT:
            do_polozenia = self.lista_kulek[self.wybrana + 2]
            do_podniesienia = self.lista_kulek[self.wybrana + 1]
        do_polozenia.poloz_kulke()
        do_podniesienia.podnies_kulke()
        kulka.podnies_kulke()
        self.stos_cofnij.append(do_polozenia)
        self.stos_cofnij.append(do_podniesienia)
        self.stos_cofnij.append(kulka)
        self.aktualizuj()

    def cofnij(self):
        if len(self.stos_cofnij) == 0:
            return
        self.stos_cofnij.pop().poloz_kulke()
        self.stos_cofnij.pop().poloz_kulke()
        self.stos_cofnij.pop().podnies_kulke()
        self.aktualizuj()


class Kulka():
    def __init__(self,type):
        self.ruchy = []
        self.czy_wybrana = False
        self.czy_mozna_wybrac = False
        self.czy_kulka = False
        self.czy_wolne = False
        self.kolor_wybrana = pygame.Color(255,200,15)
        self.zaznaczenie = 10
        if type == 'O':
            self.kolor = pygame.Color(220,0,0)
            self.rozmiar = 20
            self.czy_kulka = True
        elif type == "*":
            self.kolor = pygame.Color(0,0,0)
            self.rozmiar = 10
            self.czy_wolne = True
        else:
            self.kolor = KOLOR_TLA
            self.rozmiar = 0

    def poloz_kulke(self):
        self.kolor = pygame.Color(220, 0, 0)
        self.rozmiar = 20
        self.czy_kulka = True
        self.czy_wolne = False

    def podnies_kulke(self):
        self.kolor = pygame.Color(0, 0, 0)
        self.rozmiar = 10
        self.czy_wolne = True
        self.czy_kulka = False

UP = "UP"
DOWN ="DOWN"
LEFT = "LEFT"
RIGHT = "RIGHT"
pygame.init()
SZER = 800
WYS = 640
KOLOR_TLA = pygame.Color(25,130,55)
screen = pygame.display.set_mode((SZER,WYS))
pygame.display.set_caption("Peg Solitare")

clock =pygame.time.Clock()
i = 1
a = True
tempo= 200

plansza = Plansza("""##OOO##
##OOO##
OOOOOOO
OOO*OOO
OOOOOOO
##OOO##
##OOO##""")

while True:
    screen.fill(pygame.Color(KOLOR_TLA))
    plansza.rysuj()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_LEFT, pygame.K_a):
                plansza.wybierz(-1)
            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                plansza.wybierz(1)
            elif event.key == pygame.K_p:
                plansza.ruch()
            elif event.key == pygame.K_BACKSPACE:
                plansza.cofnij()



    pygame.display.update()
    clock.tick(tempo)