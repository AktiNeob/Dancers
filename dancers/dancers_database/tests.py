from rest_framework.test import APITestCase
from .models import DancersDataBase
from uuid import uuid4

class DanserAPITestCase(APITestCase):
    def setUp(self):
        DancersDataBase.objects.create(    
            first_name = "Александр",
            last_name =  "Евтушенко",
            patronymic = "Романович",
            gender = "м",
            club = "Империя",
            points_in_E_class = 30,
            points_in_D_class = 30,
            points_in_C_class = 30,
            points_in_B_class = 30,
            points_in_A_class = 30,
            points_in_S_class = 0,
            points_in_M_class = 0,
            trainer_rank = "Нет",
            referee_rank = "Нет",
            sport_rank = "Нет",
            class_rank =  "Нет")

    def test_get_methods(self):
        url = 'http://127.0.0.1:8000/test/test/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_post_method(self):
        url = 'http://127.0.0.1:8000/test/test/'
        response = self.client.post(url, data = {
            "first_name": "Владимир",
            "last_name": "Ульянов",
            "patronymic": "Ильич",
            "gender": "м",
            "club": "Коммунизм",
            "points_in_E_class": 30,
            "points_in_D_class": 30,
            "points_in_C_class": 30,
            "points_in_B_class": 30,
            "points_in_A_class": 30,
            "points_in_S_class": 0,
            "points_in_M_class": 0,
            "trainer_rank": "Нет",
            "referee_rank": "Нет",
            "sport_rank": "Нет",
            "class_rank": "Нет"
        })
        self.assertEqual(response.status_code, 201)

    def test_bad_post_method(self):
        url = 'http://127.0.0.1:8000/test/test/'
        response = self.client.post(url, data = {
            "first_name": "Владимир",
            "last_name": "Ульянов",
            "patronymic": "Ильич",
            "gender": "Бред",
            "club": "Коммунизм",
            "points_in_E_class": "Бред",
            "points_in_D_class": "Бред",
            "points_in_C_class": "Бред",
            "points_in_B_class": "Бред",
            "points_in_A_class": "Бред",
            "points_in_S_class": "Бред",
            "points_in_M_class": "Бред",
            "trainer_rank": "Бред",
            "referee_rank": "Бред",
            "sport_rank": "Бред",
            "class_rank": "Бред"
        })
        self.assertEqual(response.status_code, 400)



