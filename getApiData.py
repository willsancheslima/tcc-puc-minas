import requests
import utils as utl

db = 'ceis'
col = 'register_atlz'
url = 'http://www.transparencia.gov.br/api-de-dados/ceis'
pg_parameter = 'pagina'
offset = 1

col = utl.connect_mongo(db, col)
parameters = {pg_parameter: offset}
status = 200
while(status == 200):
    response = requests.get(url, parameters)
    status = response.status_code
    print(pg_parameter+' '+str(parameters[pg_parameter])+' => status = '+str(status))
    if(response.text == '[]' or status != 200):
        print('response empty')
        break
    if(status != 200):
        print('response status => '+status)
        break
    col.insert_many(response.json()) #TO-DO => implementar insertCol()
    parameters[pg_parameter] += 1