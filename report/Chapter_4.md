% ==================== Chapter 4 ====================
\chapter{Project Management \& Finance}

This chapter documents the management practices used to deliver VisionGuard.ai as a real-time surveillance anomaly-detection prototype within hackathon constraints. The focus is on traceable planning artifacts (WBS and schedule), practical cost reasoning for a student-built system, and risk-aware decisions that supported successful integration and demonstration.

\section{Work Breakdown Structure (WBS)}
The Work Breakdown Structure (WBS) decomposes VisionGuard.ai into deliverables and tasks that can be planned, assigned, and verified. The WBS was designed to align with the end-to-end pipeline (streaming $\rightarrow$ inference $\rightarrow$ persistence $\rightarrow$ alerting $\rightarrow$ UI) while keeping integration risk visible.

\subsection*{WBS (hierarchical list)}
\begin{enumerate}
\item \textbf{Project Initiation \& Requirements}
  \begin{enumerate}
  \item Define objectives, scope, and evaluation targets
  \item Identify stakeholders (Owner/Manager), user stories, and constraints
  \item Select baseline architecture (WebRTC + WebSocket + FastAPI + Next.js)
  \end{enumerate}
\item \textbf{Backend Platform (FastAPI)}
  \begin{enumerate}
  \item Authentication \& authorization (JWT, RBAC)
  \item Shop management (multi-shop Owner/Manager hierarchy)
  \item Database schema \& migrations (PostgreSQL + Alembic)
  \item REST endpoints (auth, shops, anomalies)
  \item WebSocket notification channel
  \end{enumerate}
\item \textbf{Streaming \& Real-time Transport}
  \begin{enumerate}
  \item WebRTC signaling API (SDP offer/answer)
  \item Media track handling and frame extraction
  \item Session lifecycle management (connect/reconnect/cleanup)
  \end{enumerate}
\item \textbf{AI Pipeline (Detection $\rightarrow$ Pose $\rightarrow$ Anomaly)}
  \begin{enumerate}
  \item Person detection (YOLOv8n)
  \item Person tracking (DeepSORT + ReID embeddings)
  \item Pose extraction (YOLOv8n-Pose)
  \item Spatio-temporal anomaly scoring (STG-NF)
  \item Thresholding \& severity mapping
  \end{enumerate}
\item \textbf{Evidence \& Data Management}
  \begin{enumerate}
  \item Evidence frame storage (shop-scoped directories)
  \item Anomaly record persistence and retrieval
  \item Telemetry/logging for debugging and reproducibility
  \end{enumerate}
\item \textbf{Alerting Integrations}
  \begin{enumerate}
  \item Telegram bot connection (shop binding)
  \item Telegram notification payload formatting
  \item Alert rate-control assumptions (avoid alert fatigue)
  \end{enumerate}
\item \textbf{Frontend Dashboard (Next.js)}
  \begin{enumerate}
  \item Authentication UI (login/register)
  \item Shop selection and navigation (Owner/Manager experience)
  \item Live feed view and alert panels
  \item Suspicious activity list and anomaly detail views
  \end{enumerate}
\item \textbf{Testing \& Evaluation}
  \begin{enumerate}
  \item Smoke/unit tests for core utilities
  \item Integration sanity checks (API/WebSocket/WebRTC)
  \item Model metric reporting (AUC-ROC/AUC-PR/EER)
  \end{enumerate}
\item \textbf{Documentation \& Final Delivery}
  \begin{enumerate}
  \item Environment setup and run instructions
  \item Report writing and diagram generation
  \item Demo preparation (scripts, screenshots, final packaging)
  \end{enumerate}
\end{enumerate}

\subsection*{WBS diagram code (Mermaid)}
The following Mermaid code can be pasted into a Mermaid-compatible renderer and exported as an image.

\begin{verbatim}
mindmap
  root((VisionGuard.ai))
    Initiation & Requirements
      Objectives & scope
      Stakeholders & roles
      Architecture selection
    Backend (FastAPI)
      Auth (JWT)
      RBAC (Owner/Manager)
      DB schema + Alembic
      REST APIs
      WebSocket alerts
    Streaming (WebRTC)
      Signaling (SDP)
      Media track handling
      Session lifecycle
    AI Pipeline
      YOLO person detection
      DeepSORT + ReID tracking
      YOLO pose estimation
      STG-NF anomaly scoring
      Threshold + severity
    Evidence & Persistence
      Frame storage
      Anomaly records
      Logging/telemetry
    Integrations
      Telegram binding
      Telegram notifications
    Frontend (Next.js)
      Login/Register
      Live feed
      Alerts & anomalies
      Shops UI
    Testing & Evaluation
      Smoke/unit tests
      Integration checks
      Metrics reporting
    Documentation & Demo
      Setup guides
      Diagrams/report
      Demo readiness
\end{verbatim}

\section{Project Schedule --- Gantt Chart}
Given hackathon time pressure, the schedule was driven by integration risk: transport and end-to-end dataflow were prioritized early, followed by incremental AI integration and alerting. Documentation was treated as a continuous activity rather than an end-only step.

\subsection*{Milestones}
\begin{itemize}
\item \textbf{M1: End-to-end connectivity} (WebRTC stream arrives; UI shows feed placeholder)
\item \textbf{M2: AI inference loop} (frames processed; anomaly score produced)
\item \textbf{M3: Evidence + persistence} (frame saved; anomaly record retrievable)
\item \textbf{M4: Alerts} (WebSocket UI notification + Telegram message)
\item \textbf{M5: Demo-ready build} (RBAC flows, multi-shop navigation, stability pass)
\end{itemize}

\subsection*{Gantt chart code (Mermaid)}
You can paste this into Mermaid Live Editor (or any Mermaid-supporting tool) and export as an image.

\begin{verbatim}
gantt
  title VisionGuard.ai — Hackathon Schedule (Indicative)
  dateFormat  YYYY-MM-DD
  axisFormat  %b %d

  section Planning
  Requirements & scope              :a1, 2026-01-01, 1d
  Architecture & tool choices       :a2, after a1, 1d

  section Backend
  Auth + RBAC (JWT)                 :b1, 2026-01-02, 2d
  Shops + DB schema + migrations     :b2, after b1, 2d
  Anomalies API + persistence        :b3, after b2, 2d

  section Streaming
  WebRTC signaling + session mgmt    :c1, 2026-01-02, 3d
  Frame extraction + processing loop :c2, after c1, 2d

  section AI Pipeline
  Detection + tracking integration   :d1, 2026-01-03, 3d
  Pose extraction pipeline           :d2, after d1, 2d
  STG-NF scoring + thresholding      :d3, after d2, 2d

  section Alerts & UI
  WebSocket notifications            :e1, 2026-01-04, 2d
  Telegram binding + notifications   :e2, after e1, 2d
  Frontend pages (live feed/anomaly) :e3, 2026-01-02, 6d

  section QA & Delivery
  Smoke/unit tests + sanity checks   :f1, 2026-01-06, 2d
  Integration hardening              :f2, after f1, 2d
  Documentation + demo preparation   :f3, 2026-01-01, 9d
\end{verbatim}

\textbf{Note:} Dates are indicative. If your hackathon timeline differs, adjust only the date fields while keeping task ordering consistent with dependency risk.


\section{Budget \& Financial Cost Analysis}
\subsection*{Actual cost (out-of-pocket)}
The prototype was developed using personal computers and lab PCs, with no direct monetary expenditure for compute or hosting during development.
\begin{itemize}
\item \textbf{Out-of-pocket cost:} approximately \$0
\item \textbf{No paid cloud GPUs} were used for the demo build.
\end{itemize}

\subsection*{In-kind cost (estimated equivalent value)}
Although no money was paid, the system consumed resources that have an implicit cost. To communicate financial realism, Table~\ref{tab:cost-in-kind} provides an indicative estimate using conservative assumptions.

\begin{table}[h]
\centering
\begin{tabular}{l l l l}
\hline
\textbf{Item} & \textbf{Assumption} & \textbf{Unit cost (indicative)} & \textbf{Estimated value}\\
\hline
Compute (dev/inference) & 2 PCs + lab PCs, short sessions & \$0 (paid) & \$0 paid\\
Cloud alternative (CPU) & 1 small VM for API + DB (\~1 week) & \$10--\$30 / week & \$10--\$30\\
Cloud alternative (GPU) & 1 entry GPU for experiments (\~10 hours) & \$0.5--\$2 / hour & \$5--\$20\\
Storage & \~2--5 GB frames/logs & \$0.02 / GB-month & < \$1\\
Notifications & Telegram bot & \$0 & \$0\\
\hline
\end{tabular}
\caption{Indicative in-kind cost estimate (what it might cost if replicated on cloud services).}
\label{tab:cost-in-kind}
\end{table}

\textbf{Interpretation:} the prototype is intentionally low-cost, and a minimal cloud replication (CPU-only) remains inexpensive. GPU costs become relevant mainly if one scales the system, increases resolution/FPS, or retrains models frequently.

\section{Risk Analysis \& Mitigation Plan}
Risk management emphasized integration stability and demo reliability. Table~\ref{tab:risk-plan} summarizes the primary risks and mitigations.

\begin{table}[h]
\centering
\begin{tabular}{p{3.2cm} p{3.2cm} p{7.0cm}}
\hline
\textbf{Risk} & \textbf{Impact} & \textbf{Mitigation / Response}\\
\hline
WebRTC instability / NAT issues & Live feed failure during demo & Keep fallback paths (local LAN test), implement session cleanup, validate signaling early, log connection states.\\
Model latency on CPU-only machines & Dropped frames / delayed alerts & Downscale frames, tune FPS, batch/skip frames, prioritize pipeline correctness over high resolution, use light models (YOLOv8n).\\
False positives (staff behavior) & Alert fatigue, reduced trust & Add severity mapping, allow manual review/confirmation, tune thresholds per shop, document limitations and calibration need.\\
Pose degradation (far camera/occlusion) & Reduced anomaly accuracy & Recommend camera placement constraints, consider higher-res capture or pose-robust training data in future work.\\
Database unavailability/migration issues & Loss of anomaly records & Use Alembic migrations, provide environment setup docs, run with local DB for demo, add basic health checks.\\
Security misconfiguration (JWT secret, CORS) & Unauthorized access risk & Environment-based secrets, safe defaults, RBAC enforcement in endpoints, minimize exposed surfaces in demo.\\
Integration overhead across team members & Merge conflicts, duplicated work & Define module ownership, keep interfaces stable, use documented contracts (API schemas), perform frequent integration checkpoints.\\
\hline
\end{tabular}
\caption{Risk analysis and mitigation plan for VisionGuard.ai development and demonstration.}
\label{tab:risk-plan}
\end{table}

\section{Summary of Management Decisions}
The following decisions were adopted to maximize deliverability under hackathon constraints:
\begin{itemize}
\item \textbf{Risk-first sequencing:} streaming and end-to-end connectivity were prioritized before model tuning.
\item \textbf{Cost-aware implementation:} lightweight models and local compute were favored to avoid cloud dependency.
\item \textbf{Modular interfaces:} explicit separation between transport (WebRTC/WebSocket), services (anomaly persistence), and UI reduced merge risk.
\item \textbf{RBAC as a first-class requirement:} Owner/Manager hierarchy was implemented early to keep data access consistent across features.
\item \textbf{Evidence retention policy:} anomalies were persisted with frame evidence to support human review and accountability.
\item \textbf{Demo reliability over feature breadth:} stabilization and documentation were treated as deliverables, not optional tasks.
\end{itemize}
