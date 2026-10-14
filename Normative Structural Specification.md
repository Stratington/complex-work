# Normative Structural Specification for Complex Engineering Projects

Author: Franz Bruckhoff, Stratington Systems

This is the structural document of the Framework for Keeping Complex Work Coherent Across Time. It states what an adopting Project must contain, how the elements relate, and which rules bind them. Where each element lives is declared by each Project's Path Map, not by this Specification (§1.8, §14.8). It operationalizes the five core principles of [[Governing Principles]]: Component-Oriented Decomposition (COD), Layered System Architecture (LSA), Integrated Modularity First (IMF), Verification-First Engineering (VFE), and Specifications as Contracts (SaC).

Every normative clause is traceable to one or more of the 79 Adopted structural forms (GP-01 to GP-79) in [[Generalized Patterns]] or to a frozen principle. Each clause ends with a traceability bracket naming its grounds. Appendix B gives the complete mapping. Where this Specification and any other framework document conflict on structure, this Specification governs.

**Scope of application**

This Specification defines the structural foundation for Projects that adopt the Framework for Keeping Complex Work Coherent Across Time. Its clauses bind an adopting Project, and a deviation is allowed only as recorded in the Deviation Matrix (§1.5, §9.4). Not every clause is equally relevant to every Project. The core sections apply to all adopting Projects. The depth and formality with which each required artifact is produced scale with the Criticality Class of the Component or Capability it governs and with the overall risk and complexity of the Project, as defined in §1.6 and §7.10.

## 1 Purpose, Scope, and Compliance

### 1.1 Authority
This Specification defines the required structure of every Project built under the Framework for Keeping Complex Work Coherent Across Time: the required artifacts, their content rules, their directional relationships, and the Normative Checks that enforce them. It is the structural reference for humans and AI Agents alike. Concrete storage of the artifacts is declared by each Project's Path Map (§1.8, §14.8). [Goal §6.2; SaC]

### 1.2 Domain of application
This Specification is intended to support engineered Systems of high complexity across domains, including software platforms, robotic Systems, and floating cities. Its core clauses avoid domain-specific assumptions. Domain practice adds the methods and controls required by each field, with any structural deviation recorded under §1.5. [Goal P3; GP-16]

### 1.3 Human authority
Purpose, Invariants, risk acceptance, and the definition of done belong to the human owner. AI Agents may draft, propose, and implement; they may not enact changes to purpose, Contracts, Acceptance Criteria, or risk acceptance. Every clause of this Specification preserves this division. [Goal P4; Goal §5; VFE; SaC]

### 1.4 Completeness of structure
The Project structure must cover four recursive process groups at every level of the System:

1. **Agreement**: formal commitments with external parties (customers, users, partners, regulators, vendors, contractors, etc.).
2. **Project-enabling**: the supporting work that makes the Project possible (tooling, configuration, quality infrastructure, shared services, etc.).
3. **Technical management**: planning, monitoring, decision-making, risk handling, control of the work, etc.
4. **Technical**: the actual engineering work (defining, designing, realizing, verifying, etc.) of the System.

These groups classify required coverage. They do not prescribe any particular life-cycle model. No level of the System may omit the agreement processes or the verification processes. [GP-16]

### 1.5 Compliance and deviation
Every clause of this Specification is binding.
A deviation is allowed only when it is recorded as an explicit entry in the Deviation Matrix (§9.4). Each entry must name:
- what is being waived,
- why the waiver is needed, and
- which named human accepted the risk.

The matrix starts empty. Most Projects will have few or no entries. Implicit or unspoken deviation is prohibited.
The purpose of this rule is transparency and human accountability, not bureaucracy. [GP-53; SaC]

### 1.6 Formality scales with risk; every required Entity must exist
No Entity required by this Specification may be omitted; only the depth of its instances may be adjusted.

The amount of detail, documentation, and review applied to each artifact scales with two factors:
- the Criticality Class of the Component or Capability it governs (see §7.10), and
- the overall risk and complexity of the Project.

Low-criticality work may use lightweight versions of the required artifacts. High-criticality or safety-relevant work must use fuller, more rigorous versions. The decision to use a lighter or fuller version must be recorded with a short rationale in the Criticality Record (§7.10).

This clause governs the depth of a required artifact only; it does not override §1.5. Omission of a required Entity remains possible solely as an entry in the Deviation Matrix (§9.4). [GP-39; VFE]

### 1.7 This Specification is high-stability
Individual Projects must not create their own versions of this Specification. If a Project needs to deviate from any clause, it must do so explicitly using the deviation process in §1.5.

The Specification may be changed only by a human decision recorded as a Decision Record (§11) that states the reason for the change and its consequences. [LSA; SaC]

### 1.8 Abstract information model, concrete storage
This Specification defines an abstract information architecture: the required Entities, their required content, their directional relationships, and the Gates that bind them. It does not prescribe concrete storage. Filesystem paths, directory trees, file names, and serialization formats (Markdown, YAML, JSON, domain-native model formats, etc.) are declared by each Project in its Path Map (§14.8).

This separation is deliberate, for four reasons:
- **No ontological mismatch.** A standard defines requirements and an information model. Hardcoded storage paths would conflate the meta-model of the architecture with one storage implementation of it.
- **Domain-native tooling.** Domains work in different native formats: declarative interface schemas, structured data files, parametric models, tabular mass-property data, etc. Forcing one serialization on every domain creates friction between the System description and the tools that produce and check it.
- **Checkable serialization.** Human-readable prose formats are fragile for the automated parsing of relational data (dependency graphs, ledger entries, Obligation matrices, etc.). The serialization format of each Entity is therefore a declared Project choice, so that Normative Checks can parse each Entity in a format suited to mechanical verification.
- **Composability.** A concrete layout that serves one domain well can be reused by other Projects in that domain. Ready-made layout guides for particular domains may exist outside this Specification. They are not part of it and bind nothing: a Project's Path Map governs, whatever its bindings were modelled on.
[Goal DR1; Goal P3; LSA]

## 2 Terminology
The terms below are defined once and used consistently throughout this Specification.

- **Acceptance Criteria**: the checkable statements that define "done" for a unit.
- **AI Agent**: an Executor that is an AI system rather than a human.
- **Baseline**: an approved, frozen snapshot of the description of the System or of its Realization, at a defined level.
- **Baseline Ledger**: the register that records every approved Baseline: the artifacts it governs, its snapshot identifier, its status, and the named human who accepted the lock (§9.1).
- **Blast Radius**: the set of System elements that a given change or failure can affect.
- **Capability**: a function the System delivers to its users or operators. A Capability may span several Components.
- **Component**: a bounded unit of responsibility with explicit interfaces, Contracts, and Acceptance Criteria.
- **Component Specification**: the normative document that defines one Component (Rationale, Required Behaviors, Acceptance Criteria, Constraints, Dependencies & Interfaces, plus its private Design).
- **Constraint**: an Obligation that limits how a need may be met rather than stating what must be achieved.
- **Contract**: the human-approved part of a Specification that other Components may rely on. It primarily contains the Obligations, interfaces, Invariants, and Acceptance Criteria.
- **Criticality Class**: the recorded class assigned to a Component or a Capability that determines the Obligations and the verification rigor applying to it.
- **Criticality Record**: the register that holds the Criticality Class assigned to each Component and Capability, together with the tailoring decisions and rationales that other clauses direct into it (§7.10).
- **Decision Record**: a numbered, immutable record of one binding decision.
- **Design**: how a Component satisfies its Contract. Visible only to the Component’s implementer; binds no other Component.
- **Deviation Matrix**: the register that records every deviation from this Specification, naming what is waived, why, and which named human accepted the risk (§9.4).
- **Entity**: a class of element required by this Specification, of which a Project holds one or more instances. Appendix A lists every required Entity; the Path Map (§14.8) binds each Entity to concrete storage.
- **Entry Point**: the single short document that serves as the starting map of the Project Record. Every Executor begins here and is directed from it to the deeper artifacts relevant to their work. It declares the Path Map that binds every required Entity to its concrete location (§14.3, §14.8).
- **Exploratory Work Unit**: a bounded, time- or resource-capped Work Unit executed in an isolated workspace to investigate candidate questions (feasibility, empirical models, candidate Specifications, etc.). Its completion is defined by meeting declared stopping criteria and producing structured findings recorded in the Project Record, not by modifying the canonical Realization or System description.
- **Executor**: a human or an AI system performing work under a bounded mandate.
- **Gate**: a controlled passage between Phases, closed only by a human decision recorded as a Decision Record (§11).
- **Governance Document**: a human-authored standing directive (principles, rules, instructions, etc.) addressed to Executors.
- **Invariant**: a property that must always hold and that no Executor may weaken without human authorization.
- **Key Design Parameter**: one of a small named set of parameters that govern System success.
- **Normative Check**: a mechanically executable rule that verifies whether Project artifacts comply with a structural requirement of this Specification.
- **Obligation**: one verifiable requirement statement.
- **Operational Concept**: the statement of how the System will be operated and sustained.
- **Path Map**: the deterministic declaration, held in the Entry Point, that binds every required Entity of this Specification to a concrete location pattern and a serialization format (§14.8).
- **Phase**: a bounded stage of work that produces at least one durable artifact and is entered and left through a Gate.
- **Plan Document**: the binding document that governs one Work Unit, stating its scope, its Acceptance Criteria, its progress, and the decisions taken under it. It is the artifact an Executor follows in preference to any conversational instruction.
- **Production Work Unit**: a Work Unit that modifies the canonical Realization or System description under an approved Specification and an approved Plan Document.
- **Project**: the bounded endeavor that produces and sustains one System, governed by one Project Record.
- **Project Record**: the versioned set of durable artifacts that constitutes the system of record for the Project.
- **Realization**: the actual built System or Component, as distinct from its description.
- **Reference Realization**: a maintained instance that embodies the current interpretation of a Contract, against which the governed element is compared to detect drift (§7.17). Distinct from a Verification Reference State.
- **Registry**: the machine-readable index of every Component and content item in the System.
- **Risk Register**: the register that records every identified risk with its owner, analysis, mitigation plan, tracking method, and closure (§12.1).
- **Specification**: the normative description of a Component or an effort. It consists of the Contract plus the Design.
- **Stability Class**: the classification of an element by expected rate of change. Dependencies must point only toward elements of equal or higher Stability Class.
- **Status Ledger**: the register that records the status and history of every change, deviation, waiver, and audit outcome (§9.3).
- **Subsystem**: a Component that is also a System at a lower level of decomposition. It contains interacting Components and must satisfy the Contract of its containing System.
- **System**: the engineered artifact under construction, in any domain.
- **Verification Artifact**: the durable record that an Acceptance Criterion was checked, including the outcome.
- **Verification Plan**: the governing document that fixes the scope, responsibilities, resources, and completion criteria of verification for the Project.
- **Verification Procedure**: a concrete procedure that can be executed to determine whether one or more Acceptance Criteria are satisfied. The durable record of running a Verification Procedure is a Verification Artifact.
- **Verification Reference State**: the recorded outcome of executing whatever verification exists immediately before a change begins, used as the comparison point for that change. Distinct from a Baseline (§9.1).
- **Vision Document**: the human-authored statement of the System's purpose, problem, desired future state, and long-term goals.
- **Work Record**: the single structured, queryable artifact that records every Work Unit, any typed relations between Work Units, and the discoveries made during their execution.
- **Work Unit**: a bounded unit of work with declared scope, an assigned Executor, and Acceptance Criteria.

## 3 Purpose

### 3.1 One Vision Document
Every Project must have exactly one Vision Document. It states the essential problem being solved, the concrete desired future state, and the long-term goals that define success. It is short, stable, free of implementation detail, and written so that the gap between current reality and the desired outcome is clear, credible, and memorable after a single reading. It is the first artifact created and is human-authored. [GP-13; GP-68; LSA]

### 3.2 Highest stability
The Vision Document is the highest-stability artifact of the Project. It must change only rarely, and only through the controlled change Gate (§9.2) and a Decision Record (§11).

No implementation choices, technology selections, material choices, vendor names, or detailed design decisions, etc. may appear in the Vision Document. Those details belong in lower-stability documents. [GP-50; GP-51; LSA]

### 3.3 Hierarchy of intent
The Vision Document sits at the top of the hierarchy. Every lower-level document that states or plans work (Component Specifications, Plan Documents, design documents, etc.) must explain how it serves the goals stated in the Vision Document. No lower-level document may change, contradict, or redefine the problem, desired future state, or long-term goals that the Vision Document has already accepted. [GP-13]

## 4 The Project Record

### 4.1 Sole system of record
All state that governs work must exist as durable, versioned, human-readable artifacts inside the Project Record. This includes Plan Documents, progress, decisions, open issues, and verification outcomes. Agreements held only outside the Project Record (in conversation, message channels, Executor memory, etc.) have no governing force and must be written into the Project Record before they become binding. Completed Plan Documents must remain in the record as history. The depth and formality of these artifacts may scale with Project criticality, but their existence is required. [GP-01; GP-06]

### 4.2 Durable work, disposable Executor instances
Executor instances are disposable; the work product is durable. All meaningful work product must exist as versioned artifacts in the Project Record. Shared decisions must be recorded append-only and must be read by every Executor before work where relevant. Progress must accumulate only in the Project Record, never solely in the memory or private context of an Executor. [GP-65; GP-01; GP-02]

### 4.3 One canonical source per concern
For every concern, exactly one artifact is the canonical source of truth. The Project must declare, in a single place readable by every Executor, which artifact governs each concern and how those artifacts relate to one another. Any derived artifact (indexes, ledgers, summaries, compliance records, etc.) must be generated from its canonical source and must never be maintained in parallel with it. Conflicting sources for one concern are a defect and must be resolved by designating one source and demoting the others. [GP-59]

### 4.4 Machine-readable, checkable surfaces
Every surface of the System on which an Executor is expected to act (documents, interfaces, structured records, declared instructions, etc.) must be machine-readable and checkable. The human owner must own the Contract and the top-level decomposition; Executors implement beneath. [GP-76]

### 4.5 Work Record
Every Project must maintain one Work Record: a structured, queryable artifact kept under the same version control as the System description, capturing every Work Unit and the discoveries made during execution. Unstructured prose lists must not serve as the system of record. Where Work Units carry dependencies, those dependencies must be recorded as typed relations (at minimum: blocks, part-of, supersedes, etc.); a Work Unit is then eligible for execution only when every relation that blocks it is resolved, and completing a unit must release its dependents. [GP-04; GP-05]

### 4.6 One binding Plan Document per Work Unit
Each Work Unit must be governed by one binding Plan Document, which the Executor follows in preference to any conversational instruction. The unchecked Acceptance Criteria in the document constitute the queue of remaining work. A conflict between the Plan Document and an instruction must be resolved in favor of the Plan Document or escalated to the human owner. The Plan Document itself must record its current progress and the decisions taken under it. [GP-03; GP-01]

### 4.7 Iteration discipline
Each work iteration must proceed as follows:
1. Read the current state from the Project Record.
2. Complete exactly one Work Unit.
3. Verify that unit against its Acceptance Criteria.
4. Record the new state and the verification outcome before the next iteration begins.

The size of the Work Unit is governed by the sizing and Blast Radius rules in §5.5 and §5.6. [GP-02; VFE]

### 4.8 Concurrent contributions merge through one role
Where more than one Executor contributes to the same shared artifact at the same time, their contributions must be prepared separately and merged into the canonical artifact by one named role. No Executor may write directly to a canonical artifact while a merge is pending. The named role may be a human or a declared process, and it must be recorded in the Project Record for the duration of the concurrent work. [GP-65]

### 4.9 Governance Documents are controlled artifacts
Governance Documents (including reusable instructions given to AI Agents) must be versioned, reviewable, and checkable artifacts in the Project Record under direct human editing. Governance Document content hidden inside tools or frameworks is prohibited. [GP-66]

## 5 Decomposition and Work Units

### 5.1 Deliverable-anchored decomposition
Project decomposition must be organized around the deliverables the Project produces, not around the Executors doing the work or around organizational structure. Every decomposition element must carry a short definition stating what the element is and what it delivers. The identity of an element must not depend on which Executor performs the work. Work that yields no deliverable (management, integration, etc.) must appear as explicit elements. [GP-07; COD]

### 5.2 Purpose-defined Components
The System must be decomposed into Components defined by the purpose they serve, not by physical form, packaging, or implementation technology, etc. Each Component must carry its own Obligations and design criteria, one named human owner, and a Verification Procedure that yields a binary pass/fail status readable by anyone. Obligations, ownership, and pass/fail status of any Component must be retrievable on demand. [GP-08; COD]

### 5.3 System level before Component detail
System-level interactions and cross-boundary Contracts must be defined before Component internals. Each Component must be designed against declared System behavior and the interfaces it declares with other Components. Where local and System-level optimization conflict, the System-level optimum governs. The local cost accepted for that System gain must be recorded as a Decision Record (§11). A change that crosses a boundary must be agreed at System level before it is made inside a Component. [GP-09; COD]

### 5.4 Integrated modularity first
The default structure is one coherent System with strong internal Component boundaries. Hard separation (independent ownership, strong operational or physical isolation, independent fabrication, independent evolution, etc.) is introduced only when a concrete need exists (significantly different rates or constraints of evolution, required failure isolation, regulatory or safety boundaries, physical constraints, etc.) and its benefits clearly outweigh the added coordination and interface costs. Premature hard separation is a defect. [IMF]

### 5.5 Sizing
Significant work that is assigned to an Executor must be decomposed into Work Units that one Executor can complete in one bounded effort while meeting the Work Unit’s Acceptance Criteria. An oversized Work Unit must be split before execution begins. AI Agents may propose the decomposition and the sizing. The human owner remains the final authority on any sizing decision that could affect higher-level Contracts, Invariants, or the definition of done. Work Units that stay strictly inside already-accepted higher-level Contracts and Acceptance Criteria may be sized by AI Agents. [GP-10]

### 5.6 Work Units bounded by Blast Radius
Before a Work Unit starts, its Blast Radius must be estimated and bounded. Parallel Work Units must have non-overlapping Blast Radii. A change whose Blast Radius cannot be bounded must be decomposed further before execution. [GP-12]

### 5.7 Work Units must be verifiable
Significant work assigned to an Executor must be packaged as a Work Unit: a bounded scope with checkable Acceptance Criteria. Work Units belong to one of two classes:
- **Production Work Units**: modify the canonical Realization or System description. Each unit must execute in isolation, governed by a pre-existing Specification and a human-approved Plan Document (§6.13). A Production Work Unit is complete only when its Verification Procedures pass.
- **Exploratory Work Units**: investigate feasibility, test empirical models, optimize parameters, or discover candidate Specifications. Governed by explicit research questions, resource ceilings (time, token, compute budgets, etc.), and stopping criteria. An Executor operating under a human-approved exploratory mandate may spawn and iterate internal exploratory loops autonomously within declared resource boundaries.

Large efforts must be decomposed into bounded Work Units before execution begins. [GP-11; VFE]

### 5.8 Nested levels of intent
Decomposition must form nested levels of intent: each level states why the work below it exists and is governed by Acceptance Criteria at its own level. Purpose belongs to the outermost level (the Vision Document, §3.3). No inner level may redefine the Acceptance Criteria of a level above it. [GP-13]

### 5.9 Work Units for long-horizon work
Long-horizon work must be decomposed into Work Units, each small enough for one Executor to complete and verify in one bounded effort. Each Work Unit must carry its own Acceptance Criteria and the Verification Procedures that confirm them. The Verification Procedures must run at the end of every Work Unit. Failures must be repaired before the next Work Unit starts. The governing Specification is frozen against drift; a change to it requires a Decision Record (§11). [GP-14; VFE]

### 5.10 Reusable task definitions
Recurring kinds of work must be defined once as reusable task-definition documents. In AI coding environments these are commonly called skills. In complex engineering and simulation environments they are more often called procedures or templates. Each document must contain:

- an imperative sequence of steps
- the Acceptance Criteria that must be satisfied when the work is done
- the actions the Executor must not take
- any required inputs (and their expected source)

Each document must also carry a short summary of when it applies, so an Executor can select the applicable task definition. Each task-definition document is a Governance Document (§4.9). The name and terminology used may follow the conventions of the tools and domain in use; the binding to concrete storage is declared in the Path Map (§14.8). [GP-77]

## 6 Component Specifications and Contracts

### 6.1 Component Specifications
The Project must maintain a set of atomic Component Specifications: one Component Specification per Component, each a discrete, separately addressable artifact of the Project Record. Each Component Specification defines one coherent unit of responsibility. These are the primary documents that humans and AI Agents implement against. If a Component grows too large to keep its Required Behaviors and Acceptance Criteria consistent, it must be decomposed further. Component Specifications are written in System terms. User-story language is never the primary framing; it may appear only as optional context inside the Rationale section of a truly end-user-facing Component. [COD; SaC]

### 6.2 Required sections, linted
Every Component Specification must contain these sections, checked by Normative Checks (§16):

- **Rationale**: why this Component must exist. May contain one to a few short user-story statements if the Component is end-user facing.
- **Required Behaviors**: precise description of what the Component must do, in System terms.
- **Acceptance Criteria**: testable conditions that define "done".
- **Constraints**: hard limits (performance, safety, resources, etc.).
- **Dependencies & Interfaces**: explicit declaration of relationships: the Components or interfaces this one requires; the interfaces or Contracts this one provides; and any containment ("part of") relationship.
[COD; SaC; VFE]

### 6.3 Public Contract, private Design
Each Component Specification splits into a public Contract and a private Design. The Contract comprises the five required sections listed in §6.2 and is visible to the Executors of every Component that has a declared interface or dependency relationship with it. The Design is visible only to the Executor(s) implementing that Component. Every other Component must rely on the Contract alone. An Executor working on a Component must receive that Component's full Specification and the Contracts of the Components with which it has declared interface or dependency relationships, not the whole System description. [GP-27]

### 6.4 The Specification is the durable alignment artifact
The Realization is derived from and governed by the Specification. Where a Realization can be regenerated, it must be regenerated from the Specification rather than edited independently; where it cannot, the Specification remains the governing description and any divergence between the two is a defect in the Realization. Alignment, discussion, and versioning must occur at the Specification level. Specifications must be human-readable, versioned, maintained with a changelog, and open to contribution from any relevant discipline. [GP-19; SaC]

### 6.5 Obligation statements
Obligations in Required Behaviors and Constraints must be expressed as unique, quantitative, verifiable statements. Each statement must name exactly one commitment in a fixed structure: the condition under which it holds, the subject that must act, the action, the object, and the constraint on the action. Ambiguous or compound statements must be rewritten until each statement is independently checkable. [GP-20; GP-21]

### 6.6 Obligation attributes
Every Obligation must carry fixed attributes: identifier, owner, type, priority, source, rationale, status, and verification method. Obligations are organized in levels that mirror the decomposition: from the expectations of the parties the System serves (customers, users, regulators, etc.), through the Operational Concept (§6.17), down to Component Obligations. The type of an Obligation (what it constrains) governs which verification method is admissible for it. Attribute rigor scales with Criticality Class (§7.10). [GP-22; GP-39]

### 6.7 Named owner for every Obligation
Every Obligation must be owned by one named human, never by a department or a role. The owner is the person who can be asked why the Obligation exists. An Obligation without a named human owner is not valid. [GP-23]

### 6.8 Constraint provenance
Every Constraint must be marked as externally imposed (contract, regulation, physics, etc.) or internally owned. Externally imposed Constraints are fixed for the Project. Internally owned Constraints may be questioned and renegotiated through their named owner. [GP-24]

### 6.9 Verification method assigned at authoring
The verification method for an Obligation must be assigned when the Obligation is authored, not after design is underway. An Obligation without a verification method must not enter a Baseline (§9.1). Verification Procedures must run continuously as the design develops, not only at a late Gate. [GP-25; VFE]

### 6.10 Interface declarations
Every interface between Components must be captured through one fixed lens that contains four elements: description, responsibility and change authority, reference frames with units and tolerances, and a checklist of the interaction categories and environments that apply. An interface is not declared until change authority over it is named. An interface declaration lives in the Dependencies & Interfaces section of the Specifications it connects; an interface that spans several Components lives in one declared interface document, referenced from those Specifications. [GP-26]

### 6.11 The graph is the single source of truth
Relationships between Components form a graph. The Dependencies & Interfaces section of each Component Specification is the source of truth for all links: the Components or interfaces this one requires, the interfaces or Contracts this one provides, and any containment ("part of") relationship. Any grouping imposed by the concrete layout is organizational only and carries no authority; the graph remains the authority. The graph must be acyclic; a dependency cycle is a defect. [COD; GP-55]

### 6.12 Stability rules
Every Component Specification must declare the Stability Class of the Component it defines. The set of Stability Classes and their order must be declared once in the Entry Point (§14.3). A Component may depend only on Components of equal or higher Stability Class. Configuration values and parameters that belong to Components of lower Stability Class must be kept explicit and external, never buried in the design or logic of Components of higher Stability Class. [LSA]

### 6.13 Specification-first Gate
Before any significant change is made to the canonical Realization or System description, a durable, self-contained Contract must exist. It must name the Components and interfaces affected, state what is out of scope, and define the end-to-end Verification Procedures that prove completion. Authoring the Contract and executing the corresponding Production Work Unit must remain separate efforts.

Execution of a Production Work Unit must be gated on a human-approved Plan Document. Until that approval is recorded, Executors may examine the System but must not modify it. The human owner must be able to edit the Plan Document before approval.

When the necessary Contract or design parameters are unknown, an Executor may operate inside an Exploratory Work Unit (§5.7). Exploratory execution must:
- run in an isolated environment with read-only access to the Project Record;
- log all runs, parameter sweeps, and empirical results into the location bound to Records of Exploratory Work Units in the Path Map (§14.8);
- conclude with a structured experimental record that summarizes findings against the research objective.

Artifacts produced during exploratory execution have no governing force and must not be incorporated directly into the canonical Realization or System description. Once the resulting Contract and Verification Procedures receive human approval, validated exploratory assets may be ingested and hardened under a standard Production Work Unit. [GP-17; GP-18; SaC]

### 6.14 Adversarial expansion before acceptance
A Contract must be treated as incomplete by default. Before acceptance, cases intended to expose gaps or weaknesses in the Contract (corner cases, misuse, hostile conditions, etc.) must be deliberately generated, and the Contract must be expanded to cover them. The expanded Contract becomes binding only after human approval. [GP-28]

### 6.15 Co-update of Specification and Realization
A change to a Component must update its Specification and its Realization together, or the change must not be accepted. [GP-27]

### 6.16 Protection of other Contracts
An internal change must not alter the Contract of any other Component. This bounds the Blast Radius of change. [GP-27]

### 6.17 Operational Concept
The top-level System Specification must state the Operational Concept: how the System will be operated and sustained. The Operational Concept sits as an Obligation level between the expectations of the parties the System serves (customers, users, regulators, etc.) and the Component Obligations. [GP-22]

### 6.18 Key Design Parameters
A small set of Key Design Parameters that govern System success must be named, owned, and tracked down to Component level in a dedicated register of the Project Record. A trade-off that moves a Key Design Parameter requires a Decision Record (§11). The tracked Key Design Parameters replace coordination machinery whose only function is routing information or re-approving what a named human owner already owns. The structure must not grow coordination roles or boards whose only purpose is that kind of routing or re-approval. This rule does not displace the controlled change Gate (§9.2) or any review body required by regulation or contract. [GP-29]

### 6.19 Design and planning documents use one skeleton
Every design document, and every document that describes work spanning more than one Work Unit, must use one skeleton: Why (motivation, success criteria, requirements, scope); What/How (method, framing, validation strategy, and the points at which human judgment is required); How (realization, integration, cost and resource commitment, and risks); plus an Alternatives section. The Alternatives section identifies the options rejected and points to the Decision Records that hold their trade-offs and rationale, rather than restating them. [GP-79]

## 7 Verification and Acceptance

### 7.1 Done is a checkable criterion
A Work Unit is done only when a durable, checkable Acceptance Criterion, authored or approved by the human owner, passes. Self-assessment by the Executor never constitutes verification. Verification may be gated at a strength scaled to risk, from an independent check of the result up to a mechanical Gate that blocks completion until the check passes. [GP-31; VFE]

### 7.2 The verification loop
The required loop is:
1. Draft against the stated Acceptance Criteria or Constraints.
2. Verify against them.
3. Identify specific defects (not vague dissatisfaction).
4. Correct only the identified defects.
5. Re-verify.
6. Accept and freeze only when the criteria are satisfied.

If the criteria themselves are incomplete or incorrect, the human must revise them. AI Agents may not alter Acceptance Criteria. [VFE]

### 7.3 Verifiability governs delegation
Acceptance Criteria are meaningful only if their Verification Procedures are resettable (a new attempt can start), cheap (attempts can be repeated), and verdict-yielding (each attempt receives a clear pass/fail outcome). Significant work that is assigned to an Executor must be structured so that its Verification Procedures have these three properties; where they do not, the work structure must change before autonomy is granted. [GP-32]

### 7.4 Verification Procedures are authored before the Work Unit
The Verification Procedures for a Work Unit must be authored before work on that Work Unit begins, and they must fail before the Work Unit is complete. The Work Unit is complete only when its Verification Procedures pass. Those Verification Procedures remain in the verification corpus as a permanent guard against regression. [GP-33; VFE]

### 7.5 Verification Reference State before change
Before any change to an existing System, the current verification state must be established and recorded as the Verification Reference State. Whatever verification exists must be executed, and its outcome (including every pre-existing failure) must be recorded. Where no verification exists, that absence must itself be recorded as the Verification Reference State, and closing the gap must be treated as a Work Unit. Work must never proceed on the assumption that the prior state was verified. [GP-34]

### 7.6 Durable corpus of Verification Procedures
Expected behavior must be encoded as a durable corpus of Verification Procedures. Each Verification Procedure must pair its input with the expected result that determines whether the relevant Acceptance Criteria are satisfied. The corpus is stored with the System description and is owned by the human owner. Verification Procedures that pass must be promoted into the standing corpus rather than discarded. [GP-35]

### 7.7 Layered verification
Verification must be organized in layers that correspond to the decomposition: Component-level Verification Procedures, interface-level Verification Procedures that verify Components honor their declared Contracts, and System-level Verification Procedures. Verification Artifacts at each layer are durable specifications of behavior, not disposable byproducts. [GP-36]

### 7.8 Verification correspondence
Each level of decomposition must have a corresponding level of verification that checks it. The correspondence must be explicit: every decomposition decision must be reachable from the verification that confirms it, and every verification must point back to the decision it confirms. [GP-37]

### 7.9 Governing Verification Plan
Before verification work begins, one governing Verification Plan must fix the scope, responsibilities, resources, and explicit completion criteria of verification, and must distinguish verification (the System is built right) from validation (the right System is built). Verification rigor must scale with the Criticality Class of the Components being verified. [GP-38]

### 7.10 Criticality Classes
Each Component, and each Capability that spans Components, must be assigned a Criticality Class recorded in the Criticality Record. The class must be scored on the consequence of its failure, its complexity, the degree to which humans depend on it, how soon it becomes critical, and the economic exposure it carries. The class determines the Obligations and the verification rigor that apply. The classification and any tailoring of it must be recorded with rationale.

The Criticality Record additionally holds: the rationale for using a lighter or fuller version of a required artifact (§1.6); the artifacts that fall under direct human acceptance (§7.19); and the rationale for any Baseline level recorded as not applicable (§9.1). [GP-39]

### 7.11 Independent verification
The Executor that produces a work product must not verify it. Verification must be performed by an independent Executor or context that has not participated in producing the work. Acceptance of the verified result remains with the human owner. [GP-40; VFE]

### 7.12 Acceptance Criteria must not be weakened
An Executor that disables, deletes, or silently weakens an Acceptance Criterion instead of satisfying it commits a Contract violation. Intermediate outputs must be supervised for any attempt to disable, delete, or weaken Acceptance Criteria, and any change to Acceptance Criteria requires human authorization. [GP-41; SaC]

### 7.13 Every Contract clause is linked to its Verification Procedures
Each clause of a Contract must carry a unique identifier. Each identifier must be linked to one or more Verification Procedures that confirm whether the clause is satisfied. The durable records produced by running those Verification Procedures are Verification Artifacts. The Contract is thereby both the source of Acceptance Criteria and the index of the verification corpus. [GP-42]

### 7.14 Structured outputs for verification
When a System output is hard to verify, the structure of the output must change, not only the Verification Procedures. Outputs must be decomposed into units that can be separately accepted or rejected, must carry provenance, and must be comparable against a trusted reference. Contradictions and open questions must be surfaced, not buried in a monolithic output. [GP-43]

### 7.15 Linked stage Verification Procedures across production
Verification Procedures at successive production stages must be linked into a single chain rather than being isolated per stage. Control limits and Acceptance Criteria at each stage are human-defined. An anomaly must be detected and classified at the stage where it arises, and its Verification Artifact must be linked to the Verification Artifacts of the stages before and after, with correlated measurements kept in one quality record chain. [GP-45]

### 7.16 Model-based verification before costly Realization
Where physical Verification Procedures are expensive, slow, or irreversible, behavior must be verified against a validated model of the System before physical Realization. The model used for verification must itself be verified against reality, and the substitution of a model-based Verification Procedure for a physical Verification Procedure must be human-approved and recorded as a Decision Record (§11). [GP-46]

### 7.17 Reference Realization and drift detection
A Reference Realization is a maintained instance that embodies the current interpretation of a Contract. It may be a second instance of the System or Component, a validated model, a dedicated physical unit built for testing, a reference Subsystem, etc.

The Verification Plan (§7.9) must state which Contracts, if any, are governed by a Reference Realization, with rationale, and must declare the interval at which each comparison is made. A statement that no Contract is so governed, recorded with rationale, satisfies this requirement. The designation must be made before drift is observed.

At each declared interval, the element governed by the Contract must be compared against its Reference Realization. The comparison must examine whether that element still behaves according to the current interpretation of the Contract, and must produce a drift report that records any differences found. A human must filter the drift report before any correction is made. [GP-47]

### 7.18 Durable execution records
Execution must produce durable, inspectable records sufficient for independent diagnosis (what was done, what was measured, what resulted, etc.). Records must persist beyond the activity that produced them. Transient output that exists only while a process is running and is not saved (unsaved terminal output, temporary in-memory logs, unrecorded instrument readings, etc.) is not a Verification Artifact. [GP-48]

### 7.19 Human acceptance by class
Human acceptance is mandatory for high-stability, high Blast Radius, or high-stakes artifacts: core Invariants, major Component Specifications, safety-critical Designs, significant architectural decisions, and anything that defines System-level done, etc. The Project must record which of its artifacts fall under direct human acceptance in the Criticality Record (§7.10), so that the requirement is resolvable at the point of change without judgement. Lower-level work inside already-accepted Contracts and Acceptance Criteria may be accepted by automated Verification Procedures or by AI Agents operating strictly within those already-accepted Contracts and Acceptance Criteria. The depth of verification must match the Blast Radius and stability of the artifact. [VFE; GP-31; GP-27; GP-39]

## 8 Phases and Gates

### 8.1 Artifact-gated Phase sequence
Work must proceed through a fixed sequence of Phases declared for the Project. Each Phase must produce at least one durable artifact that becomes part of the Project Record. A Phase satisfies this requirement by producing a description of the System or a description of its Realization; a Phase whose output is Realization rather than description satisfies it by producing the description of that Realization. Progression to the next Phase requires a Verification Artifact confirming that the durable artifacts produced by the Phase are complete. No Phase may be skipped or merged in a way that removes a durable artifact produced by the Phase or the Verification Artifact that confirms it. The sequence is one pipeline, not a collection of independent activities. [GP-30]

### 8.2 Evidence before, verification after
Each Phase must be preceded by a read-only evidence-gathering activity that establishes the current state of the System and must be followed by a Verification Procedure that confirms the produced artifact is internally consistent and fits with the System. Cross-artifact consistency must be verified before implementation begins. [GP-44]

### 8.3 Event-based Gates
Progression between Phases must be gated by documented entrance criteria, not by calendar dates. Every Gate must carry two distinct documented criteria sets: entrance criteria, which state when the Gate may be held, and success criteria, which state what passing it means. A Gate opens when its entrance criteria are satisfied and closes only with a Decision Record that confirms its success criteria are met and that every open discrepancy is disposed of. A Gate must not be held before its inputs are mature, and must not be delayed once they are ready. [GP-49]

### 8.4 Gate closure is recorded
The closure of a Gate must be recorded in the Project Record as a Decision Record (§11) naming the success criteria met and the disposition of every open discrepancy. A Gate that closed without this record is not closed. [GP-49; GP-60]

### 8.5 Durable human breakpoints
The control flow of long-running work must be explicit and must contain durable breakpoints at which work can be interrupted and resumed. Breakpoints must sit between decision and action, so that human review can occur before consequential action. Breakpoints are first-class structural points, not afterthoughts. [GP-75]

## 9 Baselines and Change Control

### 9.1 Approved Baselines at declared levels
The description of the System, and the description of its Realization, must be frozen as approved Baselines recorded in the Baseline Ledger. What is frozen is always a description held in the Project Record, never the Realization itself.

The Baseline levels in use and the Gate (§8.3) at which each is locked must be declared in the Entry Point (§14.3). The declaration must cover, at minimum, what the System must do (functional) and what each Component must do (allocated). Where the Realization is separately fabricated, configured, or deployed, as-built and as-deployed levels must additionally be declared. Any level that does not apply must be recorded as not applicable, with a short rationale, in the Criticality Record (§7.10).

Each Baseline entry must record:
- the artifacts it governs,
- a snapshot identifier that resolves within the version-controlled Project Record,
- its status, drawn from one fixed vocabulary: draft, locked, superseded, retired, and
- the named human who accepted the lock.

Snapshot identifiers must be derived from the version control system of the Project Record, never maintained by hand (§4.3, §10.1).

A Baseline is locked by human review at its declared Gate, and its closure is recorded as a Decision Record (§8.4). After lock, change is possible only through the controlled change Gate (§9.2). The human named on a locked entry is a record of who accepted that lock; authority over subsequent change belongs to the current named human owner (§15.1). [GP-50]

### 9.2 One controlled change Gate
Change to any locked Baseline (§9.1), or to any artifact it governs, must pass through one controlled change Gate.

Each proposed change must be classified against the set of dimensions declared in the Entry Point (§14.3), which must include, at minimum: its impact on the Baseline, its cost, its safety consequence, and its compatibility with existing Contracts.

Every change must re-issue the affected Baseline entry and must be recorded in the Status Ledger (§9.3). To re-issue an entry is to record a new snapshot identifier against it; the entry retains its locked status and its original Gate-closure Decision Record, and no new Gate is held. An unrecorded change to a locked Baseline is a defect.

Authority to pass the Gate scales with the Blast Radius of the change (§15.3):
- Changes that alter a Contract, an Invariant, an Acceptance Criterion, or an artifact placed under direct human acceptance (§7.19) require human authorization recorded in a Decision Record (§11).
- Changes confined strictly within already-accepted Contracts, Invariants, and Acceptance Criteria require the approval of the named human owner (§15.1) recorded in the Status Ledger, which may be given directly or through human-approved automated Verification Procedures (§7.19).

The Vision Document passes through this Gate and requires a Decision Record in all cases (§3.2).

Exceptions must be recorded as explicit waivers and never absorbed silently. [GP-51; GP-27; GP-39]

### 9.3 One Status Ledger
One Status Ledger must record the status and history of every change, deviation, waiver, and audit outcome.

Each entry recording a change to a locked Baseline must record:
- the affected and re-issued Baseline snapshot,
- the approving named human owner (§15.1),
- the change class, drawn from one fixed vocabulary: Contract, Invariant, Acceptance Criterion, human-acceptance artifact (§7.19), or contained (the change altered none of the preceding),
- whether the change is structural or behavioral (§9.5), and
- the governing Decision Record, which is required for every class except contained (§9.2).

Where approval was given through a human-approved automated Verification Procedure, the entry must additionally name the owner whose standing approval governs it and the procedure that executed it (§9.2). [GP-52]

### 9.4 Explicit Deviation Matrix
Every deviation from this Specification must be explicit, and consolidated into a single auditable Deviation Matrix. Implicit deviation is prohibited. Each deviation must name what is waived, why, and which named human accepted the risk. [GP-53]

### 9.5 Separate structural and behavioral change
Every change must be classified as structural (rearrangement without changed behavior) or behavioral (changed behavior). A single change must never mix the two. The classification must be recorded with the change: in the Status Ledger (§9.3) where the change is to a locked Baseline, and otherwise in the Plan Document governing the Work Unit that makes it (§4.6). The classification keeps every change legible for human review and bounds the review's scope. [GP-54]

### 9.6 Numbered generations
Major redesigns of a Component must be bounded as numbered generations. Each generation must be defined by a step-change in a small declared set of tracked Key Design Parameters (§6.18). Changes within a generation must remain minor and must not redefine the generation's identity. [GP-15]

## 10 Traceability and Lineage

### 10.1 Traceability is structural
Traceability of Obligations must be embedded in the structure of the System description itself, through identifiers, naming, and placement. Any index, matrix, or ledger used for traceability must be derived from those embedded links rather than maintained alongside them. A mapping artifact maintained by hand, which can drift from the structure it describes, is prohibited. [GP-55]

### 10.2 Bidirectional traceability
Traceability must be bidirectional: from any Obligation up to its parent Obligations and down to the Realization elements and Verification Procedures that satisfy it. Verification and validation must be traced separately. Completeness of traceability is itself a checkable property (§16). [GP-56]

### 10.3 Versioned input lineage
Every input artifact that influences a result must be versioned, and the result must reference the exact versions of the inputs used. The conditions that produced any result must be reconstructable from the Project Record alone, and the result must be reproducible wherever the Verification Procedure that produced it is itself repeatable. [GP-57]

### 10.4 The realization system is traced like the System
The realization system (the processes, supply chain, support, etc. that produce and support the Realization) must be described with the same rigor as the System. A change in the System description and a change in the description of the realization system must be traceable against each other in one connected record. [GP-58]

## 11 Decision Records

### 11.1 Format and storage
Binding decisions must be recorded as numbered, immutable Decision Records in the same Project Record as the artifacts they govern, each Decision Record a discrete, separately addressable artifact. Each record must state the context; the options considered, with the trade-offs of each; the decision; its rationale and the trade-offs accepted; its consequences; and its confirmation: how compliance with the decision will be verified. [GP-60]

### 11.2 Fixed status vocabulary
Each Decision Record must carry a status drawn from one fixed vocabulary: proposed, accepted, deprecated, superseded. A reversed decision is never deleted or rewritten; a new record supersedes it with a pointer to the old. [GP-60]

### 11.3 Significance test
Only decisions that pass a declared significance test warrant a Decision Record. The test must be stated in the Entry Point (§14.3). [GP-60]

### 11.4 Consultation and single home
Before any architecture-affecting change, the Executor must consult the relevant Decision Records. Decision Records are the single home for the options considered and the rationale of a binding decision; every other document points to them instead of restating them. [GP-60; GP-79]

## 12 Risk and Failure

### 12.1 Continuous Risk Register
Risk handling must be continuous, not a one-time assessment. One Risk Register must record every identified risk with an owner, an analysis, a mitigation plan, and a tracking method. A risk may be closed in exactly two ways: by mitigation, recorded with the evidence that the exposure is gone; or by acceptance, which requires the documented acceptance rationale of a named human. The two closures must never be recorded as one. Risks must be revisited at Gates (§8.3). [GP-61]

### 12.2 Failure closure by numbered corrective actions
A failure must produce a formal report, at a formality scaled to the Criticality Class of what failed. The report must name the root cause or causes and a numbered list of corrective actions. The failure is closed only when every corrective action is verified and accepted by a human authority; where the failure is safety-significant, that authority must be independent of the Executor whose work produced the failure. Until closure, progression past the failed state is blocked. [GP-62; GP-40]

## 13 Executor Boundaries

### 13.1 Declared Executor scope
The autonomy of each Executor must be bounded by a declared scope: the actions it may take, the data and artifacts it may access, and the boundaries it must not cross. The scope must be declared once as a durable artifact bound in the Path Map (§14.8) and enforced structurally. Freedom inside the boundary is preserved; containment at the boundary is absolute.

Executors assigned to Exploratory Work Units must be further restricted to write access only within designated experimental workspaces. Write access to the canonical Realization or System description must be prohibited. [GP-64]

### 13.2 Boundaries are structural, not prose
Invariants that must not be broken must be encoded as mechanically checkable Constraints, not as prose. Mechanical checks must run continuously, and their failure messages must tell the Executor how to remediate. Prose rules remain for judgment; enforcement belongs to the checks. A boundary that exists only as an instruction is a request, not a boundary. [GP-63; GP-65]

### 13.3 Delegated work stays isolated
Delegated work must run in isolation from the delegating Work Unit's Plan Document. A delegated unit receives a bounded scope and returns a condensed result through a declared interface; the intermediate detail of the delegated work must not enter the delegating context. The delegator retains its Plan Document. The delegate's detail must be recorded in the Project Record under the delegate's own Work Unit (§4.2), not held in Executor context alone. [GP-67]

## 14 Governance Documents and Layout

### 14.1 One governing-principles document
One human-authored Governance Document must state the Project's durable principles, quality bars, and Invariants. It must be bound in the Path Map (§14.8), versioned, and created before detailed work begins. Every later artifact and every Executor, in-house or external, is checked against it. [GP-68]

### 14.2 Governance content discipline
Governance Documents must contain only what an Executor cannot discover from the System itself: hard Invariants, safety and security boundaries, non-obvious Constraints, and non-obvious procedures, etc. Overviews, standard conventions, and restatements of discoverable content are prohibited. Each Governance Document must stay under a declared size ceiling, must reference other artifacts instead of copying their content, must separate concerns into purpose-named documents, and must mark which Specifications describe not-yet-realized work. [GP-69]

### 14.3 One Entry Point into a versioned tree
The Project must expose one short Entry Point document that serves as the root descriptor of the Project Record: a map, not an encyclopedia. The full knowledge base must live in a structured, versioned documentation tree that the Entry Point indexes. Executors start at the Entry Point and are directed to deeper sources as needed. The tree must be checkable for currency, cross-linking, and structure (§16).

Exactly one Entry Point exists per Project. Because the Path Map it carries (§14.8) binds every other Entity, the Entry Point is the one Entity whose own location this Specification fixes: it must be named `INDEX` and reside at the root of the Project Record, with the extension determined by its serialization format. No other Entity location is fixed by this Specification.

The Entry Point must declare all of the following, and nothing else is required of it:
- the Path Map (§14.8): every required Entity bound to its concrete location pattern and serialization format, including the internal layout of the Realization;
- the set of Stability Classes in use and their order (§6.12);
- the significance test for Decision Records (§11.3);
- the Baseline levels in use and the Gate at which each is locked (§9.1);
- the set of dimensions against which a proposed change is classified (§9.2).
[GP-70]

### 14.4 Governance binds to Component boundaries
Governance Documents must bind to Component boundaries: a Component may carry its own Governance Document, and within that Component the nearest document governs. Global governance applies wherever no local document overrides it. Humans must author and control all Governance Documents at every level. [GP-71]

### 14.5 Placement and naming are declared structure
Placement and naming of artifacts are part of the declared structure and carry meaning for every Executor. The location of an artifact must declare its role. The meaning assigned to placement and naming must be declared in the Governance Documents wherever that meaning cannot be derived by inspecting the System. The Path Map (§14.8) must not be restated in a Governance Document. [GP-72]

### 14.6 Documentation lives on the artifact it governs
Documentation must live on the artifact it documents, as close to the governed element as possible. Critical Constraints must be visible at the point where the governed action happens. Documentation that governs one element lives on that element; documentation that spans elements (Specifications, Decision Records, Plan Documents, design documents, etc.) lives in the documentation tree and is reached from the Entry Point. Documentation separated from the artifact it governs drifts and must be treated as suspect. [GP-73]

### 14.7 One Registry; unregistered does not exist
One machine-readable Registry must register every Component and content item of the System with its identity. Each entry's location must be derived from the Project Record, never authored in parallel with it (§4.3, §10.1), and must resolve within the pattern the Path Map (§14.8) binds for that Entity. An item that is not registered does not exist in the System. Adding or removing an item must update its Registry identity in the same change; relocating an item requires no Registry edit, since location is derived. [GP-78]

### 14.8 Required entities and the Path Map
A Project must hold every Entity listed in Appendix A, at the multiplicity stated there. Every Entity except the Realization resides in the Project Record; the Realization resides wherever the Path Map binds it. This Specification defines the Entities, their required content, and their relationships; it does not fix their storage.

Storage is fixed by the Project's Path Map (§2), which must be stated in full in the Entry Point (§14.3). The Path Map must not resolve by reference to any document outside the Project Record (§4.1).

A location pattern is a path, a directory, or a glob pattern that covers every instance of its Entity. A serialization format is any format the Project's tooling can parse: Markdown, YAML, JSON, a domain-native model format, etc.

The Path Map must satisfy the following rules:
- Every required Entity carries exactly one binding rule. That rule may bind more than one pattern where Appendix A states more than one placement for the Entity.
- The binding is deterministic: for any artifact in the Project Record, the Entity it instantiates must be unambiguously resolvable from the Path Map.
- Singleton Entities must resolve to exactly one artifact. Multi-instance Entities must resolve through a pattern that covers every instance.
- An Entity whose multiplicity permits zero instances is bound by a pattern that currently matches nothing; the binding is still required.
- The Path Map must declare the internal layout of the Realization, which this Specification does not prescribe.
- Normative Checks resolve Entity locations through the Path Map alone (§16.1).

The required Entity set is the minimum: a Project may bind additional artifacts and extend its layout, but it must not leave a required Entity unbound except through §1.5. [GP-70; GP-72; GP-78; Goal DR1]

## 15 Roles and Human Authority

### 15.1 Named owner and standing flaw-checker
Every Project and every Component must have one named human owner who answers for its success or failure. In addition, a standing independent flaw-checking function (a second person or an independent Executor pass) must be charged with finding critical flaws and blindspots. The flaw-checker does not own the work and does not dilute the owner's authority. [GP-74]

### 15.2 Non-delegable human authorities
The following authorities are human-owned and non-delegable: problem selection and purpose; Invariants and safety boundaries; Acceptance Criteria and the definition of done; risk acceptance; resource and capital allocation; escalation decisions; and any commitment with external consequences (regulatory, financial, contractual, etc.). AI Agents may draft and propose in all of these areas; they may not enact. [VFE; SaC]

### 15.3 Authority scales with Blast Radius
The authority required to approve a change scales with its Blast Radius and with how hard it is to reverse. The wider the Blast Radius and the less reversible the change, the higher the human authority required. Acceptance of high-stability or high Blast Radius artifacts requires the human owner directly (§7.19). [GP-27; VFE]

## 16 Normative Checks

### 16.1 Encode Invariants as Normative Checks
Every Invariant and structural rule of this Specification that can be checked mechanically must be encoded as a Normative Check and run continuously. Failure messages must tell the Executor how to remediate. Rules that require judgment remain as prose and are enforced by review. [GP-63]

### 16.2 Minimum Normative Check set
The following Normative Checks are mandatory at minimum. A Project may add Normative Checks; it may not remove these except through §1.5.

- Every Component Specification contains the five required sections (§6.2).
- Every Component is registered in the Registry, and every Registry entry resolves to an artifact in the Project Record (§14.7).
- Every Obligation carries an identifier, a named human owner, and a verification method; and every Constraint additionally carries a provenance marking (§6.5 to §6.9).
- The Component dependency graph is acyclic, and every dependency points toward an element of equal or higher Stability Class (§6.11, §6.12).
- Every Acceptance Criterion is linked to at least one Verification Procedure, and every Verification Procedure is linked to a Contract clause (§7.13).
- Traceability is complete in both directions: no Obligation lacks a parent path to the Vision Document or a child path to Realization elements and Verification Procedures (§10.2).
- Every Decision Record carries a valid status, and every supersession pointer resolves (§11.2).
- Every Gate closure has a Decision Record with discrepancy disposition (§8.4).
- The Verification Plan records a Reference Realization designation, with rationale, and a comparison interval for every designated Contract (§7.17).
- Every Baseline level declared in the Entry Point has a corresponding entry in the Baseline Ledger, and every entry carries a status from the fixed vocabulary (§9.1, §14.3).
- Every snapshot identifier in the Baseline Ledger resolves within the Project Record (§9.1).
- Every Baseline whose status is locked has a Gate-closure Decision Record (§8.4, §9.1).
- Every Status Ledger entry recording a change to a locked Baseline names the re-issued Baseline snapshot, an approving named human owner, a change class from the fixed vocabulary, and a structural-or-behavioral classification; and every entry whose class is not "contained" carries a Decision Record reference that resolves (§9.2, §9.3, §9.5).
- The Entry Point is named `INDEX` and resides at the root of the Project Record (§14.3).
- Every required Entity of Appendix A is bound exactly once in the Path Map, every binding resolves to artifacts in the declared format, and the Entity of every artifact in the Project Record is unambiguously resolvable (§14.8).
- Governance Documents are under their size ceiling, and all Entry Point links resolve (§14.2, §14.3).
[GP-20; GP-21; GP-22; GP-23; GP-24; GP-25; GP-42; GP-47; GP-49; GP-50; GP-51; GP-52; GP-54; GP-55; GP-56; GP-60; GP-63; GP-69; GP-70; GP-78; COD; LSA; SaC; VFE]

### 16.3 Normative Check outcomes must be recorded
The outcome of every Normative Check run must be recorded as a durable artifact in the Project Record. A Normative Check whose outcome is not recorded has not run. [GP-48; VFE]

## Appendix A: Required Entity Set
The Entity and Multiplicity columns are normative: §14.8 requires every Entity below, at the multiplicity stated, and §16.2 checks that each is bound in the Path Map. The Clause column is a non-normative index to the clauses that impose each Entity. The binding of each Entity to a concrete location and serialization format is declared by the Project's Path Map (§14.8).

| Entity | Multiplicity | Clause |
| --- | --- | --- |
| Vision Document | one | §3 |
| Governing Principles | one | §14.1 |
| Entry Point | one | §14.3 |
| Registry | one | §14.7 |
| Component Specification | one per Component | §6.1 |
| Top-level System Specification | one | §6.17 |
| Interface declarations | one per interface; those internal to a Component Specification are bound with it, those spanning Components are separately bound | §6.10 |
| Decision Records | one per binding decision | §11 |
| Records of Exploratory Work Units | one per Exploratory Work Unit; none where no Exploratory Work Unit is run | §5.7, §6.13 |
| Work Record | one | §4.5 |
| Plan Documents | one per Work Unit | §4.6, §5.9 |
| Phase artifacts | at least one per Phase | §8.1 |
| Design and planning documents | one per effort spanning more than one Work Unit; none where no such effort exists | §6.19 |
| Verification Plan | one | §7.9 |
| Verification Artifacts (Gate records, drift reports, quality record chain, Verification Reference State records, etc.) | one per verification event; element-local Verification Procedures live on the governed artifact | §7, §8.4, §14.6 |
| Baseline Ledger | one | §9.1 |
| Risk Register | one | §12.1 |
| Status Ledger | one | §9.3 |
| Deviation Matrix | one | §9.4 |
| Key Design Parameter register | one | §6.18 |
| Criticality Record | one | §7.10 |
| Executor scope declarations | one per Executor | §13.1 |
| Reusable task definitions | one per recurring kind of work | §5.10 |
| Realization and its local documentation | one Realization; internal layout declared in the Path Map | §14.8 |

## Appendix B: Traceability of the 79 Adopted Forms
Non-normative mapping. It shows where each Adopted form of [[Generalized Patterns]] is realized in this Specification. Clauses cited by number refer to sections of this document.

The Form column is the join key to [[Generalized Patterns]] and carries the provenance of each form. The Mechanism column states what this Specification requires, in the terminology defined in §2; it does not restate the source form's own wording. Where a source form's vocabulary differs from §2, §2 governs here.

| Form | Mechanism | Realized in |
| --- | --- | --- |
| GP-01 | All governing state as versioned artifacts in the Project Record | §4.1, §4.2, §4.6 |
| GP-02 | Verify-and-record iteration | §4.2, §4.7 |
| GP-03 | One binding Plan Document per Work Unit | §4.6 |
| GP-04 | Work Record | §4.5 |
| GP-05 | Typed dependencies, derived eligibility for execution | §4.5 |
| GP-06 | Documents as sole coordination medium | §4.1 |
| GP-07 | Deliverable-anchored decomposition | §5.1 |
| GP-08 | Purpose-defined Components, named owner, binary verification | §5.2 |
| GP-09 | System-level Contracts first | §5.3 |
| GP-10 | Work Unit sizing | §5.5 |
| GP-11 | The verifiable Work Unit as the unit of decomposition | §5.7 |
| GP-12 | Work Units bounded by Blast Radius | §5.6 |
| GP-13 | Nested levels of intent | §3.1, §3.3, §5.8 |
| GP-14 | Work Units with repair before progression | §5.9 |
| GP-15 | Numbered generations | §9.6 |
| GP-16 | Four recursive process groups | §1.2, §1.4 |
| GP-17 | Specification-first Contract before execution | §6.13 |
| GP-18 | Execution gated on an approved Plan Document | §6.13 |
| GP-19 | Specification as durable alignment artifact | §6.4 |
| GP-20 | Unique verifiable Obligation statements | §6.5, §16.2 |
| GP-21 | Fixed structure for Obligation statements | §6.5, §16.2 |
| GP-22 | Obligation hierarchy with fixed attributes | §6.6, §6.17, §16.2 |
| GP-23 | Named owner for every Obligation | §6.7, §16.2 |
| GP-24 | Constraint provenance marking | §6.8, §16.2 |
| GP-25 | Verification method at authoring | §6.9, §16.2 |
| GP-26 | One fixed lens for every interface | §6.10 |
| GP-27 | Public Contract, private Design, co-update, Contract protection | §6.3, §6.15, §6.16, §7.19, §9.2, §15.3 |
| GP-28 | Adversarial expansion of the Contract | §6.14 |
| GP-29 | Named Key Design Parameters | §6.18 |
| GP-30 | Artifact-gated Phase sequence | §8.1 |
| GP-31 | Done is a checkable criterion | §7.1, §7.19 |
| GP-32 | Verifiability governs delegation | §7.3 |
| GP-33 | Verification Procedures authored before the Work Unit | §7.4 |
| GP-34 | Verification Reference State before change | §7.5 |
| GP-35 | Durable corpus of Verification Procedures | §7.6 |
| GP-36 | Layered verification | §7.7 |
| GP-37 | Verification correspondence | §7.8 |
| GP-38 | Governing Verification Plan | §7.9 |
| GP-39 | Recorded Criticality Class determines rigor | §1.6, §6.6, §7.10, §7.19, §9.2 |
| GP-40 | Producing Executor and verifying Executor are independent | §7.11, §12.2 |
| GP-41 | Acceptance Criteria must not be weakened | §7.12 |
| GP-42 | Contract clause linked to its Verification Procedures | §7.13, §16.2 |
| GP-43 | Structured outputs for verification | §7.14 |
| GP-44 | Evidence before, verification after | §8.2 |
| GP-45 | Linked stage Verification Procedures | §7.15 |
| GP-46 | Model-based verification | §7.16 |
| GP-47 | Reference Realization, drift detection | §7.17, §16.2 |
| GP-48 | Durable execution records | §7.18, §16.3 |
| GP-49 | Event-based Gates | §8.3, §8.4, §16.2 |
| GP-50 | Approved Baselines | §3.2, §9.1, §16.2 |
| GP-51 | One controlled change Gate | §3.2, §9.2, §16.2 |
| GP-52 | One Status Ledger | §9.3, §16.2 |
| GP-53 | Explicit Deviation Matrix | §1.5, §9.4 |
| GP-54 | Separate structural and behavioral change | §9.5, §16.2 |
| GP-55 | Traceability as structural property | §6.11, §10.1, §16.2 |
| GP-56 | Bidirectional traceability | §10.2, §16.2 |
| GP-57 | Versioned input lineage | §10.3 |
| GP-58 | Realization system traced like the System | §10.4 |
| GP-59 | One canonical source of truth per concern | §4.3 |
| GP-60 | Numbered immutable Decision Records | §8.4, §11.1, §11.2, §11.3, §11.4, §16.2 |
| GP-61 | Continuous Risk Register | §12.1 |
| GP-62 | Failure closure by numbered corrective actions | §12.2 |
| GP-63 | Invariants as mechanically checkable Constraints | §13.2, §16.1, §16.2 |
| GP-64 | Declared Executor scope | §13.1 |
| GP-65 | Disposable Executors, durable work | §4.2, §4.8, §13.2 |
| GP-66 | Governance Documents as controlled artifacts | §4.9 |
| GP-67 | Isolated delegation behind a summary interface | §13.3 |
| GP-68 | One Governing-Principles Document | §3.1, §14.1 |
| GP-69 | Governance content discipline | §14.2, §16.2 |
| GP-70 | Short Entry Point into versioned tree | §14.3, §14.8, §16.2 |
| GP-71 | Governance bound to Component boundaries | §14.4 |
| GP-72 | Placement and naming are declared structure | §14.5, §14.8 |
| GP-73 | Documentation lives on the artifact | §14.6 |
| GP-74 | Named owner plus standing flaw-checker | §15.1 |
| GP-75 | Durable human breakpoints | §8.5 |
| GP-76 | Human-owned Contract, machine-readable surfaces | §4.4 |
| GP-77 | Reusable task definitions | §5.10 |
| GP-78 | One Registry; unregistered does not exist | §14.7, §14.8, §16.2 |
| GP-79 | Why-What-How skeleton | §6.19, §11.4 |

Frozen-principle coverage:

- **Component-Oriented Decomposition (COD)**: §5.1, §5.2, §5.3, §6.1, §6.2, §6.11, §16.2.
- **Layered System Architecture (LSA)**: §1.7, §1.8, §3.1, §3.2, §6.12, §16.2.
- **Integrated Modularity First (IMF)**: §5.4.
- **Verification-First Engineering (VFE)**: §1.3, §1.6, §4.7, §5.7, §5.9, §6.2, §6.9, §7.1, §7.2, §7.4, §7.11, §7.19, §15.2, §15.3, §16.2, §16.3.
- **Specifications as Contracts (SaC)**: §1.1, §1.3, §1.5, §1.7, §6.1, §6.2, §6.4, §6.13, §7.12, §15.2, §16.2.

Meta-clauses §1.1 to §1.3 additionally derive from Goal §2 and Goal §5 to Goal §6, which define the framework's premises, objective, and contents.
