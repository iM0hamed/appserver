import ntpath
import os
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
import appdistribution.utils.file_utils as util
import appdistribution.settings as constant

def index(request):
    return render(request, 'appserver/index.html', {'data': ['hello django!']})


def decode(request, platform, product, file):
    response = redirect('/appdistribution/download?filename=appdistribution/app/' + platform + '/' + product + '/' + file)
    return response


def settings(request):
    if request.method == "GET":
        return render(request, 'appserver/settings.html', {})

    elif request.method == "POST":
        platform = request.POST['platform']
        product = request.POST['product']
        data = {}

        # Create app folder
        if not os.path.exists('appdistribution/app/' + platform + '/' + product):
            os.mkdir('appdistribution/app/' + platform + '/' + product)

        if platform == 'android':
            data = {"platform": platform, "product": product}
        elif platform == 'ios':
            bundleid = request.POST['bundleid']
            displayimage = request.POST['displayimage']
            fullsizeimage = request.POST['fullsizeimage']
            data = {
                "platform": platform,
                "product": product,
                "bundleid": bundleid,
                "displayimage": displayimage,
                "fullsizeimage": fullsizeimage
            }

        config = util.get_config()
        if product not in config['products']:
            config['products'].append(product)

        is_found = False
        if 'productDetail' in config:
            for app in config['productDetail']:
                if platform.lower() == 'android' and app["product"].lower() == product.lower() and platform.lower() == app["platform"].lower():
                    is_found = True
                    break
                if platform.lower() == 'ios' and app["product"].lower() == product and platform.lower() == app["platform"].lower() and bundleid.lower() == app["bundleid"].lower():
                    is_found = True
                    break
        else:
            config['productDetail'] = []

        if not is_found:
            config['productDetail'].append(data)
            util.update_config(config)
            return render(request, 'appserver/settings.html', {'message': 'product added successfully!'})
        else:
            return render(request, 'appserver/settings.html', {'message': 'product already exist!'})


def show_apps(request):
    user_agent = request.META['HTTP_USER_AGENT']
    platform = request.GET.get('platform', '')
    product = request.GET.get('product', '')
    is_mobile = False

    config = util.get_config()

    print("Request is from: " + user_agent)
    if "mobile" in user_agent.lower():
        is_mobile = True

    if not platform:
        platform = config["platforms"][0]
    if not product:
        product = config["products"][0]

    print("User Agent: " + user_agent)
    print("Platform: " + platform)
    print("AppName: " + product)

    app_data = util.get_app_files(platform, product)

    response_data = {
        'host': constant.SERVER_ADDRESS,
        'platforms': config["platforms"],
        'isMobile': is_mobile,
        'products': config['products'],
        'selectedPlatform': platform,
        'selectedProduct': product,
        'appsData': app_data}

    # print(response_data)
    return render(request, 'appserver/download.html', response_data)


def download_app(request):
    user_agent = request.META['HTTP_USER_AGENT']
    file_path = request.GET.get("filename", '')
    file_name = ntpath.basename(file_path)
    print(file_path)
    if not file_name:
        return

    if file_name.endswith("plist"):
        util.generate_plist(ntpath.dirname(file_path), file_name)

    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            if file_name.endswith("apk"):
                response = HttpResponse(fh.read(), content_type="application/vnd.android.package-archive")
            elif file_name.endswith("ipa"):
                response = HttpResponse(fh.read(), content_type="application/octet-stream")
            elif file_name.endswith("plist"):
                response = HttpResponse(fh.read(), content_type="application/xml")
            elif file_name.endswith("crt"):
                response = HttpResponse(fh.read(), content_type="application/pkix-cert")

            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response

    raise Http404


def upload_apps(request):
    config = util.get_config()
    if request.method == "GET":
        return render(request, 'appserver/upload.html', {'products': config['products']})
    elif request.method == "POST":
        platform = request.POST['platform']
        product = request.POST['product']
        file = request.FILES['uploadfile']
        file_path = 'appdistribution/app/' + platform + '/' + product + '/' + file.name
        with open(file_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        if platform == 'ios':
            bundle_id = request.POST['bundleid']
            util.update_ios_product_map(file_path, bundle_id)

        return render(request, 'appserver/upload.html', {'products': config['products'], 'message': "App uploaded successfully!"})
    else:
        return render(request, 'appserver/upload.html', {'products': config['products']})


