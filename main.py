import arcade
import arcade.gui
from arcade.gui import UIManager

ANCHO = 800
ALTO = 600
BOTS = 0


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
        arcade.draw_text("POKER", ANCHO/2, ALTO/2,
                         arcade.color.WHITE, font_size=30, anchor_x="center")
        arcade.draw_text("Por Martin Silva", ANCHO / 2 , ALTO / 2 - 30,
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

        # Create variables here

    def setup(self):
        """ This should set up your game and get it ready to play """
        # Replace 'pass' with the code to set up your game
        pass

    def on_show(self):
        """ Called when switching to this view"""
        arcade.set_background_color(arcade.color.ORANGE_PEEL)

    def on_draw(self):
        """ Draw everything for the game. """
        arcade.start_render()
        arcade.draw_text("Game - press SPACE to advance", ANCHO/2, ALTO/2,
                         arcade.color.BLACK, font_size=30, anchor_x="center")

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
        arcade.draw_text("Game Over - press ESCAPE to advance", ANCHO/2, ALTO/2,
                         arcade.color.WHITE, 30, anchor_x="center")

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