from projects.models import Project, Task


def review_possible(request, project_id):
    project = Project.objects.get(id=project_id)
    tasks = get_tasks(project.id)
    participants = all_participants(tasks)
    reviewable_participants = []
    # All participants and customer can write a review when a a project is finished
    if is_project_finished(request, project_id):
        print("PROSJEKT FERDIG")
        for task in tasks:
            p = get_participants(task)
            for participant in p:
                reviewable_participants.append(participant)
        return True
    for task in tasks:
        t = Task.objects.get(title=task.title)
        if task_delivered_or_declined(project_id, t.title):
            particpants = participants_reviewable(project_id, t.title)
            for p in particpants:
                reviewable_participants.append(p)
    # A participant who has delivered or got declined can write a review to customer
    if request.user.profile in reviewable_participants:
#        print(reviewable_participants)
        return True
    # Customer should be able to to review particapants where the delivery got declined
    if is_customer(request, project_id) and len(reviewable_participants) != 0:
        for p in reviewable_participants:
            reviewable_participants.append(p)
            return True
    #TODO implement logioc
    return False


#Write a review of a participant that has delivered
def participants_reviewable(project_id, task_title):
    participants_reviewable = []
    if task_delivered_or_declined(project_id, task_title):
        task = Task.objects.get(title=task_title)
        p = get_participants(task)
        for participant in p:
            if participant not in participants_reviewable:
                participants_reviewable.append(participant)
    print("DISSE KAN REVIEWES")
    print(participants_reviewable)
    return participants_reviewable


# Check if there exist any finished projects where request.user is a participant
def is_project_finished(request, project_id):
    p = Project.objects.get(id=project_id)
    if p.status == 'f':
        return True
    return False


def task_delivered_or_declined(project_id, task_title):
    project = Project.objects.get(id=project_id)
    t = Task.objects.get(project=project, title=task_title)
    if t.status == 'da' or t.status == 'pa':
        return True
    return False


"""""
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
"""
# Return tasks of a project
def get_tasks(project_id):
    project = Project.objects.get(id=project_id)
    tasks_of_project = []
    project_tasks = project.tasks.all()
    for task in project_tasks:
        tasks_of_project.append(task)
    return tasks_of_project

def is_customer(request, project_id):
    project = Project.objects.get(id=project_id)
    if request.user == project.user.user:
        return True
    return False

# Participants => Collection of Profile objects
def all_participants(tasks):
    participants = []
    for task in tasks:
        p = get_participants(task)
        for participant in p:
            participants.append(participant)
    return participants

def get_participants(task):
    participants =[]
    p_with_read_access = task.read.all()
    p_with_write_access = task.write.all()
    p_with_mod_access = task.modify.all()
    for r in p_with_read_access :
        participants.append(r)
    for w in p_with_write_access:
        if w not in participants:
            participants.append(w)
    for m in p_with_mod_access:
        if m not in participants:
            participants.append(m)
    return participants

"""
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

# Check status of a task. Return True if task.status = delivered or declined
def task_delivered_or_declined(request, project_owner):
    tasks = tasks_by_customer(project_owner)
    for task in tasks:
        if check_user_in_task(request, task):
            if task.status == 'pa' or task.status == 'dd':
                return True
    return False
    
"""