"""Integration tests for OrderService orchestration (Q6) and 3 Additional Tests (Q7)."""

from src.config import AppConfig
from src.core import Product, OrderBuilder, Order
from src.channels import (
    Checkout,
    Notification,
    ChannelFactory,
    get_channel_factory,
    register_channel_factory,
)
from src.payments import (
    PixProcessor,
    CreditCardProcessor,
    MilhasProcessor,
)
from src.services import OrderService, EventLogger


# Q6: Integration Tests for OrderService Orchestration
def test_complete_execution_web_flow():
    """Q6: Complete execution for WEB channel using real PixProcessor."""
    # 1. Obtenção de AppConfig
    config = AppConfig()
    assert config.environment is not None

    # 2. Construção do pedido via OrderBuilder
    order = (
        OrderBuilder()
        .set_client("Beatriz")
        .add_product(Product("Monitor", 1200.0))
        .add_product(Product("Cabo HDMI", 50.0))
        .set_address("Av. Paulista, 1000")
        .set_payment_method("Pix")
        .build()
    )
    assert order.total() == 1250.0

    # 3. Obtenção da fábrica do canal WEB
    web_factory = get_channel_factory("WEB")

    # 4. Orquestração via OrderService com processador de pagamento real
    logger = EventLogger()
    service = OrderService(logger=logger)
    payment_processor = PixProcessor()

    service.process_order(order, web_factory, payment_processor)

    # 5. Verificação dos logs e eventos
    logs = logger.get_logs()
    assert len(logs) == 3
    assert any("Checkout apresentado" in log for log in logs)
    assert any("Pagamento processado" in log for log in logs)
    assert any("Notificação enviada" in log for log in logs)


def test_complete_execution_kiosk_flow():
    """Q6: Complete execution repeated for KIOSK channel using CreditCardProcessor."""
    order = (
        OrderBuilder()
        .set_client("Carlos")
        .add_product(Product("Lanche Combo", 35.0))
        .set_payment_method("Credit Card")
        .build()
    )

    kiosk_factory = get_channel_factory("KIOSK")
    logger = EventLogger()
    service = OrderService(logger=logger)
    payment_processor = CreditCardProcessor()

    service.process_order(order, kiosk_factory, payment_processor)

    logs = logger.get_logs()
    assert len(logs) == 3
    assert any("Checkout apresentado" in log for log in logs)
    assert any("Pagamento processado" in log for log in logs)
    assert any("Notificação enviada" in log for log in logs)


# Q7: Three Additional Tests (Singleton, Builder, Factory)
def test_q7_singleton_dynamic_attributes_and_idempotency():
    """
    Q7 - Teste Adicional 1 (Singleton - AppConfig):
    - Comportamento verificado: Idempotência do __init__ e persistência de novos
      atributos dinâmicos injetados em tempo de execução ao obter nova referência.
    - Resultado esperado: O novo atributo permanece acessível e os atributos
      anteriores não são restaurados para o padrão.
    - Por que é importante: Módulos podem registrar configurações customizadas
      (ex: timeouts, URLs de serviço) sem risco de perda de estado por reinicialização.
    """
    cfg1 = AppConfig()
    cfg1.custom_timeout = 45  # Injeção dinâmica de novo atributo

    cfg2 = AppConfig()
    assert hasattr(cfg2, "custom_timeout")
    assert cfg2.custom_timeout == 45
    assert cfg2.currency == "BRL"


def test_q7_builder_isolation_and_optional_defaults():
    """
    Q7 - Teste Adicional 2 (Builder - OrderBuilder):
    - Comportamento verificado: Isolamento de dados entre pedidos construídos e
      correto tratamento dos valores padrão de atributos opcionais não definidos.
    - Resultado esperado: Um pedido construído com apenas atributos obrigatórios
      mantém campos opcionais como None, sem contaminação por chamadas anteriores.
    - Por que é importante: Evita vazamento de dados de clientes anteriores
      (endereço, cupom) para novos pedidos gerados pelo sistema.
    """
    builder1 = OrderBuilder()
    order1 = (
        builder1
        .set_client("Cliente 1")
        .add_product(Product("Item A", 100.0))
        .set_address("Rua das Flores, 10")
        .set_coupon("PROMO10")
        .build()
    )

    builder2 = OrderBuilder()
    order2 = (
        builder2
        .set_client("Cliente 2")
        .add_product(Product("Item B", 200.0))
        .build()
    )

    # Verifica integridade de order1
    assert order1.client == "Cliente 1"
    assert order1.total() == 100.0
    assert order1.address == "Rua das Flores, 10"
    assert order1.coupon == "PROMO10"

    # Verifica que order2 não herdou dados opcionais de order1
    assert order2.client == "Cliente 2"
    assert order2.total() == 200.0
    assert order2.address is None
    assert order2.coupon is None
    assert order2.payment_method is None
    assert order2.observation is None


def test_q7_factory_dynamic_registration_and_protocol_compliance():
    """
    Q7 - Teste Adicional 3 (Fábrica - ChannelFactory / Registry):
    - Comportamento verificado: Capacidade de estender o sistema em tempo de
      execução registrando uma nova fábrica customizada (SmartWatchFactory) e
      garantindo que seus produtos cumpram os contratos de Checkout e Notification.
    - Resultado esperado: get_channel_factory instancia a nova fábrica e seus produtos
      são consumidos com sucesso pelo OrderService sem requerer alterações no core.
    - Por que é importante: Valida o Princípio Aberto/Fechado (OCP) e o Princípio de
      Substituição de Liskov (LSP), permitindo novos canais via plugins.
    """
    class SmartWatchCheckout(Checkout):
        def show(self, order: Order) -> str:
            msg = f"[SMARTWATCH CHECKOUT] Exibindo tela compacta de checkout para {order.client}."
            print(msg)
            return msg

    class SmartWatchNotification(Notification):
        def send(self, order: Order) -> str:
            msg = f"[SMARTWATCH NOTIFICATION] Disparando alerta tátil/vibração para {order.client}."
            print(msg)
            return msg

    class SmartWatchFactory(ChannelFactory):
        def create_checkout(self) -> Checkout:
            return SmartWatchCheckout()

        def create_notification(self) -> Notification:
            return SmartWatchNotification()

    # Registro dinâmico da nova fábrica sem editar get_channel_factory
    register_channel_factory("SMARTWATCH", SmartWatchFactory)

    # Obtenção e validação de conformidade
    sw_factory = get_channel_factory("SMARTWATCH")
    assert isinstance(sw_factory, SmartWatchFactory)

    order = (
        OrderBuilder()
        .set_client("Daniel")
        .add_product(Product("Assinatura Fitness", 80.0))
        .build()
    )

    logger = EventLogger()
    service = OrderService(logger=logger)
    payment_processor = MilhasProcessor()

    # Execução completa sem erros com a nova fábrica e Milhas
    service.process_order(order, sw_factory, payment_processor)
    logs = logger.get_logs()
    assert len(logs) == 3


def run_tests():
    print("--- Starting Integration & Q7 Tests ---\n")

    print("Test 1: Complete execution for WEB channel (Q6)...")
    test_complete_execution_web_flow()
    print("Success: WEB flow orchestrated successfully.\n")

    print("Test 2: Complete execution for KIOSK channel (Q6)...")
    test_complete_execution_kiosk_flow()
    print("Success: KIOSK flow orchestrated successfully.\n")

    print("Test 3: Q7 - Singleton dynamic attribute preservation...")
    test_q7_singleton_dynamic_attributes_and_idempotency()
    print("Success: Singleton idempotency and dynamic state verified.\n")

    print("Test 4: Q7 - Builder isolation and optional defaults...")
    test_q7_builder_isolation_and_optional_defaults()
    print("Success: Builder isolation verified.\n")

    print("Test 5: Q7 - Dynamic factory registration and protocol compliance...")
    test_q7_factory_dynamic_registration_and_protocol_compliance()
    print("Success: Dynamic factory extension verified.\n")


if __name__ == "__main__":
    run_tests()
