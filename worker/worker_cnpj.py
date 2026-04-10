from camunda.external_task.external_task_worker import ExternalTaskWorker
from datetime import datetime
import requests


def consulta_cnpj(task):
    cnpj = task.get_variable("cnpj")
    print(f"[Worker CNPJ] Recebido CNPJ: {cnpj}")

    try:
        url = f"https://www.receitaws.com.br/v1/cnpj/{cnpj}"
        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            raise ValueError(f"HTTP {response.status_code}")

        data = response.json()

        if data.get("status") == "ERROR":
            raise ValueError(data.get("message"))

        abertura = data.get("abertura")
        if abertura:
            d = datetime.strptime(abertura, "%d/%m/%Y")
            hoje = datetime.now()

            idade = hoje.year - d.year
            if (hoje.month, hoje.day) < (d.month, d.day):
                idade -= 1
        else:
            idade = 0

        return task.complete(
            {
                "razao_social": data.get("nome"),
                "nome_fantasia": data.get("fantasia"),
                "status": data.get("situacao"),
                "atividade_principal": data.get("atividade_principal", [{}])[
                    0
                ].get("text"),
                "porte": data.get("porte"),
                "uf": data.get("uf"),
                "municipio": data.get("municipio"),
                "porta_api": url,
                "idade": idade,
            }
        )

    except Exception as e:
        print("[Worker CNPJ] Erro capturado:", e)
        return task.bpmn_error(error_code="ERRO_CNPJ", error_message=str(e))


def start_worker():
    print("[Worker CNPJ] Iniciando...")
    worker = ExternalTaskWorker(
        worker_id="consulta-cnpj",
        base_url="http://localhost:8080/engine-rest",
    )
    worker.subscribe("consulta-cnpj", consulta_cnpj)
