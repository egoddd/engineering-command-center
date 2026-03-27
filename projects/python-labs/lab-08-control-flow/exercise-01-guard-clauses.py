def validate_trade(trade: Trade, config: PipelineConfig) -> ValidationError | None:
    if trade.side not in VALID_SIDES:
        return ValidationError(
            trade.trade_id,
            f"Invalid side '{trade.side}' — must be BUY or SELL"
        )

    if trade.symbol not in config.valid_symbols:
        return ValidationError(
            trade.trade_id,
            f"Unknown symbol '{trade.symbol}'"
        )

    if trade.quantity < config.min_quantity:
        return ValidationError(
            trade.trade_id,
            f"Quantity {trade.quantity} below minimum {config.min_quantity}"
        )

    if trade.quantity > config.max_quantity:
        return ValidationError(
            trade.trade_id,
            f"Quantity {trade.quantity} above maximum {config.max_quantity}"
        )

    if trade.price < config.min_price:
        return ValidationError(
            trade.trade_id,
            f"Price {trade.price} below minimum {config.min_price}"
        )

    if trade.price > config.max_price:
        return ValidationError(
            trade.trade_id,
            f"Price {trade.price} above maximum {config.max_price}"
        )

    return None