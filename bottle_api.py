# -*- coding; utf-8 -*-
from bottle import route, run, response, hook, request
import subprocess

def list():
    print("Listar vms disponiveis")
    subprocess.check_output('"C:\Program Files\Oracle\VirtualBox\VBoxManage.exe" list vms', shell=True)

def clone(so, vm_copy):
    print("Clonando a VM pelo SO selecionado")
    subprocess.check_output('"C:\Program Files\Oracle\VirtualBox\VBoxManage.exe" clonevm "' + so + '" --name "' + vm_copy + '" --register', shell=True)

def modify(memoria, cpu, ip, vm_copy):
    print("Modificando as configuracoes da VM...")

    print("Modificando a memoria...")
    subprocess.check_output('"C:\Program Files\Oracle\VirtualBox\VBoxManage.exe" modifyvm "' + vm_copy + '" --memory ' + memoria, shell=True)

    print("Modificando a quantidade de cpus...")
    subprocess.check_output('"C:\Program Files\Oracle\VirtualBox\VBoxManage.exe" modifyvm "' + vm_copy + '" --cpus ' + cpu, shell=True)

    #print("Modificando o endereco ip...")
    #subprocess.check_output("VBoxManage modifyvm " + vm_copy + " -- " + memoria, shell=True)

def showInfo(vm):
    print("Mostrando informacoes da vm selecionada")
    subprocess.check_output('"C:\Program Files\Oracle\VirtualBox\VBoxManage.exe" showvminfo ' + vm, shell=True)

def start(vm):
    print("Iniciando a vm selecionada")
    subprocess.check_output('"C:\Program Files\Oracle\VirtualBox\VBoxManage.exe" startvm ' + vm, shell=True)

def powerOff(vm):
    print("Desligando a vm selecionada")
    subprocess.check_output('"C:\Program Files\Oracle\VirtualBox\VBoxManage.exe" controlvm ' + vm + ' poweroff', shell=True)

@hook('after_request')
def enableCORSAfterRequestHook():
    print ('After request hook.')
    response.headers['Access-Control-Allow-Origin'] = '*'

@route('/', method='GET')
def index():
    return '''
        <!DOCTYPE html>
        <html lang="pt-Br">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <meta http-equiv="X-UA-Compatible" content="ie=edge">
            <title>Projeto 2</title>

            <style>
                * {
                    margin: 0;
                    padding: 0;
                    font-family: sans-serif;
                    font-size: 1rem;
                    box-sizing: border-box;
                }
                html, body {
                    height: 100%;
                    width: 100%;
                }
                body {
                    height: 100vh;
                }
                h1 {
                    font-size: 2rem;
                    color: #580276;
                    text-align: center;
                    margin-bottom: 15px;
                }
                form {
                    height: 100%;
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;
                }
                label {
                    display: flex; 
                    flex-direction: column;
                    align-items: flex-start;
                    justify-content: center;
                    color: #580276;
                    font-size: 1.2rem;
                    margin-top: 10px;
                }
                input[type="number"],
                input[type="text"], 
                select {
                    padding: 10px 15px;
                    width: 300px;
                    margin-bottom: 5px;
                    border-radius: 4px;
                    border: 1px solid rgba(0,0,0,.4);
                }
                input[type="number"]:focus,
                input[type="text"]:focus, 
                input[type="submit"]:focus,
                select:focus {
                    box-shadow:  0 .3rem .4rem 0 rgba(88,2,118,.3);
                    outline: 0;
                }
                select {
                    cursor: pointer;
                }

                input[type="submit"] {
                    padding: 15px;
                    width: 300px;
                    margin-top: 10px;
                    outline: 0;
                    background: #580276;
                    color: #f4f4f4;
                    border: none;
                    border-radius: 4px;
                    cursor: pointer;
                    transition: all .4s ease-in-out;
                }
                input[type="submit"]:hover {
                    background: rgba(88,2,118,.9);
                    box-shadow: 0 .3rem .4rem 0 rgba(0,0,0,.4);
                }
            </style>
        </head>
        <body>

            <form action="/info" method="post">
                <h1>Projeto<br>Infraestrutura de Software</h1>
                <div>
                    <label for="ip">IP</label>    
                    <input name="ip" id="ip" type="text" placeholder="Digite o endereço IP" required />
                </div>
                <div>
                    <label for="memoria">Memória</label> 
                    <input name="memoria" id="memoria" type="number" placeholder="Digite o valor em MB (Megabytes)" required /><br>
                </div> 
                <div>
                    <label for="so">SO</label>
                    <select name="so" id="so" required>
                        <option selected value="" hidden>--Selecione--</option>
                        <option value="Windows7">Windows 8.1</option>
                        <option value="Ubuntu18.04.3 LTS">Linux Ubuntu 18.04</option>
                    </select>
                </div>
                <div>
                    <label for="cpu">CPU</label>
                    <input name="cpu" id="cpu" type="number" min="1" placeholder="Quantas CPUs?" required /><br>
                </div>
                <input value="Enviar" type="submit" />
            </form>

        </body>
        </html>
    '''

@route('/info', method='POST')
def getInfo():
    ip = request.forms.get('ip')
    cpu = request.forms.get('cpu')
    so = request.forms.get('so')
    memoria = request.forms.get('memoria')
    dic = {'memoria': memoria, 'so': so, 'ip': ip, 'cpu': cpu}

    if(so == "Windows"):
        vm_copy = "Windows Copy"
    else:
        vm_copy = "Ubuntu Copy"

    try:
        print("Começando processo para clonar a VM...")

        # Listando VMs disponiveis
        #list()

        # Clonando vm de acordo com o so escolhido
        clone(so, vm_copy)

        # Moficando a vm
        modify(memoria, cpu, ip, vm_copy)

        print("Processo finalizado")

    except:
        print("Ocorreu durante o processo. Veja no terminal qual foi o erro ocorrido.")

    return dic

@route('/vmbox', method=['GET', 'OPTIONS'])
def openVMBox():
    subprocess.Popen("C:\Program Files\Oracle\VirtualBox\VirtualBox.exe", shell=True)
    return "Abrindo Oracle VM VirtualBox"

@route('/showall', method=['GET', 'OPTIONS'])
def showVMs():
    try:
        list()
    except:
        print("Error")
    return "Listando as VMs disponiveis"

@route('/test', method=['GET', 'OPTIONS'])
def test():
    print("Testando a biblioteca subprocess...")
    return subprocess.check_output("dir", shell=True)

run(host="127.0.0.1", port=8080, debug=True)