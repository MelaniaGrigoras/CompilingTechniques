import sys

from graphviz import Digraph

# read alphabet and regex from file
file = open("InputFile.txt", "r")
indexRow = 0
for row in file:
    if indexRow == 0:
        alphabet = row[:-1].split(',')
    elif indexRow == 1:
        expression = row[:-1]
    else:
        string = row
    indexRow += 1
file.close()

epsilon = '\u03B5'
other_symb = ['(', ')', '*', '|']

# validate the expression
for symb in expression:
    if symb not in (alphabet + other_symb):
        sys.exit('Invalid expression!')


# print("Alphabet:", alphabet)
# print("expression:", expression)

# add a new vertex to the graph
def addVertex(v, graph):
    if v in graph:
        print("Vertex ", v, " is already in the graph.")
    else:
        graph[v] = []


# add a new edge between vertex v1 and v2 with edge weight w
def addEdge(v1, v2, w, graph):
    if v1 not in graph:
        print("Vertex ", v1, " not found.")
    elif v2 not in graph:
        print("Vertex ", v2, " not found.")
    else:
        temp = [v2, w]
        graph[v1].append(temp)


# remove the edge between v1 and v2
def removeEdge(v1, v2, graph):
    exit = 0
    for l in graph[v1]:
        if l[0] == v2:
            exit = 1

    if (exit == 1):
        v = graph[v1]
        v.remove(l)
        graph[v1] = v
    else:
        print("The edge between ", v1, " and ", v2, " was not found.")


# update the vertex v1 with v2
def updateVertex(v, v1, v2, graph):
    exit = 0
    for l in graph[v]:
        if l[0] == v1:
            exit = 1
            break
    if (exit == 1):
        values = graph[v]
        values.remove(l)
        l[0] = v2
        values.append(l)
        graph[v] = values


# returns the vertex with the maximum value
def max_vertex():
    # print("Maximum vertex", max(graph.keys()))
    return max(graph.keys())


# Thompson's rule for Kleene closure
def star(vertex, symb):
    new_vertex = max_vertex() + 1
    addVertex(new_vertex, graph)
    addVertex(new_vertex + 1, graph)
    addVertex(new_vertex + 2, graph)

    addEdge(vertex, new_vertex, epsilon, graph)
    addEdge(vertex, new_vertex + 2, epsilon, graph)
    addEdge(new_vertex, new_vertex + 1, symb, graph)
    addEdge(new_vertex + 1, new_vertex, epsilon, graph)
    addEdge(new_vertex + 1, new_vertex + 2, epsilon, graph)

    new_vertex = new_vertex + 2
    return new_vertex


# Thompson's rule for concatenation
def concatenation(vertex, firstSymbol, secondSymbol, graph):
    new_vertex = max_vertex() + 1
    addVertex(new_vertex, graph)
    addVertex(new_vertex + 1, graph)
    addVertex(new_vertex + 2, graph)

    addEdge(vertex, new_vertex, firstSymbol, graph)
    addEdge(new_vertex, new_vertex + 1, epsilon, graph)
    addEdge(new_vertex + 1, new_vertex + 2, secondSymbol, graph)

    new_vertex = new_vertex + 2
    return new_vertex

# TODO fix union method
def union(vertex, firstSymb, secondSymb, graph):
    new_vertex = max_vertex() + 1
    addVertex(new_vertex, graph)
    addVertex(new_vertex + 1, graph)
    addVertex(new_vertex + 2, graph)
    addVertex(new_vertex + 3, graph)
    addVertex(new_vertex + 4, graph)

    addEdge(vertex, new_vertex, epsilon, graph)
    addEdge(new_vertex, new_vertex + 1, firstSymb, graph)
    addEdge(new_vertex + 1, new_vertex + 4, epsilon, graph)

    addEdge(vertex, new_vertex + 2, epsilon, graph)
    addEdge(new_vertex + 2, new_vertex + 3, secondSymb, graph)
    addEdge(new_vertex + 3, new_vertex + 4, epsilon, graph)

    new_vertex = new_vertex + 4
    return new_vertex


# show diagraph
def showGraph(graph):
    f = Digraph('NFA-ε', filename='diagraph.gv')
    f.attr(rankdir='LR', size='8,5')

    for k, v in graph.items():
        if not v:
            f.attr('node', shape='doublecircle')
            f.node(str(k))

    for k, v in graph.items():
        if v:
            for l in v:
                f.attr('node', shape='circle')
                f.edge(str(k), str(l[0]), label=l[1])

    f.view()


# constructing the graph from a regex
def algorithm(vertex, expression, graph, symb=None):
    if expression == '':
        return
    elif len(expression) == 1:
        new_vertex = max_vertex()
        new_vertex += 1
        addVertex(new_vertex, graph)
        addEdge(vertex, new_vertex, expression, graph)
    else:
        if expression[0] not in alphabet:
            if expression[0] == '(':
                expression = expression[1:]
                temp_expression = ''
                while expression[0] != ')':
                    temp_expression += expression[0]
                    expression = expression[1:]
                # delete the close paranthesis and star
                expression = expression[2:]
                star(vertex, 'expression')
                rightVertex = None
                exit = 0
                for k, v in graph.items():
                    for l in v:
                        if l[1] == 'expression':
                            rightVertex = l[0]
                            exit = 1
                            break
                    if exit == 1:
                        leftVertex = k
                        break
                removeEdge(leftVertex, rightVertex, graph)
                algorithm(leftVertex, temp_expression, graph, symb=temp_expression)
                del_vertex = max_vertex()
                updateVertex(del_vertex - 1, del_vertex, rightVertex, graph)
                graph.pop(del_vertex)
                algorithm(rightVertex + 1, expression, graph)

            elif expression[0] == '|':
                expression = expression[1:]
                initialVertex = max_vertex() + 1
                addVertex(initialVertex, graph)
                addEdge(0, initialVertex, epsilon, graph)
                algorithm(initialVertex, expression, graph)

        elif expression[0] in alphabet:
            symb = expression[0]
            expression = expression[1:]

            if expression[0] == '*':
                expression = expression[1:]
                vertex = star(vertex, symb)
                algorithm(vertex, expression, graph)

            elif expression[0] in alphabet:
                secondSymb = expression[0]
                expression = expression[1:]
                vertex = concatenation(vertex, symb, secondSymb, graph)
                algorithm(vertex, expression, graph)


graph = {}
initialVertex = 0
addVertex(initialVertex, graph)
algorithm(initialVertex, expression, graph)
print(graph)
showGraph(graph)
