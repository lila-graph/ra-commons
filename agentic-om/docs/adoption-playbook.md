# Adoption Playbook  
## GitHub-Native Operating Model for Human + AI Engineering Teams

This playbook provides a **practical, phased path** for adopting the GitHub-native operating model defined in this repository.  
It is written for engineering leaders, platform owners, and teams preparing to introduce AI agents as legitimate contributors.

---

# 🎯 Goals of the Adoption Playbook

- Provide **incremental, low-risk steps** to onboard human teams and AI agents  
- Align all contributors (human and AI) to a consistent **specification → plan → execution** workflow  
- Enforce governance **inside GitHub** using native capabilities  
- Enable **safe, auditable agent contributions** without slowing down delivery  
- Reduce entropy and maintain consistent patterns across repos  

---

# 🧭 Phase 0 — Preparation (Humans Only)

**Objective:** Establish clarity, governance, and expectations before introducing any automation.

### Required Actions
- Read the **GitHub-Native Operating Model** (`docs/github-native-operating-model.md`)
- Read the **Branching & Workflow Standard** (`docs/branching-workflow-standard.md`)
- Review and align on the **Eight Governing Principles** (Part II of operating model)
- Align teams on:
  - The definition of "AI developer"
  - PR-first workflow
  - Spec Kit flow (Constitution → Spec → Plan → Tasks → PR)
- Identify where Specs, ADRs, and docs will live inside the repo

### Success Criteria
- Team agrees on conventions and governance  
- All work is flowing through PRs  
- No bypass paths or shadow workflows  

---

# 🧱 Phase 1 — Human-Only Adoption (No Agents Yet)

**Objective:** Establish the workflow and guardrails humans will later share with agents.

### Enable the Following:

### 1. Branch Protection
- `main` is protected
- PR required for all changes
- Require reviews
- Require successful checks (if present)

### 2. PR Templates
Use the template in `dot-github/pull_request_template.md`:
- Scope classification
- Specification link
- Risk & rollback notes
- Test plan
- Checklist enforcement

### 3. Folder & File Patterns
- `/specs/*/constitution.md`
- `/specs/*/spec.md`
- `/specs/*/plan.md`
- `/docs/adr/ADR-XXXX-description.md`

### Success Criteria
- Humans are following Spec Kit and PR-first patterns  
- Repo has predictable structure  
- Governance is working **before** AI is introduced  

---

# 🧩 Phase 2 — AI-Assisted Work (AI as Helper, Not Author)

**Objective:** Allow agents to assist human engineers while maintaining full human ownership.

### Enable These Patterns:
- Agents may:
  - Generate code within human-owned branches  
  - Write tests  
  - Suggest refactors  
  - Draft documentation  
  - Create initial implementation from a spec  
- All agent work must be:
  - Attributed (“AI Involvement” section in PR template)
  - Verified by a human reviewer
  - Linked to a spec or issue

### Guardrails
- AI may NOT:
  - Create branches independently  
  - Open PRs themselves  
  - Modify protected files (unless allowed explicitly)  
  - Change governance, CI, workflows, rules  

### Success Criteria
- Agents add velocity  
- Code quality remains stable or improves  
- Review burden stays manageable  

---

# 🤖 Phase 3 — AI as Authorized Contributor

**Objective:** Allow AI agents to act as true contributors with controlled autonomy.

### Enable These Capabilities:
- Agents may create branches using standard patterns:
  - `feature/<id>-<short-description>` (new functionality)
  - `bugfix/<issue-id>-<fix>` (bug fixes)
  - `refactor/<area>` (code improvements)
  - `docs/<topic>` (documentation updates)
- Agents may create PRs using:
  - PR templates
  - Links to specs / tasks
- Agents may:
  - Implement new features
  - Refactor codebase for consistency
  - Improve documentation
  - Perform code hygiene tasks
  - Generate diagrams
  - Propose pattern-aligned changes

### Technical Infrastructure
- **Git Worktrees**: Enable parallel agent work in isolated workspaces
  - Prevents context confusion when multiple agents work simultaneously
  - Each agent operates in its own worktree without conflicts
  - See Part VII of the operating model for implementation details

### Required Guardrails
- Branch protection remains  
- AI must remain a **non-admin role**  
- Reviewers must confirm:
  - Correctness  
  - Test coverage  
  - Spec conformance  
- CI enforces:
  - Linting  
  - Tests  
  - Policy checks  

### Success Criteria
- Agents contribute safely and frequently  
- Delivery velocity increases  
- Repo consistency improves  

---

# 🧱 Phase 4 — Optimization & Automation

**Objective:** Mature the hybrid team workflows using GitHub-native capabilities.

### Optional Enhancements:
- Automatic labeling for AI-authored PRs  
- Required “AI reviewer” roles  
- PR gating based on:
  - Test coverage  
  - Policy checks  
  - Required context files  
- Scheduled agent tasks (cleanup, consistency, docs)

### Success Criteria
- Human + AI ecosystem operates smoothly  
- No chaos introduced by agent autonomy  
- Governance overhead stays low  
- Development velocity remains high  

---

# 🌱 Summary

This adoption playbook enables teams to gradually transition from human-only workflows to a **safe, scalable hybrid engineering model** where AI agents:

- Accelerate development  
- Maintain consistency  
- Follow human governance  
- Operate transparently  
- Increase team leverage  

Use this file to onboard teams, structure workshops, and conduct phased rollouts across repositories or entire GitHub organizations.
