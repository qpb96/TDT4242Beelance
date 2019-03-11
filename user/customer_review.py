from projects.models import Project, Task
from django.contrib.auth.models import User


def review_possible(request, project_owner):
    if is_any_project_finished(request, project_owner) or task_delivered_or_declined(request, project_owner):
        return True
    return False

# Get all projects
# Get all participant from project/tasks
# Check if there exist a task where a user is a participant
# Check if there exist any task with project status: isFinished or task-status pa/dd


# Check status of a task. Return True if task.status = delivered or declined
def task_delivered_or_declined(request, participant_name):
    tasks = tasks_by_user(request)
    for task in tasks:
        print("NICE")
        print(task)
        if check_user_in_task(participant_name, task):
            if task.status == 'pa' or task.status == 'dd':
                return True
            print(task.status)
    print("RIIIIIP")
    return False


# Check if there exist any finished projects where request.user is a participant
def is_any_project_finished(request, participant):
    if participant_in_project(request, participant):
        projects = projects_by_customer(request.user.username)
        for project in projects:
            if project.status == 'f':
                return True
    return False


# Check if a participant is in any project made by customer
def participant_in_project(request, participant_name):
    projects = projects_by_customer(request.user.username)
    for project in projects:
        all_participants = project.participants.all()
        participant = User.objects.get(username=participant_name)
        for p in all_participants:
            if participant.profile == p:
                return True
    return False


# Search for all projects made by a user
def projects_by_customer(customer):
    list_of_projects = Project.objects.all()
    projects_by_user = []
    for project in list_of_projects:
        if project.user.user.username == customer:
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


# Return a list of tasks made by customer
def tasks_by_user(request):
    username = request.user.username
    projects = projects_by_customer(username)
    list_tasks = []
    for project in projects:
        tasks = tasks_of_project(project.title)
        for task in tasks:
            list_tasks.append(task)
    return list_tasks


# See if user is a participant in a spesific task
def check_user_in_task(username, taskobject):
    all_tasks = Task.objects.all()
    task1 = None
    participants = None
    participant = User.objects.get(username=username)
    for t in all_tasks:
        if taskobject == t:
            task1 = t;
            participants = task1.read.all()
    for profile in participants:
        if participant.profile == profile:
            return True
    return False
