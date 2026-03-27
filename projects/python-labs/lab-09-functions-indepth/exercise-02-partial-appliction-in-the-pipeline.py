from functools import partial


def validate_field_range(
    trade: Trade,
    *,
    field_name: str,
    min_value: int | float,
    max_value: int | float,
) -> ValidationError | None:
    value = getattr(trade, field_name)

    if value < min_value:
        return ValidationError(
            trade.trade_id,
            f"{field_name.capitalize()} {value} below minimum {min_value}",
        )

    if value > max_value:
        return ValidationError(
            trade.trade_id,
            f"{field_name.capitalize()} {value} above maximum {max_value}",
        )

    return None


def make_validate_quantity(config: PipelineConfig):
    return partial(
        validate_field_range,
        field_name="quantity",
        min_value=config.min_quantity,
        max_value=config.max_quantity,
    )


def make_validate_price(config: PipelineConfig):
    return partial(
        validate_field_range,
        field_name="price",
        min_value=config.min_price,
        max_value=config.max_price,
    )


def validate_trade(trade: Trade, config: PipelineConfig) -> ValidationError | None:
    validate_quantity = make_validate_quantity(config)
    validate_price = make_validate_price(config)

    if trade.side not in VALID_SIDES:
        return ValidationError(
            trade.trade_id,
            f"Invalid side '{trade.side}' — must be BUY or SELL",
        )

    if trade.symbol not in config.valid_symbols:
        return ValidationError(
            trade.trade_id,
            f"Unknown symbol '{trade.symbol}'",
        )

    quantity_error = validate_quantity(trade)
    if quantity_error is not None:
        return quantity_error

    price_error = validate_price(trade)
    if price_error is not None:
        return price_error

    return None