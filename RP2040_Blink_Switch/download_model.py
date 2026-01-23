import urllib.request

url = "https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task"
filename = "face_landmarker.task"

print(f"Downloading {filename}...")
urllib.request.urlretrieve(url, filename)
print("✅ Download Complete!")