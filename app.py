from flask import Flask, jsonify
import json
import os

app = Flask(__name__)

# Load employee data from JSON file
def load_employees():
    json_path = os.path.join(os.path.dirname(__file__), 'employees.json')
    with open(json_path, 'r') as f:
        data = json.load(f)
    return data['employees']

employees = load_employees()

# Employee endpoints
@app.route('/employees', methods=['GET'])
def get_employees():
    return jsonify({'employees': employees}), 200

@app.route('/employees/<int:employee_id>', methods=['GET'])
def get_employee(employee_id):
    employee = next((e for e in employees if e['id'] == employee_id), None)
    if not employee:
        return jsonify({'error': 'employee not found'}), 404
    return jsonify(employee), 200

@app.route('/employees/department/<department>', methods=['GET'])
def get_employees_by_department(department):
    dept_employees = [e for e in employees if e['department'].lower() == department.lower()]
    if not dept_employees:
        return jsonify({'error': f'no employees found in {department} department'}), 404
    return jsonify({'employees': dept_employees}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
