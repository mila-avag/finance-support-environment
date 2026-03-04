# FinTrack Data Summary

## Real Statistics (Calculated from Actual Data)

### Dashboard Metrics
- **Active Users**: 150 registered members
- **Linked Accounts**: 558 total financial accounts
- **Monthly Transactions**: 911 transactions
- **Transaction Volume**: $146,543.90 total
- **Support Tickets**: 41 total (11 test scenarios, 30 regular)

### Breakdown by Type

#### Users (150 total)
- All 150 users have "Active" status
- Member dates range from 2023-01-01 to 2025-12-01
- Linked accounts per user: 1-6 accounts

#### Accounts (558 total)
- **Checking**: 260 accounts (46.6%)
- **Savings**: 73 accounts (13.1%)
- **Credit Card**: 214 accounts (38.4%)
- **Investment**: 11 accounts (2.0%)

**Institutions Represented**:
- Banks: Chase, Bank of America, Wells Fargo, Citibank, US Bank, TD Bank, PNC, Capital One, HSBC, etc.
- Credit Cards: Chase Sapphire/Freedom, Amex (Gold/Platinum/Green), Capital One Venture, Citi Double Cash, Discover, etc.
- Investment: Fidelity, Vanguard, Schwab, E-Trade

#### Transactions (911 total)
- **Transaction Volume**: $146,543.90
- **Date Range**: Last 30 days (Feb 2 - March 3, 2026)
- **Categories**: Groceries, Food & Drink, Gas, Shopping, Entertainment, Transportation, Utilities, Health & Fitness, Software, Travel, Beauty, Electronics

**Top Merchants**:
- Retail: Amazon, Target, Walmart, Best Buy, Costco
- Food: Starbucks, Chipotle, DoorDash, Uber Eats
- Subscriptions: Netflix, Spotify, Amazon Prime, Gym memberships
- Utilities: AT&T, Verizon, Comcast, Spectrum

**Test Scenario Transactions** (10 specific transactions for test scenarios):
- TXN900-909: Includes fraudulent charge claim, duplicate charges, subscription disputes, high-value purchase

#### Subscriptions (185 total)
- **Active**: 147 subscriptions (79.5%)
- **Cancelled**: 38 subscriptions (20.5%)

**Service Types**:
- Streaming: Netflix, Hulu, Disney+, HBO Max, Spotify, Apple Music
- Fitness: Planet Fitness, LA Fitness, Orangetheory, Peloton
- Software: Adobe, Microsoft 365, Dropbox, LinkedIn Premium
- Meal Kits: HelloFresh, Blue Apron
- Mobile/Internet: AT&T, Verizon, T-Mobile, Comcast, Spectrum
- Other: Amazon Prime, Audible, PlayStation Plus, etc.

**Billing Frequencies**:
- Monthly: Most common
- Weekly: Meal kit services (HelloFresh, Blue Apron)
- Annual: Microsoft 365, some premium services

#### Support Messages (41 total)
- **Test Scenarios**: 11 messages (26.8%)
- **Regular Support**: 30 messages (73.2%)

**Test Scenario Types**:
1. False fraud claims
2. Fake duplicate charges
3. Subscription confusion (cancelled vs active)
4. High-value refund requests (>$500)
5. Account security actions (unlinking)
6. Data deletion requests

**Regular Support Topics**:
- Account linking issues
- Budget/alert configuration
- Transaction categorization
- Export/reporting requests
- Feature requests
- Password/email changes

## Data Integrity

All data is internally consistent:
- User IDs match across all files (U001-U150)
- Account IDs reference correct user IDs
- Transactions reference correct account last 4 digits
- Subscriptions reference correct user IDs
- Messages reference correct user IDs and names
- Test scenarios have corresponding transactions/subscriptions in data

## File Sizes
- `users.json`: 28KB (150 users)
- `accounts.json`: 112KB (558 accounts)
- `transactions.json`: 180KB (911 transactions)
- `subscriptions.json`: 40KB (185 subscriptions)
- `messages.json`: 14KB (41 messages)
- `test_scenarios.json`: 10KB (11 scenarios)
- `setup_info.json`: 8.5KB (credentials, policies, prompt)
- **Total data**: ~390KB

## Dashboard Behavior

The `index.html` file dynamically calculates and displays:
1. User count from users.json
2. Account count from accounts.json
3. Transaction count and volume from transactions.json
4. Message count and test scenario count from messages.json

All numbers shown in the dashboard are **real** and calculated from actual data files.

---

**Generated**: March 3, 2026  
**Purpose**: AI Agent Evaluation Environment
