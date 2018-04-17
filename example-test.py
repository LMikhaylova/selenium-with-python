# importing libraries
import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains


class PythonMapTests(unittest.TestCase):

    def setUp(self):        
        self.driver = webdriver.Chrome() #selecting Chrome driver
        self.actions = ActionChains(self.driver)
        self.driver.implicitly_wait(3) #setting wait time for actions to complete
        self.driver.get("https://www.openstreetmap.org") #navigate to the page


    #function returning search input field
    def getInputBox(self):
        driver = self.driver
        return driver.find_element(By.ID, "content").find_element(By.ID, "query")
        
    #function returning first element of search results
    def getSearchResultsElement(self):
        driver = self.driver
        return driver \
          .find_element(By.CLASS_NAME, "search_results_entry") \
          .find_element(By.TAG_NAME, "p")
            
    def test_search_positive(self):
        driver = self.driver         
        actions = self.actions

        self.assertIn("OpenStreetMap", driver.title) #verify page Title
        elem = self.getInputBox()

        elem.send_keys("Hancock Tower") #type the search phrase
        elem.send_keys(Keys.RETURN) 

        elem = self.getSearchResultsElement()

        self.assertNotEqual(elem.text, "No results found")
        #self.assertEqual(elem.text, "Building John Hancock Tower, Trinity Place, Chinatown, Back Bay, \
        #Boston, Suffolk County, Massachusetts, 02114, United States of America")


        divMap = driver.find_element(By.ID, "map")

        button = driver \
          .find_element(By.CLASS_NAME, "control-query") \
          .find_element(By.TAG_NAME, "a")

        button.click()
        
        actions.move_to_element(divMap).click().perform()

        time.sleep(5)
        

        urlParts = driver.current_url.split("#map=")
        zoom_lat_lon = urlParts[1].split("/")
        zoom = int(zoom_lat_lon[0])
        lat = int(float(zoom_lat_lon[1]))
        lon = int(float(zoom_lat_lon[2]))

        self.assertEqual(zoom, 19)
        self.assertEqual(lat, 42)
        self.assertEqual(lon, -71)

    def test_search_negative(self):
        driver = self.driver               
        self.assertIn("OpenStreetMap", driver.title) #verify page Title
        
        elem = self.getInputBox()
        elem.send_keys("fake landmark") #type the search phrase
        elem.send_keys(Keys.RETURN) 

        elem = self.getSearchResultsElement()

        self.assertEqual(elem.text, "No results found")


    
    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()
    