Exercise 6 — Design Question
1. Should the config and logger be global variables? Why or why not?

Usually, no.

Globals create hidden dependencies. A function may appear to take no config or logger, but in reality it depends on external module state. That makes code harder to understand, reuse, and test.

A global logger is less harmful than a global mutable config, but it still couples modules tightly. A global config is especially problematic because changes in one place can affect behavior everywhere.

2. How would you structure the sharing of these objects across modules without using globals?

Create the shared objects once at the application entry point, then pass them into the components that need them.

Example structure:

# config.py
from dataclasses import dataclass

@dataclass(frozen=True)
class AppConfig:
    api_key: str
    max_order_size: int
    risk_limit: float
# market_data.py
class MarketDataClient:
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
# order_manager.py
class OrderManager:
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
# risk_engine.py
class RiskEngine:
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
# main.py
from config import AppConfig
from market_data import MarketDataClient
from order_manager import OrderManager
from risk_engine import RiskEngine
import logging

config = AppConfig(
    api_key="secret",
    max_order_size=1000,
    risk_limit=1_000_000.0,
)

logger = logging.getLogger("trading_system")

market_data = MarketDataClient(config, logger)
order_manager = OrderManager(config, logger)
risk_engine = RiskEngine(config, logger)

That way:

dependencies are explicit
startup is centralized
modules stay reusable
3. What happens to testability if you use globals? What happens if you use parameters?

With globals:

tests become harder to isolate
one test can affect another by modifying shared state
mocking becomes awkward
order-dependent failures become more likely

With parameters/injection:

tests can pass fake configs and fake loggers
each test controls its own environment
dependencies are visible
components are easier to unit test independently

Example:

def test_risk_engine_rejects_large_order():
    fake_config = AppConfig(api_key="x", max_order_size=100, risk_limit=1000.0)
    fake_logger = DummyLogger()

    engine = RiskEngine(fake_config, fake_logger)

    assert engine.check_order({"notional": 5000}) is False

That is much cleaner than patching module globals before each test.