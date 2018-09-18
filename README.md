# appserver

Follow this guide to generate self signed certificate: [self-signed-certificate-with-custom-ca.md](https://gist.github.com/fntlnz/cf14feb5a46b2eda428e000157447309)

## Installing appserver
```
pipenv install
```

## Run appserver(host http server at 8000 and https server at 8001)
```
python3 manage.py runserver 0:8000 & python3 manage.py runsslserver 0:8001 --certificate rootCA.crt --key rootCA.key
```

You can download **certificate**/apk at http://your-ip:8000 and download apk/**ipa** at https://your-ip:8001


## Preview
| Index Page  | Settings Page | Upload Page  | Download Page |
| ------------- | ------------- | ------------- | ------------- |
| <img src="https://github.com/rayzhouzhj/appserver/blob/master/appdistribution/static/appserver/images/index_page.png" width="200" height="200"/>  | <img src="https://github.com/rayzhouzhj/appserver/blob/master/appdistribution/static/appserver/images/settings_page.png" width="200" height="200"/>  | <img src="https://github.com/rayzhouzhj/appserver/blob/master/appdistribution/static/appserver/images/upload_page.png" width="200" height="200"/> | <img src="https://github.com/rayzhouzhj/appserver/blob/master/appdistribution/static/appserver/images/download_page.png" width="200" height="200"/>|
