import arcade
import arcade.gui
from Deck import DeckClass
from Poker import poker
from arcade.gui import UIManager

ANCHO = 1200
ALTO = 900
BOTS = 0


class BotonJuego(arcade.gui.UIFlatButton):

    def __init__(self, text, center_x, center_y, width):
        super(BotonJuego, self).__init__(text=text, center_x=center_x, center_y=center_y, width=width)

    def on_click(self):
        if self.text == 'Cambiar':
            self.dispatch_event('cambiar_cartas')
        elif self.text == 'Retirarse':
            self.dispatch_event('retirarse')
        elif self.text == 'Repartir':
            self.dispatch_event('repartir')


class BotonNroBots(arcade.gui.UIFlatButton):

    def on_click(self):
        """ Metodo que se ejecuta al hacer click en un boton """
        global BOTS
        if self.text == '1':
            BOTS = 1
        elif self.text == '2':
            BOTS = 2
        elif self.text == '3':
            BOTS = 3
        elif self.text == '4':
            BOTS = 4
        elif self.text == '5':
            BOTS = 5

        game_view = GameView()
        game_view.setup()
        MenuView().window.show_view(game_view)


class MenuView(arcade.View):
    """ Vista del menu principal """

    def __init__(self):
        super().__init__()
        self.ui_manager = UIManager()

    def on_show_view(self):
        self.setup()
        arcade.set_background_color(arcade.color.AMAZON)

    def on_hide_view(self):
        self.ui_manager.unregister_handlers()

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("POKER", ANCHO / 2, ALTO / 2,
                         arcade.color.WHITE, font_size=30, anchor_x="center")
        arcade.draw_text("Por Martin Silva", ANCHO / 2, ALTO / 2 - 30,
                         arcade.color.WHITE, font_size=15, anchor_x="center")
        arcade.draw_text("Elija con cuantos bots quiere jugar", ANCHO / 2, ALTO / 2 - 80,
                         arcade.color.WHITE, font_size=15, anchor_x="center")

    def setup(self):

        self.ui_manager.purge_ui_elements()

        button = BotonNroBots(
            '1',
            center_x=1 * self.window.width // 6,
            center_y=self.window.height // 4,
            width=60,
        )
        self.ui_manager.add_ui_element(button)

        button = BotonNroBots(
            '2',
            center_x=2 * self.window.width // 6,
            center_y=self.window.height // 4,
            width=60,
        )
        self.ui_manager.add_ui_element(button)

        button = BotonNroBots(
            '3',
            center_x=3 * self.window.width // 6,
            center_y=self.window.height // 4,
            width=60,
        )
        self.ui_manager.add_ui_element(button)

        button = BotonNroBots(
            '4',
            center_x=4 * self.window.width // 6,
            center_y=self.window.height // 4,
            width=60,
        )
        self.ui_manager.add_ui_element(button)

        button = BotonNroBots(
            '5',
            center_x=5 * self.window.width // 6,
            center_y=self.window.height // 4,
            width=60,
        )
        self.ui_manager.add_ui_element(button)


class GameView(arcade.View):
    """ Vista de la pantalla del juego """

    def __init__(self):
        super().__init__()

        # Variables que contendran listas de sprites
        self.player_list = None
        self.bot_list = []

        self.ui_manager = UIManager()

        # Variables con informacion de los jugadores
        self.player_sprite = None
        self.bot_sprite = None
        self.cartas_jugador = None
        self.player_score = None
        self.cartas_bots = []

        # Variables miscelaneas
        self.game_state = None
        self.ganador = ""
        self.deck = None

    def on_hide_view(self):
        self.ui_manager.unregister_handlers()

    def setup(self):
        """ Configuracion inicial para dejar listo el juego """

        self.deck = DeckClass()
        self.deck.shuffle()
        self.ui_manager.purge_ui_elements()

        """Los estados van a ser:
        0 - Mesa cerrada
        1 - Mesa abierta
        """
        self.game_state = {"descripcion": "Seleccione desde 0 hasta 5 cartas y cambielas o retirese de la ronda",
                           "estado": 1}

        # Jugador

        self.player_list = arcade.SpriteList()
        self.player_score = 10
        self.cartas_jugador = self.deck.draw_cards(5)

        for i in range(5):
            self.player_sprite = arcade.Sprite('./resources/deck/%s.png' % self.cartas_jugador[i].name, 1)
            self.player_sprite.center_x = ANCHO / 24 + i * 80
            self.player_sprite.center_y = ALTO / 9
            self.player_list.append(self.player_sprite)

        # Botones

        boton_cambio = BotonJuego(
            'Cambiar',
            center_x=2 * self.window.width // 6,
            center_y=self.window.height // 4,
            width=160
        )

        self.ui_manager.add_ui_element(boton_cambio)

        boton_retirarse = BotonJuego(
            'Retirarse',
            center_x=3 * self.window.width // 6,
            center_y=self.window.height // 4,
            width=160
        )

        self.ui_manager.add_ui_element(boton_retirarse)

        boton_repartir = BotonJuego(
            'Repartir',
            center_x=4 * self.window.width // 6,
            center_y=self.window.height // 4,
            width=160
        )

        self.ui_manager.add_ui_element(boton_repartir)

        BotonJuego.register_event_type('cambiar_cartas')
        BotonJuego.register_event_type('retirarse')
        BotonJuego.register_event_type('repartir')

        # Bots

        for i in range(BOTS):
            self.bot_list.append(arcade.SpriteList())
            self.cartas_bots.append(self.deck.draw_cards(5))
            for j in range(5):
                self.bot_sprite = arcade.Sprite('./resources/card_back.png', 1)
                self.bot_sprite.center_x = ANCHO / 24 + j * 10 + i * 200
                self.bot_sprite.center_y = ALTO / 1.125
                self.bot_list[i].append(self.bot_sprite)

        @boton_cambio.event()
        def cambiar_cartas():

            if self.game_state.get("estado") == 1:
                cartas_a_cambiar = []

                for carta in self.cartas_jugador:
                    if carta.selected:
                        cartas_a_cambiar.append(carta)

                for carta in cartas_a_cambiar:
                    carta.selected = False
                    self.cartas_jugador.remove(carta)

                self.cartas_jugador.extend(self.deck.draw_cards(len(cartas_a_cambiar)))
                self.deck.put(cartas_a_cambiar)

                for i in range(5):
                    self.player_list[i].texture = arcade.load_texture(
                        "./resources/deck/%s.png" % self.cartas_jugador[i].name)
                    self.player_list[i].center_y = ALTO / 9

                self.player_list.update()
                entrar()

        def entrar():

            if self.game_state.get("estado") == 1:

                cartas_en_juego = self.cartas_bots + [self.cartas_jugador]
                resultado = poker(cartas_en_juego)

                if resultado.get("ganador") == len(cartas_en_juego):
                    self.ganador = "Gano el jugador con " + resultado.get("jugada")
                    self.player_score += 2
                else:
                    self.ganador = "Gano el bot " + str(resultado.get("ganador")) + " con " + resultado.get("jugada")
                    self.player_score -= 2

                    # MOSTRAR CARTAS GANADORAS
                    for i in range(5):
                        self.bot_list[resultado.get("ganador") - 1][i].texture = arcade.load_texture(
                            "./resources/deck/%s.png" % self.cartas_bots[resultado.get("ganador") - 1][i].name)
                        self.bot_list[resultado.get("ganador") - 1][i].center_x = ANCHO / 2.8 + i * 80
                        self.bot_list[resultado.get("ganador") - 1][i].center_y = ALTO / 2

                    self.bot_list[resultado.get("ganador") - 1].update()

                self.game_state["descripcion"] = "Presione repartir para continuar"
                self.game_state["estado"] = 2
                self.check_score()

        @boton_retirarse.event()
        def retirarse():

            if self.game_state.get("estado") == 1:
                self.player_score -= 1
                resultado = poker(self.cartas_bots)

                for i in range(5):
                    self.bot_list[resultado.get("ganador") - 1][i].texture = arcade.load_texture(
                        "./resources/deck/%s.png" % self.cartas_bots[resultado.get("ganador") - 1][i].name)
                    self.bot_list[resultado.get("ganador") - 1][i].center_x = ANCHO / 2.8 + i * 80
                    self.bot_list[resultado.get("ganador") - 1][i].center_y = ALTO / 2

                self.bot_list[resultado.get("ganador") - 1].update()
                self.ganador = "Gano el bot " + str(resultado.get("ganador")) + " con " + resultado.get("jugada")
                self.game_state["descripcion"] = "Presione repartir para continuar"
                self.check_score()
                self.game_state["estado"] = 2

        @boton_repartir.event()
        def repartir():

            if self.game_state.get("estado") == 2:
                self.game_state["descripcion"] = "Seleccione desde 0 hasta 5 cartas y cambielas o retirese de la ronda"
                self.ganador = ""
                self.game_state["estado"] = 1
                self.deck = DeckClass()
                self.deck.shuffle()
                self.cartas_jugador = self.deck.draw_cards(5)

                for i in range(5):
                    self.player_list[i].texture = arcade.load_texture(
                        "./resources/deck/%s.png" % self.cartas_jugador[i].name)
                    self.player_list[i].center_y = ALTO / 9

                self.player_list.update()

                self.cartas_bots = []

                for i in range(BOTS):
                    self.cartas_bots.append(self.deck.draw_cards(5))

                    for j in range(5):
                        self.bot_list[i][j].texture = arcade.load_texture("./resources/card_back.png")
                        self.bot_list[i][j].center_x = ANCHO / 24 + j * 10 + i * 200
                        self.bot_list[i][j].center_y = ALTO / 1.125

                    self.bot_list[i].update()

    def check_score(self):
        if self.player_score >= 20:
            game_over_view = GameOverView(True)
            self.window.show_view(game_over_view)
        if self.player_score <= 0:
            game_over_view = GameOverView(False)
            self.window.show_view(game_over_view)

    def on_show(self):
        arcade.set_background_color(arcade.color.AMAZON)

    def on_draw(self):
        """ Dibujar en pantalla lo necesario para el juego """
        arcade.start_render()
        arcade.draw_text(str(self.game_state.get("descripcion")), ANCHO / 2.5, ALTO / 9,
                         arcade.color.BLACK, font_size=15, anchor_x="left")
        arcade.draw_text(self.ganador, ANCHO / 2, ALTO / 3,
                         arcade.color.BLACK, font_size=20, anchor_x="center")
        self.player_list.draw()
        arcade.draw_text('Puntos: ' + str(self.player_score), ANCHO / 60, ALTO / 30, arcade.color.WHITE, 14)
        for i in range(BOTS):
            self.bot_list[i].draw()
            arcade.draw_text("Bot {}".format(i + 1), ANCHO / 60 + i * 200, ALTO / 1.232, arcade.color.WHITE, 14)

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        """ Metodo para seleccionar las cartas al hacer click izquierdo"""

        if button == arcade.MOUSE_BUTTON_LEFT and self.game_state.get("estado") == 1:
            if y in range(self.min_y(self.player_list[0].get_adjusted_hit_box()),
                          self.max_y(self.player_list[0].get_adjusted_hit_box())):
                if x in range(self.min_x(self.player_list[0].get_adjusted_hit_box()),
                              self.max_x(self.player_list[0].get_adjusted_hit_box())):

                    self.cartas_jugador[0].selected = not self.cartas_jugador[0].selected
                    if self.cartas_jugador[0].selected:
                        self.player_list[0].center_y += 20
                    else:
                        self.player_list[0].center_y -= 20
                    self.player_list.update()

                elif x in range(self.min_x(self.player_list[1].get_adjusted_hit_box()),
                                self.max_x(self.player_list[1].get_adjusted_hit_box())):

                    self.cartas_jugador[1].selected = not self.cartas_jugador[1].selected
                    if self.cartas_jugador[1].selected:
                        self.player_list[1].center_y += 20
                    else:
                        self.player_list[1].center_y -= 20
                    self.player_list.update()

                elif x in range(self.min_x(self.player_list[2].get_adjusted_hit_box()),
                                self.max_x(self.player_list[2].get_adjusted_hit_box())):

                    self.cartas_jugador[2].selected = not self.cartas_jugador[2].selected
                    if self.cartas_jugador[2].selected:
                        self.player_list[2].center_y += 20
                    else:
                        self.player_list[2].center_y -= 20
                    self.player_list.update()

                elif x in range(self.min_x(self.player_list[3].get_adjusted_hit_box()),
                                self.max_x(self.player_list[3].get_adjusted_hit_box())):

                    self.cartas_jugador[3].selected = not self.cartas_jugador[3].selected
                    if self.cartas_jugador[3].selected:
                        self.player_list[3].center_y += 20
                    else:
                        self.player_list[3].center_y -= 20
                    self.player_list.update()

                elif x in range(self.min_x(self.player_list[4].get_adjusted_hit_box()),
                                self.max_x(self.player_list[4].get_adjusted_hit_box())):

                    self.cartas_jugador[4].selected = not self.cartas_jugador[4].selected
                    if self.cartas_jugador[4].selected:
                        self.player_list[4].center_y += 20
                    else:
                        self.player_list[4].center_y -= 20
                    self.player_list.update()

    @staticmethod
    def min_x(puntos):
        """ Las hitboxes automaticas no son perfectas, pueden tener mas de 4 puntos
            por eso se necesitan estos metodos """
        minx = puntos[0][0]
        for punto in puntos:
            if minx > punto[0]:
                minx = punto[0]

        return int(minx)

    @staticmethod
    def max_x(puntos):
        maxx = puntos[0][0]
        for punto in puntos:
            if maxx < punto[0]:
                maxx = punto[0]

        return int(maxx)

    @staticmethod
    def min_y(puntos):
        miny = puntos[0][1]
        for punto in puntos:
            if miny > punto[1]:
                miny = punto[1]

        return int(miny)

    @staticmethod
    def max_y(puntos):
        maxy = puntos[0][1]
        for punto in puntos:
            if maxy < punto[1]:
                maxy = punto[1]

        return int(maxy)


class GameOverView(arcade.View):
    """ Vista de la pantalla del juego terminado  """

    def __init__(self, victoria: bool):
        super(GameOverView, self).__init__()
        self.victoria = victoria

    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        arcade.start_render()
        if self.victoria:
            arcade.draw_text("Ha ganado la partida", ANCHO / 2, ALTO / 2,
                             arcade.color.WHITE, 30, anchor_x="center")
        else:
            arcade.draw_text("Ha perdido la partida", ANCHO / 2, ALTO / 2,
                             arcade.color.WHITE, 30, anchor_x="center")
        arcade.draw_text("Presione ESCAPE para ir al menu principal", ANCHO / 2, ALTO / 2 - 30,
                         arcade.color.WHITE, 20, anchor_x="center")

    def on_key_press(self, key, _modifiers):
        """ Si el jugador presiona escape, vuelve a la pantalla principal """
        if key == arcade.key.ESCAPE:
            menu_view = MenuView()
            self.window.show_view(menu_view)


def main():
    """ Startup """
    window = arcade.Window(ANCHO, ALTO, "Poker")
    menu_view = MenuView()
    window.show_view(menu_view)
    arcade.run()


if __name__ == "__main__":
    main()
