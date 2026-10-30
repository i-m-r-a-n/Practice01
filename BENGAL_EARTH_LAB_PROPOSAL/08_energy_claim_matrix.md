# Bengal Earth Lab — energy claim-to-evidence gate

**30 October 2026.** This is a **proposed** claim register, not a factory energy audit, regulatory certification, PV design or an assertion that measurements exist. The site, floor, electricity and all-energy boundaries have not been signed. No installation, generator, load or meter evidence has been submitted.

## Claim protocol

Every public sentence must define **site/floor boundary + electricity versus all energy + time period + numerator/denominator accounting + meter/source + independent review + decision owner**. Marketing cannot infer source of electricity from the presence of a panel, solar roof rendering, monthly utility net-credit or annual offset. Imported renewable electricity and solar generated physically on site are not interchangeable claims. See US EPA's annual vs hourly discussion [E1].

| ID | Proposed statement | Evidence needed before public release | Review role | Current status / safe wording |
|---|---|---|---|---|
| C01 | “Designed for a Solar-Powered Future” | Owner confirmation that this is a **vision**, visibly not operating data; no implication installed | Owner + communications | **Allowed only as design aspiration**, with concept disclaimer |
| C02 | “Solar PV installed at our site” | Dated as-built design, owned-array ID, commissioning certificate/photos, physical inspection, location/ownership | Electrical engineer + owner | **HOLD**; no installation evidence supplied |
| C03 | “Installed solar capacity is ___ kWp DC” | Verified DC module count/rating, as-built strings, nameplates, commissioning | Electrical engineer | **HOLD**; kWp unknown |
| C04 | “Generated ___ kWh last month” | Calibrated generation meter with period, missing-data audit, AC/DC boundary and onsite array identification | Energy data steward + engineer | **HOLD**; no meter stream |
| C05 | “Solar covers ___% of facility electricity” | Precise definition of direct vs storage-origin PV vs annual matched; site/production meter map; interval electricity balance and exports; storage charging source | Engineer + independent claims reviewer | **HOLD**; no share or denominator |
| C06 | “Entire factory powered only by solar, 24/7” | **Entire declared facility including night loads**, interval PV/load, grid imports, backup fuel and storage provenance over stated representative period, outages and evidence for all operational energy where claimed | Owner + independent engineer/claims reviewer | **HOLD**; currently unsubstantiated; do not display |
| C07 | “100% renewable electricity on an annual basis” | Full-year demand, valid energy attribute accounting/retirement where applicable, hourly vs annual method disclosure, no double claim | Independent sustainability reviewer | **HOLD**; not equivalent to C06 [E1,E2] |
| C08 | “Zero-carbon / carbon-neutral factory” | Defined Scope 1/2/(3 where used), measured all fuels/electricity, robust method and review, residuals/offset accounting disclosed | Independent emissions/claims specialist | **HOLD**; unsupported |
| C09 | “Solar runs the factory during outages” | Engineered and commissioned islanding/backup capability, utility interlock/protection, critical-load test and duration log; normal grid-tied PV may stop in outage [E3] | Licensed electrical professional | **HOLD**; not proven |
| C10 | “100% Bangladesh-made solar system / materials” | Component-level manufacturing, processing, raw-material and assembly origin for modules, cells, inverter, batteries, cables, frames, electronics; explicit exceptions | Procurement + origin reviewer | **HOLD**; no verified country-of-origin dossier |
| C11 | “No diesel/gas used in operations” | Full fuel, gas, backup and thermal equipment inventory; signed zero-use logs for specific period; site visit | Operations + audit reviewer | **HOLD**; no evidence |
| C12 | “Grid export saves X BDT / earns credit” | Correct current Bangladesh utility net-meter agreement, meter/bill reconciliation, tariff/credit rates for specific account and period [E4] | Owner + utility | **HOLD**; no approved account or amounts |

## Dashboard release-control fields

For each claim, track `claim_id`, `exact_text`, `locale`, `boundary_id`, `period_start`, `period_end`, `data_sources`, `meter_quality`, `evidence_links`, `methods_and_exclusions`, `approver`, `approval_at`, `expires_at`, `status` and `display_allowed`. Default `display_allowed=false`. “Unknown” is not zero. Draft/rejected claims never leak to public interface. Store **claim wording versions**, not just a pass/fail stamp.

**Owner decision gate:** only C01 may be used as a carefully labelled aspiration today. All measured claims remain on HOLD pending actual site evidence and competent review.

## Sources (official, accessed 30 October 2026)

- E1 — US EPA, *24/7 Hourly Matching of Electricity* (annual volume versus time-aligned electricity): https://www.epa.gov/green-power-markets/247-hourly-matching-electricity
- E2 — US EPA, *Energy Attribute Certificates* (rights, unique claims, double counting): https://www.epa.gov/green-power-markets/energy-attribute-certificates-eacs
- E3 — US Department of Energy, *Islanding a Microgrid* (PV and grid disturbance / islanding example): https://www.energy.gov/cmei/femp/articles/islanding-microgrid
- E4 — SREDA, *Net Metering Rooftop Solar Programme* (Bangladesh 2025 guideline and import/export): https://sreda.gov.bd/pages/static-pages/6922dfb4933eb65569e23942

EPA/DOE sources explain technical/claims concepts; they are NOT local Bangladesh regulatory permission or certifications.
