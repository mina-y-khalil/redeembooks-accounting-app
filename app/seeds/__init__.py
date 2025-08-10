from flask.cli import AppGroup
from .users import seed_users, undo_users
from .companies import seed_companies, undo_companies
from .vendors import seed_vendors, undo_vendors
from .categories import seed_categories, undo_categories
from .invoices import seed_invoices, undo_invoices
from .payments import seed_payments, undo_payments
from .payment_batches import seed_payment_batches, undo_payment_batches
from .bank_balances import seed_bank_balances, undo_bank_balances
from .audit_logs import seed_audit_logs, undo_audit_logs
from .user_companies import seed_user_companies, undo_user_companies


from app.models.db import db, environment, SCHEMA

# Creates a seed group to hold our commands
# So we can type `flask seed --help`
seed_commands = AppGroup('seed')


# Creates the `flask seed all` command
@seed_commands.command('all')
def seed():
    if environment == 'production':
        # Before seeding in production, you want to run the seed undo 
        # command, which will  truncate all tables prefixed with 
        # the schema name (see comment in users.py undo_users function).
        # Make sure to add all your other model's undo functions below
        undo_audit_logs()
        undo_bank_balances()
        undo_payment_batches()
        undo_payments()
        undo_invoices()
        undo_categories()
        undo_vendors()
        undo_user_companies()
        undo_companies()
        undo_users()

    seed_users()
    # Add other seed functions here
    seed_companies()
    seed_user_companies()
    seed_vendors()
    seed_categories()
    seed_invoices()
    seed_payments()
    seed_payment_batches()
    seed_bank_balances()
    seed_audit_logs()



# Creates the `flask seed undo` command
@seed_commands.command('undo')
def undo():
    undo_audit_logs()
    undo_bank_balances()
    undo_payment_batches()
    undo_payments()
    undo_invoices()
    undo_categories()
    undo_vendors()
    undo_user_companies()
    undo_companies()
    undo_users()
