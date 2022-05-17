import requests
import json
import glob
import os
import re
import time

INSTANCE = os.environ.get('INSTANCE')
BTOKEN = os.environ.get('BTOKEN')
CHATID = os.environ.get('CHATID')
DEBUG = os.environ.get('DEBUG')





def get_dodf_json(INSTANCE, BTOKEN, CHATID, DEBUG):
    files = glob.glob('./dodf_json/*.json')

    try:
        latest_file = max(files, key=os.path.getctime)
    except ValueError:
        latest_file = ''
    try:
        r = requests.get('https://www.dodf.df.gov.br/index/jornal-json')
    except Exception as e:
        error_m = repr(e)
        if DEBUG == 'TRUE':
            rt = requests.post('https://api.telegram.org/bot' + BTOKEN + '/sendMessage?chat_id='+ CHATID + '&text=' 'Erro na instância: ' + INSTANCE + '\n' + error_m)


    if r.status_code == 200:
        dodf_json = json.loads(r.content)
        file_name = dodf_json['lstJornalDia'][0].replace(' INTEGRA.pdf\n', '')
        if len(re.findall(file_name, latest_file)) == 0:
            with open('./dodf_json/' + file_name + '.json', 'w') as js:
                json.dump(dodf_json, js, ensure_ascii=True)
                print("Arquivo baixado com sucesso!")
                rt = requests.post('https://api.telegram.org/bot' + BTOKEN + '/sendMessage?chat_id='+ CHATID + '&text=' 'Instância: ' + INSTANCE + '\n' + file_name + " baixado com sucesso!")

        else:
            print("Arquivo já existe!")

    time.sleep(10800)


while True:
    get_dodf_json(INSTANCE, BTOKEN, CHATID, DEBUG)

