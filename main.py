import arcade
import arcade.gui
from Deck import DeckClass
from Card import CardClass
from arcade.gui import UIManager

ANCHO = 1200
ALTO = 900
BOTS = 0


class BotonCambio(arcade.gui.UIFlatButton):

    def __init__(self, text, center_x, center_y, width, deck: DeckClass, cartas: CardClass,player_list):
        super(BotonCambio, self).__init__(text=text, center_x=center_x, center_y=center_y, width=width)
        self.deck = deck
        self.cartas = cartas
        self.player_list = player_list

    def on_click(self):

        cartas_a_cambiar = []

        for carta in self.cartas:
            if carta.selected:
                cartas_a_cambiar.append(carta)

        for carta in cartas_a_cambiar:
            self.cartas.remove(carta)

        self.cartas.extend(self.deck.draw(len(cartas_a_cambiar)))
        self.deck.put(cartas_a_cambiar)

        for i in range(5):
            self.player_list[i].texture = arcade.load_texture("./resources/deck/%s.png" % self.cartas[i].name)
            self.player_list[i].center_y = 100

        self.player_list.update()


class MyFlatButton(arcade.gui.UIFlatButton):
    """
    To capture a button click, subclass the button and override on_click.
    """

    def on_click(self):
        """ Called when user lets off button """
        self.set_bots()
        game_view = GameView()
        game_view.setup()
        MenuView().window.show_view(game_view)

    def set_bots(self):
        pass


class Button1(MyFlatButton):
    """
    To capture a button click, subclass the button and override on_click.
    """

    def set_bots(self):
        global BOTS
        BOTS = 1


class Button2(MyFlatButton):
    """
    To capture a button click, subclass the button and override on_click.
    """

    def set_bots(self):
        global BOTS
        BOTS = 2


class Button3(MyFlatButton):
    """
    To capture a button click, subclass the button and override on_click.
    """

    def set_bots(self):
        global BOTS
        BOTS = 3


class Button4(MyFlatButton):
    """
    To capture a button click, subclass the button and override on_click.
    """

    def set_bots(self):
        global BOTS
        BOTS = 4


class Button5(MyFlatButton):
    """
    To capture a button click, subclass the button and override on_click.
    """

    def set_bots(self):
        global BOTS
        BOTS = 5


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

        button = Button1(
            '1',
            center_x=1 * self.window.width // 6,
            center_y=self.window.height // 4,
            width=60,
        )
        self.ui_manager.add_ui_element(button)

        button = Button2(
            '2',
            center_x=2 * self.window.width // 6,
            center_y=self.window.height // 4,
            width=60,
        )
        self.ui_manager.add_ui_element(button)

        button = Button3(
            '3',
            center_x=3 * self.window.width // 6,
            center_y=self.window.height // 4,
            width=60,
        )
        self.ui_manager.add_ui_element(button)

        button = Button4(
            '4',
            center_x=4 * self.window.width // 6,
            center_y=self.window.height // 4,
            width=60,
        )
        self.ui_manager.add_ui_element(button)

        button = Button5(
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
        self.coin_list = None

        self.ui_manager = UIManager()

        # Set up the player info
        self.player_sprite = None
        self.bot_sprite = None
        self.cartas_jugador = None
        self.cartas_bots = []
        self.player_score = 0
        # Create variables here

    def on_hide_view(self):
        self.ui_manager.unregister_handlers()

    def setup(self):
        """ This should set up your game and get it ready to play """
        # Replace 'pass' with the code to set up your game
        deck = DeckClass()
        deck.shuffle()

        self.ui_manager.purge_ui_elements()

        # Jugador
        self.player_list = arcade.SpriteList()
        print(type(self.player_list))
        self.player_score = 0
        self.cartas_jugador = deck.draw(5)

        for carta in self.cartas_jugador:
            carta.revealed = True

        for i in range(5):
            self.player_sprite = arcade.Sprite('./resources/deck/%s.png' % self.cartas_jugador[i].name, 1)
            self.player_sprite.center_x = 50 + i * 80
            self.player_sprite.center_y = 100
            self.player_list.append(self.player_sprite)

        button = BotonCambio(
            'Cambiar',
            center_x=1 * self.window.width // 6,
            center_y=self.window.height // 4,
            width=160,
            deck=deck,
            cartas=self.cartas_jugador,
            player_list=self.player_list
        )

        self.ui_manager.add_ui_element(button)

        # Bots

        for i in range(BOTS):
            self.bot_list.append(arcade.SpriteList())
            print(type(self.bot_list[0]))
            self.cartas_bots.append(deck.draw(5))
            for j in range(5):
                self.bot_sprite = arcade.Sprite('./resources/card_back.png', 1)
                self.bot_sprite.center_x = 50 + j * 10 + i * 200
                self.bot_sprite.center_y = 800
                self.bot_list[i].append(self.bot_sprite)

    def on_show(self):
        """ Called when switching to this view"""
        arcade.set_background_color(arcade.color.AMAZON)

    def on_draw(self):
        """ Draw everything for the game. """
        arcade.start_render()
        arcade.draw_text("Game - press SPACE to advance", ANCHO / 2, ALTO / 2,
                         arcade.color.BLACK, font_size=30, anchor_x="center")

        self.player_list.draw()
        for i in range(BOTS):
            self.bot_list[i].draw()

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

    def min_x(self, puntos=[]):
        minx = puntos[0][0]
        for punto in puntos:
            if minx > punto[0]:
                minx = punto[0]

        return int(minx)

    def max_x(self, puntos=[]):
        maxx = puntos[0][0]
        for punto in puntos:
            if maxx < punto[0]:
                maxx = punto[0]

        return int(maxx)

    def min_y(self, puntos=[]):
        miny = puntos[0][1]
        for punto in puntos:
            if miny > punto[1]:
                miny = punto[1]

        return int(miny)

    def max_y(self, puntos=[]):
        maxy = puntos[0][1]
        for punto in puntos:
            if maxy < punto[1]:
                maxy = punto[1]

        return int(maxy)

    def on_key_press(self, key, _modifiers):
        """ Handle keypresses. In this case, we'll just count a 'space' as
        game over and advance to the game over view. """
        if key == arcade.key.SPACE:
            game_over_view = GameOverView()
            self.window.show_view(game_over_view)


class GameOverView(arcade.View):
    """ Class to manage the game over view """

    def on_show(self):
        """ Called when switching to this view"""
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        """ Draw the game over view """
        arcade.start_render()
        arcade.draw_text("Juego terminado", ANCHO / 2, ALTO / 2,
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
