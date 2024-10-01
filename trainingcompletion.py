import json
from datetime import datetime, timedelta

with open("trainings (correct).txt",'r') as file:
    data = json.load(file)



# 1. List each completed training with a count of how many people have completed that training.
def list_training_completions(data):
    results = {}
    for person in data:
        seen = set()
        for completion in person['completions']:
            training_name = completion['name']
            if training_name not in seen:
                if training_name in results:
                    results[training_name] += 1
                else:
                    results[training_name] = 1
            seen.add(training_name)
    return results


# 2. Given a list of trainings and a fiscal year (defined as 7/1/n-1 – 6/30/n), for each specified training, list all people that completed that training in the specified fiscal year.
def list_training_completions_in_fiscal_year(data, training_list, fiscal_year):
    fiscal_start_date = datetime(fiscal_year-1,7,1)
    fiscal_end_date = datetime(fiscal_year,6,30)
    
    results = {}
    for training_name in training_list:
        results[training_name] = []
        for person in data:
            for completion in person['completions']:
                if completion['name'] == training_name:
                    completion_date = datetime.strptime(completion['timestamp'], "%m/%d/%Y")
                    if fiscal_start_date <= completion_date <= fiscal_end_date:
                        results[training_name].append(person['name'])
    return results


# 3. Given a date, find all people that have any completed trainings that have already expired, or will expire within one month of the specified date (A training is considered expired the day after its expiration date). For each person found, list each completed training that met the previous criteria, with an additional field to indicate expired vs expires soon.
def find_expired_or_soon_to_expire(data, given_date):
    given_date = datetime.strptime(given_date, "%m/%d/%Y")
    soon_date = given_date + timedelta(days=30)

    results = []
    for person in data:
        person_result = {
            "name": person['name'],
            "expiring_trainings": []
        }
        for completion in person['completions']:
            if completion['expires']:
                expire_date = datetime.strptime(completion['expires'], "%m/%d/%Y")
                if expire_date < given_date:
                    person_result["expiring_trainings"].append({
                        "name": completion['name'],
                        "status": "expired"
                    })
                elif given_date <= expire_date <= soon_date:
                    person_result["expiring_trainings"].append({
                        "name": completion['name'],
                        "status": "expires soon"
                    })
        if person_result["expiring_trainings"]:
            results.append(person_result)
    return results

# Output functions to JSON file

# 1.
with open("output1.txt",'w') as file:
    json.dump(list_training_completions(data), file)

# 2.
fiscal_year = 2024
training_list = ["Electrical Safety for Labs", "X-Ray Safety","Laboratory Safety Training"]
with open("output2.txt",'w') as file:
    json.dump(list_training_completions_in_fiscal_year(data, training_list, fiscal_year), file)



# 3.
given_date = "10/01/2024"
with open("output3.txt",'w') as file:
    json.dump(find_expired_or_soon_to_expire(data, given_date), file)
