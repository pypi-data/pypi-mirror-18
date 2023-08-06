import email
import io


def parse_http_request(request):
    stream = io.StringIO() 
    rxString = request.decode("utf-8").split('\r\n', 1)[1]
    stream.write(rxString) 
    headers = email.message_from_string(rxString)
    return headers