from django.shortcuts import render, HttpResponse, HttpResponseRedirect, redirect
import json, requests

# Create your views here.
def client(request):
    return render(request, 'client.html', locals())


def authorize(request):
    try:
        # if request.method == "GET":
        r2 = requests.get(url='http://192.168.10.18:8002/oauth/authorize',
                            params={
                                "grant_type": "authorization_code",
                                "code": request.GET['code'],
                                "redirect_uri": "http://192.168.10.18:8001/oauth/authorize",
                                "client_id": "8001"
                            })
        r2.encoding = 'utf-8'
        datas = json.dumps(r2.text)
        print("'==auth===")
        print(json.loads(datas))
        datas = json.loads(datas)
        return render(request, 'success.html', locals())
    except Exception as e:
        return HttpResponse('error')
    # return redirect('/oauth/test')
        # return HttpResponseRedirect('http://192.168.10.18:8002/oauth/server?callback=192.168.10.18:8001/oauth/client')
    return HttpResponse('no url')

def test(request):
    return render(request, 'test.html', locals())
