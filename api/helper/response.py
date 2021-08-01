
def pin_errors(errors, status_code):
    return {
        'status': 'fail',
        'data': { 'message': errors }
    }, status_code
