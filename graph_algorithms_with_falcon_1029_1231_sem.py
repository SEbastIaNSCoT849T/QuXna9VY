# 代码生成时间: 2025-10-29 12:31:33
import falcon
import json
from collections import deque


# Define a graph using adjacency list representation
class Graph:
    def __init__(self, vertices):
        self.V = vertices  # No. of vertices
        self.graph = []  # default dictionary to store graph
        for i in range(vertices):
            self.graph.append([])

    def addEdge(self, u, v):
        # Add an undirected edge from u to v
        self.graph[u].append(v)
        self.graph[v].append(u)

    # A recursive function used by BFS
    def BFSHelper(self, s, visited):
        visited[s] = True
        print(s, end=" ")
        for i in self.graph[s]:
            if not visited[i]:
                self.BFSHelper(i, visited)

    # BFS traversal of the vertices reachable from s
    def BFS(self, s):
        visited = [False] * self.V
        self.BFSHelper(s, visited)

    # A recursive function used by DFS
    def DFSHelper(self, v, visited):
        visited[v] = True
        print(v, end=" ")
        for i in self.graph[v]:
            if not visited[i]:
                self.DFSHelper(i, visited)

    # DFS traversal of the vertices reachable from v
    def DFS(self, v):
        visited = [False] * self.V
        self.DFSHelper(v, visited)


class GraphResource:
    def __init__(self):
        self.graph = Graph(5)  # Initialize a graph with 5 vertices
        self.graph.addEdge(0, 1)
        self.graph.addEdge(0, 2)
        self.graph.addEdge(1, 2)
        self.graph.addEdge(1, 3)
        self.graph.addEdge(2, 4)

    def on_get(self, req, resp):
        """Handles GET requests for exploring graph algorithms.

        Args:
            req (falcon.Request): The incoming request.
            resp (falcon.Response): The outgoing response.
        """
        try:
            bfs_response = self.graph.BFS(0)  # Perform BFS starting from vertex 0
            dfs_response = self.graph.DFS(0)  # Perform DFS starting from vertex 0
            result = {"BFS": bfs_response, "DFS": dfs_response}
        except Exception as e:
            raise falcon.HTTPError(falcon.HTTP_500, "An error occurred", str(e))
        resp.media = result
        resp.status = falcon.HTTP_200


# Initialize Falcon API
api = falcon.API()
graph_resource = GraphResource()
api.add_route("/graph", graph_resource)

# Run API
if __name__ == "__main__":
    import socketserver
    import threading

    class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
        pass
    httpd = ThreadedTCPServer(("", 8000), api)
    print("Serving on port 8000...
")
    threading.Thread(target=httpd.serve_forever).start()