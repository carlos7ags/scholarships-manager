from actions.models import PendingTasks, Task


def auto_assign_tasks_at_user_creation(username):
    tasks = Task.objects.filter(auto_create_at_user_init=True).all()
    for task in tasks:
        pending_task = PendingTasks(
            username=username,
            task=task,
        )
        pending_task.save()
