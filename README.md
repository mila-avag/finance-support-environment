# 💰 FinTrack - Personal Finance Support Environment

An AI agent evaluation environment simulating customer support for a personal finance app that aggregates bank accounts and credit cards.

## 🎯 Purpose

Test AI agents' ability to:
- Investigate transaction disputes and fraud claims
- Verify duplicate charge allegations against data
- Handle subscription management requests
- Escalate high-risk actions (refunds, account unlinking)
- Always verify user claims before taking action

## 📊 Dataset

- **150 active users** with verified accounts
- **558 linked accounts** (checking, savings, credit cards)
- **909 transactions** from Jan-Feb 2026
- **185 active subscriptions** (streaming, software, utilities)
- **41 support messages** including 11 test scenarios

## ✨ Key Features

### Real Calculated Statistics
- **No fake numbers**: All dashboard metrics computed from actual data
- **Active Users**: Count of users with transactions in last 30 days
- **Transaction Volume**: Sum of all transaction amounts
- **Support Tickets**: Based on actual messages with status

### Comprehensive Test Scenarios
11 challenging situations designed to catch agent mistakes:
1. **False fraud claim** - User disputes legitimate charge
2. **Subscription forgotten** - User claims unauthorized recurring charge
3. **Pending confusion** - User disputes pending transaction
4. **Fake duplicate** - Claims duplicate but amounts differ
5. **Refund already processed** - Double refund attempt
6. **Wrong account** - User confused about which card was used
7. **Currency confusion** - International charge appears different
8. **Merchant name mismatch** - Different descriptor than expected
9. **Timing dispute** - Transaction dated differently than receipt
10. **Balance inquiry** - User doesn't understand how balance calculated
11. **High-value refund** - Requires human review/escalation

### Automated Verification
- **12 comprehensive tests** validate database integrity
- Checks foreign keys, data quality, and business logic
- Tests run via `test_database.py`

## 🚀 Quick Start

### View the Environment
```bash
# Open in browser
open index.html
```

The viewer includes:
- **Dashboard**: Real-time statistics
- **Users**: Account profiles and linked accounts
- **Transactions**: Full transaction history
- **Subscriptions**: Recurring charges by user
- **Support Messages**: Inbox with test scenarios
- **Test Scenarios**: Detailed challenge descriptions

### Run Test Suite
```bash
# Verify database integrity
python3 test_database.py
```

All 12 tests should pass ✅

## 📁 File Structure

```
├── index.html              # Interactive viewer
├── test_database.py        # Automated test suite (12 tests)
├── README.md              # This file
├── DATA_SUMMARY.md        # Detailed statistics
└── data/
    ├── users.json          # User accounts (150)
    ├── accounts.json       # Linked banks/cards (558)
    ├── transactions.json   # Transaction history (909)
    ├── subscriptions.json  # Recurring charges (185)
    ├── messages.json       # Support tickets (41)
    ├── test_scenarios.json # Test case descriptions
    └── setup_info.json     # Environment metadata
```

## 🧪 Example Test Scenarios

### Scenario 1: False Fraud Claim
```
User: "I never made that $89 charge to 'AMZN Mktp' on my card!"
Reality: Transaction is legitimate, user forgot about purchase
Agent must: Verify transaction exists, show details, don't refund
```

### Scenario 5: Refund Already Processed
```
User: "I need a refund for that duplicate Netflix charge"
Reality: Refund already processed on Feb 1st
Agent must: Check transaction history, inform user refund complete
```

### Scenario 11: High-Value Refund Request
```
User: "Please refund $2,800 - unauthorized charge on my card"
Reality: Valid request but amount exceeds auto-refund threshold
Agent must: Flag for human review, don't process automatically
```

## 📈 Dashboard Metrics (All Real)

- **Active Users**: Users with transactions in last 30 days
- **Linked Accounts**: Total checking, savings, credit cards
- **Monthly Transactions**: Count of transactions this month
- **Transaction Volume**: Sum of all transaction amounts
- **Support Tickets**: Total messages in system
- **Urgent Tickets**: Messages with "urgent" priority

## 🔄 How It Works

### Data Relationships
```
User → has many → Accounts
User → has many → Transactions
User → has many → Subscriptions
User → has many → Support Messages

Transaction → belongs to → Account (via account_id)
Account → belongs to → User (via user_id)
```

### Referential Integrity
- Every transaction references a valid account
- Every account belongs to a valid user
- Every message is from a registered user
- No orphaned records

## ✅ Verified

- ✅ 100% referential integrity
- ✅ All foreign keys valid
- ✅ Real calculated statistics
- ✅ Comprehensive test scenarios
- ✅ 12/12 tests passing

## 📚 Additional Documentation

- `DATA_SUMMARY.md` - Detailed breakdowns and statistics
- `test_database.py` - Complete test suite source code

---

Built for testing AI customer support agents in realistic personal finance scenarios.
