from dis import dis
import numpy as np
from PIL import Image
import math
from perlin_noise import PerlinNoise

def ClosestDist(point):
    temp_dist = []
    for shape in objects:
        temp_dist.append(shape.dist(point))
    mindist = min(temp_dist)
    return (mindist,objects[temp_dist.index(mindist)])

def CastRay(angleX, angleY, ClipEnd):
    ray = Ray(CameraPosition[0],CameraPosition[1],CameraPosition[2],angleX,angleY)
    traveldist = 0
    dist = ClosestDist(ray.pos)[0]
    count = 0
    while True:
        dist = ClosestDist(ray.pos)[0]
        traveldist+=dist
        ray.traverseRay(dist)
        count+=1
        if dist <= 0.0001:
            shape = ClosestDist(ray.pos)[1]
            # UV COLOR MODE
            # red = shape.size.x*2+ray.pos.x*shadowFactor
            # green = shape.size.y*2+ray.pos.y*shadowFactor
            # blue = shape.size.z*2+ray.pos.z*shadowFactor
            
            # return 1, [red,green,blue]

            #SHADED COLOR MODE
            color = shape.color(ray.pos)
            
            return 1, [color,color,color]
        if dist >= ClipEnd:
            return 0, [0,0,0]
    
 
    

    
# Create a resolutionXresolutionX3 array of 8 bit unsigned integers
resolution = 512
data = np.zeros((resolution,resolution,3))
imagearray = np.zeros((resolution,resolution,3),dtype=np.uint8)

# Classes
class Vector3:
    x = 0
    y = 0
    z = 0
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    
    def length(self, vector3):
        return math.sqrt((self.x-vector3.x)**2+(self.y-vector3.y)**2+(self.z-vector3.z)**2)

class Ray:
    pos = 0
    origin = 0
    angleX = 0
    angleY = 0 
    def __init__(self, x, y, z, angleX, angleY):
        self.pos = Vector3(x,y,z)
        self.origin = Vector3(x,y,z)
        self.angleX = angleX
        self.angleY = angleY
    
    def traverseRay(self,dist):
        self.pos.z += dist*math.sin(math.radians(self.angleY))
        self.pos.x += dist*math.cos(math.radians(self.angleY))*math.sin(math.radians(self.angleX))
        self.pos.y += dist*math.cos(math.radians(self.angleY))*math.cos(math.radians(self.angleX))

class Point:
    pos = 0
    def __init__(self, x, y, z):
        self.pos = Vector3(x,y,z)
    
    def dist(self, pointPos):
        return math.sqrt((self.pos.x-pointPos.x)**2+(self.pos.y-pointPos.y)**2+(self.pos.z-pointPos.z)**2)

class Sphere:
    center = 0
    radius = 0
    def __init__(self, x, y, z, radius):
        self.center = Vector3(x,y,z)
        self.radius = radius
    
    def dist(self, pointPos):
        return (math.sqrt((self.center.x-pointPos.x)**2+(self.center.y-pointPos.y)**2+(self.center.z-pointPos.z)**2))-self.radius
    def color(self,pointPos):
        return ((pointPos.y-self.center.y)+self.radius)/self.radius*2

# class Glob:
#     x = 0
#     y = 0
#     z = 0
#     radiusnum = 0
#     noise = PerlinNoise(octaves=20)
#     def __init__(self, x, y, z, radius):
#         self.x = x
#         self.y = y
#         self.z = z
#         self.radiusnum = radius
        
    
#     def dist(self, point):
#         return (math.sqrt((self.x-point.x)**2+(self.y-point.y)**2+(self.z-point.z)**2))-(self.radiusnum+(self.noise([point.x,point.y]))*3)
#     def radius(self,point):
#         return self.radiusnum+self.noise([point.x,point.y,point.z])

# TODO ADD CUBES DIST FUNCTION

class RectPrism:
    pos = 0
    size = 0
    def __init__(self, x, y, z, width, lenght, height):
        self.pos = Vector3(x,y,z)
        self.size = Vector3(width, lenght, height)

    def dist(self, pointVec):
        return math.sqrt((max([abs(pointVec.x)-(self.pos.x+self.size.x),0]))**2+(max([abs(pointVec.y)-(self.pos.y+self.size.y),0]))**2+(max([abs(pointVec.z)-(self.pos.z+self.size.z),0]))**2)

    def color(self,pointPos):
        return pointPos.y
        


# Objects

objects = [
    #RectPrism(200,0,0,10,10,10)
    Sphere(100,0,0,20)
]

# Camera Settings

CameraPosition=[0,20,0]
RotationX=0
RotationY=0

FOV = 90
ClipEnd=1000

shadowFactor=1

RayXOffset = FOV/resolution
RayYOffset = FOV/resolution

# Radius Calc

# point1 = Point(110,120,0)
# point2 = Point(100,110,10)
# print(point1.dist(point2))


# angle1 = 20
# angle2 = 10
# distanceMove = 4
# x = distanceMove*math.cos((angle1/360)*2*math.pi)*math.sin((angle2/360)*2*math.pi)
# y = distanceMove*math.sin((angle1/360)*2*math.pi)*math.sin((angle2/360)*2*math.pi)
# z = distanceMove*math.cos((angle2/360)*2*math.pi)


for y in range(resolution):
    print(round(100*y/resolution))
    for x in range(resolution):
        collision, color = CastRay(((x+resolution/2)*RayXOffset)+RotationX,((y-resolution/2)*RayYOffset)+RotationY,ClipEnd)
        data[x,y] = color

print(data)

data_max = np.amax(data)

for y in range(len(imagearray)):
    for x in range(len(imagearray)):
        for i in range(len(data[x,y])):
            imagearray[x,y,i] = int((data[x,y,i]/data_max)*255)

image = Image.fromarray(imagearray)
image.show()
#image.save("/home/micr0byte/SnowManRayMarching/"+str(frame)+".png")
