package com.example.java;

import org.springframework.retry.annotation.Backoff;
import org.springframework.retry.annotation.Retryable;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/operation")
public class CalculadoraController {

    /**
     * Método para operações matemáticas.
     * Este método com Retry automático: em caso de falhaa, tenta novamente 3 vezes.
     */
    @Retryable(
            maxAttempts = 3,                     // tenta 3 vezes
            backoff = @Backoff(delay = 1000)     // espera 1s entre tentativas
    )
    private double calcular(String operacao, double p1, double p2) {

        switch (operacao) {
            case "soma":
                return p1 + p2;

            case "subtracao":
                return p1 - p2;

            case "multiplicacao":
                return p1 * p2;

            case "divisao":
                if (p2 == 0) {
                    throw new IllegalArgumentException("Divisão por zero não permitida");
                }
                return p1 / p2;

            default:
                throw new IllegalArgumentException("Operação inválida");
        }
    }

    /**
     * Endpoint POST para SOMA
     */
    @PostMapping("/soma")
    public CalculadoraResponse soma(@RequestBody OperationRequest req) {
        double result = calcular("soma", req.getParam1(), req.getParam2());
        return new CalculadoraResponse(result);
    }

    @PostMapping("/subtracao")
    public CalculadoraResponse subtracao(@RequestBody OperationRequest req) {
        double result = calcular("subtracao", req.getParam1(), req.getParam2());
        return new CalculadoraResponse(result);
    }

    @PostMapping("/multiplicacao")
    public CalculadoraResponse multiplicacao(@RequestBody OperationRequest req) {
        double result = calcular("multiplicacao", req.getParam1(), req.getParam2());
        return new CalculadoraResponse(result);
    }

    @PostMapping("/divisao")
    public CalculadoraResponse divisao(@RequestBody OperationRequest req) {
        double result = calcular("divisao", req.getParam1(), req.getParam2());
        return new CalculadoraResponse(result);
    }
}
