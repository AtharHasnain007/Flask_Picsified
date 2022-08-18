# import matplotlib.pyplot as plt
# import cv2
# import numpy as np
# import os
# def converter():
#     path="uploads\\21"
#     MainImage=cv2.imread(os.path.join(path,"MAIN.jpg"))
#     # MainImage=cv2.resize(MainImage,(20250,13500))
#     heightmain = MainImage.shape[0]
#     widthmain = MainImage.shape[1]
#     if(widthmain/heightmain>=1):
#         MainImage=cv2.resize(MainImage,(20250,13500))
#     elif(widthmain/heightmain<1):
#         MainImage=cv2.resize(MainImage,(12500,17000))
#     plt.imshow(cv2.cvtColor(MainImage,cv2.COLOR_BGR2RGB))
#     MainImage=cv2.cvtColor(MainImage, cv2.COLOR_BGR2HSV)

#     ImPerRow=20
#     Count=0
#     data=[]
#     for i in range(1,ImPerRow**2+1):
#         name = str(Count) + ".jpg"
#         ImPath=os.path.join(path,name)
#         Img=cv2.imread(ImPath)
#         Img=cv2.resize(Img,(900,1350))
#         Count+=1
#         if i%106==0:
#             Count=0
#         data.append(Img)
#         Tile=np.array(data)
#     n,h,w,c=Tile.shape 
#     Tile=(Tile.reshape(ImPerRow,ImPerRow,h,w,c).swapaxes(1,2).reshape(h*ImPerRow,w*ImPerRow,c))
#     if(widthmain/heightmain>=1):
#         Tile=cv2.resize(Tile,(20250,13500))
#     elif(widthmain/heightmain<1):
#         Tile=cv2.resize(Tile,(12500,17000))
#     Tile=cv2.cvtColor(Tile, cv2.COLOR_BGR2HSV)
#     Tile[:,:,0]=MainImage[:,:,0]
#     Tile[:,:,1]=MainImage[:,:,1]
#     MainImage=MainImage[:,:,2]
#     Tile[:,:,2]=0.8*MainImage+0.2*Tile[:,:,2]


#     Tile=cv2.cvtColor(Tile,cv2.COLOR_HSV2RGB)
#     plt.figure(2)
#     plt.imshow(Tile) 
#     cv2.imwrite(os.path.join(path,"TILE.jpg"),cv2.cvtColor(Tile,cv2.COLOR_BGR2RGB))
#     #h1,s1,v1 = cv2.split(hsv1)

# if __name__ == "__main__":
#     converter()