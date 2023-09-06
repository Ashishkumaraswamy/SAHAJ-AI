from flask import Flask, request, jsonify

app = Flask(__name__)

employees = []


@app.route('/greeting', methods=['GET'])
def greeting():
    return "Hello World!", 200


@app.route('/employee', methods=['POST'])
def create_employee():
    data = request.json
    employee = {
        'id': str(len(employees) + 1),
        'name': data['name'],
        'city': data['city'],
    }
    employees.append(employee)
    return jsonify({'employeeId': employee['id']}), 201


@app.route('/employee/<id>', methods=['GET'])
def get_employee_by_id(id):
    for employee in employees:
        if employee['id'] == id:
            return jsonify(employee)
    return jsonify({'message': "Employee with {} was not found".format(id)}), 404


@app.route('/employees/search', methods=['POST'])
def search_employees():
    data = request.json
    fields = data.get('fields', [])
    condition = data.get('condition', 'AND')

    if not fields:
        return jsonify({'message': 'Please provide at least one filter criterion in the "fields" list'}), 400

    result = employees.copy()

    result_list = []

    for criterion in fields:
        field_name = criterion['fieldName']
        eq = criterion.get('eq')
        neq = criterion.get('neq')
        if field_name == 'name':
            if eq:
                result = [
                    employee for employee in employees if employee['name'] == eq]
            elif neq:
                result = [
                    employee for employee in employees if employee['name'] != neq]
        elif field_name == 'city':
            if eq:
                result = [
                    employee for employee in employees if employee['city'] == eq]
            elif neq:
                result = [
                    employee for employee in employees if employee['city'] != neq]
        if result:
            result_list.append(result)

    if condition == 'OR':
        union_result = list(set(tuple(d.items())
                            for sublist in result_list for d in sublist))

        result = [dict(item) for item in union_result]

    elif condition == 'AND':
        result = result_list[0]
        for sublist in result_list[1:]:
            result = [
                d for d in result if d in sublist]

    return jsonify(result)


@app.route('/employees/all', methods=['GET'])
def get_all_employees():
    return jsonify(employees)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
