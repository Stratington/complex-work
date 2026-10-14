# Governing Principles for Complex Engineering Projects

Author: Franz Bruckhoff, Stratington Systems

## Component-Oriented Decomposition

AI Agents working on complex long-horizon projects require stable, bounded units of work with explicit Contracts. They get that through Hierarchical Component Specifications, and not through flat lists of features or a monolithic requirements document.

This holds for software Systems, physical megastructures such as floating cities, energy Systems, transportation networks, or any other engineered System of high complexity.

Large Systems that stay coherent over time are decomposed into pieces with clear responsibilities, interfaces, and ownership boundaries. Those pieces are Components, such as modules, services, Subsystems, libraries, AI Agents, and layers. Without that decomposition the System becomes a monolith that no human team and no set of AI Agents can reason about, divide into parallel work, or change without constant global coordination.

It's therefore essential to prefer Components that can be replaced, upgraded, or removed with limited disruption to the rest of the System. Clean interfaces and explicit Contracts make this practical. Both humans and AI Agents benefit when a Component can be swapped without forcing redesign of high-stability elements.

Feature-centric thinking works only while the System is still small and mostly user-facing. Once the majority of the work is internal infrastructure, coordination logic, reliability mechanisms, or performance-critical paths, "features" become a forced and misleading frame. In software Systems that have end users, there are obviously user-facing Capabilities. In a floating city there are residential modules, power generation, desalination, docking systems, emergency response, governance interfaces, and so on. Some of those Capabilities are commonly called "features".

But the word "feature" has certain implications as a unit of work and specification:
- It carries the assumption that the primary consumer is an end user and that the right framing is a user story.
- Thinking in terms of "features" works cleanly only while the System is still small and mostly surface-level.
- Once the majority of the effort is internal (coordination, reliability, interfaces between Subsystems, performance under load, safety Constraints, long-term maintainability, etc), forcing everything into "features" becomes artificial and misleading.

A floating city’s power distribution network, structural integrity monitoring, or waste-processing loops are not usefully described as features with user stories. They are Components with required behaviors, interfaces, Constraints, and Acceptance Criteria. The same is true for the majority of the work inside any ambitious software System after the first few user-visible slices.

So how do we go about features then?
- A user-facing Capability is either its own Component or a required behavior of a larger Component.
- When it's truly end-user facing, you may include one or a few short "user story" statements inside the Rationale section of the Component's Specification, which helps explain why the Component exists from the user's perspective.

In some rare edge cases like pure dataflow Systems the primary mental model starts with flows or roles rather than static Components. But even then those Systems end up being implemented as Components with defined interfaces.

There are some scenarios where the Component lens becomes secondary and impractical:
- If you work on pure open-ended scientific exploration with no engineering deliverable or target artifact.
- Certain forms of pure mathematical or theoretical work producing a single unified proof or insight rather than a constructed System.
- Small-scale artistic or expressive works where modularity would actively harm the intended holistic quality.
- Extremely short-lived, single-person prototypes where the overhead of formal decomposition exceeds any benefit (you already know that those days are counted).

But even in those scenarios, some form of decomposition emerges once the work grows beyond a certain size.

Therefore it is correct to treat Component-oriented decomposition as the default mental model.


## Layered System Architecture

AI Agents working on complex long-horizon projects need a stable source of truth. They operate by reading Specifications, code, and Designs, then proposing or making changes. When essential purpose and critical Constraints are entangled with volatile implementation details, AI Agents must continually re-infer what must remain true. This increases inconsistency and error.

Stable, high-value parts of the System must not depend on volatile implementation details.

The essential purpose, Invariants (conditions or properties that must always remain true for the System, regardless of its state), and critical behaviors are treated as high-stability elements. These define what the System is and what it must guarantee.

The particular ways those guarantees are achieved (choice of technologies, materials, vendors, control systems, construction methods, interfaces, delivery mechanisms, configuration values, operating parameters, etc.) are treated as lower-stability elements.

Configuration values and parameters that belong to lower-stability elements should be kept explicit and external rather than buried inside high-stability design or logic.

Dependencies must flow from lower-stability elements toward higher-stability elements. High-stability elements must never depend on lower-stability elements.

Consequences:
- AI Agents and humans can reason about, verify, and evolve the essential purpose and Invariants without being entangled in particular implementation choices.
- Changes to materials, vendors, software frameworks, sensors, or construction techniques do not force redesign of what the System must guarantee.
- The Blast Radius of AI Agent actions is limited: AI Agents may freely modify lower-stability elements without silently breaking the high-stability core.
- High-stability elements can carry strong, relatively unchanging Acceptance Criteria that AI Agents or verification processes can check independently of current Realization details.
- Multiple AI Agents can work on different lower-stability parts in parallel while sharing a common, stable Contract.
- Over long-horizon projects, the core remains authoritative even as implementation technologies and methods are replaced repeatedly.

This principle applies equally to software Systems and to physical Systems like floating cities.

In software, high-stability elements include core domain rules, business Invariants, and critical System behaviors. Lower-stability elements include particular databases, web frameworks, UI libraries, cloud providers, or third-party services.

In a floating city, high-stability elements include structural integrity under marine conditions, life-support balance, safety Invariants, and long-term habitability. Lower-stability elements include specific hull materials, power-generation hardware, sensor models, or construction sequences.


## Integrated Modularity First

For complex, long-horizon Systems, prefer a coherent design with strong internal Component boundaries over early hard separation.

A coherent design means the System has a clear overall purpose and fits together logically. Its parts work toward the same goals without conflicting or creating unnecessary complexity.

Establish clear Components and interfaces from the beginning. Keep the System as integrated as practical so that humans and AI Agents can reason about it, verify it, and evolve it with manageable coordination cost. Introduce hard separation only when the benefits clearly outweigh the added coordination and interface costs. Hard separation includes independent ownership, strong operational or physical isolation, independent fabrication, or independent evolution.

Valid reasons for hard separation include:
- Different parts must evolve, be fabricated, or be operated at significantly different rates or under different constraints
- Failure isolation is required so that problems in one part cannot cascade
- Regulatory, safety, security, or ownership boundaries demand isolation
- Geographic, environmental, or latency constraints force physical separation

Premature hard separation increases interface complexity, coordination overhead, and verification difficulty. Start with strong modularity inside a coherent System. Separate only when the need is concrete and the trade-offs are understood.

In software, this means starting with a modular monolith (one coherent codebase with clear internal Components) rather than jumping early to microservices. Split into separate services only when independent scaling, deployment, or failure isolation becomes a real requirement.

For a floating city, this means designing the overall structure, power, life support, and modules as an integrated System with clear interfaces, rather than treating every major Subsystem as fully independent from the start. Some strong physical separations (such as watertight compartments and fire zones) are required early for safety. Beyond those necessary isolations, introduce further hard separation only when safety, environmental, or functional constraints demand it.


## Verification-First Engineering

No unit of work is done until it has been verified against explicit Acceptance Criteria and corrected until those criteria are met. Every meaningful artifact must have checkable criteria before it is accepted.

The required loop is:

1. Draft against a stated set of Acceptance Criteria or Constraints.
2. Verify the draft against those criteria.
3. Identify specific defects (not vague dissatisfaction).
4. Correct only the identified defects. If the criteria themselves are incomplete or incorrect, the human must revise them; AI Agents may not alter Acceptance Criteria.
5. Re-verify. Accept and freeze the result only when the criteria are satisfied.

Human acceptance is mandatory for high-stability, high-blast-radius, or high-stakes artifacts (core Invariants, major Component Specifications, safety-critical Designs, significant architectural decisions, and anything that defines System-level "done"). Lower-level work that sits inside already-accepted Contracts and criteria may be accepted by automated checks or by AI Agents operating strictly within those pre-approved bounds. The depth of verification must match the Blast Radius and stability of the artifact.

AI Agents may generate verification evidence and perform checks. They may not change the Acceptance Criteria.

Consequences:
- Drift and silent quality loss are reduced because every change is checked against a fixed reference.
- AI Agents receive clear, local signals about what is wrong instead of global or ambiguous feedback.
- Rework stays bounded; corrections target concrete failures rather than restarting from scratch.
- Long-horizon coherence is protected because accepted artifacts remain stable until a new, justified change is required.
- Human attention stays on the decisions that only a human may make.

The principle is domain-general. In software it governs code, tests, and specifications. In a floating city it governs design documents, calculations, safety cases, and fabrication specifications. The form of the evidence differs between domains, but in every domain work is incomplete until it is verified.

An artifact that has not passed this loop is not done.


## Specifications as Contracts

Specifications that define required behaviors, interfaces, or Acceptance Criteria are Contracts, not suggestions.

These Contracts state what must be true and what "done" means. Humans and AI Agents implement against them. They do not reinterpret, expand, or weaken them without explicit human authority.

Changing a Contract requires human decision. AI Agents may propose revisions; they may not enact them. Once accepted, a Contract remains the authoritative reference until the human revises it.

Consequences:
- Work has a fixed target instead of open-ended interpretation.
- Implementation drift is constrained.
- Verification has a stable reference.
- Humans keep control of purpose, scope, and the definition of "done".

This applies to any engineered System. The documents may be Component Specifications, interface definitions, design specifications, or safety requirements. In each case, the document is a Contract.

A Specification treated as optional guidance is not a Contract and does not satisfy this principle.


## Normative Structural Specification

The Normative Structural Specification is written in full in [[Normative Structural Specification]]. That file is the authoritative structural document of the Framework for Keeping Complex Work Coherent Across Time.

The Specification defines the required project artifacts (VISION, Governing Principles, the Component Specification Graph, Interface Declarations, Decision Records, Verification Artifacts, Baselines, Registers, and the Work Record) together with their layout, their content rules, and the deterministic checks that enforce them. It operationalizes the five principles above: every clause is traceable to one or more of the 79 Adopted structural forms in research/project-structure-patterns/Generalized Patterns.md or to a frozen principle.

In any conflict over project structure, the Normative Structural Specification governs.
