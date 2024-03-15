from aiogram import types

commands = [
    types.BotCommand(command="start", description="Start"),
    types.BotCommand(command="products", description="List of Products"),
    types.BotCommand(command="cart", description="View a cart"),
    types.BotCommand(command="help", description="Help"),
    types.BotCommand(command="cancel", description="Cancel"),
]

admin_commands = [
    types.BotCommand(command="orders", description="List of Orders"),
    types.BotCommand(command="product_add", description="Add Product"),
    types.BotCommand(command="products", description="List of Products"),
    types.BotCommand(command="statistics", description="Show a Statistics"),
    types.BotCommand(command="help", description="Help"),
    types.BotCommand(command="cancel", description="Cancel"),
]
