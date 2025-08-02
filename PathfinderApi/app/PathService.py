from .models import Node

def findPath(from_name, to_name):
    try:
        start = Node.objects.get(name=from_name)
        path = []
        while start:
            path.append(start.name)
            if start.name == to_name:
                return path
            start = start.parent
        return None
    except Node.DoesNotExist:
        return None