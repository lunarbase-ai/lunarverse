import requests

url = "https://arpeggi.io/api/kits/v1/stem-splits"
files = { 'inputFile': open("/tmp/lunarcore/workflows/958a9148-923a-4160-966a-d2acd599137b/uploads/audio_example.mp3", 'rb') }
headers = { 'Authorization': f'Bearer bAfIbDP9.VIvKr1ku3sud35Ml3ZVi6j4F' }

response = requests.post(url, files=files, headers=headers)
stem_splitter_job = response.json()

print(stem_splitter_job)
