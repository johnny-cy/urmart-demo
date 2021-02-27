import requests
import inspect

API_BASE = "https://ap3.test-vm.life/urmart/urmart-api/"
API_GENREPORT = "GenReport"

def main():
    # conn = sqlite3.connect("./db.sqlite3")
    # cursor = conn.cursor()

    # result = requests.get(API_BASE + API_GENREPORT)
    print(inspect.stack()[3])
    

if __name__ == "__main__":
    main()
