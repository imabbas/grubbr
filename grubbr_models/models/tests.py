from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from .models import User, Meal
import urllib.request
import urllib.parse
import json

class UserTestCase(TestCase):
    #setUp method is called before each test in this class
    def setUp(self):
        self.first_user = User.objects.create(email = "test@example.com", password = "password", first_name = "first", last_name = "user")
        
        self.sample_data = {'email': 'testp@virginia.edu',
                       'password': 'password',
                       'first_name': 'tester',
                       'last_name': 'testing'
        }
        
    def test_create_user(self):
        url = reverse('user_create')
        user_data = {'email': 'dankramp@virginia.edu',
                     'password': 'password',
                     'first_name': 'Dan',
                     'last_name': 'Kramp'
        }
        
        response = self.client.post(url, user_data, format='json')

        # Verify response is successful
        res = json.loads(response.content.decode('utf-8'))
        self.assertTrue(res['success'])

        # Verify that there are now two objects in the database
        self.assertEqual(User.objects.count(), 2)

        # Compare email addresses of objects
        new_user = User.objects.get(pk=2)
        self.assertEqual(new_user.email, user_data['email'])

            
    def test_update_user(self):
        url = reverse('user_action', args=[self.first_user.id])

        response = self.client.post(url, {'email': 'testemail@test.net'}, format='json')

        # Verify that it returns the desired status code
        self.assertEqual(response.status_code, 200)

        # Verify still just one user in db
        self.assertEqual(User.objects.count(), 1)

        # Compare email addresses to make sure they changed
        self.assertEqual(User.objects.get(pk=self.first_user.id).email, 'testemail@test.net')
            
    def test_delete_user(self):
        uid = self.first_user.id
        url = reverse('user_action', args=[uid])
        response = self.client.delete(url)

        # Verify return status
        self.assertEqual(response.status_code, 200)

        # Verify that there are no User objects left in db
        self.assertEqual(User.objects.count(), 0)
            
    def test_get_user(self):
        url = reverse('user_action', args=[self.first_user.id])
        response = self.client.get(url)

        # Verify return status
        self.assertEqual(response.status_code, 200)

        # Verify response is successful
        res = json.loads(response.content.decode('utf-8'))
        self.assertEqual(res['result']['email'], self.first_user.email)
              
    def tearDown(self):
        pass


class MealTestCase(TestCase):
    #setUp method is called before each test in this class
    def setUp(self):
        self.first_meal = Meal.objects.create(price = 8, name = "Cheeseburger", description = "Angus beef patty with New York sharp cheddar on a Kaiser roll.", portions = 2)
        
        self.sample_data = {'name': 'Hamburger',
                       'price': 7,
                       'description': 'Angus beef patty on Kaiser roll.',
                       'portions': 1
        }
        
    def test_create_meal(self):
        url = reverse('meal_create')
        
        response = self.client.post(url, self.sample_data, format='json')

        # Verify response is successful
        res = json.loads(response.content.decode('utf-8'))
        self.assertTrue(res['success'])

        # Verify that there are now two objects in the database
        self.assertEqual(Meal.objects.count(), 2)

        # Compare name and description of Meals
        new_meal = Meal.objects.get(pk=2)
        self.assertEqual(new_meal.name, self.sample_data['name'])
        self.assertEqual(new_meal.description, self.sample_data['description'])

            
    def test_update_meal(self):
        url = reverse('meal_action', args=[self.first_meal.id])

        response = self.client.post(url, {'name': 'Vegan Burger', 'description': 'Tofu patty on cardboard roll.'}, format='json')

        # Verify that it returns the desired status code
        self.assertEqual(response.status_code, 200)

        # Verify still just one user in db
        self.assertEqual(Meal.objects.count(), 1)

        # Compare name and description
        meal = Meal.objects.get(pk=self.first_meal.id)
        self.assertEqual(meal.name, 'Vegan Burger')
        self.assertEqual(meal.description, 'Tofu patty on cardboard roll.')
            
    def test_delete_meal(self):
        url = reverse('meal_action', args=[self.first_meal.id])
        response = self.client.delete(url)

        # Verify return status
        self.assertEqual(response.status_code, 200)

        # Verify that there are no User objects left in db
        self.assertEqual(Meal.objects.count(), 0)
            
    def test_get_meal(self):
        url = reverse('meal_action', args=[self.first_meal.id])
        response = self.client.get(url)

        # Verify return status
        self.assertEqual(response.status_code, 200)

        # Verify response is successful
        res = json.loads(response.content.decode('utf-8'))
        self.assertEqual(res['result']['name'], self.first_meal.name)
              
    def tearDown(self):
        pass
        
