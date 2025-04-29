from src.config import CACHED_IMAGE_NAME, CACHE_PATH
from src.api_func import get_image
from pathlib import Path


class TestGetImage:
    correct_test_data = (37.582457, 55.581307, 0.003, 'map', [])
    incorrect_test_data = (2000, 2000, 5, "hry", [])

    def test_error(self):
        image_path = get_image(*self.incorrect_test_data)
        assert image_path == None

    def test_get_image(self):
        image_path = get_image(*self.correct_test_data)
        expected_iamge_path = f"{CACHE_PATH}/{CACHED_IMAGE_NAME}"
        image_file = Path(image_path) # type: ignore

        assert image_path == expected_iamge_path

        assert image_file.is_file() is True



