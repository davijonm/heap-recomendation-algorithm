import datetime
from collections import Counter
from itertools import groupby

def extract_related_claims(data, claim_id):
    """Extract all claims related to a given claim ID."""
    related_claims = []
    for patient in data['patients']:
        for claim in patient['claims']:
            if claim['id'] == claim_id:
                related_claims.append(claim)
    return related_claims

def max_claim_last_n_days(data, patient_id, n):
    """Find the maximum claim amount in the last 'n' days for a given patient ID."""
    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days=n)

    for patient in data['patients']:
        if patient['id'] == patient_id:
            claims = [
                claim['amount'] for claim in patient['claims']
                if start_date <= datetime.date.fromisoformat(claim['date']) <= end_date
            ]
            return max(claims, default=None)
    return None

def merge_claims(data, patient_id, billing_code):
    """Merge claims for a specific patient and billing code."""
    merged_claim = {
        'total_amount': 0,
        'claims': []
    }
    for patient in data['patients']:
        if patient['id'] == patient_id:
            for claim in patient['claims']:
                if claim['billingCode'] == billing_code:
                    merged_claim['total_amount'] += claim['amount']
                    merged_claim['claims'].append(claim)
    return merged_claim

def most_frequent_billing_code(data, patient_id):
    """Find the most frequently occurring billing code for a given patient ID."""
    billing_codes = []
    for patient in data['patients']:
        if patient['id'] == patient_id:
            billing_codes = [claim['billingCode'] for claim in patient['claims']]
            break
    if not billing_codes:
        return None
    return Counter(billing_codes).most_common(1)[0]

def filter_claims_by_date(data, patient_id, start_date, end_date):
    """Filter claims for a given patient within a specific date range."""
    filtered_claims = []
    start_date = datetime.date.fromisoformat(start_date)
    end_date = datetime.date.fromisoformat(end_date)

    for patient in data['patients']:
        if patient['id'] == patient_id:
            filtered_claims = [
                claim for claim in patient['claims']
                if start_date <= datetime.date.fromisoformat(claim['date']) <= end_date
            ]
    return filtered_claims

def longest_contiguous_subarray_same_code(data, patient_id):
    """Find the longest contiguous subarray of claims with the same billing code."""
    for patient in data['patients']:
        if patient['id'] == patient_id:
            billing_codes = [claim['billingCode'] for claim in patient['claims']]
            max_length = max((len(list(group)) for _, group in groupby(billing_codes)), default=0)
            return max_length
    return 0

def group_claims_by_age_and_treatment(data):
    """Group claims by patient age and treatment type."""
    # Assuming patient data includes age and treatment type
    groups = {}
    for patient in data['patients']:
        age = patient.get('age')
        for claim in patient['claims']:
            treatment_type = claim.get('treatmentType')
            key = (age, treatment_type)
            groups.setdefault(key, []).append(claim)
    return groups

def valid_sequence_billing_codes(data, patient_id):
    """Determine if there exists a valid sequence of billing codes where each subsequent code is greater than the previous one."""
    for patient in data['patients']:
        if patient['id'] == patient_id:
            billing_codes = [claim['billingCode'] for claim in patient['claims']]
            return all(billing_codes[i] < billing_codes[i+1] for i in range(len(billing_codes)-1))
    return False

def identify_fraud_patterns(data):
    """Identify patterns of potential fraud (e.g., repeated claims for the same billing code)."""
    fraud_patterns = {}
    for patient in data['patients']:
        billing_codes = [claim['billingCode'] for claim in patient['claims']]
        repeated_codes = [code for code, count in Counter(billing_codes).items() if count > 1]
        if repeated_codes:
            fraud_patterns[patient['id']] = repeated_codes
    return fraud_patterns

def first_unique_billing_code(data, patient_id):
    """Find the first unique billing code for a specific patient."""
    for patient in data['patients']:
        if patient['id'] == patient_id:
            billing_codes = [claim['billingCode'] for claim in patient['claims']]
            counts = Counter(billing_codes)
            for code in billing_codes:
                if counts[code] == 1:
                    return code
    return None

if __name__ == "__main__":
    data = {
        "patients": [
            {
                "id": "P001",
                "claims": [
                    {"id": "C001", "amount": 100, "billingCode": "B001", "date": "2025-01-01"},
                    {"id": "C002", "amount": 200, "billingCode": "B002", "date": "2025-01-05"},
                    {"id": "C003", "amount": 150, "billingCode": "B003", "date": "2025-01-10"}
                ]
            },
            {
                "id": "P002",
                "claims": [
                    {"id": "C001", "amount": 100, "billingCode": "B001", "date": "2025-01-01"},
                    {"id": "C002", "amount": 200, "billingCode": "B002", "date": "2025-01-15"},
                    {"id": "C003", "amount": 150, "billingCode": "B002", "date": "2025-01-10"}
                ]
            },
        ]
    }

    print("\nRelated Claims")
    print(extract_related_claims(data, "C001"))

    print("\nMax Claim in the last days")
    print(max_claim_last_n_days(data, "P001", 10))

    print("\nMerge claims for a specific patient and billing")
    print(merge_claims(data, "P001", "B001"))

    print("\nMost frequently occurring billing code for a given patient ID.")
    print(most_frequent_billing_code(data, "P001"))

    print("\nFilter claims for a given patient within a specific date range.")
    print(filter_claims_by_date(data, "P001", "2025-01-01", "2025-01-06"))

    print("\nLength of the longest contiguous subarray of claims with the same billing code for a given patient ID.")
    print(longest_contiguous_subarray_same_code(data, "P001"))

    print("\nGroup claims by patient age and treatment type.")
    print(group_claims_by_age_and_treatment(data))

    print("\nDetermine if there exists a valid sequence of billing codes where each subsequent code is greater than the previous one.")
    print(valid_sequence_billing_codes(data, "P001"))

    print("\nIdentify patterns of potential fraud (e.g., repeated claims for the same billing code).")
    print(identify_fraud_patterns(data))

    print("\nFind the first unique billing code for a specific patient.")
    print(first_unique_billing_code(data, "P001"))
