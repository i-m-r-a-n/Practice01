# Material Passport — EXAMPLE ONLY, NOT A REAL PRODUCT

**Prepared 30 October 2026.** This demonstration contains *deliberately unfilled* fields. It is designed to match [07_material_passport_schema.json](07_material_passport_schema.json). No maker, laboratory, buyer, material-source, test result, accreditation or solar system has been confirmed. It is a **concept**, not a commercial product, buyer offer or safety declaration.

```json
{
  "schema_version": "1.0.0",
  "item_id": "DEMO-CLAY-CUP-NOT-A-SKU",
  "item_name": "Illustrative Bengal Earth clay cup",
  "item_revision": "concept-0",
  "last_reviewed_date": "2026-10-30",
  "design_status": "concept",
  "collection": "Bengal Nordic (proposed)",
  "intended_use": {
    "description": "Possible reusable clay drinking cup; NO use authorised",
    "target_markets": [
      "EU market to be confirmed",
      "GB/NI to be confirmed"
    ],
    "food_contact": "yes",
    "use_conditions": "Hot/cold beverage profile and cleaning to be defined by owner/buyer and qualified tester",
    "warnings": [
      "FOOD CONTACT NOT VERIFIED — DO NOT SERVE FOOD OR DRINK",
      "Not a manufactured or tested product"
    ]
  },
  "maker_records": [
    {
      "role": "potter / ceramic artisan",
      "credit_name": null,
      "maker_identified": false,
      "permission_for_public_credit": false,
      "consent_evidence_ids": [],
      "benefit_sharing_status": "not_started"
    }
  ],
  "components": [
    {
      "component_id": "C01",
      "part_name": "fired clay body",
      "material_name": "ceramic body composition to verify",
      "mass_g": null,
      "supplier_name": null,
      "raw_origin": {
        "country": null,
        "district": null,
        "verification_level": "unknown",
        "evidence_ids": []
      },
      "processing": {
        "country": null,
        "district": null,
        "verification_level": "unknown",
        "evidence_ids": []
      },
      "component_manufacture": {
        "country": null,
        "district": null,
        "verification_level": "unknown",
        "evidence_ids": []
      },
      "final_assembly": {
        "country": null,
        "district": null,
        "verification_level": "unknown",
        "evidence_ids": []
      },
      "component_evidence_ids": [],
      "safety_questions": [
        "Clay body formulation, kiln temperature and lot not documented",
        "Finished product Pb/Cd migration must be checked"
      ]
    },
    {
      "component_id": "C02",
      "part_name": "food-facing glaze / pigments",
      "material_name": "glaze or unglazed finish not yet selected",
      "mass_g": null,
      "supplier_name": null,
      "raw_origin": {
        "country": null,
        "district": null,
        "verification_level": "unknown",
        "evidence_ids": []
      },
      "processing": {
        "country": null,
        "district": null,
        "verification_level": "unknown",
        "evidence_ids": []
      },
      "component_manufacture": {
        "country": null,
        "district": null,
        "verification_level": "unknown",
        "evidence_ids": []
      },
      "final_assembly": {
        "country": null,
        "district": null,
        "verification_level": "unknown",
        "evidence_ids": []
      },
      "component_evidence_ids": [],
      "safety_questions": [
        "Full ingredient/finish data needed",
        "EU/GB metal-release and EU/NI coating chemistry review required where applicable"
      ]
    }
  ],
  "evidence_register": [],
  "test_register": [
    {
      "test_id": "PLANNED-FCM-01",
      "topic": "Finished ceramic lead/cadmium release",
      "market": "EU and GB rules to be reconciled",
      "method": null,
      "result": "not_started",
      "report_evidence_ids": [],
      "limitations": "No samples or test results exist; lab and category to confirm"
    }
  ],
  "claim_register": [
    {
      "claim_text": "Food-safe",
      "claim_type": "safety",
      "claim_boundary": "finished cup",
      "claim_period": null,
      "decision": "not_supported_do_not_publish",
      "evidence_ids": [],
      "reviewed_by": null
    },
    {
      "claim_text": "100% Bangladesh-made",
      "claim_type": "origin",
      "claim_boundary": "all components including glaze",
      "claim_period": null,
      "decision": "not_supported_do_not_publish",
      "evidence_ids": [],
      "reviewed_by": null
    },
    {
      "claim_text": "Powered by 100% solar",
      "claim_type": "solar",
      "claim_boundary": "workshop/site undefined",
      "claim_period": null,
      "decision": "not_supported_do_not_publish",
      "evidence_ids": [],
      "reviewed_by": null
    }
  ],
  "commercial_release": {
    "status": "hold",
    "holds": [
      "No identified/consenting maker",
      "Unverified origin for body/glaze",
      "No laboratory migration results",
      "No intended-use or market-specific legal review",
      "No importer/label and declaration"
    ],
    "decision_maker": null,
    "decision_date": null
  }
}
```

## How to use the actual passport
1. Create a new item ID and a separate revision per material/finish change. Assign a responsible owner. Keep source documents private if they contain commercial information, but expose the evidence **status** honestly to the buyer.
2. Verify each stage of each component separately: raw country/district → processing → component manufacture → final assembly. Bangladesh assembly alone is **not** proof that all raw materials or components were Bangladeshi-produced.
3. Obtain maker consent before public name, photograph, cultural story, workshop location or provenance detail is published. Indigenous/community motifs require a separate consent and benefit-sharing workflow.
4. Attach exact laboratory scope, report and finish lot to the test register. Never set test result to `passed` because a supplier promises safety. For intended tableware see [the test gate](FOOD_CONTACT_CLAY_WOOD_TEST_BRIEF.md).
5. Keep claim register marked `not_supported_do_not_publish` until a reviewer checks evidence, scope and use; if no solar load/generation data exist, do not claim a solar-only workshop.
6. Release only for the specifically reviewed market/use. A schema-valid JSON file is **not** regulatory compliance and does not approve manufacturing, food contact or sale.

## Owner review fields still to fill
Actual product dimensions, supplier/maker details with consent, batch records, country-specific market access, sample results, importer/DoC, safe-use claims, origin evidence, and approved product photography.
