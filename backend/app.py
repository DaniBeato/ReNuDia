import os
from main import db
from main import create_app
import csv
from main.models.doctor_model import DoctorModel
from main.maps.doctor_schema import DoctorSchema
from main.repositories.doctor_repository import DoctorRepository

app = create_app()
app.app_context().push()
doctor_schema = DoctorSchema()
doctor_repository = DoctorRepository()


def load_doctors():
    doctors = doctor_schema.dump(doctor_repository.get_all(), many=True)
    if len(doctors) == 0:
        with open('./doctors_list.csv', encoding='utf-8') as csv_file:
            try:
                csv_reader = csv.reader(csv_file, delimiter=',')
                for row in csv_reader:
                    doctor = doctor_repository.create(DoctorModel(id_card=str(row[0]), surname=str(row[1]), name=str(row[2]),
                                         medical_speciality=str(row[3]), doctor_license=str(row[4])))
                db.session.close()
            except:
                db.session.rollback()
        print('Doctors created successfully')
    else:
        print('Doctors before created')

if __name__ == '__main__':
    db.create_all()
    load_doctors()
    app.run(debug=True, port=os.getenv('PORT'), host='0.0.0.0')