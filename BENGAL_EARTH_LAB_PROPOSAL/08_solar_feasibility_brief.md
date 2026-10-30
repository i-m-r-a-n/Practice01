# Bengal Earth Lab — solar feasibility inputs and scenario equations

**Date:** 30 October 2026 (Asia/Dhaka). **Status:** engineering data-request template, NOT a solar design, simulation result, installation report or proof of factory operation. No actual rooftop dimensions, load meters, inverter model, PV generation, battery size, electrical tariff, fossil-fuel usage or construction approval has been received.

## Project claim boundary — decide first

Fill in a signed boundary register. Choose **floor / entire building / whole factory site** and state the exact electricity accounts/meters, roof or offsite production, production equipment, outsourced processes, visitor displays, HVAC, training, cooking, transport, heating fuels, backup generator and any diesel/LPG/biomass inputs. Record operating days and reporting period. Ownership of generation and the rights to its environmental attributes must be documented; kWh exports or an annual net-zero bill do not automatically show 24/7 solar-only operation [S1, S4]. The same building may have distinct boundaries for **electricity-only** and **all energy** claims.

**Current allowed public wording:** “Designed for a Solar-Powered Future” (aspirational design direction, not a measured power claim). Solar wall must say “Concept demonstration — not live factory data” until a verified and connected telemetry feed is commissioned.

## Required owner/engineer inputs

1. **Occupancy and building boundary:** verified address/site ID kept private; floor/whole-site area; precise consumer utility and metering topology; export meter orientation; owner-approved operating shifts; major maintenance shutdowns.
2. **Load survey:** complete the companion `08_load_inventory_template.csv` with **actual** named equipment, number, nameplate kW, measured operating hours and critical status. Obtain electricity bills with billing periods, demand peaks and **interval meter readings** (prefer enough to cover seasonal shifts and full operating cycle), plus submeter records for production/cooling/labs/IT. A nameplate rating is NOT proof of measured energy consumed. Add motor starting/surge loads, standby/night loads and power quality through electrical survey.
3. **Non-electric energy:** generator fuel bills/run-hours, gas/LPG and thermal process fuel logs, outsourced process boundary and purchased energy. No “100% solar factory” claim while alternative inputs are unaccounted.
4. **Roof/PV:** measured usable roof area, structural analysis, shading/obstacles/rights, access routes, fire separation, waterproofing, mounting, wind and maintenance access; actual module/inverter specifications, origin, equipment approval and installation records if any. Do not assume the 1,030.3 m² concept-floor area equals usable PV roof.
5. **Storage/grid:** single-line diagram; sanctioned/connected load; utility and metering class; grid export/import arrangements; PV & storage operating mode, usable SOC range, charging source, inverter/ATS/islanding and anti-islanding behavior, generator ties, grounding, fire provisions and protection coordination; actual degradation assumptions.
6. **Telemetry:** meter identifiers, correct wiring/polarity, sampling interval, calibration/accuracy, timestamp/timezone, retention, data ownership, missing-record behavior and reconciliation against bills.
7. **Regulatory and professional sign-offs:** qualified local electrical/structural/fire professionals and utility verify the actual applicable Bangladesh net-metering guideline, approved equipment and permits. SREDA describes the 2025 programme and its bidirectional electricity import/export method [S2]; do not treat this as permission to connect equipment without technical review.

## Calculation *templates*, NOT plant sizing

Only calculate after verified inputs have been entered. Use matching periods, common boundaries and compatible AC/DC measurement points.

- `Daily_estimated_kWh = Σ_i [quantity_i × measured_average_kW_i × run_hours_per_day_i]`. If only nameplate ratings are available, use `nameplate_kW × quantity × operating_hours × independently established duty/load factor` as a **scenario estimate**, not measured consumption. Do not silently assume a duty factor.
- `Interval_Load_kWh = ∫_(interval) Load_kW(t) dt` (with proper sample integration and units). `Peak_demand_kW = max coincident interval / demand-measurement window`; independently assess motor inrush and apparent power (kVA).
- `Annual_AC_PV_kWh = PV_DC_size_kWp × site/specific annual AC yield (kWh per kWp)` as a *rough* comparison; determine yield and uncertainty through a site-specific PV simulation that includes weather, plane-of-array shading, temperature, soiling, orientation, inverter clipping and outages [S3]. A PVWatts default is NOT a site survey or a Bangladesh guaranteed yield.
- At each reconciled interval and well-defined metering boundary, `PV_AC_generation + Grid_import + Backup_AC_generation + Battery_AC_discharge = Facility_load + Grid_export + Battery_AC_charge + AC_system_losses + measurement_residual`. Physical energy flows on the **same** AC bus are required; adjust for DC coupling explicitly. Electricity charged from PV **then discharged from battery is not new solar generation twice**. Quantify residual/uncertainty instead of forcing an equality by inventing values.
- `Storage_deliverable_AC_kWh = Nominal_battery_kWh × permitted_usable_fraction × condition_derating × conversion_efficiency` (all parameters vendor/engineer verified). For a candidate outage period, `Required_deliverable_AC_kWh ≥ ∫ Critical_load_kW dt − verified coincident islanded PV_AC_kWh`, with worst-case weather, degradation, reserves and safety margins assessed separately. Confirm islanding controls, battery inverter **kW**, surge, thermal and autonomy; energy alone is not enough.
- `Site_solar_electricity_share`: do **not** publish a single universal formula before choosing whether it means physical direct consumption, PV plus storage sourced from PV, or accounted annual purchased renewable generation. Use transparent methodology and allocation to prevent export/charge/discharge double counting. **Annual netted electricity ≠ 24/7 solar supplied** [S1].

## Scenario comparison — empty until engineering inputs exist

| Scenario | Model intent | Required proof | Current disposition |
|---|---|---|---|
| S0 existing electricity | Grid/generator/unknown baseline, quantify all loads | utility data, generator & fuel logs, meters | No data: unavailable |
| S1 net-metered rooftop PV | PV + normal grid, exports credited per actual utility terms | utility eligibility, load profile, PV site/roof/structural and SREDA approvals | Study only; cannot claim “solar-only” |
| S2 PV plus storage hybrid | PV + battery with explicitly recorded grid/backup | hourly dispatch, battery charge origin, islanding protection, engineering | Study only; cannot claim “solar-only” |
| S3 engineered off-grid 24/7 | Adequate PV, storage and backup strategy for all declared loads in weather extremes | independent hourly reliability simulations, controls, commissioning and measured operations | No feasibility or reliability evidence; do not claim viable |

**Decision gates:** G0 scope and meter map signed; G1 baseline readings complete; G2 site/structural and fire concept reviewed; G3 utility/interconnection and protection requirements confirmed; G4 scenario simulation & sensitivity reviewed; G5 procurement/installation approved by owner; G6 commissioning and recorded monitoring; G7 owner-controlled external claims review. **All currently open.**

## Source register (read 30 October 2026)

- **S1** US Environmental Protection Agency, *24/7 Hourly Matching of Electricity*, distinction between annual-volume and hourly matching (context, not a Bangladesh regulation): https://www.epa.gov/green-power-markets/247-hourly-matching-electricity
- **S2** Sustainable and Renewable Energy Development Authority (SREDA), *Net Metering Rooftop Solar Programme*, 2025 guideline overview and bidirectional metering, accessed 30 Oct 2026: https://sreda.gov.bd/pages/static-pages/6922dfb4933eb65569e23942
- **S3** National Laboratory of the Rockies (formerly NREL), *PVWatts Calculator*, system-loss and production simulation inputs: https://pvwatts.nlr.gov/pvwatts.php
- **S4** US Department of Energy, *Islanding a Microgrid*, illustrating conventional PV shutdown on utility loss unless microgrid operation is engineered: https://www.energy.gov/cmei/femp/articles/islanding-microgrid
- **S5** SREDA, *Approved Equipment for Net Metering*, official equipment-listing/verification entry (not evidence any project item is approved): https://sreda.gov.bd/pages/static-pages/695b97d8c4774958d7b702d2

Never imply S1/S3/S4 create Bangladesh legal compliance; consult actual local regulators and engineers. This package includes **zero site measurements and zero performance numbers**.
