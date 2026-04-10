from camunda.external_task.external_task_worker import ExternalTaskWorker


def salvar_no_banco(task):
    print("[Worker DB] Salvando dados...")

    dados = {
        "cnpj": task.get_variable("cnpj"),
        "razao_social": task.get_variable("razao_social"),
        "status": task.get_variable("status"),
        "uf": task.get_variable("uf"),
        "porte": task.get_variable("porte"),
        "idade": task.get_variable("idade"),
        "selecionada": task.get_variable("selecionada"),
    }

    print("[Worker DB] Dados:", dados)

    # futuro: salvar no banco

    return task.complete({})


def start_worker():
    print("[Worker DB] Iniciando...")
    worker = ExternalTaskWorker(
        worker_id="salva-db",
        base_url="http://localhost:8080/engine-rest",
    )
    worker.subscribe("salva-db", salvar_no_banco)
