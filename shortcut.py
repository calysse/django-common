from django.http import HttpResponse
from simplejson import dumps

def json_response(json_content):
    return HttpResponse(dumps(json_content), mimetype="application/json")

def success_json_response(json_content):
  json_content.update({'status': "OK"})
  return json_response(json_content)


def error_json_response(json_content):
  json_content.update({'status': "ERROR"})
  return json_response(json_content)

