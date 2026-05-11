import pickle

class CookieManager:

    @staticmethod
    def save_cookies(driver, file_path="cookies.pkl"):
        with open(file_path, "wb") as file:
            pickle.dump(driver.get_cookies(), file)

    @staticmethod
    def load_cookies(driver, file_path="cookies.pkl"):
        with open(file_path, "rb") as file:
            cookies = pickle.load(file)
            for cookie in cookies:
                driver.add_cookie(cookie)