import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from scipy.integrate import solve_ivp

# ── Shared style ──────────────────────────────────────────────────────────────
plt.rcParams.update({
    'font.family': 'serif',
    'font.size': 10,
    'axes.labelsize': 10,
    'axes.titlesize': 10,
    'legend.fontsize': 9,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'axes.linewidth': 0.8,
    'lines.linewidth': 1.5,
    'figure.dpi': 150,
})
COLORS = ['#1b6ca8', '#c0392b', '#27ae60', '#8e44ad']

# ── Parameters ────────────────────────────────────────────────────────────────
Cm   = 8.0      # W yr m^-2 K^-1  (mixed-layer heat capacity)
Cd   = 100.0    # W yr m^-2 K^-1  (deep-ocean heat capacity)
lam  = 1.13     # W m^-2 K^-1     (climate feedback)
kap  = 0.73     # W m^-2 K^-1     (ocean heat exchange)
F2x  = 3.71     # W m^-2          (CO2 doubling forcing)
C0   = 280.0    # ppm              (pre-industrial CO2)
N0   = 270.0    # ppb              (pre-industrial N2O)
tau_N = 116.0   # yr               (N2O lifetime)
kN   = 0.0031   # W m^-2 ppb^-1   (N2O forcing coefficient)
alpha = 0.45    # airborne fraction
beta_fert = 0.0015  # CO2 fertilisation gain (ppm^-1)
gamma_T   = 0.04    # temperature sensitivity of land sink (K^-1)
S0_land   = 2.5    # PgC yr^-1  (baseline land sink)
S0_ocean  = 2.2    # PgC yr^-1  (baseline ocean sink)
ppm_per_PgC = 0.4706

# ── Emission trajectories ─────────────────────────────────────────────────────
def emissions(t, scenario):
    """Anthropogenic CO2 emissions [PgC/yr]."""
    E0 = 10.0  # current emissions
    if scenario == 'baseline':
        peak = 2040; rate = 0.025
        return E0 * np.exp(-rate * np.maximum(t - peak, 0))
    elif scenario == 'rapid_infra':
        return E0 * (1 + 0.01 * np.minimum(t, 60)) * np.exp(-0.015 * np.maximum(t - 60, 0))
    elif scenario == 'restoration':
        return E0 * np.exp(-0.04 * t)
    elif scenario == 'high_n2o':
        return E0 * np.exp(-0.025 * np.maximum(t - 40, 0))
    return E0

def n2o_emissions(t, scenario):
    """Anthropogenic N2O emissions [Tg N/yr] → ppb/yr conversion included."""
    base = 8.0  # Tg N/yr  → ~1 ppb/yr after stratospheric loss
    if scenario == 'high_n2o':
        return base * (1 + 0.015 * t)
    return base

def infra_fraction(t, scenario):
    """Fraction of land converted to built surface (0–1)."""
    if scenario == 'rapid_infra':
        return np.minimum(0.05 + 0.003 * t, 0.35)
    elif scenario == 'restoration':
        return np.maximum(0.12 - 0.001 * t, 0.03)
    else:
        return np.minimum(0.08 + 0.001 * t, 0.18)

def F_built(t, scenario):
    """Radiative forcing from built surfaces [W m^-2]."""
    return 0.15 * infra_fraction(t, scenario)

# ── ODE system ────────────────────────────────────────────────────────────────
def system(t, y, scenario):
    Tm, Td, C, N = y
    C = max(C, C0)
    N = max(N, N0)

    # Radiative forcing
    Fco2  = F2x * np.log(C / C0) / np.log(2)
    FN2O  = kN * (N - N0)
    Fb    = F_built(t, scenario)
    F_tot = Fco2 + FN2O + Fb

    # Climate
    dTm = (F_tot - lam * Tm - kap * (Tm - Td)) / Cm
    dTd = kap * (Tm - Td) / Cd

    # Carbon cycle
    phi   = 1.0 - infra_fraction(t, scenario)   # productive land fraction
    S_land  = phi * S0_land * (1 + beta_fert * (C - C0)) * np.exp(-gamma_T * max(Tm, 0))
    S_ocean = S0_ocean * (1 - 0.01 * max(Tm, 0))
    E       = emissions(t, scenario) / ppm_per_PgC  # PgC/yr → ppm/yr
    dC = alpha * E - S_land * ppm_per_PgC - S_ocean * ppm_per_PgC

    # N2O
    EN  = n2o_emissions(t, scenario) * 0.12   # rough ppb/yr
    dN  = EN - N / tau_N

    return [dTm, dTd, dC, dN]

# ── Solve all scenarios ───────────────────────────────────────────────────────
t_span = (0, 200)
t_eval = np.linspace(0, 200, 2001)
y0 = [0.0, 0.0, 280.0, 270.0]   # anomalies for T; absolute for C, N
scenarios = {
    'Baseline':          'baseline',
    'Rapid Infrastructure': 'rapid_infra',
    'Ecological Restoration': 'restoration',
    'Elevated N₂O':     'high_n2o',
}
sols = {}
for label, key in scenarios.items():
    sol = solve_ivp(system, t_span, y0, args=(key,),
                    t_eval=t_eval, method='RK45', rtol=1e-8, atol=1e-10)
    sols[label] = sol

years = t_eval + 2025   # calendar years

# ══════════════════════════════════════════════════════════════════════════════
# FIGURE 1 – Temperature & forcing scenarios (2 × 2)
# ══════════════════════════════════════════════════════════════════════════════
fig1, axes = plt.subplots(2, 2, figsize=(7.5, 5.5), constrained_layout=True)
((ax_T, ax_F), (ax_C, ax_N)) = axes

for i, (label, sol) in enumerate(sols.items()):
    Tm  = sol.y[0]
    C   = sol.y[2]
    N   = sol.y[3]
    t_  = sol.t

    Fco2 = F2x * np.log(np.maximum(C, C0+0.01) / C0) / np.log(2)
    FN2O = kN * (N - N0)
    Fb   = np.array([F_built(tt, list(scenarios.values())[i]) for tt in t_])
    Ftot = Fco2 + FN2O + Fb

    ax_T.plot(years, Tm,   color=COLORS[i], label=label)
    ax_F.plot(years, Ftot, color=COLORS[i], label=label)
    ax_C.plot(years, C,    color=COLORS[i], label=label)
    ax_N.plot(years, N,    color=COLORS[i], label=label)

for ax, ylabel, title in [
    (ax_T, r'$\Delta T_m$ (K)',      'Mixed-layer temperature anomaly'),
    (ax_F, r'$F_\mathrm{total}$ (W m$^{-2}$)', 'Total radiative forcing'),
    (ax_C, 'CO$_2$ (ppm)',           'Atmospheric CO$_2$'),
    (ax_N, 'N$_2$O (ppb)',           'Atmospheric N$_2$O'),
]:
    ax.set_xlabel('Year')
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.set_xlim(2025, 2225)
    ax.grid(True, linewidth=0.4, alpha=0.5)

ax_T.legend(fontsize=8, loc='upper left', framealpha=0.8)
fig1.savefig('/home/claude/paper/temperature_scenarios.pdf', bbox_inches='tight')
plt.close(fig1)
print("Figure 1 saved.")

# ══════════════════════════════════════════════════════════════════════════════
# FIGURE 2 – Carbon feedbacks (land sink suppression by infrastructure)
# ══════════════════════════════════════════════════════════════════════════════
fig2, axes2 = plt.subplots(1, 3, figsize=(7.5, 3.2), constrained_layout=True)
ax_phi, ax_sink, ax_cum = axes2

for i, (label, key) in enumerate(scenarios.items()):
    sol  = sols[label]
    t_   = sol.t
    C    = sol.y[2]
    Tm   = sol.y[0]

    phi      = 1.0 - np.array([infra_fraction(tt, key) for tt in t_])
    S_land   = phi * S0_land * (1 + beta_fert * np.maximum(C - C0, 0)) \
               * np.exp(-gamma_T * np.maximum(Tm, 0))
    S_ocean  = S0_ocean * (1 - 0.01 * np.maximum(Tm, 0))

    from scipy.integrate import cumulative_trapezoid
    cum_land  = cumulative_trapezoid(S_land,  t_, initial=0)
    cum_ocean = cumulative_trapezoid(S_ocean, t_, initial=0)

    ax_phi.plot(years,  phi,     color=COLORS[i], label=label)
    ax_sink.plot(years, S_land,  color=COLORS[i], label=label)
    ax_cum.plot(years,  cum_land + cum_ocean, color=COLORS[i], label=label)

for ax, ylabel, title in [
    (ax_phi,  'Productive land fraction $\phi$', 'Available biotic land'),
    (ax_sink, 'Land sink (PgC yr$^{-1}$)',        'Terrestrial C uptake'),
    (ax_cum,  'Cumulative sink (PgC)',             'Cumulative biosphere + ocean'),
]:
    ax.set_xlabel('Year')
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.set_xlim(2025, 2225)
    ax.grid(True, linewidth=0.4, alpha=0.5)

ax_phi.legend(fontsize=7.5, loc='lower left', framealpha=0.8)
fig2.savefig('/home/claude/paper/carbon_feedbacks.pdf', bbox_inches='tight')
plt.close(fig2)
print("Figure 2 saved.")

# ══════════════════════════════════════════════════════════════════════════════
# FIGURE 3 – Sensitivity: lambda vs kappa phase portrait + ECS curve
# ══════════════════════════════════════════════════════════════════════════════
fig3, (ax_p, ax_ecs) = plt.subplots(1, 2, figsize=(7.5, 3.5), constrained_layout=True)

# ECS as a function of lambda
lam_vals = np.linspace(0.6, 2.5, 300)
ECS      = F2x / lam_vals
ax_ecs.plot(lam_vals, ECS, color=COLORS[0], linewidth=2)
ax_ecs.axvline(lam, color='k', linestyle='--', linewidth=0.9, label=r'Default $\lambda$')
ax_ecs.axhline(F2x / lam, color=COLORS[2], linestyle=':', linewidth=0.9, label=fr'ECS = {F2x/lam:.2f} K')
ax_ecs.set_xlabel(r'Feedback parameter $\lambda$ (W m$^{-2}$ K$^{-1}$)')
ax_ecs.set_ylabel('Equilibrium climate sensitivity (K)')
ax_ecs.set_title('ECS vs. Climate Feedback Parameter')
ax_ecs.legend(fontsize=8)
ax_ecs.grid(True, linewidth=0.4, alpha=0.5)

# Phase portrait: Tm vs Td for baseline scenario
sol_b = sols['Baseline']
Tm_b  = sol_b.y[0]
Td_b  = sol_b.y[1]
sc = ax_p.scatter(Tm_b[::10], Td_b[::10],
                  c=years[::10], cmap='plasma',
                  s=8, zorder=3)
cb = fig3.colorbar(sc, ax=ax_p, label='Year', pad=0.02)
ax_p.set_xlabel(r'$T_m$ (K)')
ax_p.set_ylabel(r'$T_d$ (K)')
ax_p.set_title(r'Phase portrait: $T_m$ vs $T_d$ (Baseline)')
ax_p.plot([0, Tm_b[-1]], [0, Tm_b[-1]], 'k--', linewidth=0.7, alpha=0.5, label=r'$T_m = T_d$')
ax_p.legend(fontsize=8)
ax_p.grid(True, linewidth=0.4, alpha=0.5)

fig3.savefig('/home/claude/paper/sensitivity_analysis.pdf', bbox_inches='tight')
plt.close(fig3)
print("Figure 3 saved.")

print("All figures generated successfully.")
