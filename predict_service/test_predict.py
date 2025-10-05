import requests
def test_predict():
    url = "http://localhost:8000/predict"
    payload = {"N":90,"P":42,"K":43,"temperature":20.88,"humidity":82.0,"ph":6.5,"rainfall":202.9}
    r = requests.post(url, json=payload, timeout=10)
    print(r.status_code, r.json())

if __name__ == '__main__':
    test_predict()
