"""Main executable script demonstrating complete system integration (Q6).

Demonstrates:
1. Application configuration retrieval via Singleton (AppConfig).
2. Factory registration and initial PaymentProcessor selection (PaymentFactory).
3. Order construction via Builder (OrderBuilder).
4. Full workflow execution on the WEB channel.
5. Full workflow repetition on the KIOSK channel.
6. Event logging and audit trail via EventLogger.
"""

from src.config import AppConfig
from src.core import Product, OrderBuilder
from src.channels import (
    register_channel_factory,
    get_channel_factory,
    WebFactory,
    MobileFactory,
    KioskFactory,
)
from src.payments import (
    PixProcessor,
    CreditCardProcessor,
    BoletoProcessor,
    MilhasProcessor,
)
from src.services import OrderService, EventLogger


def main():
    print("=" * 70)
    print(" SISTEMA DE PEDIDOS E CANAIS DE VENDA - DEMONSTRAÇÃO COMPLETA (Q6)")
    print("=" * 70)

    # 1. Obtenção da Configuração Global (Singleton)
    print("\n[1] Inicialização e Configuração Global:")
    config = AppConfig()
    print(f"    - Ambiente: {config.environment}")
    print(f"    - Moeda: {config.currency}")
    print(f"    - Debug: {config.debug}")

    # 2. Inicialização do Registro de Fábricas e Processadores
    print("\n[2] Registro de Canais e Inicialização de Processadores:")
    register_channel_factory("WEB", WebFactory)
    register_channel_factory("MOBILE", MobileFactory)
    register_channel_factory("KIOSK", KioskFactory)
    print("    - Canais registrados: WEB, MOBILE, KIOSK")

    pix_processor = PixProcessor()
    card_processor = CreditCardProcessor()
    print("    - Processadores de pagamento instanciados: PixProcessor, CreditCardProcessor")

    # Instanciação do serviço orquestrador com logger compartilhado
    logger = EventLogger()
    order_service = OrderService(logger=logger)

    # 3. Fluxo 1: Pedido pelo Canal WEB com pagamento via PIX
    print("\n" + "-" * 70)
    print("[3] FLUXO COMPLETO - CANAL WEB (Pagamento: PIX)")
    print("-" * 70)

    order_web = (
        OrderBuilder()
        .set_client("Maria Silva")
        .add_product(Product("Macbook Pro 14", 8500.00))
        .add_product(Product("Mouse Wireless", 180.00))
        .set_address("Av. Paulista, 67 - São Paulo/SP")
        .set_coupon("TECH10")
        .set_payment_method("Pix")
        .set_observation("Entregar na recepção comercial")
        .build()
    )
    print(f"Pedido construído para '{order_web.client}' com {len(order_web.products)} produtos.")
    print(f"Valor total calculado pelo Order: R$ {order_web.total():.2f}")

    web_factory = get_channel_factory("WEB")
    order_service.process_order(order_web, web_factory, pix_processor)

    # 4. Fluxo 2: Pedido pelo Canal KIOSK com pagamento via Cartão
    print("\n" + "-" * 70)
    print("[4] FLUXO COMPLETO - CANAL KIOSK (Pagamento: Cartão de Crédito)")
    print("-" * 70)

    order_kiosk = (
        OrderBuilder()
        .set_client("Lucas Silva")
        .add_product(Product("Hambúrguer Artesanal Duplo", 42.00))
        .add_product(Product("Batata Rústica", 18.00))
        .add_product(Product("Refrigerante", 10.00))
        .set_payment_method("Credit Card")
        .set_observation("Sem cebola e com maionese à parte")
        .build()
    )
    print(f"Pedido construído para '{order_kiosk.client}' com {len(order_kiosk.products)} produtos.")
    print(f"Valor total calculado pelo Order: R$ {order_kiosk.total():.2f}")

    kiosk_factory = get_channel_factory("KIOSK")
    order_service.process_order(order_kiosk, kiosk_factory, card_processor)

    # 5. Auditoria e Logs Consolidados (EventLogger)
    print("\n" + "=" * 70)
    print(" RELATÓRIO DE AUDITORIA DO EVENT LOGGER")
    print("=" * 70)
    for idx, log_entry in enumerate(logger.get_logs(), 1):
        print(f" {idx:02d}. {log_entry}")

    print("\nExecução finalizada com sucesso!\n")


if __name__ == "__main__":
    main()
