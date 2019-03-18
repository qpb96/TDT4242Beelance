from django.test import TestCase, RequestFactory
from projects import models, views
from user.models import User, Profile
from .views import project_view



# Create your tests here.
# Test  project_view


class ProjectViewTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory();
        projectCategory = models.ProjectCategory.objects.create(pk=1, name="Cleaning")
        user = User.objects.create(pk=1, username="user", first_name="Per", last_name="Jørgensen",
                                   email="qpb96@gmail.com")
        user_freelancer = User.objects.create(pk=2, username="qpb96", first_name="Tom", last_name="Kjellnes", email="ninja96@gmail.com")
        profile = Profile.objects.get(user=user)
        project = models.Project.objects.create(pk=1, user=profile, title="Vask bilen min",
                                                description="Så fort som mulig", category=projectCategory, status="o")
        task = models.Task.objects.create(pk=1, project=project, title="VASK MEG", description="plz", budget=200)
        task_offer = models.TaskOffer.objects.create(pk=1, task=task, offerer=user_freelancer.profile, title="Jeg kan", price=200, description="jeg kan")

        self.user_customer = user
        self.project = project
        self.task = task
        self.user_freelancer = user_freelancer
        self.task_offer = task_offer



    def test_project_view(self):
        request = self.factory.get('/project/'+str(self.user_customer.id));
        request.user = self.user_customer
        response = project_view(request, self.project.id)
        self.assertEqual(response.status_code, 200)

        #Offer respone
        post = self.factory.post('/project/'+str(self.user_customer.id),
                                 {'taskofferid': self.task_offer.id, 'offer_response':'', 'feedback': "I accept",
                                  'status': 'a'})
        post.user = self.user_customer
        response = project_view(post, self.project.id)
        self.assertEqual(response.status_code, 200)

        #Project's status change
        post = self.factory.post('/project/'+str(self.user_customer.id),
                                 {'status_change': '', 'status': 'i'})
        post.user = self.user_customer
        response = project_view(post, self.project.id)
        self.assertEqual(response.status_code, 200)

        #Send offer for a task
        post = self.factory.post('/project/'+str(self.user_freelancer.id),
                                 {'offer_submit': '', 'title': 'M19 Tar jobben',
                                  'description': "Jeg kan gjøre det for 10kr billigere",
                                  'price': 99, 'taskvalue': self.task.id})
        post.user = self.user_freelancer
        respone = project_view(post, self.project.id)
        self.assertEqual(response.status_code, 200)


