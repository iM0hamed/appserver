import json
import os
import datetime
import appdistribution.settings as constant
from threading import Lock

lock = Lock()


def get_config():
    with lock:
        with open('appdistribution/config.json') as file:
            config = json.load(file)

        return config


def update_config(data):
    with lock:
        with open('appdistribution/config.json', 'w') as outfile:
            json.dump(data, outfile)


def update_ios_product_map(app_name, app_bundle_id):
    config = get_config()
    is_updated = False

    for record in config["iosProductMap"]:
        if record["name"] == app_name:
            record["bundleID"] = app_bundle_id
            is_updated = True
            break

    if not is_updated:
        config["iosProductMap"].append({'name': app_name, 'bundleID': app_bundle_id})

    print(config)
    update_config(config)


def get_app_files(platform, product):
    path = "appdistribution/app/" + platform + "/" + product
    if not os.path.exists(path):
        os.makedirs(path)

    files = list(filter(lambda x: os.path.isfile(path + "/" + x) and (x.endswith('.ipa') or x.endswith('.apk')), os.listdir(path)))
    files = sorted(files, key=lambda x: os.path.getctime(path + "/" + x), reverse=True)

    app_data = []
    for x in files:
        file_path = path + "/" + x

        app_data.append({
            'fileName': x,
            'filePath': file_path,
            'plistPath': x.replace('.ipa', '.plist'),
            "buildTime": datetime.datetime.fromtimestamp(os.path.getctime(file_path)).strftime("%Y-%m-%d %H:%M:%S")
        })

    return app_data


def generate_plist(file_path, file_name):
    ipa_file = file_path + '/' + file_name.replace('.plist', '.ipa')
    bundle_id = ""
    product = ""
    display_image = ""
    full_size_image = ""

    config = get_config()
    for app in config["iosProductMap"]:
        if app["name"] == ipa_file:
            bundle_id = app["bundleID"]
            break

    for app in config["productDetail"]:
        if app['platform'] == 'ios' and app['bundleid'] == bundle_id:
            product = app["product"]
            display_image = app['displayimage']
            full_size_image = app['fullsizeimage']

    with open('appdistribution/app/ios/manifest.plist', 'r') as ipa_file:
        data = ipa_file.read() \
            .replace('{{@bundle-identifier}}', bundle_id) \
            .replace('{{@title}}', product) \
            .replace('{{@displayimage}}', display_image) \
            .replace('{{@fullsizeimage}}', full_size_image) \
            .replace('{{@url}}',
                     constant.SERVER_ADDRESS + '/appdistribution/download?filename='
                     + ipa_file)

        f = open(file_path + "/" + file_name, "w")
        f.write(data)

        print(data)


