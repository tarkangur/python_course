import turtle
import pandas
import state_write

screen = turtle.Screen()
screen.title("U.S. States Game")
image = "blank_states_img.gif"
screen.addshape(image)
turtle.shape(image)
writer = state_write.Writer()


data = pandas.read_csv("50_states.csv")
states = data["state"].to_list()
answers = []
score = 0
game_is_on = True
while game_is_on:
    answer = screen.textinput(title=f"{score}/50 States Correct", prompt="What's another state's name?")
    if answer is None:
        game_is_on = False
    if answer in states and answer not in answers:
        index = states.index(answer)
        correct = data[data.state == answer]
        score += 1
        writer.correct_write(correct.x[index], correct.y[index], correct.state[index])
        answers.append(answer)
    if score == 50:
        game_is_on = False

screen.exitonclick()
