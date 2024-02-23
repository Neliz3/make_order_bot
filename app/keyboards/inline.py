from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


builder = InlineKeyboardBuilder()
builder.row(
    InlineKeyboardButton(text='Add to cart', callback_data='add'),
)


# products_key = InlineKeyboardMarkup(
#     inline_keyboard=[
#         [
#             InlineKeyboardButton(text='Add to cart', callback_data='add'),
#         ]
#     ],
#     resize_keyboard=True
# )
