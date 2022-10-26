import re
from django.shortcuts import render


def home(request):
    return render(request, 'home.html')


def result(request):
    raw_data = request.GET['data']
    raw_polynomial_code = request.GET['polynomial-code']
    raw_surplus_data = request.GET['surplus-data']

    binary_pattern = re.compile('^1[01]*$')
    surplus_pattern = re.compile('^[01]+$')

    if bool(binary_pattern.match(raw_data)) and bool(binary_pattern.match(raw_polynomial_code)):
        data = [int(d) for d in raw_data]
        polynomial_code = [int(c) for c in raw_polynomial_code]

        if raw_surplus_data == "":
            surplus_data = [0 for _ in range(0, len(polynomial_code) - 1)]
        elif bool(surplus_pattern.match(raw_surplus_data)) and len(raw_surplus_data) == len(polynomial_code) - 1:
            surplus_data = [int(s) for s in raw_surplus_data]
        else:
            return render(request, 'error.html')

        return render(request, 'result.html', {'checksum': get_checksum(data, polynomial_code, surplus_data)})

    return render(request, 'error.html')


def get_checksum(data, polynomial_code, surplus_data):
    combined_data = data + surplus_data
    combined_data_size, polynomial_code_size = len(combined_data), len(polynomial_code)
    calculation_count = combined_data_size - polynomial_code_size + 1

    zero_quotient = [0 for _ in range(0, polynomial_code_size)]
    temp = combined_data[0:polynomial_code_size]

    for quotient_digit in range(0, calculation_count):
        temp = get_xor(temp, zero_quotient if temp[0] == 0 else polynomial_code)

        del temp[0]
        if quotient_digit != calculation_count - 1:
            temp.append(combined_data[polynomial_code_size + quotient_digit])

    return ''.join(str(t) for t in temp)


def get_xor(list1, list2):
    return list(x ^ y for x, y in zip(list1, list2))
