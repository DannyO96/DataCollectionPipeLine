from typing import Counter
import cv2
from keras.models import load_model
import numpy as np
model = load_model('YOUR_MODEL.h5')
cap = cv2.VideoCapture(0)
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

counter = 3

while counter >= 0: 
    ret, frame = cap.read()
    resized_frame = cv2.resize(frame, (224, 224), interpolation = cv2.INTER_AREA)
    image_np = np.array(resized_frame)
    normalized_image = (image_np.astype(np.float32) / 127.0) - 1 # Normalize the image
    data[0] = normalized_image
    prediction = model.predict(data)
    cv2.imshow('frame', frame)
    # Press q to close the window
    if prediction [0][0] > 0.5:
        print("r")
    elif prediction [0][1] > 0.5:
        print("p")
    elif prediction [0][2] > 0.5:
        print("s")
    else:
        print("nothing")
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    counter -= 1        
# After the loop release the cap object
cap.release()
# Destroy all the windows
cv2.destroyAllWindows()