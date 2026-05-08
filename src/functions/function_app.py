import azure.functions as func
import logging
import json

# Inicializa o aplicativo da Function
app = func.FunctionApp()

@app.service_bus_queue_trigger(
    arg_name="azmsg", 
    queue_name="fila-pedidos", 
    connection="ServiceBusConnection"
) 
def process_event_message(azmsg: func.ServiceBusMessage):
    """
    Esta função é disparada automaticamente quando uma nova mensagem 
    chega na fila do Azure Service Bus.
    """
    try:
        # 1. Recupera e decodifica o corpo da mensagem
        body = azmsg.get_body().decode('utf-8')
        data = json.loads(body)
        
        logging.info('----------------------------------------------')
        logging.info(f"Mensagem recebida com sucesso! ID: {data.get('id', 'N/A')}")

        # 2. Simulação de Lógica de Negócio / Automação
        # Aqui você poderia integrar um modelo de IA ou script de segurança
        valor = data.get('valor', 0)
        origem = data.get('origem', 'Desconhecida')

        if valor > 5000:
            logging.warning(f"ALERTA: Transação de alto valor detectada vinda de: {origem}")
        else:
            logging.info(f"Processamento padrão executado para origem: {origem}")

        # 3. Exemplo de saída formatada para o Application Insights
        logging.info(f"Payload processado: {json.dumps(data)}")
        logging.info('----------------------------------------------')

    except json.JSONDecodeError:
        logging.error("Erro: A mensagem recebida não é um JSON válido.")
    except Exception as e:
        logging.error(f"Erro inesperado no processamento: {str(e)}")

@app.route(route="http_health_check", auth_level=func.AuthLevel.ANONYMOUS)
def health_check(req: func.HttpRequest) -> func.HttpResponse:
    """
    Endpoint HTTP adicional para verificar se a Function está online.
    """
    logging.info('Verificação de status via HTTP executada.')
    return func.HttpResponse(
        "Azure Function está ativa e operando.",
        status_code=200
    )
