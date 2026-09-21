"""Module with Abstract Factory and Registry for sales channels."""

from abc import ABC, abstractmethod
from typing import Type
from src.core import Order


# Abstract Products
class Checkout(ABC):
    """Abstract Product representing the checkout presentation for a channel."""

    @abstractmethod
    def show(self, order: Order) -> str:
        """Presents the checkout screen/interface for the given order."""
        ...


class Notification(ABC):
    """Abstract Product representing the notification mechanism for a channel."""

    @abstractmethod
    def send(self, order: Order) -> str:
        """Sends an order notification/confirmation to the client."""
        ...


# Abstract Factory
class ChannelFactory(ABC):
    """Abstract Factory interface to create families of channel-specific products."""

    @abstractmethod
    def create_checkout(self) -> Checkout:
        """Creates a channel-specific Checkout instance."""
        ...

    @abstractmethod
    def create_notification(self) -> Notification:
        """Creates a channel-specific Notification instance."""
        ...


# Concrete Products and Factories
# WEB Channel
class WebCheckout(Checkout):
    """Concrete Checkout product for the WEB channel."""

    def show(self, order: Order) -> str:
        message = (
            f"[WEB CHECKOUT] Renderizando página web de checkout para {order.client}. "
            f"Total a pagar: R$ {order.total():.2f}."
        )
        print(message)
        return message


class WebNotification(Notification):
    """Concrete Notification product for the WEB channel."""

    def send(self, order: Order) -> str:
        message = (
            f"[WEB NOTIFICATION] Enviando e-mail de confirmação do pedido para {order.client} "
            f"(Total: R$ {order.total():.2f})."
        )
        print(message)
        return message


class WebFactory(ChannelFactory):
    """Concrete Factory for creating WEB channel products."""

    def create_checkout(self) -> Checkout:
        return WebCheckout()

    def create_notification(self) -> Notification:
        return WebNotification()


# MOBILE Channel
class MobileCheckout(Checkout):
    """Concrete Checkout product for the MOBILE channel."""

    def show(self, order: Order) -> str:
        message = (
            f"[MOBILE CHECKOUT] Renderizando tela nativa mobile de checkout para {order.client}. "
            f"Total a pagar: R$ {order.total():.2f}."
        )
        print(message)
        return message


class MobileNotification(Notification):
    """Concrete Notification product for the MOBILE channel."""

    def send(self, order: Order) -> str:
        message = (
            f"[MOBILE NOTIFICATION] Disparando Push Notification para o dispositivo de {order.client} "
            f"(Total: R$ {order.total():.2f})."
        )
        print(message)
        return message


class MobileFactory(ChannelFactory):
    """Concrete Factory for creating MOBILE channel products."""

    def create_checkout(self) -> Checkout:
        return MobileCheckout()

    def create_notification(self) -> Notification:
        return MobileNotification()


# KIOSK Channel
class KioskCheckout(Checkout):
    """Concrete Checkout product for the KIOSK channel."""

    def show(self, order: Order) -> str:
        message = (
            f"[KIOSK CHECKOUT] Apresentando tela touchscreen no totem de autoatendimento para {order.client}. "
            f"Total a pagar: R$ {order.total():.2f}."
        )
        print(message)
        return message


class KioskNotification(Notification):
    """Concrete Notification product for the KIOSK channel."""

    def send(self, order: Order) -> str:
        message = (
            f"[KIOSK NOTIFICATION] Imprimindo comprovante/recibo térmico no totem para {order.client} "
            f"(Total: R$ {order.total():.2f})."
        )
        print(message)
        return message


class KioskFactory(ChannelFactory):
    """Concrete Factory for creating KIOSK channel products."""

    def create_checkout(self) -> Checkout:
        return KioskCheckout()

    def create_notification(self) -> Notification:
        return KioskNotification()


# Factory Registry & Selection (Open/Closed Principle)
_CHANNEL_FACTORIES: dict[str, Type[ChannelFactory]] = {}


def register_channel_factory(channel: str, factory_cls: Type[ChannelFactory]) -> None:
    """
    Registers a ChannelFactory class in the channel registry.
    
    Allows extending the system with new channels without modifying
    the retrieval logic (OCP).
    """
    if not isinstance(factory_cls, type) or not issubclass(factory_cls, ChannelFactory):
        raise TypeError(f"A classe de fábrica '{factory_cls}' deve herdar de ChannelFactory.")
    _CHANNEL_FACTORIES[channel.strip().upper()] = factory_cls


def get_channel_factory(channel: str) -> ChannelFactory:
    """
    Retrieves and instantiates a ChannelFactory registered for the given channel name.
    
    Raises ValueError with a clear message if the channel is not recognized.
    """
    key = channel.strip().upper() if channel else ""
    if key not in _CHANNEL_FACTORIES:
        available = ", ".join(_CHANNEL_FACTORIES.keys()) if _CHANNEL_FACTORIES else "nenhum"
        raise ValueError(
            f"Canal desconhecido: '{channel}'. Canais registrados disponíveis: [{available}]."
        )
    return _CHANNEL_FACTORIES[key]()


# Initial registration of default channels (Q4)
register_channel_factory("WEB", WebFactory)
register_channel_factory("MOBILE", MobileFactory)

# Registration of KIOSK channel (Q5)
register_channel_factory("KIOSK", KioskFactory)
