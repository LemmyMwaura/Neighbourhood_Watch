from django.test import TestCase
from .models import Profile, Neighbourhood, Business, Post
from django.contrib.auth.models import User

class AwwardsClone(TestCase):
    @classmethod
    def setUpTestData(cls):
        '''
        The setup method will run before each test case
        '''
        cls.user = User.objects.create_user(
            username='lemmy',
            email='lemmy@lemmy.com',
            password='lemmy1234'
        )

        cls.profile = Profile.objects.get(id=1)

        cls.neighbourhood = Neighbourhood.objects.create(
            name='Limuru neighbourhood',
        )

        cls.post = Post.objects.create(
            user = Profile.objects.get(id=1),
            hood = Neighbourhood.objects.get(id=1),
            message = 'Party tomorrow,My house',
        )

        cls.business = Business.objects.create(
            name = 'Laundry Mat business',
            description = 'Laundry business',
            email = 'laundrymat@laundry.com',
            business_number = 2554556,
            users_name = Profile.objects.get(id=1),
            Neighbourhood_bsns = Neighbourhood.objects.get(id=1),
        )

    def tearDown(self):
        '''
        The teardown method does the cleanup after each test has run.
        '''
        User.objects.all().delete()
        Profile.objects.all().delete()
        Neighbourhood.objects.all().delete()
        Business.objects.all().delete()

    def test_instance(self):
        '''
        Test the instance of each object
        '''
        self.assertTrue(isinstance(self.user, User))
        self.assertTrue(isinstance(self.profile, Profile))
        self.assertTrue(isinstance(self.neighbourhood, Neighbourhood))
        self.assertTrue(isinstance(self.business, Business))

    def test_create_objects(self):
        '''
        test_create_objects test case to test if the objects are successfully 
        created
        '''
        self.neighbourhood_two = Neighbourhood(
            name='Limuru neighbourhood',
        )

        self.post_two = Post(
            user = Profile.objects.get(id=1),
            hood = Neighbourhood.objects.get(id=1),
            message = 'Party tomorrow,My house',
        )

        self.business_two = Business(
            name = 'Laundry Mat business',
            description = 'Laundry business',
            email = 'laundrymat@laundry.com',
            business_number = 2554556,
            users_name = Profile.objects.get(id=1),
            Neighbourhood_bsns = Neighbourhood.objects.get(id=1),
        )
        
        self.neighbourhood_two.create_neighbourhood()
        self.post_two.create_post()
        self.business_two.create_business()

        neighbourhoods = Neighbourhood.objects.all()
        businesses = Business.objects.all()
        posts = Post.objects.all()

        self.assertEqual(len(neighbourhoods), 2)
        self.assertEqual(len(businesses), 2)
        self.assertEqual(len(posts), 2)

    def test_delete_objects(self):
        '''
        test_delete_object test case to test if the objects are removed from
        the db.
        '''
        self.neighbourhood.delete_neighbourhood()
        self.business.delete_business()
        self.post.delete_post()

        neighbourhood = Neighbourhood.objects.all()
        businesses = Business.objects.all()
        posts = Post.objects.all()

        self.assertEqual(len(neighbourhood), 0)
        self.assertEqual(len(businesses), 0)
        self.assertEqual(len(posts), 0)
    
    def test_update_objects(self):
        '''
        test_update_objects test case to test if the objects are updated in
        the db
        '''
        self.neighbourhood.name = 'Limuru'
        self.neighbourhood.update_neighbourhood()
        self.assertEqual(self.neighbourhood.name, 'Limuru')

        self.business.name = 'CarWash'
        self.business.update_business()
        self.assertEqual(self.business.name, 'CarWash')

    def test_find_objects(self):
        '''
        test_find_objects_by test case to test a specific object can be queried by its ID.
        '''
        get_neighbourhood = Neighbourhood.find_neighbourhood(self.neighbourhood.id)
        self.assertEqual(get_neighbourhood, self.neighbourhood)

        get_business = Business.find_business(self.business.id)
        self.assertEqual(get_business, self.business)
