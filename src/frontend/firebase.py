import firebase_admin
from firebase_admin import credentials

def initialize_firebase():
    # Check if Firebase has already been initialized
    if not firebase_admin._apps:
        cred = credentials.Certificate('shopsync-9ecdc-firebase-adminsdk-60nyc-7e5a173fe8.json')
        # cred = credentials.Certificate('shopsync-se-firebase-adminsdk-nkzuw-ca6838f54f.json')
        firebase_admin.initialize_app(cred)
        