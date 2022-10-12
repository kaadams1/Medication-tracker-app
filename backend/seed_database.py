"""Script to seed database."""

import os
import json
import model
import server

os.system("dropdb medications")
os.system("createdb medications")

model.connect_to_db(server.app)
model.db.create_all()


# Create 10 users
for n in range(10):
    email = f"user{n}@test.com"
    password = "test"

    user = model.User.create(email, password)
    model.db.session.add(user)


#create 10 meds
for n in range(10):
    user_id = f"{n}"
    med_name = "test name"
    med_dosage = "test dosage"
    med_quantity = "test quantity"
    med_frequency = "test frequency"

    med = model.Medication.create(user_id, med_name, med_dosage, med_quantity, med_frequency)
    model.db.session.add(med)
    

model.db.session.commit()