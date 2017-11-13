import pyrebase

config = {
  "apiKey": "AIzaSyAtLq-HbsgKKhJWD8HC2EaWV2FMQMeSfJc",
  "authDomain": "test-8c400.firebaseapp.com",
  "databaseURL": "https://test-8c400.firebaseio.com",
  "storageBucket": "projectId.appspot.com",
  "serviceAccount": "config/serviceAccountKey.json"
}

def stream_handler(message):
    print(message["data"])

firebase = pyrebase.initialize_app(config)

# Get a reference to the auth service
auth = firebase.auth()
# print auth
# Log the user in
user = auth.sign_in_with_email_and_password("admin@admin.cl", "adminadmin")
# print user
# Get a reference to the database service
db = firebase.database()
# print db.child("test-8c400").get()
# users = db.child("School_bus").get()
# print(users.val())
# print db.child("/School_bus").get()
School_bus = db.child("School_bus").get()
for user in School_bus.each():
    print(user.key())  # Morty
    print(user.val())  # {name": "Mortimer 'Morty' Smith"}
    my_stream = db.child("School_bus").child(user.key()).stream(stream_handler)
    my_stream.close()







# data to save
# data = {
#     "name": "Mortimer 'Morty' Smith"
# }

# Pass the user's idToken to the push method
# results = db.child("users").push(data, user['idToken'])

# print firebase

# var config = {
#     apiKey: "AIzaSyAtLq-HbsgKKhJWD8HC2EaWV2FMQMeSfJc",
#     authDomain: "test-8c400.firebaseapp.com",
#     databaseURL: "https://test-8c400.firebaseio.com",
    
#   };
