# Trabalho de Engenharia de Software - A2

**Dupla:** 
- [Gabrielle Mascarelo](https://github.com/g4briwlle); 
- [Henrique Beltrão](https://github.com/riqueu).

## Sistema de Pedidos com Design Patterns em Python

Implementação de um sistema de pedidos utilizando os padrões Singleton, Builder, Factory Method e Abstract Factory, com foco em separação de responsabilidades (SRP) e extensibilidade (OCP).

---

## Execução

### Exemplo de Integração (main.py)
Para executar o fluxo completo do sistema (canais WEB e KIOSK com diferentes formas de pagamento):

```bash
python3 main.py
```

---

## Testes

### Executar todos os testes:
```bash
python3 -m tests.test_config && \
python3 -m tests.test_core && \
python3 -m tests.test_payments && \
python3 -m tests.test_channels && \
python3 -m tests.test_integration
```

### Executar testes por módulo:
- **Singleton (AppConfig):**
  ```bash
  python3 -m tests.test_config
  ```
- **Builder (OrderBuilder):**
  ```bash
  python3 -m tests.test_core
  ```
- **Factory Method (Pagamentos):**
  ```bash
  python3 -m tests.test_payments
  ```
- **Abstract Factory (Canais de Venda):**
  ```bash
  python3 -m tests.test_channels
  ```
- **Integração e Testes Adicionais:**
  ```bash
  python3 -m tests.test_integration
  ```