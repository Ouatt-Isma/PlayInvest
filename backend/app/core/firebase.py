import firebase_admin
from firebase_admin import credentials, auth

cred = credentials.Certificate("playinvestapp-firebase-adminsdk-fbsvc-9c66c163a8.json")
firebase_admin.initialize_app(cred)
