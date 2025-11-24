# Importa o decorador de retry e estratégias de parada/espera da biblioteca tenacity
from tenacity import retry, stop_after_attempt, wait_exponential
import requests
     
# Define a classe da calculadora que se comunica com a API REST
class CalculadoraRest:
    # Construtor que  a URL base da API
    def __init__(self, base_url):
        # Armazena a URL base para todas as operações
        self.base_url = base_url
        
    # Implementa a lógica de retry automático:
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1))
    def op_escolhida(self, operacao, p1, p2):

        url = f"{self.base_url}/{operacao}/{p1}/{p2}"

        # Faz a requisição POST para a API com timeout de 5 segundos
        resp = requests.post(url, timeout=5)

        # Levanta uma exceção se a resposta tiver status code de erro (4xx ou 5xx)
        resp.raise_for_status()

        # Extrai e retorna o valor do campo "result" do JSON de resposta
        return resp.json().get("result")

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
        if b == 0:
            return "Erro: divisão por zero."
        # Se não for divisão por zero, chama a API
        return self.op_escolhida("divisao", a, b)


if __name__ == "__main__":
    # Cria uma instância da calculadora com a URL da API
    calc = CalculadoraRest("https://calculadora-fxpc.onrender.com/operation")

    # Testa todas as operações e imprime os resultados
    print("Soma:", calc.soma(5, 3))
    print("Subtração:", calc.subtracao(10, 4))
    print("Multiplicação:", calc.multiplicacao(6, 7))
    print("Divisão:", calc.divisao(20, 4))