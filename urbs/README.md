# URBS — City Policy Field Simulator

URBS is a lattice-based urban dynamics simulator that models a city as a coupled field system rather than a collection of independent variables. Each district evolves through interacting scalar, vector, and entropy-like quantities, producing emergent patterns such as stable urban cores, peripheral decay, migration flows, and systemic collapse.

The simulator is designed both as an interactive policy sandbox and as a minimal computational realization of a scalar–vector–entropy framework applied to socio-economic systems.

---

Conceptual Model

URBS treats the city as a discretized field over a 2D grid. Each cell represents a district with evolving state variables, but these variables are not independent. Instead, they are projections of three underlying fields:

- Φ (Structural Potential)
  Represents the capacity and coherence of a district. High Φ corresponds to strong infrastructure, housing, health systems, and environmental quality.

- v (Flow Field)
  Governs movement of population and economic activity. Flow emerges from gradients in structural potential and collapse pressure.

- S (Entropy / Collapse Pressure)
  Measures systemic failure, instability, and degradation. High S corresponds to breakdown of services and cascading decline.

All visible quantities (population, wealth, housing, etc.) are derived from or coupled through these fields.

---

Core Dynamics

The system evolves through three interacting processes:

Structural Evolution

Structural potential grows through policy investment and decays under collapse pressure. Diffusion smooths spatial inequalities while local reinforcement creates stable urban cores.

Entropy (Collapse)

Collapse emerges when structural support falls below viability thresholds. It spreads spatially and is reduced by strong service networks. Collapse is not an arbitrary penalty but a derived instability field.

Flow (Migration & Capital Movement)

Population and economic activity move along gradients of:

Φ − S

This produces:

- inward migration toward stable cores
- outward flight from collapsing districts
- persistent spatial structure

---

Features

URBS produces a range of emergent behaviors without scripted events:

- formation of dense urban cores
- suburban and peripheral decay
- inequality-driven instability
- cascading infrastructure failure
- recovery through coordinated policy
- metastable equilibria rather than fixed outcomes

The system is intentionally nonlinear, with threshold effects and feedback loops.

---

Policy System

The user controls global policy levers:

- Housing
- Environmental Regulation
- Healthcare
- Infrastructure
- Redistribution
- Security

These do not directly set outcomes. Instead, they bias the evolution of Φ and indirectly influence S and flow dynamics. Overextension creates diminishing returns rather than immediate collapse.

---

Simulation Structure

Each timestep performs:

1. Field evaluation (Φ, S)
2. Local updates (growth, decay, policy effects)
3. Population evolution (growth + flow)
4. Collapse diffusion
5. Rendering and metric aggregation

The system is fully deterministic aside from initial noise and optional stochastic migration.

---

Interpretation

URBS can be understood as a minimal model of:

- urban economics
- infrastructure resilience
- socio-political policy effects
- spatial inequality
- entropy-driven system failure

More abstractly, it represents a general class of systems where:

- structure (Φ) competes with entropy (S)
- flows (v) reorganize the system toward local optima
- stability emerges from feedback, not equilibrium assumptions

---

Why This Model

Traditional city simulators often rely on discrete rules and scripted interactions. URBS instead uses continuous field interactions, allowing:

- smoother transitions
- emergent macrostructure
- fewer arbitrary rules
- easier theoretical analysis

This makes it suitable both for experimentation and as a conceptual bridge between simulation and formal field theory.

---

Running the Simulator

URBS is a single HTML file.

To run:

1. Clone the repository
2. Open "index.html" in a browser

No dependencies or build steps are required.

---

Controls

- Run / Pause — start or stop the simulation
- Step — advance one timestep
- Reset — regenerate the city
- Scenario — load predefined policy configurations
- Policy Sliders — adjust global investment levels
- View Tabs — inspect different field layers
- Grid Click — inspect individual districts

---

Metrics

The simulator tracks:

- total population
- average wellbeing
- inequality (Gini coefficient)
- environmental health
- collapse pressure

These are aggregated from the underlying field state.

---

Future Directions

The current system can be extended in several directions:

- continuous PDE formulation (removing grid artifacts)
- vector field visualization (explicit flow arrows)
- multi-scale regions (city → metro → nation)
- endogenous policy adaptation
- stochastic shocks and external forcing
- integration with formal scalar–vector–entropy frameworks

---

Citation

If referencing the conceptual model:

@phdthesis{Denham2025-DENSCI-2,
  author = {Sam Denham},
  school = {Hard Knock},
  title = {Semantic Collapse in Embedding Space: Neighborhood Semantics and Entropic Drift},
  year = {2025}
}

---

Closing Note

URBS is not a predictive model of real cities. It is a structural experiment: a way of exploring how constraint, flow, and entropy interact to produce organized or collapsing systems.

The goal is not realism, but insight into how complex systems maintain coherence—or fail to.
