  
import csv,io
import subprocess
from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from django.http import *
from .models import *
from django.contrib import messages
from django.contrib.auth.models import auth,User
from django.template import Context, loader
from urllib.error import HTTPError
import json
import http.client

JOBE_SERVER = 'localhost'


def homepage(request):
    try:
        codesubmit = request.POST['codevalue']
        print(codesubmit)
        '''Demo of a java program run'''
        print("Running java program")
        result_obj = run_test('java', codesubmit, 'Main.java')
        output = display_result(result_obj)
        context = {
            'code' :codesubmit,
            'output':output,
            'resobj':result_obj,
        }
        return render(request,'editor.html',context)
    except:
        return render(request,'editor.html')

def run_test(language, code, filename):
    """Execute the given code in the given language.
       Return the result object.
    """
    runspec = {
        'language_id': language,
        'sourcefilename': filename,
        'sourcecode': code,
    }

    resource = '/jobe/index.php/restapi/runs/'
    data = json.dumps({ 'run_spec' : runspec })
    result = {}
    content = ''
    headers = {"Content-type": "application/json; charset=utf-8",
               "Accept": "application/json"}
    try:
        connect = http.client.HTTPConnection(JOBE_SERVER)
        connect.request('POST', resource, data, headers)
        response = connect.getresponse()
        if response.status != 204:
            content = response.read().decode('utf8')
            if content:
                result = json.loads(content)
        connect.close()

    except (HTTPError, ValueError) as e:
        print("\n***************** HTTP ERROR ******************\n")
        if response:
            print(' Response:', response.status, response.reason, content)
        else:
            print(e)
    return result



def display_result(ro):
    '''Display the given result object'''
    if not isinstance(ro, dict) or 'outcome' not in ro:
        print("Bad result object", ro)
        return

    outcomes = {
        0:  'Successful run',
        11: 'Compile error',
        12: 'Runtime error',
        13: 'Time limit exceeded',
        15: 'Successful run',
        17: 'Memory limit exceeded',
        19: 'Illegal system call',
        20: 'Internal error, please report',
        21: 'Server overload'}

    code = ro['outcome']
    print("{}".format(outcomes[code]))
    print()
    if ro['cmpinfo']:
        print("Compiler output:")
        print(ro['cmpinfo'])
        print()
        return ro['cmpinfo']
    else:
        if ro['stdout']:
            print("Output:")
            print(ro['stdout'])
            return ro['stdout']
        else:
            print("No output")
        if ro['stderr']:
            print()
            print("Error output:")
            print(ro['stderr'])
            return ro['stderr']




 