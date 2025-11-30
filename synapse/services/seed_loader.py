import json
import os
from synapse.business_model.patient import Patient
from synapse.business_model.psychologist import Psychologist
from synapse.business_model.user import User
from synapse.business_model.clinic import Clinic
from synapse.business_model.appointment import Appointment
from synapse.business_model.availability import Availability
from synapse.business_model.lead import Lead

SEEDS_FILE = os.path.join(os.path.dirname(__file__), '..', 'seeds.json')

class SeedLoader:
    @staticmethod
    def load():
        with open(SEEDS_FILE, encoding='utf-8') as f:
            data = json.load(f)
        patients = [Patient.from_dict(d) for d in data.get("patients", [])]
        psychologists = [Psychologist.from_dict(d) for d in data.get("psychologists", [])]
        users = [User.from_dict(d) for d in data.get("users", [])]
        clinics = [Clinic.from_dict(d) for d in data.get("clinics", [])]
        availabilities = [Availability.from_dict(d) for d in data.get("availabilities", [])]
        appointments = [Appointment.from_dict(d) for d in data.get("appointments", [])]
        leads = [Lead.from_dict(d) for d in data.get("leads", [])]
        return {
            "patients": patients,
            "psychologists": psychologists,
            "users": users,
            "clinics": clinics,
            "availabilities": availabilities,
            "appointments": appointments,
            "leads": leads
        }
