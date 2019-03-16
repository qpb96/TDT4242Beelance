from django.test import TestCase
from django.contrib.auth.models import User

# Create your tests here.
from projects.models import Project, ProjectCategory, Task, TaskOffer
from projects.views import get_user_task_permissions
from user.models import Profile


class get_user_task_permissions_testcase(TestCase):
    def setUp(self):
        ProjectCategory.objects.create(name="CategoryOne")
        projectOwner = Profile.objects.create(user=User.objects.create(username="ProjectOwner"), user_id=8787)
        taskParticipant = Profile.objects.create(user=User.objects.create(username="TaskParticipant"), user_id=8788)
        nonTaskParticipant = Profile.objects.create(user=User.objects.create(username="NonTaskParticipant"), user_id=8789)
        project = Project.objects.create(user=Profile.objects.get(user=User.objects.get(username="ProjectOwner")), title="title", description="description", category=ProjectCategory.objects.get(name="CategoryOne"))
        task = Task.objects.create(project=project, title="task", description="description")
        taskoffer = TaskOffer.objects.create(task=task, offerer=taskParticipant, title="task offer", description="desciption", status='a')

    def test_taskParticipant(self):
        project=Project.objects.get(title="title")
        task=Task.objects.get(project=project)
        taskParticipant = Profile.objects.get(user_id=8788)
        permissionForTp={
            'write': True,
            'read': True,
            'modify': True,
            'owner': False,
            'upload': True,
        }
        self.assertEqual(get_user_task_permissions(taskParticipant, task), permissionForTp)

    def test_owner(self):
        project=Project.objects.get(title="title")
        task=Task.objects.get(project=project)
        projectOwner = Profile.objects.get(user=User.objects.get(username="ProjectOwner"))
        permissionForOwner={
            'write': True,
            'read': True,
            'modify': True,
            'owner': True,
            'upload': True,
        }
        self.assertEqual(get_user_task_permissions(projectOwner, task), permissionForOwner)
        pass

    def test_nonParticipant(self):
        project=Project.objects.get(title="title")
        task=Task.objects.get(project=project)
        nonTaskParticipant = Profile.objects.get(user=User.objects.get(username="NonTaskParticipant"))
        permissionForNonTp={
            'write': False,
            'read': False,
            'modify': False,
            'owner': False,
            'view_task': False,
            'upload': False,
        }
        self.assertEqual(get_user_task_permissions(nonTaskParticipant, task), permissionForNonTp)


