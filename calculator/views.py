import re
from django.shortcuts import render


def home(request):
    return render(request, 'home.html')


def result(request):
    binary_pattern = re.compile('^[0-1]+$')
    data, polynomial_code = request.GET['data'], request.GET['polynomial-code']

    if bool(binary_pattern.match(data)) and bool(binary_pattern.match(polynomial_code)):
        data = [int(d) for d in data]
        polynomial_code = [int(c) for c in polynomial_code]
        surplus_data = [0 for _ in range(0, len(polynomial_code) - 1)]
        return render(request, 'result.html', {'checksum': get_checksum(data, polynomial_code, surplus_data)})
    else:
        return render(request, 'error.html')


def get_checksum(data, polynomial_code, surplus_data):
    data = data + surplus_data
    data_size, polynomial_code_size = len(data), len(polynomial_code)
    calculation_count = data_size - polynomial_code_size + 1
    zero_quotient = [0 for _ in range(0, len(polynomial_code))]
    temp = data[0:polynomial_code_size]

    for quotient_digit in range(0, calculation_count):
        temp = get_xor(temp, zero_quotient if temp[0] == 0 else polynomial_code)

        del temp[0]
        if quotient_digit != calculation_count - 1:
            temp.append(data[polynomial_code_size + quotient_digit])

    return ''.join(str(i) for i in temp)


def get_xor(list1, list2):
    return list(x ^ y for x, y in zip(list1, list2))
