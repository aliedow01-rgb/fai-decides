
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django_daraja.mpesa.core import MpesaClient
from.models import Candidate, Vote

def home(request):
    candidates = Candidate.objects.all()
    results = {c.name: c.total_votes() for c in candidates}
    return render(request, 'index.html', {'candidates': candidates, 'results': results})

def stk_push(request):
    if request.method == "POST":
        phone = request.POST.get('phone')
        candidate_id = request.POST.get('candidate_id')
        candidate = Candidate.objects.get(id=candidate_id)

        cl = MpesaClient()
        phone = '254' + phone[-9:] # convert 07 to 2547
        response = cl.stk_push(phone, 85, 'FAI Vote', candidate.name)

        return JsonResponse(response.response_description, safe=False)

@csrf_exempt
def callback(request):
    data = json.loads(request.body)
    if data['Body']['stkCallback']['ResultCode'] == 0:
        items = data['Body']['stkCallback']['CallbackMetadata']['Item']
        receipt = next(i['Value'] for i in items if i['Name'] == 'MpesaReceiptNumber')
        phone = next(i['Value'] for i in items if i['Name'] == 'PhoneNumber')
        candidate_name = next(i['Value'] for i in items if i['Name'] == 'AccountReference')

        candidate = Candidate.objects.get(name=candidate_name)
        Vote.objects.create(
            candidate=candidate,
            phone=phone,
            mpesa_receipt=receipt
        )
    return JsonResponse({"ResultCode": 0, "ResultDesc": "Accepted"})