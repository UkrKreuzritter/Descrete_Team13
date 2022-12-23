from queue import PriorityQueue
import math
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
    # множимо на степ, бо по іншому воно не змінюється


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
        # додає вершину xy у visited

    return None


if __name__=="__main__":
    graph = read_csv('example3.csv')
    dist = int(graph[0][1])
    start_vertex = (int(graph[1][0]), int(graph[1][1]))
    finish = (int(graph[2][0]), int(graph[2][1]))
    graph = graph[4:]
    print(dijkstra(graph,dist,start_vertex,finish))
