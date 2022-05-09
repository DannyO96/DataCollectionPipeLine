import random
import cv2
from keras.models import load_model
import numpy as np
model = load_model('keras_model.h5')
cap = cv2.VideoCapture(0)
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

user_choice = read_user(cap)
possible_choice = ["rock", "paper", "scissors", "nothing"]
computer_choice = random.choice(possible_choice)
print(f"\nYou chose {user_choice}, computer chose {computer_choice}.\n")

if user_choice == computer_choice:
    print(f"Both players selected {user_choice}. Drawing with a robot is losing unlucky!")
elif user_choice == "rock":
    if computer_choice == "scissors":
        print("Rock beats scissors! WINNER!")
    else:
        print("Paper beats rock! LOSER!")
elif user_choice == "paper":
    if computer_choice == "rock":
        print("Paper beats rock! WINNER!!")       
    else:
        print("Scissors beats paper! LOSER!")
elif user_choice == "scissors":
    if computer_choice == "paper":
        print("Scissors beats paper! LOSER!")
    else:
        print("Rock beats scissors! LOSER!")
        

def read_user(fcap, fcv2):
    while True: 
        ret, frame = fcap.read()
        resized_frame = cv2.resize(frame, (224, 224),fx=0,fy=0, interpolation = cv2.INTER_CUBIC)
        image_np = np.array(resized_frame)
        normalized_image = (image_np.astype(np.float32) / 127.0) - 1 # Normalize the image
        data[0] = normalized_image
        prediction = model.predict(data)
    if prediction [0][0] > 0.5:
        print("Rock")
        return("rock")
    elif prediction [0][1] > 0.5:
        print("Paper")
        return("paper")
    elif prediction [0][2] > 0.5:
        print("Scissors")
        return("scissors")
    else:
        print("nothing")
    cv2.imshow('frame', frame)
    # Press q to close the window
    print(prediction)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        return("Quit")


# After the loop release the cap object
cap.release()
# Destroy all the windows
cv2.destroyAllWindows()