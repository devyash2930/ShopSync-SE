import firebase_admin
from firebase_admin import credentials

def initialize_firebase():
    # Check if Firebase has already been initialized
    if not firebase_admin._apps:
        cred = credentials.Certificate('shopsync-se-firebase-adminsdk-nkzuw-e871ea65d4.json')
        firebase_admin.initialize_app(cred)
