import imageio
import os

images = []
for filename in os.listdir("./ant/"):
    if int(filename[1:5])%2:
        continue
    images.append(imageio.imread("./ant/"+filename))
imageio.mimsave('./movie.gif', images)