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

## 4. Receipt Service 

```text
┌─────────────────────────────────────────────────────────────────┐
│                    RECEIPT PROCESSING FLOW                       │
└─────────────────────────────────────────────────────────────────┘

User uploads receipt image
         │
         ▼
┌────────────────────────┐
│ 1. UPLOAD & VALIDATION │
│    ─────────────────   │
│    • Check file size   │
│    • Check format      │
│    • Virus scan        │
└───────┬────────────────┘
        │
        ▼
┌────────────────────────┐
│ 2. STORAGE             │
│    ────────            │
│    • Store in MinIO/S3 │
│    • Generate URL      │
│    • Create DB record  │
└───────┬────────────────┘
        │
        ▼
┌────────────────────────┐
│ 3. OCR EXTRACTION      │
│    ──────────────      │
│    • Extract text      │
│    • Find merchant     │
│    • Find amount       │
│    • Find date         │
│    • Extract items     │
└───────┬────────────────┘
        │
        ▼
┌────────────────────────┐
│ 4. AI CLASSIFICATION   │
│    ─────────────────   │
│    • Send to LLM       │
│    • Get category      │
│    • Get confidence    │
│    • Apply CRA rules   │
└───────┬────────────────┘
        │
        ▼
┌────────────────────────┐
│ 5. REVIEW ROUTING      │
│    ──────────────      │
│    • If conf > 0.9     │
│      → Auto-approve    │
│    • If conf < 0.9     │
│      → Flag for review │
└───────┬────────────────┘
        │
        ▼
┌────────────────────────┐
│ 6. SAVE & NOTIFY       │
│    ─────────────       │
│    • Update DB         │
│    • Send notification │
│    • Update dashboard  │
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