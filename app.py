"""A simple in-memory Task Manager."""


class Task:
    """A single task with an id, a title, and a completed flag."""

    def __init__(self, id, title, completed=False):
        self.id = id
        self.title = title
        self.completed = completed

    def __repr__(self):
        return f"Task(id={self.id}, title={self.title!r}, completed={self.completed})"


# In-memory storage
_tasks = []
_next_id = 1


def _find_task(task_id):
    """Return the task with the given id, or raise ValueError if not found."""
    for task in _tasks:
        if task.id == task_id:
            return task
    raise ValueError(f"No task found with id {task_id}")


def add_task(title):
    """Create a new task and return it. Rejects empty or whitespace-only titles."""
    global _next_id

    if not isinstance(title, str):
        raise ValueError("Task title must be a string")

    title = title.strip()
    if not title:
        raise ValueError("Task title cannot be empty")

    task = Task(_next_id, title)
    _tasks.append(task)
    _next_id += 1
    return task


def get_tasks():
    """Return a copy of the list of all tasks."""
    return list(_tasks)


def complete_task(task_id):
    """Mark a task as completed and return it."""
    task = _find_task(task_id)
    task.completed = True
    return task


def delete_task(task_id):
    """Remove a task from storage and return it."""
    task = _find_task(task_id)
    _tasks.remove(task)
    return task


def reset_tasks():
    """Clear all tasks and reset the id counter. Useful for tests."""
    global _next_id
    _tasks.clear()
    _next_id = 1
