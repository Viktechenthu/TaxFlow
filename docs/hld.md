# High level design for TaxFlow AI

## 1. CHAT SERVICE (Tax Assistant)

```text
┌─────────────────────────────────────────────────────────────────┐
│                      CHAT SERVICE FLOW                           │
└─────────────────────────────────────────────────────────────────┘

User asks tax question
         │
         ▼
┌──────────────────────┐
│  1. CHAT ENDPOINT    │
│     ──────────       │
│  • Receive question  │
│  • Validate user     │
│  • Load conversation │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│  2. RAG RETRIEVAL    │
│     ─────────────    │
│  • Generate query    │
│    embedding         │
│  • Search vector DB  │
│  • Get relevant docs │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│  3. CONTEXT BUILD    │
│     ─────────────    │
│  • Combine docs      │
│  • Add chat history  │
│  • Format for LLM    │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│  4. LLM GENERATION   │
│     ──────────────   │
│  • Send to Ollama    │
│  • Get response      │
│  • Parse citations   │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│  5. SAVE & RESPOND   │
│     ──────────────   │
│  • Save message      │
│  • Return to user    │
│  • Update session    │
└──────────────────────┘
```

## 2. KNOWLEDGE BASE SERVICE

```text
┌─────────────────────────────────────────────────────────────────┐
│                  KNOWLEDGE BASE SERVICE FLOW                     │
└─────────────────────────────────────────────────────────────────┘

Upload PDF (CRA Guide)
         │
         ▼
┌──────────────────────┐
│  1. DOCUMENT UPLOAD  │
│     ───────────      │
│  • Validate PDF      │
│  • Store in MinIO    │
│  • Create DB record  │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│  2. TEXT EXTRACTION  │
│     ───────────      │
│  • Extract pages     │
│  • Parse structure   │
│  • Extract metadata  │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│  3. CHUNKING         │
│     ────────         │
│  • Split into chunks │
│  • Semantic splits   │
│  • Add overlap       │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│  4. EMBEDDINGS       │
│     ──────────       │
│  • Generate vectors  │
│  • Batch process     │
│  • Use Ollama embed  │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│  5. INDEX IN DB      │
│     ───────────      │
│  • Store in Qdrant   │
│  • Add metadata      │
│  • Enable search     │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│  6. READY FOR RAG    │
│     ─────────────    │
│  • Document indexed  │
│  • Searchable        │
│  • Available to chat │
└──────────────────────┘
```

## 3. USER SERVICE

```text
┌─────────────────────────────────────────────────────────────────┐
│                      USER SERVICE FLOW                           │
└─────────────────────────────────────────────────────────────────┘

User Registration/Login
         │
         ▼
┌──────────────────────┐
│  1. AUTHENTICATION   │
│     ──────────────   │
│  • Register user     │
│  • Login with email  │
│  • Generate JWT      │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│  2. AUTHORIZATION    │
│     ─────────────    │
│  • Validate token    │
│  • Check permissions │
│  • Load user profile │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│  3. PROFILE MGMT     │
│     ────────────     │
│  • Update info       │
│  • Set preferences   │
│  • Manage settings   │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│  4. ROLE MANAGEMENT  │
│     ───────────────  │
│  • Client role       │
│  • Accountant role   │
│  • Admin role        │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│  5. SESSION MGMT     │
│     ────────────     │
│  • Track sessions    │
│  • Refresh tokens    │
│  • Logout            │
└──────────────────────┘
```

## 4. Receipt Service (Asynchronous Architecture)

```text
┌─────────────────────────────────────────────────────────────────┐
│                     RECEIPT PROCESSING FLOW                     │
│               (Async / Event-Driven Architecture)               │
└─────────────────────────────────────────────────────────────────┘

User uploads receipt image
          │
          ▼
┌────────────────────────┐
│ 1. API INGESTION LAYER │
│    (Synchronous)       │
│    ─────────────────   │
│    • Validate file     │
│    • Upload to MinIO   │◄─────── [MinIO Storage]
│    • Create DB Record  │         (Status: PENDING)
│      (Status: QUEUED)  │
│    • Push Job ID to    │
│      Redis Queue       │
│    • Return "202 OK"   │───────► User sees "Processing..."
└─────────┬──────────────┘
          │
          ▼
┌────────────────────────┐
│ 2. JOB QUEUE (Redis)   │
│    ─────────────────   │
│    • Buffers requests  │
│    • Ensures no loss   │
└─────────┬──────────────┘
          │
          ▼
┌────────────────────────┐
│ 3. BACKGROUND WORKER   │
│    (Asynchronous)      │
│    ─────────────────   │
│    • Dequeue Job       │
│    • Fetch Img (MinIO) │
└─────────┬──────────────┘
          │
          ▼
┌────────────────────────┐
│ 4. INTELLIGENCE PIPELINE
│    ─────────────────   │
│    A. OCR ENGINE       │
│       • Extract raw    │
│         text/coordinates
│                        │
│    B. LLM CLASSIFIER   │
│       • Prompt: "Map   │
│         to CRA codes"  │
│       • Output JSON    │
└─────────┬──────────────┘
          │
          ▼
┌────────────────────────┐
│ 5. BUSINESS LOGIC      │
│    ─────────────────   │
│    • Confidence Check  │
│      (If > 0.90)       │
│        → Status: APPROVED
│      (If < 0.90)       │
│        → Status: REVIEW
│                        │
│    • Rules Engine      │
│      (e.g., if "Meals" │
│       set deduct=50%)  │
└─────────┬──────────────┘
          │
          ▼
┌────────────────────────┐
│ 6. COMPLETION & NOTIFY │
│    ─────────────────   │
│    • Update PostgreSQL │
│    • Trigger WebSocket │───────► Frontend updates
│      event             │         automatically
└────────────────────────┘

```

## 4. SYSTEM OVERVIEW - ALL SERVICES

```text
┌─────────────────────────────────────────────────────────────────┐
│                    COMPLETE SYSTEM DIAGRAM                       │
└─────────────────────────────────────────────────────────────────┘

                          ┌──────────────┐
                          │    CLIENT    │
                          │   (Web/App)  │
                          └──────┬───────┘
                                 │
                                 ▼
                    ┌────────────────────────┐
                    │     API GATEWAY        │
                    │     (FastAPI)          │
                    └────┬───────────────────┘
                         │
         ┌───────────────┼───────────────┬──────────────┐
         │               │               │              │
         ▼               ▼               ▼              ▼
    ┌────────┐     ┌─────────┐    ┌──────────┐   ┌──────────┐
    │  USER  │     │ RECEIPT │    │   CHAT   │   │KNOWLEDGE │
    │SERVICE │     │ SERVICE │    │ SERVICE  │   │   BASE   │
    │        │     │         │    │          │   │ SERVICE  │
    └───┬────┘     └────┬────┘    └────┬─────┘   └────┬─────┘
        │               │              │              │
        │               │              │              │
        ▼               ▼              ▼              ▼
    ┌──────────────────────────────────────────────────────┐
    │              LLM ORCHESTRATOR                         │
    │              (Manages all AI providers)               │
    └─────────────────────┬────────────────────────────────┘
                          │
              ┌───────────┼───────────┐
              │           │           │
              ▼           ▼           ▼
         ┌────────┐  ┌────────┐  ┌────────┐
         │OLLAMA  │  │  OCR   │  │VECTOR  │
         │ (LLM)  │  │ENGINE  │  │  DB    │
         └────────┘  └────────┘  └────────┘
                          │
                          ▼
         ┌────────────────────────────────────┐
         │        DATA LAYER                  │
         │  ┌──────────┐  ┌──────────┐       │
         │  │PostgreSQL│  │  MinIO   │       │
         │  │  (Data)  │  │ (Files)  │       │
         │  └──────────┘  └──────────┘       │
         └────────────────────────────────────┘

```