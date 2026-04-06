from camunda.external_task.external_task_worker import ExternalTaskWorker
import requests


def consulta_cnpj(task):
    cnpj = task.get_variable("cnpj")

    print(f"[Worker] Recebido CNPJ: {cnpj}")

    url = f"https://www.receitaws.com.br/v1/cnpj/{cnpj}"
    response = requests.get(url)
    data = response.json()

    print("[Worker] Dados recebidos:", data)

    return task.complete(
        {
            "razao_social": data.get("nome"),
            "nome_fantasia": data.get("fantasia"),
            "status": data.get("situacao"),
            "atividade_principal": data.get("atividade_principal", [{}])[
                0
            ].get("text"),
            "uf": data.get("uf"),
            "municipio": data.get("municipio"),
            "porta_api": url,
        }
    )


worker = ExternalTaskWorker(
    worker_id="consulta-cnpj", base_url="http://localhost:8080/engine-rest"
)

print("[Worker] Iniciando...")
worker.subscribe("consulta-cnpj", consulta_cnpj)
