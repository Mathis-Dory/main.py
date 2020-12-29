from tkinter import *


class Ball:
    def __init__(self, Game):
        self.dx = 2
        self.dy = -6
        self.Game = Game
        self.static = True
        self.Game.root.bind("<Button-1>", self.launch_ball)

        self.create_label()
        self.create_ball()

    def create_label(self):
        self.label = self.Game.canevas.create_text(400, 300, text="Clique gauche pour lancer la balle",
                                                   font=("Arial", 25))

    def create_ball(self):
        self.ball = self.Game.canevas.create_oval(390, 480,
                                                  390 + 20, 480 + 20,
                                                  fill='red')

    def launch_ball(self, event):
        if not self.static:
            return 0
        else:
            self.Game.canevas.itemconfigure(self.label, text="")
            self.animation()
            self.static = False
            self.Game.canevas.pack()

    def animation(self):
        if self.Game.canevas.coords(self.ball)[1] < 0:
            self.dy = -1 * self.dy
        if self.Game.canevas.coords(self.ball)[3] > 600:
            self.Game.update_json_file()
            self.Game.life -= 1
            self.Game.canevas.itemconfigure(self.Game.lives_label, text="Lives : " + str(self.Game.life))
            self.Game.root.unbind("<Button-1>") # empeche le spam click et donc de faire lag le programme
            self.static = True #remet la balle en position initiale
            self.dy = -1 * self.dy  #Permet de relancer la balle vers le haut pour le nouveau lancer au lieu part dans le paddle et lag

            if self.Game.life == 0:
                self.Game.leave_loose_game()
            return 0

        if self.Game.canevas.coords(self.ball)[0] < 0:
            self.dx = -1 * self.dx
        if self.Game.canevas.coords(self.ball)[2] > 800:
            self.dx = -1 * self.dx
        self.Game.canevas.move(self.ball, self.dx, self.dy)
        self.Game.root.after(15, self.animation) #le premier parametre indique la vitesse de la balle, plus petit = plus rapide

        # collision paddle
        if len(self.Game.canevas.find_overlapping(self.Game.canevas.coords(self.Game.paddle.paddle)[0],
                                                  self.Game.canevas.coords(self.Game.paddle.paddle)[1],
                                                  self.Game.canevas.coords(self.Game.paddle.paddle)[2],
                                                  self.Game.canevas.coords(self.Game.paddle.paddle)[3])) > 1:
            self.Game.ball.dy = -1 * self.Game.ball.dy

        # collision briques
        for i in self.Game.brick.bricks:
            if len(self.Game.canevas.find_overlapping(self.Game.canevas.coords(i)[0],
                                                      self.Game.canevas.coords(i)[1],
                                                      self.Game.canevas.coords(i)[2],
                                                      self.Game.canevas.coords(i)[3])) > 1:
                self.Game.ball.dy = -1 * self.Game.ball.dy

                # Score
                self.Game.score += 100
                self.Game.canevas.itemconfigure(self.Game.score_label, text="Score : " + str(self.Game.score))

                # Change the color and solidity of the brick
                color = self.Game.canevas.gettags(i)
                if color == ('blue',):
                    self.Game.brick.bricks.remove(i)
                    self.Game.canevas.delete(i)
                elif color == ('pink',):
                    self.Game.life += 1
                    self.Game.canevas.itemconfigure(self.Game.lives_label,
                                                    text="Lives : " + str(self.Game.life))
                    self.Game.brick.bricks.remove(i)
                    self.Game.canevas.delete(i)
                elif color == ('green',):
                    self.Game.canevas.itemconfig(i, fill='blue', tag='blue')
                elif color == ('yellow',):
                    self.Game.canevas.itemconfig(i, fill='green', tag='green')
                elif color == ('red',):
                    self.Game.canevas.itemconfig(i, fill='yellow', tag='yellow')

                if len(self.Game.brick.bricks) == 0:
                    self.Game.update_json_file()
                    self.Game.leave_win_game()

# Destroy the ball first !
