import requests

# need a center of registeration in future
API_BASE = "https://ap4.test-vm.life/urmart/urmart-api/"
API_GENREPORT = "GenReport"

def main():
    try:
        requests.get(API_BASE + API_GENREPORT)
    except Exception as e:
        print(e)
    

if __name__ == "__main__":
    main()
