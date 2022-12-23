from turtle import *
import time
from tkinter import *
from functools import partial
from queue import PriorityQueue
import math

hideturtle()
turz=Turtle()
turz.pensize(3)
turz.hideturtle()
turz._delay(0)
turf=Turtle()
turf.hideturtle()
turf.pensize(3)
turf._delay(0)
screen = Screen()
screen.tracer(0)

def read_csv(path):
    try:
        with open(path, 'r', encoding='utf-8') as file_csv:
            matrix = []
            lines = file_csv.readlines()
            for line in lines:
                matrix.append(line.strip().split())
                for i in range(len(matrix[-1])):
                    matrix[-1][i] = float(matrix[-1][i])
        return matrix
    except FileExistsError:
        print("File doesn't exist")
    # читає файл і записує кожен останній доданий рядок у флоат


def h(step,xs,ys,xf,yf):
    return (abs(xs-xf)+abs(ys-yf))*step
    # евристична функція
    # знаходить відстань між початковою і кінцевої вершиною; найбільш оптимальний варіант 
    # множимо на степ, бл по іншому воно не змінюється


def print_way(ways,finish,m):
    waymass=[finish]
    finish=finish[0]*m+finish[1]
    while ways[finish][1]:
        finish+=ways[finish][1]
        waymass.append((finish//m,finish%m))
    return waymass[::-1]
    # повертає список пар індексів шляху


def calc(graph,step,visited,queue,ways,x,y,dx,dy,fx,fy):
    n=len(graph)
    m=len(graph[0])
    if 0<=x+dx<n and 0<=y+dy<m and not visited[(x+dx)*m+y+dy]:
        new_dist=math.sqrt((graph[x][y]-graph[x+dx][y+dy])**2+step**2)
        if ways[(x+dx)*m+y+dy]==(0,0) or ways[x*m+y][0]+new_dist<ways[(x+dx)*m+y+dy][0]:
            ways[(x+dx)*m+y+dy]=(ways[x*m+y][0]+new_dist,-((dx)*m+dy))
            queue.put((ways[(x+dx)*m+y+dy][0]+h(step,dx+x,y+dy,fx,fy),(x+dx,y+dy)))
#  перевіряє довжину і за потреби змінює


def dijkstra(graph, step,start,finish):
    n=len(graph)
    # кількість рядків в таблиці
    m=len(graph[0])
    # кількість стовпців
    visited=[0]*(n*m)
    # створення масиву відвіданих вершин
    ways=[(0,0)]*(n*m)
    # масив, який зберігає в першому рядку відстань від початкової до теперішної вершини, а в іншому напрямок звідки прийшли
    queue=PriorityQueue()
    queue.put((0,start))
    # відстань від початкової вершини до теперішньої, вершина
    while not queue.empty():
        temp_v=queue.get()
        # отримує найменший елемент і вилучає
        while not queue.empty() and visited[temp_v[1][0]*m+temp_v[1][1]]:
            temp_v=queue.get()
        if temp_v[1]==finish:
            return print_way(ways,finish,m)
        x=temp_v[1][0]
        y=temp_v[1][1]    
        calc(graph,step,visited,queue,ways,x,y,1,0,finish[0],finish[1])
        calc(graph,step,visited,queue,ways,x,y,-1,0,finish[0],finish[1])
        calc(graph,step,visited,queue,ways,x,y,0,1,finish[0],finish[1])
        calc(graph,step,visited,queue,ways,x,y,0,-1,finish[0],finish[1])
        visited[x*m+y]=1
        # додає вершину [x][y] у visited

    return None


def draw_tower(turtle,height,step,degrees,color1,color2,x,y):
    turtle.penup()
    turtle.setheading(degrees)
    turtle.forward(x*step)
    turtle.setheading(-degrees)
    turtle.forward((len(table[0])-y)*step)
    turtle.pendown()
    if height>=0:
        turtle.fillcolor(color1)
        turtle.begin_fill()
        turtle.forward(step)
        turtle.setheading(90)
        turtle.forward(height)
        turtle.setheading(180-degrees)
        turtle.forward(step)
        turtle.setheading(-90)
        turtle.forward(height)
        turtle.end_fill()
        turtle.setheading(-degrees)
        turtle.forward(step)
        turtle.setheading(degrees)
        turtle.begin_fill()
        turtle.forward(step)
        turtle.setheading(90)
        turtle.forward(height)
        turtle.setheading(180+degrees)
        turtle.forward(step)
        turtle.setheading(-90)
        turtle.forward(height)
        turtle.end_fill()
        turtle.backward(height)
        turtle.setheading(degrees)
        turtle.fillcolor(color2)
        turtle.begin_fill()
        for i in range(2):
            turtle.forward(step)
            turtle.left(180-2*degrees)
            turtle.forward(step)
            turtle.left(2*degrees)
        turtle.end_fill()
        turtle.setheading(90)
        turtle.backward(height)
    if height<0:
        turtle.penup()
        turtle.setheading(degrees)
        turtle.forward(step)
        turtle.setheading(90)
        turtle.forward(height)
        turtle.setheading(degrees)
        turtle.backward(step)
        turtle.setheading(-degrees)
        turtle.forward(step)
        turtle.pendown()
        turtle.setheading(degrees)
        turtle.fillcolor(color2)
        turtle.begin_fill()
        for i in range(2):
            turtle.forward(step)
            turtle.left(180-2*degrees)
            turtle.forward(step)
            turtle.left(2*degrees)
        turtle.end_fill()
        turtle.penup()
        turtle.setheading(-90)
        turtle.forward(height)
        turtle.pendown()
    turtle.penup()
    turtle.setheading(-degrees)
    turtle.backward((len(table[0])-y+1)*step)
    turtle.setheading(degrees)
    turtle.backward(x*step)
    turtle.pendown()


def create_towers(turtle,table,n,m,n1,m1):
    global degrees,step,draw_table,screen
    color1="brown"
    for k in range(n-1,m-1,-1):
        for i in range(n1-1,m1-1,-1):
            draw_tower(turtle,table[k][i],step,degrees,color1,draw_table[k][i],k,i)


class player:
    global table,step,screen,degrees,draw_table,turz,turf
    r=10
    x=0
    y=0
    GameObj=None
    slow=False
    def __init__(self,start,r,color,slow):
        self.x=start[0]
        self.y=start[1]
        self.GameObj=Turtle()
        self.slow=slow
        self.GameObj.color(color)
        self.GameObj.hideturtle()
        self.GameObj.penup()
        self.r=r
        self.GameObj.backward(500)
        turz.penup()
        turf.penup()
        turz.backward(500)
        turf.backward(500)
        turz.pendown()
        turf.pendown()
        draw_table[start[0]][start[1]]="yellow"
        create_towers(turz,table,len(table),0,len(table[0]),0)
        self.take_pos(start[0],start[1])


    def move_player(self,direction,delta,gotox,gotoy):
        turz.clear()
        move=0
        move_delta=1
        self.GameObj.setheading(direction)
        if delta<0:
            move_delta*=-1
        if self.slow:
            self.GameObj.clear()
            self.GameObj.forward(delta)
            self.GameObj.dot(self.r)
            return
        create_towers(turz,table,len(table),gotox+1,len(table[0]),0)
        create_towers(turz,table,gotox+1,gotox,len(table[0]),gotoy)
        while abs(move)<=abs(delta):
            turf.clear()
            self.GameObj.clear()
            self.GameObj.forward(move_delta)
            self.GameObj.dot(self.r)
            move+=move_delta
            create_towers(turf,table,gotox+1,gotox,gotoy,0)
            create_towers(turf,table,gotox,0,len(table[0]),0)
            screen.update()
    def change_pos(self,dx,dy):
        self.GameObj.clear()
        if table[self.x+dx][self.y+dy]>table[self.x][self.y]:
            if table[self.x+dx][self.y+dy]-table[self.x][self.y]:
                self.move_player(90,table[self.x+dx][self.y+dy]-table[self.x][self.y],self.x,self.y)
            if dy==0:
                self.move_player(degrees,step*dx,self.x+dx,self.y+dy)
            else:
                self.move_player(180-degrees,step*dy,self.x+dx,self.y+dy)
        else:
            if dy==0:
                self.move_player(degrees,step*dx,self.x,self.y)
            else:
                self.move_player(180-degrees,step*dy,self.x,self.y)
            if table[self.x+dx][self.y+dy]-table[self.x][self.y]:
                self.move_player(-90,table[self.x][self.y]-table[self.x+dx][self.y+dy],self.x+dx,self.y+dy)
        self.x+=dx
        self.y+=dy
        draw_table[self.x][self.y]="yellow"
        turz.clear()
        turf.clear()
        create_towers(turz,table,len(table),self.x+1,len(table[0]),0)
        create_towers(turz,table,self.x+1,self.x,len(table[0]),self.y)
        self.GameObj.dot(self.r)
        create_towers(turz,table,self.x+1,self.x,self.y,0)
        create_towers(turz,table,self.x,0,len(table[0]),0)
        screen.update()

    def take_pos(self,x,y):
        self.GameObj.setheading(90)
        self.GameObj.forward(table[x][y])
        self.GameObj.setheading(-degrees)
        self.GameObj.forward((len(table[0])-y+0.5)*step)
        self.GameObj.setheading(degrees)
        self.GameObj.forward((x+0.5)*(step))
        self.GameObj.dot(self.r)
        screen.update()
        time.sleep(2)

    def draw_path(self,path):
        for i in range(1,len(path)):
            self.change_pos(path[i][0]-path[i-1][0],path[i][1]-path[i-1][1])
            time.sleep(1)

def convert_table(table):
    minim=min(min(table))
    if minim<0:
        for i in range(len(table)):
            for j in range(len(table[i])):
                table[i][j]+=abs(minim)
    for i in range(len(table)//2):
        table[i],table[len(table)-1-i]=table[len(table)-1-i],table[i]
    new_arr=[[0]*len(table) for i in range(len(table[0]))]
    for i in range(len(table[0])):
        for j in range(len(table)):
            new_arr[i][j]=table[j][i]
    return new_arr

def full_draw_table(table):
    rem=[["green"]*len(table[0]) for i in range(len(table))]
    for i in range(len(rem)):
        for j in range(len(rem[0])):
            if table[i][j]<0:
                rem[i][j]="grey"
    return rem

table=[
    [103,10,34,13,10],
    [50,10,45,10,10],
    [20,10,90,10,10],
    [60,100,100,math.sqrt(200),100+23-12/3],
    [10,80,10,250,40]
    
]
degrees=30
step=100
start=(0,0)
finish=(3,2)
teleport=True
if __name__=="__main__":
    table=convert_table(table)
    draw_table=full_draw_table(table)
    player=player(start,step/2,"red",teleport)
    rem=dijkstra(table,step,start,finish)
    player.draw_path(rem)
    screen.update()
    done()    


