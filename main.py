import pygame
import time

pygame.init()

class Plansza():
    def __init__(self, wzor=None):
        if wzor is None:
            return
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
        self.zbite = 0
        self.do_zbicia = -1
        for kulka in self.lista_kulek:
            if kulka.czy_kulka:
                self.do_zbicia += 1

    def rysuj(self):
        for i, line in enumerate(self.tablica):
            for j, kulka in enumerate(line):
                y_kulki = (i + 1) * (WYS / (self.wysokosc + 1))
                x_kulki = (j + 1) * (SZER / (self.szerokosc + 1))
                if kulka.czy_wybrana:
                    pygame.draw.circle(screen, kulka.kolor_wybrana, (x_kulki, y_kulki),
                                       kulka.rozmiar + kulka.zaznaczenie, 0)
                pygame.draw.circle(screen, kulka.kolor, (x_kulki, y_kulki), kulka.rozmiar, 0)
                if kulka.czy_kulka:
                    pygame.draw.circle(screen, (220, 110, 165), (x_kulki + 5, y_kulki + 5), kulka.rozmiar - 10, 0)
        napis(str(self.zbite) + "/" + str(self.do_zbicia), 20, 20, 24)
        napis("kliknij [i], aby wyświetlić instrukcję ", 490, 20, 20)
        if self.zbite == self.do_zbicia:
            napis("Gratulacje!", 0, 200, 100, centered=True, background=True)
            napis("Udało Ci się rozwiązać łamigłówkę ^^", 0, 400, 30, centered=True, background=True)

    def wybierz(self, kierunek):
        self.lista_kulek[self.wybrana].czy_wybrana = False
        self.wybrana = (self.wybrana + kierunek + len(self.lista_kulek)) % len(self.lista_kulek)
        counter = self.szerokosc * self.wysokosc
        while not self.lista_kulek[self.wybrana].czy_mozna_wybrac and counter > 0:
            counter -= 1
            self.wybrana = (self.wybrana + kierunek + len(self.lista_kulek)) % len(self.lista_kulek)
        if counter > 0:
            self.lista_kulek[self.wybrana].czy_wybrana = True
        else:
            self.wybrana = -1

    def aktualizuj(self):
        for i, line in enumerate(self.tablica):
            for j, kulka in enumerate(line):
                kulka.czy_mozna_wybrac = False
                kulka.ruchy = []
                if kulka.czy_kulka:
                    if i > 1:
                        if self.tablica[i - 1][j].czy_kulka and self.tablica[i - 2][j].czy_wolne:
                            kulka.czy_mozna_wybrac = True
                            kulka.ruchy.append(UP)
                    if i < self.wysokosc - 2:
                        if self.tablica[i + 1][j].czy_kulka and self.tablica[i + 2][j].czy_wolne:
                            kulka.czy_mozna_wybrac = True
                            kulka.ruchy.append(DOWN)
                    if j > 1:
                        if self.tablica[i][j - 1].czy_kulka and self.tablica[i][j - 2].czy_wolne:
                            kulka.czy_mozna_wybrac = True
                            kulka.ruchy.append(LEFT)
                    if j < self.szerokosc - 2:
                        if self.tablica[i][j + 1].czy_kulka and self.tablica[i][j + 2].czy_wolne:
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
            nowy_kolor = pygame.Color(100, 100, 250)
            kulka.kolor = nowy_kolor
            self.rysuj()
            napis("Wybierz kierunek zbicia!   " * 3, 50, 600, 20)
            pygame.display.update()

            stop = False
            while not stop:

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        quit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key in (pygame.K_LEFT, pygame.K_a) and LEFT in kulka.ruchy:
                            ruch = LEFT
                            stop = True
                        elif event.key in (pygame.K_RIGHT, pygame.K_d) and RIGHT in kulka.ruchy:
                            ruch = RIGHT
                            stop = True
                        elif event.key in (pygame.K_UP, pygame.K_w) and UP in kulka.ruchy:
                            ruch = UP
                            stop = True
                        elif event.key in (pygame.K_DOWN, pygame.K_s) and DOWN in kulka.ruchy:
                            ruch = DOWN
                            stop = True
                        elif event.key == pygame.K_i:
                            self.instrukcja()
                            screen.fill(KOLOR_TLA)
                            self.rysuj()
                            napis("Wybierz kierunek zbicia!   " * 3, 50, 600, 20, centered=True)
                            pygame.display.update()
            kulka.kolor = stary_kolor

        if ruch == UP:
            do_polozenia = self.lista_kulek[self.wybrana - self.szerokosc * 2]
            do_podniesienia = self.lista_kulek[self.wybrana - self.szerokosc]
        if ruch == DOWN:
            do_polozenia = self.lista_kulek[self.wybrana + self.szerokosc * 2]
            do_podniesienia = self.lista_kulek[self.wybrana + self.szerokosc]
        if ruch == LEFT:
            do_polozenia = self.lista_kulek[self.wybrana - 2]
            do_podniesienia = self.lista_kulek[self.wybrana - 1]
        if ruch == RIGHT:
            do_polozenia = self.lista_kulek[self.wybrana + 2]
            do_podniesienia = self.lista_kulek[self.wybrana + 1]

        kulka.podnies_kulke()
        self.animacja(ruch)

        do_polozenia.poloz_kulke()
        do_podniesienia.podnies_kulke()

        self.stos_cofnij.append(do_polozenia)
        self.stos_cofnij.append(do_podniesienia)
        self.stos_cofnij.append(kulka)
        self.aktualizuj()
        self.zbite += 1

    def cofnij(self):
        if len(self.stos_cofnij) == 0:
            return
        self.stos_cofnij.pop().poloz_kulke()
        self.stos_cofnij.pop().poloz_kulke()
        self.stos_cofnij.pop().podnies_kulke()
        self.aktualizuj()
        self.zbite -= 1

    def instrukcja(self, czy_tylko=True):
        if czy_tylko:
            napis("Instrukcja:", 0, 100, 30, centered=True, background=True)
        napis("Gra ta została rzekomo wymyślona na polecenie Ludwika XIV \n"
              "i zyskała sporą popularnosć we Francji w XVII wieku, a następnie\n"
              "w innych krajach europejskich. Rozgrywka polega na usunięciu z planszy\n"
              "wszystkich pionków poza ostatnim, aby tego dokonać gracz może\n"
              "zbijać inne pionki przeskakując nad nimi w pionie i poziomie.\n"
              "Nie można skakać po skosie, ani zbijać więcej niż jednego pionka\n"
              "naraz. Sterujesz za pomocą strzałek lub klawiszy wasd, aby wybrać\n"
              "pionek, którym chesz się poruszyć kliknij [P], w przypadku, gdy \n"
              "możliwy jest ruch w więcej niż jedną stronę wybierz kierunek za\n"
              "pomocą strzałek lub wasd. Jeżeli popełnisz błąd możesz cofnąć ruch\n"
              "za pomocą przycisku [backspace].", 100, 200, 18, centered=True, background=True)

        pygame.display.update()
        if czy_tylko:
            napis("Kliknij dowolny klawisz, by wrócić do gry.", 250, 550, 22, centered=True, background=True)
            pygame.display.update()
        while czy_tylko:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    return
                elif event.type == pygame.QUIT:
                    quit()

    def animacja(self, kierunek):
        kulka = self.lista_kulek[self.wybrana]
        x_kulki = self.wybrana % self.wysokosc
        y_kulki = self.wybrana // self.wysokosc

        x_kulki = (x_kulki + 1) * (SZER // (self.szerokosc + 1))
        y_kulki = (y_kulki + 1) * (WYS // (self.wysokosc + 1))

        STEPS = 50
        if kierunek == UP:
            step_x = 0
            step_y = -2 * (WYS / (self.wysokosc + 1)) / STEPS
        elif kierunek == DOWN:
            step_x = 0
            step_y = 2 * (WYS / (self.wysokosc + 1)) / STEPS
        elif kierunek == LEFT:
            step_x = -2 * (SZER / (self.szerokosc + 1)) / STEPS
            step_y = 0
        elif kierunek == RIGHT:
            step_x = 2 * (SZER / (self.szerokosc + 1)) / STEPS
            step_y = 0
        for i in range(STEPS):
            screen.fill(KOLOR_TLA)
            self.rysuj()
            pygame.draw.circle(screen, Kulka("O").kolor, (x_kulki + i*step_x, y_kulki+i*step_y), Kulka("O").rozmiar, 0)
            pygame.draw.circle(screen, (220, 110, 165), (x_kulki + i*step_x + 5, y_kulki+i*step_y + 5), Kulka("O").rozmiar - 10, 0)
            pygame.display.update()
            clock.tick(400)

    def animacja_start(self):
        self.lista_kulek[self.wybrana].czy_wybrana = False
        temp = [Kulka("*") if x.czy_wolne else (Kulka("O") if x.czy_kulka else Kulka("#")) for x in self.lista_kulek]
        for kulka in self.lista_kulek:
            if kulka.czy_kulka:
                kulka.podnies_kulke()
        for i, kulka in enumerate (self.lista_kulek):
            if temp[i].czy_kulka:
                kulka.poloz_kulke()
            screen.fill(pygame.Color(KOLOR_TLA))
            self.rysuj()
            pygame.display.update()
            if kulka.czy_kulka:
                time.sleep(0.1)
        self.lista_kulek[self.wybrana].czy_wybrana = True

    def menu(self):

        screen.fill(KOLOR_TLA)
        napis("Witaj w Peg Solitaire",0,100,50,centered=True,background=True)
        self.instrukcja(False)
        napis("Wybierz wersję gry:\n [1] Europejska, [2] Angielska, [3] Trójkątna(jeszcze nie gotowa)", 0, 530, 20,
              centered=True, background=True)
        pygame.display.update()
        while True:
            clock.tick(tempo)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        return """##OOO##
#OOOOO#
OOOOOOO
OOO*OOO
OOOOOOO
#OOOOO#
##OOO##"""
                    elif event.key == pygame.K_2:
                        return """##OOO##
##OOO##
OOOOOOO
OOO*OOO
OOOOOOO
##OOO##
##OOO##"""



class Kulka():
    def __init__(self, type):
        self.ruchy = []
        self.czy_wybrana = False
        self.czy_mozna_wybrac = False
        self.czy_kulka = False
        self.czy_wolne = False
        self.kolor_wybrana = pygame.Color(255, 200, 15)
        self.zaznaczenie = 10
        if type == 'O':
            self.kolor = pygame.Color(220, 0, 0)
            self.rozmiar = 20
            self.czy_kulka = True
        elif type == "*":
            self.kolor = pygame.Color(0, 0, 0)
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


def napis(tekst, x, y, rozmiar, centered=False, background=False, to_render=False):
    KOLOR_NAPIS_TLO = (170, 170, 170)
    KOLOR_NAPIS_RAMKA = (100, 100, 100)
    ALPHA = 200
    if len(tekst.split("\n")) > 1:
        padding = 10
        ramka = 3
        interlinia = 5
        whole_height = 0
        max_width = 0
        renders = []
        for i, line in enumerate(tekst.split("\n")):
            render = napis(line, x, y + (rozmiar + 5) * i, rozmiar, to_render=True)
            whole_height += render.get_height() + interlinia
            max_width = max(max_width, render.get_width())
            renders.append(render)

        if background:
            s = pygame.Surface((max_width + 2 * padding, whole_height + 2 * padding))
            s.set_alpha(ALPHA)
            s.fill(KOLOR_NAPIS_TLO)
            screen.blit(s, ((SZER - max_width) // 2 - padding, y - padding))
            pygame.draw.rect(screen, KOLOR_NAPIS_RAMKA, pygame.Rect((SZER - max_width) // 2 - padding - ramka,
                                                                    y - padding - ramka,
                                                                    max_width + 2 * padding + 2 * ramka,
                                                                    whole_height + 2 * padding + 2 * ramka),
                             ramka)
        for i, render in enumerate(renders):
            screen.blit(render, ((SZER - render.get_width()) // 2, y + i * (render.get_height() + interlinia)))
        return
    font = pygame.font.SysFont("Arial", rozmiar)
    render = font.render(tekst, True, (0, 0, 0))
    if centered:
        x = (SZER - render.get_width()) // 2
    if to_render:
        return render
    if background:
        padding = 5
        ramka = 3
        s = pygame.Surface((render.get_width() + 2 * padding, render.get_height() + 2 * padding))
        s.set_alpha(ALPHA)
        s.fill(KOLOR_NAPIS_TLO)
        screen.blit(s, (x - padding, y - padding))
        pygame.draw.rect(screen, KOLOR_NAPIS_RAMKA, pygame.Rect(x - padding - ramka,
                                                                y - padding - ramka,
                                                                render.get_width() + 2 * padding + 2 * ramka,
                                                                render.get_height() + 2 * padding + 2 * ramka),
                         ramka)
    screen.blit(render, (x, y))


UP = "UP"
DOWN = "DOWN"
LEFT = "LEFT"
RIGHT = "RIGHT"

SZER = 800
WYS = 640
KOLOR_TLA = pygame.Color(25, 130, 55)
screen = pygame.display.set_mode((SZER, WYS))
pygame.display.set_caption("Peg Solitare")

clock = pygame.time.Clock()
i = 1
a = True
tempo = 200

plansza = Plansza(Plansza().menu())
plansza.animacja_start()



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
            elif event.key == pygame.K_i:
                plansza.instrukcja()



    pygame.display.update()
    clock.tick(tempo)
