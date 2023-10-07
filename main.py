import logging
import json

from datetime import datetime, timedelta
from telegram import Update
from telegram.ext import ApplicationBuilder, CallbackContext, CommandHandler

TOKEN_BOT = "6542697255:AAElISMx5CuGRwGpkHIpKwDYTiPm_YsbhWo"

categories = ['walk', 'shop', 'home', 'car']

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
try:
    with open('data.json', 'r') as f:
        data = json.load(f)


except FileNotFoundError:
    data = {'income': [], 'expenses': []}
# data = {'income': [], 'expenses': []}


def save_data():
    with open('data.json', 'w') as s:
        json.dump(data, s)


async def start(update: Update, context: CallbackContext) -> None:
    logging.info('Command "start" was triggered!')
    user_id = update.message.from_user.id
    # if user_id not in data:
    #     data[user_id] = {'expenses': [], 'incomes': []}
    await update.message.reply_text(
        "Привіт! Я телеграмбот для ведення доходів і витрат.\n"
        "Я можу допомогти вам контролювати свої фінанси.\n"
        "Ось що я вмію:\n"
        "/add_expense - додати витрати, вказуючи категорію\n"
        "/add_income - додати доходи, вказуючи категорію доходів\n"
        "/view_expenses - переглянути всі витрати\n"
        "/view_income - переглянути всі доходи\n"
        "/delete_expense - видалити витрати\n"
        "/delete_income - видалити доходи\n"
        "/view_statistics - переглянути статистику доходів та витрат за категоріями за день,\n"
        "місяць, тиждень та рік.\n"
        "/helps - показати інструкцію"
    )


async def helps(update: Update, context: CallbackContext) -> None:
    logging.info('Command "help" was triggered!')
    user_id = update.message.from_user.id
    # if user_id not in data:
    #     data[user_id] = {'expenses': [], 'incomes': []}
    await update.message.reply_text(
        "Привіт! Я телеграмбот для ведення доходів і витрат.\n"
        "Я можу допомогти вам контролювати свої фінанси.\n"
        "Ось що я вмію:\n"
        "/add_expense [категорія] [сумма]\n"
        "/add_income [категорія] [сумма]\n"
        "/view_expenses \n"
        "/view_income\n"
        "/delete_expense [номер строки яку видалити]\n"
        "/delete_income [номер строки яку видалити]\n"
        "/view_statistics [категорія] [income] або[expenses]\n"
        "/help - показати інструкцію"
    )


async def add_expense(update: Update, context: CallbackContext) -> None:
    logging.info('Command "add_expense" was triggered!')
    expense_parts = " ".join(context.args).split()
    category = expense_parts[0].strip()
    amount = int(expense_parts[1].strip())

    if category not in categories:
        await update.message.reply_text("Такої категорії немає, доступні -"
                                        " walk, shop, home, car")
        return

    data['expenses'].append({'amount': amount, 'category': category})
    save_data()
    await update.message.reply_text(f'Ви додали витрати {amount} до категорії {category}!')


async def add_income(update: Update, context: CallbackContext) -> None:
    logging.info('Command "add_income" was triggered!')
    expense_parts = " ".join(context.args).split()
    category = expense_parts[0].strip()
    amount = int(expense_parts[1].strip())

    if category not in categories:
        await update.message.reply_text("Такої категорії немає, доступні -"
                                        " walk, shop, home, car")
        return

    data['income'].append({'amount': amount, 'category': category})
    save_data()
    await update.message.reply_text(f'Ви додали доходи {amount} до категорії {category}!')


async def view_expenses(update: Update, context: CallbackContext) -> None:
    logging.info('Command "view_expenses" was triggered!')
    if not data['expenses']:
        await update.message.reply_text("Ви не додали жодних витрат!")
        return
    expenses = '\n'.join([f"{expense['category']}  {expense['amount']}" for expense in data['expenses']])
    await update.message.reply_text(f"Витрати:\n{expenses}")


async def view_income(update: Update, context: CallbackContext) -> None:
    logging.info('Command "view_income" was triggered!')
    if not data['income']:
        await update.message.reply_text("Ви не додали жодних доходів!")
        return
    incomes = '\n'.join([f"{income['category']} {income['amount']}" for income in data['income']])
    await update.message.reply_text(f"Доходи:\n{incomes}")


async def delete_expense(update: Update, context: CallbackContext) -> None:
    logging.info('Command "delete_expense" was triggered!')
    if not data['expenses']:
        await update.message.reply_text("У вас немає категорій витрат!")
        return
    try:
        index = int(context.args[0]) - 1
        category = data['expenses'].pop(index)
        save_data()
        await update.message.reply_text(f"{category} успішно видалено!")
    except (ValueError, IndexError):
        await update.message.reply_text("Ви ввели неправельний індекс елементу!")


async def delete_income(update: Update, context: CallbackContext) -> None:
    logging.info('Command "delete_income" was triggered!')
    if not data['income']:
        await update.message.reply_text("Ви не додали жодних доходів!")
        return
    try:
        index = int(context.args[0]) - 1
        category = data['income'].pop(index)
        save_data()
        await update.message.reply_text(f"{category} успішно видалено!")
    except (ValueError, IndexError):
        await update.message.reply_text("Ви ввели неправельний індекс елементу!")


async def view_statistics(update: Update, context: CallbackContext) -> None:
    logging.info('Command "view_statistics" was triggered!')
    if len(context.args) != 2:
        await update.message.reply_text("Неправильна кількість аргументів. Використовуйте команду так:"
                                        "/view_statistics [період] [категорія]")
        return

    # period = context.args[0].strip().lower()  # Перший аргумент - період (day, month, week, year)
    category = context.args[1].strip().lower()
    #
    # if category not in categories:
    #     await update.message.reply_text("Такої категорії немає, доступні -"
    #                                     " walk, shop, home, car")
    #     return
    #
    # if period not in ['day', 'month', 'week', 'year']:
    #     await update.message.reply_text("Невірний період. Використовуйте 'day', 'month', 'week' або 'year'.")
    #     return
    if category == 'income':
        if not data['income']:
            await update.message.reply_text("Немає доходів")
            return
        total_income = sum([income['amount'] for income in data['income']])
        income_by_category = {}
        for income in data['income']:
            if income['category'] not in income_by_category:
                income_by_category[income['category']] = 0
            income_by_category[income['category']] += income['amount']
        income_by_category_str = '\n'.join(
            [f"{category}: {amount}" for category, amount in income_by_category.items()]
        )
        await update.message.reply_text(
            f"Total expenses: {total_income}\nExpenses by category:\n{income_by_category_str}"
        )
    elif category == 'expenses':
        if not data['expenses']:
            await update.message.reply_text("Немає доходів")
            return
        total_expenses = sum([expense['amount'] for expense in data['expenses']])
        expenses_by_category = {}
        for expense in data['expenses']:
            if expense['category'] not in expenses_by_category:
                expenses_by_category[expense['category']] = 0
            expenses_by_category[expense['category']] += expense['amount']
        expenses_by_category_str = '\n'.join(
            [f"{category}: {amount}" for category, amount in expenses_by_category.items()]
        )
        await update.message.reply_text(
            f"Total expenses: {total_expenses}\nExpenses by category:\n{expenses_by_category_str}"
        )


def run():
    app = ApplicationBuilder().token("6542697255:AAElISMx5CuGRwGpkHIpKwDYTiPm_YsbhWo").build()
    logging.info("Application built successfully!")
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("helps", helps))
    app.add_handler(CommandHandler("add_expense", add_expense))
    app.add_handler(CommandHandler("add_income", add_income))
    app.add_handler(CommandHandler("view_expenses", view_expenses))
    app.add_handler(CommandHandler("view_income", view_income))
    app.add_handler(CommandHandler("delete_expense", delete_expense))
    app.add_handler(CommandHandler("delete_income", delete_income))
    app.add_handler(CommandHandler("view_statistics", view_statistics))
    app.run_polling()


if __name__ == '__main__':
    run()
