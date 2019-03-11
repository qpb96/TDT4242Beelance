
from projects.models import Project, Task


def review_possible(request, project_owner):
    if is_any_project_finished(request, project_owner) or task_delivered_or_declined(request, project_owner):
        return True
    return False


# Check status of a task. Return True if task.status = delivered or declined
def task_delivered_or_declined(request, project_owner):
    tasks = tasks_by_customer(project_owner)
    for task in tasks:
        if check_user_in_task(request, task):
            if task.status == 'pa' or task.status == 'dd':
                return True
    return False


# Check if there exist any finished projects where request.user is a participant
def is_any_project_finished(request, project_owner):
    if participant_in_project(request, project_owner):
        projects = project_by_user(project_owner)
        for project in projects:
            if project.status == 'f':
                return True
    return False


# Check if request.user is a participant in any project made by a user
def participant_in_project(request, project_owner):
    projects = project_by_user(project_owner)
    for project in projects:
        all_participants = project.participants.all()
        for participant in all_participants:
            if request.user.profile == participant:
                return True
    return False


# Search for all projects made by a user
def project_by_user(username):
    list_of_projects = Project.objects.all()
    projects_by_user = []
    for project in list_of_projects:
        if project.user.user.username == username:
            projects_by_user.append(project)
    return projects_by_user


# Return tasks of a project
def tasks_of_project(project_name):
    project = Project.objects.get(title=project_name)
    tasks_of_project = []
    project_tasks = project.tasks.all()
    print(project_tasks)
    for task in project_tasks:
        tasks_of_project.append(task)
    return tasks_of_project


# Return a list of tasks made by a user
def tasks_by_customer(username):
    projects = project_by_user(username)
    list_tasks = []
    for project in projects:
        tasks = tasks_of_project(project.title)
        for task in tasks:
            list_tasks.append(task)
    return list_tasks


# See if user is a participant in a spesific task
def check_user_in_task(request, taskobject):
    all_tasks = Task.objects.all()
    task1 = None
    participants = None
    for t in all_tasks:
        if taskobject == t:
            task1 = t;
            participants = task1.read.all()
    print(participants)
    for profile in participants:
        if request.user.profile == profile:
            return True
    return False
