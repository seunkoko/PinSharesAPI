
def pin_errors(errors, status_code):
    return {
        'status': 'fail',
        'data': { 'message': errors }
    }, status_code

def pin_success(message, response_data, status_code):
    return dict(
            status='success',
            data={
                'message': message,
                **response_data
            }
        ), status_code
