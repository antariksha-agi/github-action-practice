"""Tests for the in-memory Task Manager in app.py."""

import pytest

import app


@pytest.fixture(autouse=True)
def clean_storage():
    """Give every test a fresh, empty task list and reset ids."""
    app.reset_tasks()
    yield
    app.reset_tasks()


# --- Creating tasks ---

def test_add_task_returns_task_with_title_and_id():
    task = app.add_task("Buy milk")

    assert isinstance(task, app.Task)
    assert task.title == "Buy milk"
    assert task.id == 1


def test_add_task_stores_task():
    task = app.add_task("Buy milk")

    assert app.get_tasks() == [task]


def test_add_task_strips_whitespace():
    task = app.add_task("  Buy milk  ")

    assert task.title == "Buy milk"


def test_new_task_is_incomplete_by_default():
    task = app.add_task("Buy milk")

    assert task.completed is False


# --- Retrieving tasks ---

def test_get_tasks_returns_all_in_order():
    app.add_task("First")
    app.add_task("Second")
    app.add_task("Third")

    tasks = app.get_tasks()

    assert [t.title for t in tasks] == ["First", "Second", "Third"]
    assert [t.id for t in tasks] == [1, 2, 3]


def test_get_tasks_empty_when_no_tasks():
    assert app.get_tasks() == []


def test_get_tasks_returns_copy():
    app.add_task("Buy milk")

    tasks = app.get_tasks()
    tasks.clear()

    assert len(app.get_tasks()) == 1


# --- Completing tasks ---

def test_complete_task_marks_completed():
    task = app.add_task("Buy milk")

    result = app.complete_task(task.id)

    assert result is task
    assert result.completed is True
    assert app.get_tasks()[0].completed is True


def test_complete_task_only_affects_target():
    first = app.add_task("First")
    second = app.add_task("Second")

    app.complete_task(first.id)

    assert first.completed is True
    assert second.completed is False


# --- Deleting tasks ---

def test_delete_task_removes_task():
    task = app.add_task("Buy milk")

    result = app.delete_task(task.id)

    assert result is task
    assert app.get_tasks() == []


def test_delete_task_keeps_other_tasks():
    app.add_task("First")
    app.add_task("Second")
    app.add_task("Third")

    app.delete_task(2)

    assert [t.id for t in app.get_tasks()] == [1, 3]


def test_ids_not_reused_after_delete():
    app.add_task("First")
    app.add_task("Second")
    app.delete_task(2)

    new_task = app.add_task("Third")

    assert new_task.id == 3


# --- Rejecting invalid titles ---

@pytest.mark.parametrize("title", ["", " ", "   ", "\t\n"])
def test_add_task_rejects_blank_titles(title):
    with pytest.raises(ValueError):
        app.add_task(title)


def test_rejected_title_does_not_store_task():
    with pytest.raises(ValueError):
        app.add_task("   ")

    assert app.get_tasks() == []
    assert app.add_task("Valid").id == 1


# --- Nonexistent task ids ---

def test_complete_nonexistent_task_raises():
    with pytest.raises(ValueError):
        app.complete_task(99)


def test_delete_nonexistent_task_raises():
    app.add_task("Buy milk")

    with pytest.raises(ValueError):
        app.delete_task(99)

    assert len(app.get_tasks()) == 1


def test_delete_same_task_twice_raises():
    task = app.add_task("Buy milk")
    app.delete_task(task.id)

    with pytest.raises(ValueError):
        app.delete_task(task.id)
