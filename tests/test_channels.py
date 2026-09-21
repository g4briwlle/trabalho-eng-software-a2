"""Tests for Abstract Factory, Channel Products and Registry (Q4 and Q5)."""

from src.core import Product, OrderBuilder
from src.channels import (
    Checkout,
    Notification,
    ChannelFactory,
    WebCheckout,
    WebNotification,
    WebFactory,
    MobileCheckout,
    MobileNotification,
    MobileFactory,
    KioskCheckout,
    KioskNotification,
    KioskFactory,
    register_channel_factory,
    get_channel_factory,
)


def _create_sample_order():
    return (
        OrderBuilder()
        .set_client("Alice")
        .add_product(Product("Livro", 50.0))
        .add_product(Product("Caneta", 10.0))
        .build()
    )


def test_web_factory_family():
    """Verify that WebFactory produces WebCheckout and WebNotification."""
    order = _create_sample_order()
    factory = WebFactory()

    checkout = factory.create_checkout()
    notification = factory.create_notification()

    assert isinstance(checkout, Checkout)
    assert isinstance(checkout, WebCheckout)
    assert isinstance(notification, Notification)
    assert isinstance(notification, WebNotification)

    checkout_msg = checkout.show(order)
    assert "WEB CHECKOUT" in checkout_msg
    assert "Alice" in checkout_msg

    notif_msg = notification.send(order)
    assert "WEB NOTIFICATION" in notif_msg
    assert "Alice" in notif_msg


def test_mobile_factory_family():
    """Verify that MobileFactory produces MobileCheckout and MobileNotification."""
    order = _create_sample_order()
    factory = MobileFactory()

    checkout = factory.create_checkout()
    notification = factory.create_notification()

    assert isinstance(checkout, Checkout)
    assert isinstance(checkout, MobileCheckout)
    assert isinstance(notification, Notification)
    assert isinstance(notification, MobileNotification)

    checkout_msg = checkout.show(order)
    assert "MOBILE CHECKOUT" in checkout_msg
    assert "Alice" in checkout_msg

    notif_msg = notification.send(order)
    assert "MOBILE NOTIFICATION" in notif_msg
    assert "Alice" in notif_msg


def test_get_channel_factory_default_channels():
    """Verify retrieval of default registered factories (WEB and MOBILE)."""
    web_factory = get_channel_factory("WEB")
    assert isinstance(web_factory, WebFactory)

    mobile_factory = get_channel_factory("mobile")  # Case insensitive
    assert isinstance(mobile_factory, MobileFactory)


def test_get_channel_factory_unknown_channel_error():
    """Verify that an unknown channel raises a clear ValueError."""
    try:
        get_channel_factory("TELEPATHY")
        assert False, "Deveria ter lançado ValueError para canal desconhecido."
    except ValueError as e:
        error_msg = str(e)
        assert "Canal desconhecido" in error_msg
        assert "TELEPATHY" in error_msg


def test_kiosk_factory_family_and_registration():
    """Verify KIOSK factory creation and retrieval via registry."""
    order = _create_sample_order()
    kiosk_factory = get_channel_factory("KIOSK")

    assert isinstance(kiosk_factory, KioskFactory)
    checkout = kiosk_factory.create_checkout()
    notification = kiosk_factory.create_notification()

    assert isinstance(checkout, Checkout)
    assert isinstance(checkout, KioskCheckout)
    assert isinstance(notification, Notification)
    assert isinstance(notification, KioskNotification)

    checkout_msg = checkout.show(order)
    assert "KIOSK CHECKOUT" in checkout_msg

    notif_msg = notification.send(order)
    assert "KIOSK NOTIFICATION" in notif_msg


def run_tests():
    print("--- Starting Channel & Abstract Factory Tests (Q4 & Q5) ---\n")

    print("Test 1: WebFactory creates WebCheckout and WebNotification...")
    test_web_factory_family()
    print("Success: WebFactory correctly produces Web family products.\n")

    print("Test 2: MobileFactory creates MobileCheckout and MobileNotification...")
    test_mobile_factory_family()
    print("Success: MobileFactory correctly produces Mobile family products.\n")

    print("Test 3: get_channel_factory retrieves default channels...")
    test_get_channel_factory_default_channels()
    print("Success: WEB and MOBILE retrieved correctly.\n")

    print("Test 4: get_channel_factory raises clear error for unknown channel...")
    test_get_channel_factory_unknown_channel_error()
    print("Success: Clear ValueError raised for unknown channel.\n")

    print("Test 5: KioskFactory creates Kiosk family products and is retrieved via registry...")
    test_kiosk_factory_family_and_registration()
    print("Success: KIOSK channel registered and working correctly.\n")


if __name__ == "__main__":
    run_tests()

