# Technical Architecture & Design Document

## AI-Driven Explainable Resume Analytics Platform

### 1. Executive Summary

This document outlines the technical architecture for an intelligent platform designed to revolutionize recruitment transparency. By leveraging Large Language Models (LLMs) and Vector Space Modeling, the system moves beyond keyword matching to Semantic Understanding and Explainable AI (XAI), addressing the core research problem of "Black Box" hiring algorithms.

---

### 2. Technology Stack Strategy

#### 2.1 Frontend Layer (User Experience)

- **Framework:** **Next.js 14 (React)** - Chosen for its strong SEO and SSR.
- **Styling:** **Tailwind CSS** - For modern, responsive design.

#### 2.2 Backend Layer (Compute)

- **Framework:** **FastAPI (Python)** - Asynchronous, high-performance API.
- **Libraries:** `pdfplumber`, `python-docx` (Parsing), `scikit-learn` (ML).

#### 2.3 AI Layer (Intelligence)

- **Engine:** **GPT-4o** (Reasoning) + **OpenAI Embeddings**.
- **Logic:** **Cosine Similarity** for semantic matching.

---

### 3. System Architecture (Detailed UML Specifications)

_Below are the technical specifications for the diagrams. You can copy these codes into any Mermaid editor to generate the visuals._

#### 3.1 Use Case Diagram

**Description:** Defines the interactions between the Candidate and the System features.
_(Using robust flowchart syntax to ensure visibility)_

```mermaid
graph LR
    subgraph System ["Resume AI Platform"]
        UC1(Upload Resume - PDF/Word/Img)
        UC2(Input Job Description)
        UC3(View Analysis Dashboard)
        UC4(Download Unbiased Resume)
        UC5(Chat with AI Recruiter)

        UC_Inc(Extract Text / OCR)
        UC_Ext(Check Bias)
    end

    User((Candidate))

    User --> UC1
    User --> UC2
    User --> UC3
    User --> UC4
    User --> UC5

    UC1 -.-> |include| UC_Inc
    UC_Ext -.-> |extend| UC3

    style User fill:#f9f,stroke:#333,stroke-width:2px
    style System fill:#e1f5fe,stroke:#333,stroke-width:2px,stroke-dasharray: 5 5
```

#### 3.2 Sequence Diagram

**Description:** The complete flow of a resume analysis request.

```mermaid
sequenceDiagram
    autonumber
    actor User as Candidate
    participant UI as Frontend (Next.js)
    participant API as Backend (FastAPI)
    participant Engine as Parsing Engine
    participant AI as AI Model (OpenAI)
    participant DB as Vector Store

    User->>UI: Uploads File & Job Description
    UI->>API: POST /analyze {file, job_text}
    activate API

    API->>Engine: Parse File Content
    activate Engine
    alt is Image
        Engine->>Engine: Perform OCR
    else is PDF/Doc
        Engine->>Engine: Extract Text
    end
    Engine-->>API: Return Raw Text
    deactivate Engine

    API->>AI: Generate Embeddings (Text + Job)
    activate AI
    AI-->>API: Return Vectors [v1, v2]
    deactivate AI

    API->>API: Calculate Cosine Similarity

    par Parallel Features
        API->>AI: Generate Explainable Feedback (XAI)
        API->>AI: Generate Heatmap Coordinates
        API->>AI: Check for Bias/Ethics
    end

    AI-->>API: Return JSON Insights

    API-->>UI: Return Full Analysis Object
    deactivate API

    UI->>User: Render Dashboard (Charts, Graph, Chat)
```

#### 3.3 Class Diagram

**Description:** The internal data structure and Object-Oriented design.

```mermaid
classDiagram
    class User {
        +UUID id
        +String email
        +uploadResume()
        +viewHistory()
    }

    class Resume {
        +UUID id
        +String content_text
        +List skills
        +Vector embedding
        +parseFormattedText()
    }

    class JobDescription {
        +String title
        +String requirements_text
        +Vector embedding
    }

    class AnalysisResult {
        +Float match_score
        +String xai_explanation
        +List missing_skills
        +Map heatmap_coordinates
        +calculateCosineSimilarity()
    }

    class BiasChecker {
        +Boolean has_photo
        +Boolean has_age
        +generateWarning()
    }

    User "1" --> "*" Resume : owns
    Resume "1" --> "1" AnalysisResult : generates
    JobDescription "1" -- "1" AnalysisResult : compared_against
    AnalysisResult *-- BiasChecker : composition
```

#### 3.4 Activity Diagram

**Description:** The decision logic flow for the entire process.

```mermaid
flowchart TD
    Start([Start]) --> Upload[User Uploads File]
    Upload --> CheckFormat{File Format?}

    CheckFormat -- Image --> OCR[Run OCR Process]
    CheckFormat -- PDF/Doc --> Parse[Extract Text Library]

    OCR --> Clean[Clean & Normalize Text]
    Parse --> Clean

    Clean --> Vectorize[Generate Vector Embeddings]
    Vectorize --> Calc[Compute Cosine Similarity]

    Calc --> Parallel{Parallel Tasks}
    Parallel --> XAI[Generate AI Explanation]
    Parallel --> Ethics[Run Bias Check]
    Parallel --> Graph[Build Knowledge Graph]

    XAI & Ethics & Graph --> Aggr[Aggregate Results]
    Aggr --> Response[Send JSON to Frontend]
    Response --> Stop([End])
```

---

### 4. Mathematical Foundation

The system implements the **Vector Space Model** defined in Chapter 2:

**Similarity(A, B) = (A · B) / (||A|| × ||B||)**

Where:

- **A**: Vector representation of the candidate's content.
- **B**: Vector representation of the job description.
- The result is a semantic score (0.0 to 1.0).

---

### 5. Ethical & Privacy

- **Bias Checker:** Automatically flags PII (images, age) to prevent algorithmic bias.
- **Privacy:** No personal data is stored permanently (Stateless).
