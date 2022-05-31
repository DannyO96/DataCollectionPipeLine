#imports

import cv2
import numpy as np
import random
import time
from keras.models import load_model

#Classes 

class Player:
    def __init__(self):
        self.score = 0
    def win(self):
        self.score += 1

# Functions
# Computers move: Function to determine the computers move namely a random integer between 0 & 2

def computer_option():
    comp_choice = random.randint(0,2)
    if comp_choice == 0:
        return(0)
    elif comp_choice == 1:
        return(1)
    elif comp_choice == 2:
        return(2)

# Finding out who won: Function to determine the winner of the round based upon the computer and users moves

def get_winner(user_move, computer_move):
    if user_move == computer_move or computer_move == user_move:
        return "NO ONE"
    elif user_move == "rock" and computer_move == "scissors":
        return "User"
    elif user_move == "rock" and computer_move == "paper":
        return "Computer"
    elif user_move == "paper" and computer_move == "rock":
        return "User"
    elif user_move == "paper" and computer_move == "scissors":
        return "Computer"
    elif user_move == "scissors" and computer_move == "rock":
        return "Computer"
    elif user_move == "scissors" and computer_move == "paper":
        return "User"

model = load_model('keras_model.h5')
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32) 
attempts = 5
computer_move = "nothing"
user_move = "nothing"
label_names = ['rock', 'paper', 'scissors', 'nothing']
font = cv2.FONT_HERSHEY_SIMPLEX
cap = cv2.VideoCapture(-1)
box_size = 234
width = int(cap.get(3))
rect_color = (255, 0, 0)
key ='0'
comp = Player()
user = Player()

# Below is the while loop

while (comp.score < 3) and (user.score < 3): 
    # Define a named window showing the video capture
    ret, frame = cap.read()
    center_x = int(frame.shape[0]/2) # These two lines define the centre of the frame these variables  
    center_y = int(frame.shape[0]/2) # will be used to make the countdown appear in the centre of the screen.
    intkey = cv2.waitKey(1)
    # This code prompts the user to press E or Q to begin the next round or exit the game
    cv2.rectangle(frame, (width - box_size, 0), (width, box_size), (0, 250, 150), 2,5)
    cv2.putText(frame, "Press E to start press Q to stop", (50, 280), font, 1, (0, 0, 255), 1, cv2.LINE_AA)
    cv2.putText(frame, "Computer score:{}      User score: {}".format(comp.score, user.score), (20, 350), font, 1, (0, 255, 255), 1, cv2.LINE_AA)
    cv2.imshow('Rock Paper Scissors', frame) 
    # return if the frame was closed
    if not ret:
        break
    comp_choice = label_names[computer_option()]
    # Initialise the countdown if the player presses 'e' break the loop if the player presses 'q'
    if intkey > 0:
        key = chr(intkey)
        if key == 'q':   # Press q to close the window
            break
        elif key == 'e':
                num=3
                for i in range(num, 0, -1):
                    ret, frame = cap.read()
                    cv2.putText(frame, str(i), (center_x, center_y), font, 5, (0 , 0, 255),2,cv2.LINE_AA)
                    cv2.rectangle(frame, (width - box_size, 0), (width, box_size), (0, 250, 150), 2,5)
                    cv2.imshow('Rock Paper Scissors', frame)
                    cv2.waitKey(1)
                    time.sleep(1)    
                ret, frame = cap.read()
                cv2.putText(frame, "GO", (center_x, center_y), font, 5, (0, 0, 255),2,cv2.LINE_AA)
                cv2.imshow('Rock Paper Scissors', frame)
                cv2.waitKey(1)
                # Region of image is the top right quarter of the video image/frame

                roi = frame[5: box_size -5 , width-box_size + 5: width -5]
                roi = np.array([roi]).astype('float64') / 255.0 # Normalize the image

                # Use out RPS Model to analyse the ROI & return the most likely hand shape

                pred = model.predict(roi) 
                best_prediction = np.argmax(pred[0])
                user_choice = label_names[best_prediction]
                prob = np.max(pred[0])
                time.sleep(1)
                ret, frame = cap.read()

                # After the get winner functions has been run the player object scores are updated in line with the results of the round

                the_winner = get_winner(user_choice, comp_choice)
                if the_winner == "User":
                    user.score += 1
                elif the_winner == "Computer":
                    comp.score += 1
                else:
                    the_winner == "NO ONE"

                #The following block is to show the results of the round in the camera frame and show the updated scores following the result of the round

                cv2.putText(frame, comp_choice, (100, 270), font, 1,(0, 0, 255), 2, cv2.LINE_AA)
                cv2.putText(frame, label_names[best_prediction], (400, 270), font, 1, (0, 255, 0), 2, cv2.LINE_AA)
                cv2.putText(frame, "prediction: {} {:.2f}%".format(label_names[np.argmax(pred[0])], prob*100 ), (380, 300), font, 0.6, (0, 255, 0), 2, cv2.LINE_AA)
                cv2.putText(frame, 'The winner was {}'.format(the_winner), (20, 30), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
                cv2.putText(frame, "Computer score:{}      User score: {}".format(comp.score, user.score), (20, 350), font, 1, (0, 255, 255), 1, cv2.LINE_AA)
                cv2.rectangle(frame, (width - box_size, 0), (width, box_size), (0, 250, 150), 2,5)
                cv2.imshow('Rock Paper Scissors', frame)
                cv2.waitKey(0)

# Finally two if statements to print the results of the best of three on the screen

if user.score > 2:
    ret, frame = cap.read()
    cv2.putText(frame, "Congratulations you beat the machine", (15, center_y), font, 1, (0, 255, 0), 2, cv2.LINE_AA)
    cv2.putText(frame, "Press any key to quit" , (120, 400), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.imshow('Rock Paper Scissors', frame)
    cv2.waitKey(0)

elif comp.score > 2:
    ret, frame = cap.read()
    cv2.putText(frame, "Unlucky defeated by a machine", (60, center_y), font, 1, (0, 0, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, "Press any key to quit" , (120, 400), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.imshow('Rock Paper Scissors', frame)
    cv2.waitKey(0)

# After the loop release the cap object
cap.release()
cv2.destroyAllWindows()