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
        elif self.text == 'Entrar':
            self.dispatch_event('entrar')
        elif self.text == 'Retirar':
            self.dispatch_event('retirar')


class BotonNroBots(arcade.gui.UIFlatButton):
    """
    To capture a button click, subclass the button and override on_click.
    """

    def on_click(self):
        """ Called when user lets off button """
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
        arcade.draw_text("Eliga con cuantos bots quiere jugar", ANCHO / 2, ALTO / 2 - 80,
                         arcade.color.WHITE, font_size=15, anchor_x="center")

    def setup(self):
        """ Set up this view. """
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
    """ Manage the 'game' view for our program. """

    def __init__(self):
        super().__init__()

        # Variables that will hold sprite lists
        self.player_list = None
        self.bot_list = []

        self.ui_manager = UIManager()

        # Set up the player info
        self.player_sprite = None
        self.bot_sprite = None
        self.cartas_jugador = None
        self.player_score = None

        # Create variables here
        self.deck = DeckClass()
        self.cartas_bots = []
        self.bot_score = [] * BOTS

    def on_hide_view(self):
        self.ui_manager.unregister_handlers()

    def setup(self):
        """ This should set up your game and get it ready to play """
        # Replace 'pass' with the code to set up your game

        self.deck.shuffle()
        self.ui_manager.purge_ui_elements()

        # Jugador

        self.player_list = arcade.SpriteList()
        self.player_score = 10
        self.cartas_jugador = self.deck.draw_cards(5)

        for carta in self.cartas_jugador:
            carta.revealed = True

        for i in range(5):
            self.player_sprite = arcade.Sprite('./resources/deck/%s.png' % self.cartas_jugador[i].name, 1)
            self.player_sprite.center_x = 50 + i * 80
            self.player_sprite.center_y = 100
            self.player_list.append(self.player_sprite)

        # Botones

        boton_cambio = BotonJuego(
            'Cambiar',
            center_x=1 * self.window.width // 6,
            center_y=self.window.height // 4,
            width=160
        )

        self.ui_manager.add_ui_element(boton_cambio)

        boton_entrar = BotonJuego(
            'Entrar',
            center_x=2 * self.window.width // 6,
            center_y=self.window.height // 4,
            width=160
        )

        self.ui_manager.add_ui_element(boton_entrar)

        boton_retirar = BotonJuego(
            'Retirar',
            center_x=3 * self.window.width // 6,
            center_y=self.window.height // 4,
            width=160
        )

        self.ui_manager.add_ui_element(boton_retirar)

        # Bots
        self.bot_score = [10] * BOTS
        for i in range(BOTS):
            self.bot_list.append(arcade.SpriteList())
            self.cartas_bots.append(self.deck.draw_cards(5))
            for j in range(5):
                self.bot_sprite = arcade.Sprite('./resources/card_back.png', 1)
                self.bot_sprite.center_x = 50 + j * 10 + i * 200
                self.bot_sprite.center_y = 800
                self.bot_list[i].append(self.bot_sprite)

        BotonJuego.register_event_type('cambiar_cartas')
        BotonJuego.register_event_type('entrar')
        BotonJuego.register_event_type('retirar')

        @boton_cambio.event()
        def cambiar_cartas():

            cartas_a_cambiar = []

            for carta in self.cartas_jugador:
                if carta.selected:
                    cartas_a_cambiar.append(carta)

            for carta in cartas_a_cambiar:
                self.cartas_jugador.remove(carta)

            self.cartas_jugador.extend(self.deck.draw_cards(len(cartas_a_cambiar)))
            self.deck.put(cartas_a_cambiar)

            for i in range(5):
                self.player_list[i].texture = arcade.load_texture(
                    "./resources/deck/%s.png" % self.cartas_jugador[i].name)
                self.player_list[i].center_y = 100

            self.player_list.update()

        @boton_entrar.event()
        def entrar():

            cartas_en_juego = self.cartas_bots + [self.cartas_jugador]
            resultado = poker(cartas_en_juego)
            if resultado.get("ganador") == len(cartas_en_juego):
                print("Ganó el jugador con " + resultado.get("jugada"))
                self.player_score += 2
            else:
                print("Ganó el bot " + str(resultado.get("ganador")) + " con " + resultado.get("jugada"))
                self.player_score -= 2
                for i in range(BOTS):
                    if i == resultado.get("ganador")-1:
                        self.bot_score[i] += 2
                    else:
                        if self.bot_score[i] > 0:
                            self.bot_score[i] -= 2
            if self.player_score >= 20:
                game_over_view = GameOverView(True)
                self.window.show_view(game_over_view)
            if self.player_score <= 0:
                game_over_view = GameOverView(False)
                self.window.show_view(game_over_view)

        @boton_retirar.event()
        def retirar():
            print(self.player_score)
            self.player_score -= 1
            if self.player_score == 0:
                game_over_view = GameOverView(False)
                self.window.show_view(game_over_view)
            print(self.player_score)

    def on_show(self):
        """ Called when switching to this view"""
        arcade.set_background_color(arcade.color.AMAZON)

    def on_draw(self):
        """ Draw everything for the game. """
        arcade.start_render()
        arcade.draw_text("Game - press SPACE to advance", ANCHO / 2, ALTO / 2,
                         arcade.color.BLACK, font_size=30, anchor_x="center")

        self.player_list.draw()
        arcade.draw_text('Puntos: ' + str(self.player_score), 20, 30, arcade.color.WHITE, 14)
        for i in range(BOTS):
            self.bot_list[i].draw()
            arcade.draw_text('Puntos: ' + str(self.bot_score[i]), 20 + i * 200, 730, arcade.color.WHITE, 14)




    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):

        if button == arcade.MOUSE_BUTTON_LEFT:
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

    def on_key_press(self, key, _modifiers):
        """ Handle keypresses. In this case, we'll just count a 'space' as
        game over and advance to the game over view. """
        if key == arcade.key.SPACE:
            game_over_view = GameOverView(True)
            self.window.show_view(game_over_view)


class GameOverView(arcade.View):
    """ Class to manage the game over view """

    def __init__(self, victoria: bool):
        super(GameOverView, self).__init__()
        self.victoria = victoria

    def on_show(self):
        """ Called when switching to this view"""
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        """ Draw the game over view """
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
        """ If user hits escape, go back to the main menu view """
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
