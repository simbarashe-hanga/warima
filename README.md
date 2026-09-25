# Warima

**Warima** is a WhatsApp-first community finance platform designed to help stokvels and community savings groups manage contributions, wallets, treasuries, and investment infrastructure.

Warima combines conversational finance through WhatsApp with programmable financial infrastructure, including digital wallets, treasury management, blockchain accounts, and multi-rail settlement.

> **From community savings to community-owned assets.**

---

## Overview

Traditional stokvels often rely on:

- Manual record keeping
- Cash or bank-based processes
- WhatsApp messages without structured financial records
- Limited transparency
- Fragmented financial infrastructure
- Difficulty accessing productive investment opportunities

Warima provides a digital infrastructure layer that allows communities to interact with financial services through WhatsApp while maintaining structured financial records and programmable settlement infrastructure.

---

## Core Product

Warima currently focuses on:

- WhatsApp-first community finance
- Stokvel and community management
- Member accounts
- Wallets
- Contributions
- Treasury management
- Blockchain accounts
- Settlement orchestration
- Solana integration
- Agricultural-backed community savings
- Future tokenized ownership of agricultural assets

---

# Architecture

Warima separates the business action from the settlement rail.

```text
WhatsApp
   │
   ▼
Contribution Flow
   │
   ▼
WalletTransaction
   │
   ▼
Resolve Stokvel
   │
   ▼
Resolve Treasury
   │
   ▼
Determine Asset / Rail
   │
   ▼
SettlementOrchestrator
   │
   ▼
SettlementRouter
   │
   ├── SolanaSettlementHandler
   │        │
   │        ▼
   │   SettlementService
   │        │
   │        ▼
   │   SolanaService
   │        │
   │        ▼
   │   Solana Network
   │
   ├── EVMSettlementHandler
   │
   └── OffChainSettlementHandler

System Architecture

Warima is structured into several major domain layers.

Phase 1 — Identity
User
UserIdentity
UserSession
WhatsAppAccount

The identity layer separates the user from the communication provider.

WhatsApp is the current provider, with the architecture allowing additional providers such as email or mobile applications in the future.

Phase 2 — Membership
MemberAccount
MemberProfile

A MemberAccount represents the user's financial identity inside Warima.

Phase 3 — Communities
Club
Membership
Role
Permission

This layer manages community membership and permissions.

Phase 4 — Finance
Wallet
Ledger
LedgerEntry
Transaction
WalletTransaction

This layer manages financial obligations, balances, and transaction records.

Phase 5 — Blockchain
BlockchainAccount
SmartContract
Treasury
Settlement

This layer connects Warima's financial infrastructure to blockchain networks.

Contribution Flow

A normal contribution follows this lifecycle:

Member
   │
   ▼
WhatsApp
   │
   ▼
"contribute"
   │
   ▼
Select Stokvel
   │
   ▼
Enter Amount
   │
   ▼
Confirm
   │
   ▼
WalletTransaction
   │
   ▼
Resolve Stokvel Treasury
   │
   ▼
Determine Asset
   │
   ▼
SettlementOrchestrator
   │
   ▼
SettlementRouter
   │
   ▼
Settlement Handler
   │
   ▼
Blockchain / Off-chain Settlement
   │
   ▼
Settlement Record
   │
   ▼
WhatsApp Confirmation

For a Solana-based digital stokvel:

Member Solana Account
        │
        │ SOL
        ▼
Digital Stokvel Treasury
Settlement Architecture

Warima uses a generic settlement layer rather than embedding blockchain logic inside the contribution flow.

SettlementOrchestrator

The SettlementOrchestrator is responsible for coordinating settlement.

It:

Validates the transaction
Resolves the relevant treasury
Resolves the settlement asset
Determines whether conversion is required
Resolves the settlement rail
Routes the transaction to the correct settlement handler
Returns a structured settlement result
SettlementRouter

The router selects the appropriate settlement mechanism.

SOLANA
   → SolanaSettlementHandler

EVM
   → EVMSettlementHandler

OFF_CHAIN
   → OffChainSettlementHandler

This makes the settlement layer extensible.

Treasury Model

Each stokvel can have a treasury configuration.

A treasury defines:

Denomination
Rail
Network
Strategy
Return Source
Blockchain Address

Supported denominations include:

SOL
WZAR
ZAR

Supported rails include:

SOLANA
EVM
OFF_CHAIN

Supported strategies include:

ON_CHAIN
AGRICULTURE
CASH

This allows different communities to use different financial rails while maintaining the same core Warima architecture.

Solana Integration

Warima currently supports Solana Devnet settlement.

Configuration:

SOLANA_NETWORK=devnet
SOLANA_RPC_URL=https://api.devnet.solana.com

The Solana integration is responsible for:

Creating managed Solana accounts
Resolving Solana accounts for members
Resolving treasury accounts
Checking balances
Creating SOL transfers
Broadcasting transactions
Tracking transaction signatures
Persisting settlement records
Reconciling settlement status
Blockchain Accounts

Each member can have a blockchain account associated with their MemberAccount.

The relationship is:

MemberAccount
      │
      ▼
BlockchainAccount
      │
      ▼
Solana Address

A unique constraint prevents multiple active blockchain accounts for the same member, chain, and network.

member_account_id
chain
network

The current Devnet implementation uses managed Solana accounts.

Devnet Account Provider

The current Devnet implementation keeps Solana signing keys in worker process memory.

Conceptually:

BlockchainAccount
      │
      │ address
      ▼
SolanaAccountProvider
      │
      │ in-memory signer
      ▼
Keypair

This is suitable for development and demonstration.

It is not production custody infrastructure.

A production implementation should use secure key management such as:

AWS KMS
HSM
MPC custody
Encrypted key storage
Dedicated custody infrastructure

Private keys must never be committed to Git or stored directly in this repository.

Settlement Lifecycle

A successful settlement follows:

WalletTransaction
      │
      ▼
PENDING
      │
      ▼
PROCESSING
      │
      ▼
Blockchain Transaction
      │
      ▼
Transaction Signature
      │
      ▼
COMPLETED

If the transaction fails:

PROCESSING
      │
      ▼
FAILED

The settlement record stores the relationship between the internal Warima transaction and the external blockchain transaction.

Database

Warima uses:

PostgreSQL
SQLAlchemy
Alembic

The database is the source of truth for application state.

Important entities include:

User
UserIdentity
UserSession
WhatsAppAccount

MemberAccount
MemberProfile

Stokvel
Membership

Wallet
WalletTransaction

BlockchainAccount
StokvelTreasury
Settlement
Technology Stack
Backend
Python 3.12
FastAPI
SQLAlchemy
Alembic
PostgreSQL
Infrastructure
AWS EC2
AWS RDS
Docker
Docker Compose
Nginx
Messaging
WhatsApp Business API
WhatsApp Webhooks
Blockchain
Solana
Solana Devnet
solana
solders
Web3 infrastructure for future EVM support
AI

Warima can use an LLM as a conversational fallback while deterministic commands handle sensitive financial operations.

Financial actions should remain deterministic and should not rely on an LLM to invent balances, transactions, or financial state.

Project Structure

A simplified structure:

warima/
│
├── backend/
│   └── app/
│       │
│       ├── api/
│       │   └── routes/
│       │
│       ├── engine/
│       │   └── wallet_engine.py
│       │
│       ├── models/
│       │
│       ├── services/
│       │   ├── wallet/
│       │   ├── treasury/
│       │   ├── settlement/
│       │   ├── blockchain/
│       │   └── solana/
│       │
│       ├── workers/
│       │
│       └── main.py
│
├── docker-compose.yml
├── Dockerfile
├── alembic.ini
├── README.md
└── .env
Docker Development

Start the services:

docker compose up -d

Check running services:

docker compose ps

View API logs:

docker compose logs -f api

View worker logs:

docker compose logs -f worker

Open a shell inside the worker:

docker compose exec -T worker bash

Run Python inside the worker:

docker compose exec -T worker python

Run database-related commands inside the worker:

docker compose exec -T worker python -m alembic current

Run migrations:

docker compose exec -T worker alembic upgrade head

Restart the worker:

docker compose restart worker

Rebuild the worker:

docker compose build worker
docker compose up -d --force-recreate worker
Environment Configuration

Create a .env file containing the required environment variables.

Example:

DATABASE_URL=postgresql://USER:PASSWORD@HOST:5432/DATABASE

SOLANA_NETWORK=devnet
SOLANA_RPC_URL=https://api.devnet.solana.com

SOLANA_TREASURY_PRIVATE_KEY=<SECRET>

WHATSAPP_ACCESS_TOKEN=<SECRET>
WHATSAPP_PHONE_NUMBER_ID=<SECRET>
WHATSAPP_VERIFY_TOKEN=<SECRET>

OPENAI_API_KEY=<SECRET>

Never commit .env files or private keys.

Recommended:

.env
.env.*
!.env.example

in .gitignore.

WhatsApp Integration

Warima uses WhatsApp as the primary user interface.

The high-level flow is:

WhatsApp User
      │
      ▼
Meta WhatsApp Business API
      │
      ▼
Webhook
      │
      ▼
Warima API
      │
      ▼
Worker
      │
      ▼
Wallet / Community / Settlement Services

The webhook is responsible for receiving messages.

The worker performs asynchronous processing.

This separation keeps the webhook responsive while financial and blockchain operations execute in the background.

Deterministic Commands

Sensitive financial actions should be handled through deterministic commands.

Examples include:

contribute
wallet
balance
kyc
agent
exit

The general principle is:

Known financial command
        ↓
Deterministic application logic

rather than:

Financial command
        ↓
LLM decides what to do

The LLM can assist with conversational fallback, but it should not be the source of truth for financial state.

Example Contribution

A user can interact with Warima through WhatsApp:

User:
contribute

Warima:
Choose a stokvel:
1. My Savings Club
2. My Digital Club

User:
2

Warima:
Enter contribution amount in SOL.

User:
0.01

Warima:
You are about to contribute 0.01 SOL.
Reply 1 to confirm or 2 to cancel.

User:
1

Warima:
Contribution successful.

The application then records the transaction and settlement.

Security

Security is a core requirement because Warima handles financial transactions and blockchain assets.

Never commit

Do not commit:

Private keys
API keys
Access tokens
Database passwords
WhatsApp credentials
AWS credentials
Production custody

The current in-memory signer implementation is for Devnet development.

Production should replace it with secure custody infrastructure.

Financial integrity

Financial operations should:

Validate transaction state
Prevent duplicate settlement
Validate destination addresses
Validate supported assets
Persist transaction state
Persist settlement state
Record external transaction signatures
Support reconciliation
Idempotency

Settlement operations must be safe to retry.

The settlement layer checks existing transaction states before execution.

Typical states include:

PENDING
PROCESSING
COMPLETED
FAILED
CANCELLED

A transaction already marked COMPLETED must not be executed again.

This protects against duplicate blockchain transfers caused by worker retries or network interruptions.

Current Development Status

Warima currently has working infrastructure for:

WhatsApp message processing
User sessions
Member accounts
Stokvels
Membership
Wallets
Wallet transactions
Treasury resolution
Blockchain account creation
Solana Devnet accounts
Solana Devnet transfers
Settlement orchestration
Settlement routing
Settlement persistence
Settlement reconciliation concepts

The Solana Devnet integration has successfully demonstrated a real on-chain transaction connected to a Warima settlement record.

The current development focus is connecting this infrastructure into the normal contribution lifecycle.

Development Roadmap
Phase 1 — Core Community Finance
 User accounts
 Member accounts
 Stokvels
 Membership
 Wallets
 Wallet transactions
 WhatsApp interaction
Phase 2 — Treasury Infrastructure
 Treasury model
 Treasury resolution
 Treasury strategies
 Multiple settlement rails
 Settlement orchestration
Phase 3 — Solana
 Solana service
 Solana Devnet
 Blockchain accounts
 Managed member accounts
 Solana settlement handler
 On-chain transaction tracking
 Settlement persistence
 Production custody
 Mainnet deployment
Phase 4 — Digital Assets
 Tokenized community assets
 Agricultural asset representation
 Smart contract integration
 Community-owned productive assets
 On-chain treasury management
Phase 5 — Agriculture
 Livestock-backed savings
 Smallholder farmer liquidity
 Agricultural asset tracking
 Produce tokenization
 Farm-to-community settlement
Long-Term Vision

Warima is being built as infrastructure for community-owned finance.

The long-term architecture is intended to connect:

Community Savings
        │
        ▼
Digital Wallets
        │
        ▼
Community Treasuries
        │
        ▼
Programmable Settlement
        │
        ▼
Productive Assets
        │
        ▼
Agriculture
        │
        ▼
Community-Owned Wealth

The goal is not simply to digitize stokvel record keeping.

The broader vision is to provide communities with programmable infrastructure for saving, coordinating capital, and eventually owning productive assets together.

Solana / StockLana Integration

Warima's broader blockchain roadmap includes experimentation with tokenized investment infrastructure and Solana-based asset settlement.

StockLana-related investment infrastructure is maintained separately from the core contribution settlement layer.

The core principle remains:

Warima Community Finance
          │
          ├── Contributions
          ├── Wallets
          ├── Treasuries
          └── Settlement
                    │
                    ▼
                 Solana
                    │
                    ▼
              Digital Assets
Testing

Before testing financial flows, verify the services:

docker compose ps

Check worker logs:

docker compose logs --tail=100 worker

Check API logs:

docker compose logs --tail=100 api

Verify the database migration state:

docker compose exec -T worker alembic current

For Solana Devnet testing, verify the configured network:

docker compose exec -T worker python - <<'PY'
from app.services.solana.solana_service import SolanaService

service = SolanaService()

print("Network:", service.network)
print("RPC:", service.rpc_url)
PY
Production Considerations

Before production launch, the following areas require additional work:

Secure blockchain custody
Key rotation
Transaction monitoring
Reconciliation
Rate limiting
Authentication hardening
KYC/AML compliance
Regulatory licensing
Financial audit trails
Database backups
Disaster recovery
Monitoring and alerting
Mainnet infrastructure
Smart contract security audits
WhatsApp production configuration
Payment provider integration

The Devnet architecture should not be treated as production-ready custody infrastructure.

Contributing

Development should follow the existing domain architecture.

When adding a new financial capability:

Identify the business action.
Persist the appropriate transaction.
Resolve the relevant community and treasury.
Determine the asset.
Route through the settlement layer where applicable.
Persist settlement results.
Make the operation retry-safe.
Avoid placing business logic inside the WhatsApp router.
Keep blockchain-specific logic inside blockchain/settlement services.
Architecture Principles

Warima follows several important principles.

1. Business actions are rail-agnostic

A contribution should not inherently mean "Solana transaction."

It means:

Member contributes to community

The settlement rail is determined separately.

2. WhatsApp is an interface, not the financial system

WhatsApp is the current user interface.

The source of truth remains Warima's backend and database.

3. Blockchain is infrastructure

Blockchain should provide useful capabilities such as:

Transparent settlement
Programmable ownership
Verifiable transactions
Digital assets
Community treasury infrastructure

It should not be introduced merely for branding.

4. Financial state is deterministic

Balances, transactions, contributions, and settlements must come from application state and verified external systems.

LLMs should not invent financial facts.

5. Settlement must be idempotent

A retry must not accidentally create a second financial transfer.

License

License information will be added as the project moves toward public release.

Warima

Community finance infrastructure for the next generation of stokvels.

WhatsApp
   +
Community Finance
   +
Programmable Treasuries
   +
Blockchain Settlement
   +
Productive Assets

Built for communities.
Designed for transparency.
Engineered for programmable finance.
