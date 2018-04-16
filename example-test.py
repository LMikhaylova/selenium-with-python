import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

class PythonMapTests(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(3)

    def test_search(self):
        driver = self.driver
        driver.get("https://www.openstreetmap.org")
        
        self.assertIn("OpenStreetMap", driver.title)
        
        elem = driver.find_element(By.ID, "content").find_element(By.ID, "query")

        elem.send_keys("Hancock Tower")
        elem.send_keys(Keys.RETURN)

        elem = driver \
          .find_element(By.CLASS_NAME, "search_results_entry") \
          .find_element(By.TAG_NAME, "p")

        self.assertNotEqual(elem.text, "No results found")

        urlParts = driver.current_url.split("#map=")
        zoom_lat_lon = urlParts[1].split("/")
        zoom = int(zoom_lat_lon[0])
        lat = int(float(zoom_lat_lon[1]))
        lon = int(float(zoom_lat_lon[2]))

        self.assertEqual(zoom, 19)
        self.assertEqual(lat, 42)
        self.assertEqual(lon, -71)

    #def map_click(self):    


    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()
    