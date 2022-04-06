import requests
import json
import glob
import os
import re
import time


def get_dodf_json():
    files = glob.glob('./dodf_json/*.json')

    try:
        latest_file = max(files, key=os.path.getctime)
    except ValueError:
        latest_file = ''

    r = requests.get('https://www.dodf.df.gov.br/index/jornal-json')
    if r.status_code == 200:
        dodf_json = json.loads(r.content)
        file_name = dodf_json['lstJornalDia'][0].replace(' INTEGRA.pdf\n', '')
        if len(re.findall(file_name, latest_file)) == 0:
            with open('./dodf_json/' + file_name + '.json', 'w') as js:
                json.dump(dodf_json, js, ensure_ascii=True)
                print("Arquivo baixado com sucesso!")
                rt = requests.post('https://api.telegram.org/bot5120194773:AAHET51g_tM1Nos_LoHxKFbed19Io47qRFc/sendMessage?chat_id=-1001719693537&text=' + file_name + " baixado com sucesso!")

        else:
            print("Arquivo já existe!")

    time.sleep(10800)


while True:
    get_dodf_json()

