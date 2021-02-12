# Instrucciones para compilar

1- Instalar Git desde la terminal con:

<code>sudo apt install git-all</code>


2- Descargar desde la terminal el IDE PyCharm Community con el comando (para Ubuntu):

<code>sudo snap install pycharm-community --classic</code>

3- Abrir PyCharm

4- Seleccionar "Get from VCS"

5- Poner la URL de este mismo repositorio (https://github.com/Martin-Silva-UTN/Poker) y hacer click en Clone

6- Desplegar la pestaña "Project" a la izquierda, desplegar la carpeta Poker y hacer doble click en main.py

![asd](https://user-images.githubusercontent.com/63522064/107830371-685fc580-6d6a-11eb-8191-37f3250a786a.png)

7- En la barra verde que aparecerá arriba haga click en "configure python interpreter" y luego en "Add interpreter"

![asd2](https://user-images.githubusercontent.com/63522064/107830557-dd32ff80-6d6a-11eb-815e-6895ae6e8426.png)

8- Dejar seleccionada la opción por defecto (usar el interprete existente en el virtual enviroment) y aceptar

9- Click derecho sobre main.py seleccionar Run

# Instrucciones del juego

La dificultad está regida por la cantidad de bots en juego (1-5) ya que para ganar una ronda debe ganarle a las manos de todos y cada uno de ellos

El objetivo del juego es llegar a los 20 puntos, empezando con 10. Si el puntaje llega a 0 pierde la partida.

Ganar una ronda suma 2 puntos, perder una ronda resta 2 puntos, y si considera que la mano que le tocó es muy mala y no vale la pena entrar a la ronda, con el boton retirarse pasa la ronda perdiendo sólo 1 punto.

Para participar en una ronda debe hacer click en el botón "cambiar" luego de haber hecho click en las cartas que desee cambiar.

Puede no seleccionar cartas si así lo desea, entrará a la ronda igual luego de apretar "cambiar"
