from src.api_func import *



# Тесты для координат
class Api_Func:
    def test_geocoder(self):
        assert geocoder('') == None


    def test_get_image(self):
        assert get_image(37.582457, 55.581307, 0.003, 'map', []) == 'picture.png'
        assert get_image('', '', 0.003, 'map', []) == None


    def test_get_adress(self):
        assert get_adress(37.582457, 55.581307) == 'Россия, Москва, Варшавское шоссе, 170Ек4'


test = Api_Func()

print(test.test_geocoder())
print(test.test_get_adress())

