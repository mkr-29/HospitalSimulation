import simpy
import random

class Hospital:
    def __init__(self, env, num_beds, num_doctors, num_nurses):
        self.env = env
        self.num_beds = num_beds
        self.num_doctors = num_doctors
        self.num_nurses = num_nurses
        self.beds = simpy.Resource(env, capacity=num_beds)
        self.doctors = simpy.Resource(env, capacity=num_doctors)
        self.nurses = simpy.Resource(env, capacity=num_nurses)

    # Define the patient arrival process
    def patient_arrival(self, arrival_rate, triage):
        patient_id = 0
        while True:
            yield self.env.timeout(random.expovariate(arrival_rate))
            patient_id += 1
            triage_priority = random.choice(triage)
            print(f"Patient {patient_id} triaged with priority {triage_priority} at time {self.env.now:.2f}")
            self.env.process(self.patient_treatment(patient_id, triage_priority))

    # Define the patient treatment process
    def patient_treatment(self, patient_id, triage_priority):
        with self.beds.request() as bed_request:
            yield bed_request
            with self.doctors.request() as doctor_request:
                yield doctor_request
                with self.nurses.request() as nurse_request:
                    yield nurse_request
                    treatment_time = random.uniform(5, 20) * triage_priority
                    print(f"Patient {patient_id} started treatment at time {self.env.now:.2f}")
                    yield self.env.timeout(treatment_time)
                    print(f"Patient {patient_id} completed treatment at time {self.env.now:.2f}")
                    self.env.process(self.patient_discharge(patient_id))

    # Define the patient discharge process
    def patient_discharge(self, patient_id):
        with self.nurses.request() as nurse_request:
            yield nurse_request
            discharge_time = random.uniform(10, 30)
            print(f"Patient {patient_id} started discharge at time {self.env.now:.2f}")
            yield self.env.timeout(discharge_time)
            print(f"Patient {patient_id} discharged at time {self.env.now:.2f}")

    # Define 

# # Initialize the simulation environment and the hospital
# env = simpy.Environment()
# num_beds = 10
# num_doctors = 3
# num_nurses = 5
# hospital = Hospital(env, num_beds, num_doctors, num_nurses)

# # Start the patient arrival process
# arrival_rate = 0.5 # patients per minute
# triage = [1, 2, 3, 4] # triage priorities
# env.process(hospital.patient_arrival(arrival_rate, triage))

# # Run the simulation for 10 minutes
# env.run(until=10)