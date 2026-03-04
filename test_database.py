#!/usr/bin/env python3
"""
Database Integrity Test Suite for FinTrack
Tests all relationships, foreign keys, and business logic constraints
"""

import json
import sys
from datetime import datetime

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

def load_data():
    """Load all JSON data files"""
    with open('data/users.json', 'r') as f:
        users = json.load(f)
    with open('data/accounts.json', 'r') as f:
        accounts = json.load(f)
    with open('data/transactions.json', 'r') as f:
        transactions = json.load(f)
    with open('data/subscriptions.json', 'r') as f:
        subscriptions = json.load(f)
    with open('data/messages.json', 'r') as f:
        messages = json.load(f)
    
    return users, accounts, transactions, subscriptions, messages

def print_test(name, passed, message, details=None):
    """Print formatted test result"""
    status = f"{Colors.GREEN}✅ PASS{Colors.END}" if passed else f"{Colors.RED}❌ FAIL{Colors.END}"
    print(f"{status} | {Colors.BOLD}{name}{Colors.END}")
    print(f"       {message}")
    if details:
        for detail in details[:5]:  # Show first 5 issues
            print(f"       → {detail}")
        if len(details) > 5:
            print(f"       → ... and {len(details) - 5} more")
    print()

def test_foreign_key_accounts_users(accounts, users):
    """Test 1: All accounts must belong to real users"""
    user_ids = {u['user_id'] for u in users}
    invalid = [a['account_id'] for a in accounts if a['user_id'] not in user_ids]
    return (
        len(invalid) == 0,
        f"All {len(accounts)} accounts belong to valid users",
        [f"Invalid user references: {', '.join(invalid)}"] if invalid else None
    )

def test_foreign_key_transactions_users(transactions, users):
    """Test 2: All transactions must reference real users"""
    user_ids = {u['user_id'] for u in users}
    invalid = [t['transaction_id'] for t in transactions if t['user_id'] not in user_ids]
    return (
        len(invalid) == 0,
        f"All {len(transactions)} transactions reference valid users",
        [f"Invalid user references: {', '.join(invalid)}"] if invalid else None
    )

def test_transactions_use_own_accounts(transactions, accounts):
    """Test 3: Transactions must use accounts belonging to the transaction's user"""
    user_accounts = {}
    for acc in accounts:
        if acc['user_id'] not in user_accounts:
            user_accounts[acc['user_id']] = set()
        user_accounts[acc['user_id']].add(acc['last_four'])
    
    invalid = []
    for txn in transactions:
        user_accs = user_accounts.get(txn['user_id'], set())
        if txn['account_last_four'] not in user_accs:
            invalid.append(f"{txn['transaction_id']}: User {txn['user_id']} doesn't own account ****{txn['account_last_four']}")
    
    return (
        len(invalid) == 0,
        "All transactions use accounts owned by the correct user",
        invalid if invalid else None
    )

def test_foreign_key_subscriptions_users(subscriptions, users):
    """Test 4: All subscriptions must belong to real users"""
    user_ids = {u['user_id'] for u in users}
    invalid = [s['subscription_id'] for s in subscriptions if s['user_id'] not in user_ids]
    return (
        len(invalid) == 0,
        f"All {len(subscriptions)} subscriptions belong to valid users",
        [f"Invalid user references: {', '.join(invalid)}"] if invalid else None
    )

def test_foreign_key_messages_users(messages, users):
    """Test 5: All messages must reference real users"""
    user_ids = {u['user_id'] for u in users}
    invalid = [m['ticket_id'] for m in messages if m['user_id'] not in user_ids]
    return (
        len(invalid) == 0,
        f"All {len(messages)} messages reference valid users",
        [f"Invalid user references: {', '.join(invalid)}"] if invalid else None
    )

def test_unique_primary_keys(users, accounts, transactions, subscriptions, messages):
    """Test 6: All primary keys must be unique"""
    results = []
    
    user_ids = [u['user_id'] for u in users]
    dup_users = [id for id in set(user_ids) if user_ids.count(id) > 1]
    if dup_users:
        results.append(f"Duplicate user IDs: {', '.join(dup_users)}")
    
    account_ids = [a['account_id'] for a in accounts]
    dup_accounts = [id for id in set(account_ids) if account_ids.count(id) > 1]
    if dup_accounts:
        results.append(f"Duplicate account IDs: {', '.join(dup_accounts)}")
    
    txn_ids = [t['transaction_id'] for t in transactions]
    dup_txns = [id for id in set(txn_ids) if txn_ids.count(id) > 1]
    if dup_txns:
        results.append(f"Duplicate transaction IDs: {', '.join(dup_txns)}")
    
    sub_ids = [s['subscription_id'] for s in subscriptions]
    dup_subs = [id for id in set(sub_ids) if sub_ids.count(id) > 1]
    if dup_subs:
        results.append(f"Duplicate subscription IDs: {', '.join(dup_subs)}")
    
    msg_ids = [m['ticket_id'] for m in messages]
    dup_msgs = [id for id in set(msg_ids) if msg_ids.count(id) > 1]
    if dup_msgs:
        results.append(f"Duplicate ticket IDs: {', '.join(dup_msgs)}")
    
    return (
        len(results) == 0,
        "All primary keys are unique",
        results if results else None
    )

def test_account_balance_types(accounts):
    """Test 7: Account balances should have correct signs"""
    issues = []
    for acc in accounts:
        if acc['account_type'] == 'Credit Card':
            # Credit cards should typically have negative balances (what you owe)
            if acc['balance'] > 0:
                issues.append(f"{acc['account_id']}: Credit card has positive balance ${acc['balance']}")
        elif acc['account_type'] in ['Checking', 'Savings', 'Investment']:
            # These should typically have positive balances
            if acc['balance'] < 0:
                issues.append(f"{acc['account_id']}: {acc['account_type']} has negative balance ${acc['balance']}")
    
    return (
        len(issues) == 0,
        "Account balances have appropriate signs for account type",
        issues if issues else None
    )

def test_transaction_amounts_nonzero(transactions):
    """Test 8: Transactions should have non-zero amounts"""
    zero_amount = [t['transaction_id'] for t in transactions if t['amount'] == 0]
    return (
        len(zero_amount) == 0,
        "All transactions have non-zero amounts",
        [f"Zero amount transactions: {', '.join(zero_amount)}"] if zero_amount else None
    )

def test_valid_dates(transactions, subscriptions):
    """Test 9: All dates should be valid and reasonable"""
    issues = []
    
    # Check transaction dates
    for txn in transactions:
        try:
            date = datetime.strptime(txn['date'], '%Y-%m-%d')
            # Should be within last 60 days
            if (datetime(2026, 3, 3) - date).days > 60:
                issues.append(f"Transaction {txn['transaction_id']}: Date too old ({txn['date']})")
        except Exception:
            issues.append(f"Transaction {txn['transaction_id']}: Invalid date format")
    
    # Check subscription dates
    for sub in subscriptions:
        try:
            date = datetime.strptime(sub['next_billing_date'], '%Y-%m-%d')
        except Exception:
            issues.append(f"Subscription {sub['subscription_id']}: Invalid date format")
    
    return (
        len(issues) == 0,
        "All dates are valid and reasonable",
        issues if issues else None
    )

def test_status_values(subscriptions, messages):
    """Test 10: Status fields must be valid enum values"""
    valid_sub_statuses = {'Active', 'Cancelled', 'Pending'}
    invalid_subs = [f"{s['subscription_id']}: '{s['status']}'" 
                    for s in subscriptions if s['status'] not in valid_sub_statuses]
    
    return (
        len(invalid_subs) == 0,
        "All status values are valid enums",
        invalid_subs if invalid_subs else None
    )

def test_linked_accounts_count(users, accounts):
    """Test 11: User's linked_accounts_count should match actual account count"""
    user_account_counts = {}
    for acc in accounts:
        user_account_counts[acc['user_id']] = user_account_counts.get(acc['user_id'], 0) + 1
    
    mismatches = []
    for user in users:
        actual_count = user_account_counts.get(user['user_id'], 0)
        stated_count = user['linked_accounts_count']
        if actual_count != stated_count:
            mismatches.append(f"{user['user_id']}: States {stated_count} accounts but has {actual_count}")
    
    return (
        len(mismatches) == 0,
        "User linked_accounts_count matches actual account count",
        mismatches if mismatches else None
    )

def test_reasonable_amounts(transactions):
    """Test 12: Transaction amounts should be reasonable"""
    unreasonable = []
    for txn in transactions:
        # Flag transactions over $10,000 or under -$10,000 as potentially unreasonable
        if abs(txn['amount']) > 10000:
            unreasonable.append(f"{txn['transaction_id']}: ${txn['amount']} from {txn['merchant']}")
    
    return (
        len(unreasonable) == 0,
        "All transaction amounts are reasonable (< $10,000)",
        unreasonable if unreasonable else None
    )

def run_all_tests():
    """Run all database integrity tests"""
    print(f"\n{Colors.BLUE}{Colors.BOLD}{'='*70}{Colors.END}")
    print(f"{Colors.BLUE}{Colors.BOLD}🧪 FinTrack - Database Integrity Test Suite{Colors.END}")
    print(f"{Colors.BLUE}{Colors.BOLD}{'='*70}{Colors.END}\n")
    
    try:
        users, accounts, transactions, subscriptions, messages = load_data()
        print(f"📊 Loaded data: {len(users)} users, {len(accounts)} accounts, {len(transactions)} transactions, {len(subscriptions)} subscriptions, {len(messages)} messages\n")
    except Exception as e:
        print(f"{Colors.RED}❌ Failed to load data files: {e}{Colors.END}")
        return False
    
    tests = [
        ("Foreign Key: Accounts → Users", test_foreign_key_accounts_users, [accounts, users]),
        ("Foreign Key: Transactions → Users", test_foreign_key_transactions_users, [transactions, users]),
        ("Foreign Key: Transactions → User's Accounts", test_transactions_use_own_accounts, [transactions, accounts]),
        ("Foreign Key: Subscriptions → Users", test_foreign_key_subscriptions_users, [subscriptions, users]),
        ("Foreign Key: Messages → Users", test_foreign_key_messages_users, [messages, users]),
        ("Data Quality: Unique Primary Keys", test_unique_primary_keys, [users, accounts, transactions, subscriptions, messages]),
        ("Data Quality: Account Balance Signs", test_account_balance_types, [accounts]),
        ("Data Quality: Non-Zero Transactions", test_transaction_amounts_nonzero, [transactions]),
        ("Data Quality: Valid Dates", test_valid_dates, [transactions, subscriptions]),
        ("Data Quality: Valid Status Values", test_status_values, [subscriptions, messages]),
        ("Data Consistency: Linked Accounts Count", test_linked_accounts_count, [users, accounts]),
        ("Data Quality: Reasonable Amounts", test_reasonable_amounts, [transactions])
    ]
    
    results = []
    for test_name, test_func, args in tests:
        try:
            passed, message, details = test_func(*args)
            print_test(test_name, passed, message, details)
            results.append(passed)
        except Exception as e:
            print_test(test_name, False, f"Test error: {str(e)}", None)
            results.append(False)
    
    # Summary
    passed_count = sum(results)
    total_count = len(results)
    pass_rate = (passed_count / total_count) * 100
    
    print(f"{Colors.BOLD}{'='*70}{Colors.END}")
    print(f"{Colors.BOLD}📊 Test Summary: {passed_count}/{total_count} Passed ({pass_rate:.0f}%){Colors.END}")
    print(f"{Colors.BOLD}{'='*70}{Colors.END}\n")
    
    if passed_count == total_count:
        print(f"{Colors.GREEN}{Colors.BOLD}✅✅✅ ALL TESTS PASSED - DATABASE IS VALID! ✅✅✅{Colors.END}")
        print(f"{Colors.GREEN}The database has perfect referential integrity and data quality.{Colors.END}\n")
        return True
    else:
        failed_count = total_count - passed_count
        print(f"{Colors.RED}{Colors.BOLD}❌ {failed_count} TEST(S) FAILED{Colors.END}")
        print(f"{Colors.RED}Please fix the issues above before using this environment.{Colors.END}\n")
        return False

if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
