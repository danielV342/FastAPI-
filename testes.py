import requests

headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI0IiwiZXhwIjoxNzc5NjMwOTczfQ.PuLKzuaDvBGZydHF6jrUgARXFGuqV5CSzkLO0WGw6tI"
}

requisicao = requests.get("http://127.0.0.1:8000/auth/refresh", headers=headers)

print(requisicao)
print(requisicao.json())