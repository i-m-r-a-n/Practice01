# Bengal Earth Lab — honest Sun Flow dashboard display specification

**Version 1.0, 30 October 2026.** Intended for concept-only buyer display F05 and future separately approved live system. This document defines **interface and data requirements**, not site telemetry, code deployment or a completed dashboard. Current state: **NO LIVE METERS, NO APPROVED PV PLAN, NO VERIFIED ELECTRICITY CLAIMS.** Claude owns the 3D Worker and visual integration.

## What a visitor sees *now*

A simple Bengali-inspired visual sequence: **Sun → Potential PV Array → [Direct use / Storage] → Operations**, plus **Grid** and **Backup** branches. All connectors are **neutral schematic lines**: no moving arrows suggesting actual energy flows. Text directly beside the graphic, not hidden in a tooltip:

> **Concept demonstration — not live factory data**
>
> Designed for a Solar-Powered Future.
>
> Solar plant capacity, current generation, storage and grid contribution: **Unavailable / not verified**.

No fake live wattage, percentages, charts, animations that represent live operation, made-up CO2 savings, installed equipment logos, or “100% solar” badges. Allow a link to the evidence method, not to an imaginary certification. F05 must not obstruct the existing Z03 visitor passage or equipment; fixing and visitor accessibility require physical review.

## Future live mode — approval gate

Enable `mode=live` **only** after the owner confirms a real system, independent engineer signs off metering topology and equipment, telemetry access is authorised, data quality is validated, claims are approved under [C01–C12](08_energy_claim_matrix.md), and privacy/security access rules are established. Before that, only `mode=concept` exists. Do **not** auto-switch to live because any one API responded.

### Minimum telemetry schema (conceptual)

Each non-null observation is linked to:

```json
{
  "recorded_at_utc": "ISO-8601 UTC string, actual value required",
  "period_start_utc": "ISO-8601 UTC string",
  "period_end_utc": "ISO-8601 UTC string",
  "boundary_id": "approved-floor-or-site-scope",
  "meter_id": "real meter mapping identifier",
  "channel": "pv_ac_kwh|load_ac_kwh|grid_import_kwh|grid_export_kwh|battery_charge_ac_kwh|battery_discharge_ac_kwh|backup_ac_kwh|battery_soc_pct",
  "value": "number only from authorised calibrated source; null means unavailable",
  "unit": "kWh|percent",
  "source_class": "metered|modelled|manual-verified",
  "quality": "valid|stale|missing|estimated|error",
  "calibration_reference": "document or status reference",
  "data_provenance_id": "immutable collection/source reference"
}
```

This is a **schema illustration**, not actual JSON data. Additional fields: interval kW where measured, sample counter rollover policy, utility meter import/export direction, commissioning IDs, battery chemistry only if necessary and approved, and consent/visibility roles. **Never output private meter serial numbers or business costs to buyer-facing pages**. Raw telemetry and customer billing stay access-controlled.

### Rules for display, rates, missing data and contradictions

1. Convert all timestamps from UTC into **Asia/Dhaka** for human display. Show current period, collection time, last successful update and source name. Use energy (kWh) only for integrated interval quantities; use power (kW) for instantaneous/averaged rate with its exact measurement window. Never confuse kW and kWh.
2. The UI's freshness threshold must be configured from the source's real expected sampling cadence after commissioning. If any required source is late, missing, miscalibrated, negative without a supported reverse-flow convention or outside its agreed validity period: show **Unavailable** for dependent flows and suppress aggregates. Never substitute 0 or last-known-good as current.
3. The word **Estimated** stays on any modeled or imputed value; **Historical** plus date on past actuals; **Live** only on valid near-current data. Estimated data cannot silently support the C06 solar-only claim.
4. If grid/PV/storage/backup records have unequal intervals, align them conservatively or mark unreconciled. Respect meter location and energy direction. Surface `unreconciled` with source data quality; never force arithmetic balance or silently suppress backup.
5. **Prevent double counting:** PV energy charged to storage and later discharged is **not** counted as extra PV generation. Track charge provenance (PV/grid/unknown) and storage losses. Distinguish grid import from net utility billing credits, which are not on-site PV generation.
6. A production halt, no utility bill, solar roof depiction or closed grid connection does not justify 100% solar. Night-time, rainy weather, non-electric energy and all site boundaries must be included if claimed.
7. A meter or API error must never switch to a flattering default green state. Show non-alarm wording explaining data loss, with last verified date and a contact role, without exposing server logs or secrets.
8. If outage/islanding status is displayed, require commissioned instrumentation and authorised inputs. A normal grid-connected PV system may shut down on utility outage [D3].

### Validation tests to execute before any live release

- **Missing data:** null PV source produces “Unavailable”; no fake 0 kWh.
- **Stale input:** last feed beyond signed cadence threshold displays stale, not “Live”.
- **Unit mismatch:** kW falsely submitted as kWh is rejected.
- **Time zones:** UTC to Asia/Dhaka daylight calendar boundaries verified with real timestamps.
- **Meter sign:** import/export polarity checked against utility bill in a test environment.
- **Double counting:** PV → battery charge → discharge is not treated as two PV units.
- **Cross-boundary:** array on adjacent owner's site does not appear as on-site generation without correct scope.
- **Backup:** generator electricity and fuel use remain visible in all-energy boundary.
- **Visual accessibility:** keyboard/readable text fallback, no reliance on animation/color alone.
- **Security:** no secret API token in frontend; role-based data access and safe failure.
- **Regression:** existing `/`, `/realistic/`, `/revised/` stay unchanged; separate approved release required.

**No tests above have been executed on a live energy system**. They are acceptance criteria to be applied after real inputs exist.

## Roles / linked evidence

- Owner/operations: boundary, authorised public data and claim review.
- Qualified electrical/solar engineer: physical metering, balance equations, rooftop/site feasibility and commissioned controls.
- Data engineer: sample windows, versioning, integrity, access and missing-data states.
- Communications/legal reviewer: claim wording with sources and independent approvals.

See [08_solar_feasibility_brief.md](08_solar_feasibility_brief.md), [08_energy_claim_matrix.md](08_energy_claim_matrix.md), and blank [08_load_inventory_template.csv](08_load_inventory_template.csv). Data input must come from authorised installed meters, not mock dashboards.

## Official source links (verified 30 October 2026)

- D1 — SREDA, Bangladesh net-metered PV programme: https://sreda.gov.bd/pages/static-pages/6922dfb4933eb65569e23942
- D2 — US EPA, hourly vs annual electricity matching: https://www.epa.gov/green-power-markets/247-hourly-matching-electricity
- D3 — US Department of Energy, islanding a microgrid: https://www.energy.gov/cmei/femp/articles/islanding-microgrid
