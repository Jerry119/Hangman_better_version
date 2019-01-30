import unittest
from main import app, getHint, setWord, setGuess

class HangmanGameTest(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def tearDown(self):
        pass

    def test_home_status_code(self):
        result = self.app.get('/')
        self.assertEqual(result.status_code, 200)

    def test_home_page(self):
        result = self.app.get('/')
        hint = getHint()
        print("\nTesting initial home page...\n")
        print("Testing if hint is displayed correctly...")
        self.assertTrue(bytes("Hint: %s" % hint, 'utf-8') in result.data)
        print("passed")
        print("Testing if remaining count is displayed correctly...")
        self.assertTrue(b'<input type="text" name="remain_cnt" class="remain_cnt" value="5" readonly />' in result.data)
        print('remaining count is 5 -- passed')
        print("Testing if best score is displayed correctly...")
        self.assertTrue(b'<input type="text" name="best_score" class="remain_cnt" value=0 readonly />' in result.data)
        print("best score is 0 -- passed")

    def test_in_game(self):
        print("\nTesting the game in play...\n")
        print("setting the correct word to be 'hello'")
        setWord("hello")
        print("setting the current guess to be '_e___'")
        setGuess("_e___")
        
        print("mocking the scenario where remaining count is 4, 'r' is enter")
        
        with app.test_client() as client:
            sent = {'remain_cnt':4, 'char':'r', 'best_score':0}
            result = client.post('/in_game', data=sent)
    
        print("Testing if remaining count is changed to 3...")
        self.assertTrue(b'<input type="text" name="remain_cnt" class="remain_cnt" value="3" readonly />' in result.data)
        print("remaining count is 3 -- passed")
        
        print("mocking the scenario where remaining count is 3, 'l' is enter")
        result = client.post('/in_game', data={'remain_cnt':3, 'char':'l', 'best_score':0})
        print("Testing if the remaining count is the same...")
        self.assertTrue(b'<input type="text" name="remain_cnt" class="remain_cnt" value="3" readonly />' in result.data)
        print("remaining count is 3 -- passed")
        print("Testing if the current guess has been updated")
        self.assertTrue(b'l&nbsp;' in result.data)
        print("passed")

    def test_fail_page(self):
        print("\nTesting failing page...\n")
        print("setting the correct word to be 'the United States'")
        setWord("the United States")
        
        print("setting up the situation where remaining count is 1, 'r' is entered")
        with app.test_client() as client:
            result = client.post('/in_game', data={'remain_cnt':1, 'char':'r', 'best_score':1})
        
        print("Testing if 'PLAY AGAIN' button exist...")
        self.assertTrue(b'<button id="again" onclick="window.location.href=\'/1\'">PLAY AGAIN</button>' in result.data)
        print("passed")
        print("Testing if the correct word is displayed...")
        self.assertTrue(bytes('the United States', 'utf-8') in result.data)
        print("passed")
        print("Testing if the remaining count is changed to 0...")
        self.assertTrue(b'<input type="text" name="remain_cnt" class="remain_cnt" value="0" readonly />' in result.data)
        print("remaining count is 0 -- Passed")

    def test_win_page(self):
        print("\nTesting winning page...\n")
        print("setting the correct word to be 'Easy'")
        setWord("Easy")
        print("setting the current guess to be 'Ea_y'")
        setGuess("Ea_y")

        print("setting up the scenario where remaining count is 4, 's' is entered, best score is 2")
        with app.test_client() as client:
            result = client.post('/in_game', data={'remain_cnt':4, 'char':'s', 'best_score':'2'})
        
        print("Testing if 'NEXT PUZZLE' button exist...")
        self.assertTrue(b'<button id="again" onclick="window.location.href=\'/4\'">NEXT PUZZLE</button>' in result.data)
        print("passed")
        print("Testing if the correct word is displayed...")
        self.assertTrue(bytes('Easy', 'utf-8') in result.data)
        print("passed")
        print("Testing if the remaining count is 4...")
        self.assertTrue(b'<input type="text" name="remain_cnt" class="remain_cnt" value="4" readonly />' in result.data)
        print("remaining count is 4 -- Passed")
        print("Testing if the best score is changed to 4...")
        self.assertTrue(b'<input type="text" name="best_score" class="remain_cnt" value=4 readonly />' in result.data)
        print("best score is 4 -- passed")


if __name__ == "__main__":
    unittest.main()
