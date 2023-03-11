import numpy as np 
import pandas as pd
from collections import Counter
from random import shuffle
import cv2

train_data = np.load('training_data.npy',allow_pickle=True)

df = pd.DataFrame(train_data)
print(Counter(df[1].apply(str)))
# for data in train_data:
#     img = data[0]
#     choice = data[1]
#     cv2.imshow("Hehe",img)
#     print(choice)

#     if cv2.waitKey(25) & 0xFF == ord('q'):
#         cv2.destroyAllWindows()
#         break