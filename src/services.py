"""Module with EventLogger and OrderService orchestration (SRP)."""

from typing import Any, Protocol, runtime_checkable
from src.core import Order
from src.channels import ChannelFactory


# Protocol for PaymentProcessor (allows loose coupling with payments.py)
@runtime_checkable
class PaymentProcessorProtocol(Protocol):
    """Protocol defining the interface required for payment processors."""

    def process_order(self, order: Order) -> Any:
        """Processes the payment for the given order."""
        ...


# EventLogger (Dedicated logging responsibility)
class EventLogger:
    """Component dedicated exclusively to recording and managing system event logs."""

    def __init__(self):
        self._logs: list[str] = []

    def log(self, message: str) -> None:
        """Records an event log entry."""
        entry = f"[LOG] {message}"
        self._logs.append(entry)
        print(entry)

    def get_logs(self) -> list[str]:
        """Returns a shallow copy of the recorded logs."""
        return list(self._logs)

    def clear(self) -> None:
        """Clears all recorded logs."""
        self._logs.clear()


# OrderService (Orchestrator respecting SRP)
class OrderService:
    """
    Orchestrates the order fulfillment workflow.
    
    Adheres strictly to the Single Responsibility Principle (SRP):
    - Does NOT construct orders (delegated to OrderBuilder).
    - Does NOT calculate totals (delegated to Order.total()).
    - Does NOT choose concrete payment implementations (delegated to PaymentProcessor).
    - Does NOT choose concrete notification/checkout implementations (delegated to ChannelFactory).
    - Does NOT store global application configuration (delegated to AppConfig).
    - Does NOT handle persistence or formatting of logs directly (delegated to EventLogger).
    """

    def __init__(self, logger: EventLogger | None = None):
        self.logger = logger or EventLogger()

    def process_order(
        self,
        order: Order,
        channel_factory: ChannelFactory,
        payment_processor: PaymentProcessorProtocol
    ) -> None:
        """
        Coordinates the complete order processing lifecycle:
        1. Shows the channel-specific checkout.
        2. Processes the payment via the chosen payment processor.
        3. Sends the channel-specific notification.
        4. Emits audit logs for each step through EventLogger.
        """
        # 1. Channel checkout presentation
        checkout = channel_factory.create_checkout()
        checkout.show(order)
        self.logger.log(f"Checkout apresentado com sucesso para o cliente '{order.client}'.")

        # 2. Payment processing
        payment_processor.process_order(order)
        self.logger.log(
            f"Pagamento processado com sucesso para o pedido de '{order.client}' "
            f"(Total: R$ {order.total():.2f})."
        )

        # 3. Channel notification dispatch
        notification = channel_factory.create_notification()
        notification.send(order)
        self.logger.log(f"Notificação enviada com sucesso para o cliente '{order.client}'.")
