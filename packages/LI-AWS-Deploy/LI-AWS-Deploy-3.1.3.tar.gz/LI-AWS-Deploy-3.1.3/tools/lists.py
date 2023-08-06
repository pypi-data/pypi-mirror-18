# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals, with_statement, nested_scopes
import yaml
import os
from tabulate import tabulate
from git import Repo
from tools.config import get_config_data
from tools.utils import run_command, bcolors
from tools.settings import DOCKER_PATH_VAR, LIBRARIES


def show_list(libs=[]):
    data = get_config_data()
    if not data:
        return False

    dc_path = os.path.join(
        data['docker_compose_path'],
        'docker-compose.yml'
    )

    with open(dc_path, 'r') as file:
        dc_data = yaml.load(file)

    print("\n\033[93m>> Listar Aplicações LI")
    print("***********************\033[0m\n")

    services_list = dc_data['services']

    table_data = []
    for service in sorted(services_list):
        # 1. Checa se o container está rodando
        docker_ret = run_command(
            command_list=[
                {
                    'command': "docker ps | grep {service}".format(
                        service=service),
                    'run_stdout': False
                }
            ],
            get_stdout=True,
            title=False
        )
        if docker_ret:
            container = docker_ret[:12]
        else:
            container = None

        if container:
            rodando = "{}SIM{}".format(bcolors.OKGREEN, bcolors.ENDC)
        else:
            rodando = "{}NÃO{}".format(bcolors.FAIL, bcolors.ENDC)

        # 2. Checa a branch
        try:
            caminho_dict = services_list.get(service)
            caminho_path = caminho_dict.get('build').get('context')
            caminho_path.replace(DOCKER_PATH_VAR, data['project_path'])
            repo = Repo(caminho_path)
            branch = repo.active_branch.name
        except:
            branch = "--"
            caminho_path = None

        # 3. Checa versão das livrarias padrões
        lib_list = []
        pip_ret = None
        if caminho_path:
            for lib in LIBRARIES + libs:
                if container:
                    pip_ret = run_command(
                        command_list=[
                            {
                                'command': 'docker exec -ti {container} pip freeze | grep -i {library}== | tail -1'.format(
                                    container=container,
                                    library=lib),
                                'run_stdout': False}],
                        get_stdout=True,
                        title=None)
                # elif branch != "--":
                #     pip_ret = run_command(
                #         command_list=[
                #             {
                #                 'command': 'cd {path} && docker-compose run {service} pip freeze | grep {library}'.format(
                #                     path=data['docker_compose_path'],
                #                     service=service,
                #                     library=lib
                #                 ),
                #                 'run_stdout':False
                #             }
                #         ],
                #         get_stdout=True,
                #         title=None
                #     )
                if pip_ret:
                    lib_list.append(pip_ret.split("==")[1])
                else:
                    lib_list.append("--" if "SIM" in rodando else "")

        table_data.append([service, branch, rodando] + lib_list)

    print(tabulate(
        table_data,
        headers=["Aplicação", "Branch", "Rodando"] + LIBRARIES + libs
    )
    )
