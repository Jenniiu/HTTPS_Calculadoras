# Importa o decorador de retry e estratégias de parada/espera da biblioteca tenacity
# O tenacity é usado para implementar tentativas automáticas em caso de falhas
from tenacity import retry, stop_after_attempt, wait_exponential
# Importa a biblioteca requests para fazer requisições HTTP
import requests

# Define a classe da calculadora que se comunica com a API REST
class CalculadoraRest:
    # Construtor que inicializa a URL base da API
    def __init__(self, base_url):
        # Armazena a URL base para todas as operações
        # Exemplo: "http://localhost:8080/operation"
        self.base_url = base_url
        
    # Implementa a lógica de retry automático:
    # @retry é um decorador que automaticamente re-tenta a função em caso de exceção
    # stop_after_attempt(3): para depois de 3 tentativas
    # wait_exponential(multiplier=1): espera exponencial entre tentativas (1, 2, 4 segundos...)
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1))
    def op_escolhida(self, operacao, p1, p2):
        # Constrói a URL completa para a operação específica
        # Exemplo: "http://localhost:8080/operation/soma/5/3"
        url = f"{self.base_url}/{operacao}/{p1}/{p2}"
        
        # Imprime a URL para debug/monitoramento
        print(f"Fazendo requisição para: {url}")
        
        # Faz a requisição POST para a API com timeout de 5 segundos
        # Se não receber resposta em 5 segundos, levanta exceção
        resp = requests.post(url, timeout=5)
        
        # Levanta uma exceção se a resposta tiver status code de erro (4xx ou 5xx)
        # Exemplo: 404 Not Found, 500 Internal Server Error
        resp.raise_for_status()
        
        # Converte a resposta JSON em um objeto Python e retorna
        # Exemplo: se a API retornar {"result": 8}, retorna 8
        return resp.json()

    # Método para operação de soma - encapsula a chamada para op_escolhida
    def soma(self, a, b):
        return self.op_escolhida("soma", a, b)

    # Método para operação de subtração - encapsula a chamada para op_escolhida
    def subtracao(self, a, b):
        return self.op_escolhida("subtracao", a, b)

    # Método para operação de multiplicação - encapsula a chamada para op_escolhida
    def multiplicacao(self, a, b):
        return self.op_escolhida("multiplicacao", a, b)

    # Método para operação de divisão com verificação de divisão por zero
    def divisao(self, a, b):
        # Verifica se o divisor é zero para evitar requisição desnecessária
        # Esta verificação é feita localmente antes de chamar a API
        if b == 0:
            return {"error": "Divisão por zero"}
        # Se não for divisão por zero, chama a API normalmente
        return self.op_escolhida("divisao", a, b)

# Bloco que executa apenas quando o arquivo é rodado diretamente
# (não quando importado como módulo)
if __name__ == "__main__":
    # Cria uma instância da calculadora com a URL da API local
    # "http://localhost:8080/operation" aponta para servidor rodando na mesma máquina
    calc = CalculadoraRest("http://localhost:8080/operation")
    
    # Imprime mensagem inicial
    print("Testando calculadora REST...")
    
    # Bloco try-except para capturar e tratar possíveis erros
    try:
        # Testa a operação de soma: 5 + 3 = 8
        print("Soma:", calc.soma(5, 3))
        
        # Testa a operação de subtração: 10 - 4 = 6
        print("Subtração:", calc.subtracao(10, 4))
        
        # Testa a operação de multiplicação: 6 × 7 = 42
        print("Multiplicação:", calc.multiplicacao(6, 7))
        
        # Testa a operação de divisão: 20 ÷ 4 = 5
        print("Divisão:", calc.divisao(20, 4))
        
        # Testa divisão por zero - deve retornar mensagem de erro
        print("Divisão por zero:", calc.divisao(20, 0))
        
    # Captura qualquer exceção que ocorrer durante os testes
    except Exception as e:
        # Imprime a mensagem de erro
        print(f"Erro: {e}")