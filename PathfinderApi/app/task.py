from celery import shared_task
from time import sleep
from .PathService import findPath

@shared_task(bind=True)
def slow_find_path_task(self, from_node_name, to_node_name):
    """
    Celery task that simulates slow path finding by sleeping for 5 seconds
    then calling the FindPath logic
    """
    try:
        # Simulate slow processing
        sleep(5)
        
        # Call the actual path finding logic
        result = findPath(from_node_name, to_node_name)
        
        return {
            'status': 'SUCCESS',
            'result': result,
            'from_node': from_node_name,
            'to_node': to_node_name
        }
    except Exception as exc:
        # Update task state to FAILURE
        self.update_state(
            state='FAILURE',
            meta={
                'error': str(exc),
                'from_node': from_node_name,
                'to_node': to_node_name
            }
        )
        raise exc