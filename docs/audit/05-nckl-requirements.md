# 05 - NCKL Requirements

## Source Material Status

Status: verified fact.

Seven NCKL client images were supplied and visually inspected in sequence from the conversation attachments:

| File | Inspection status | Notes |
| --- | --- | --- |
| `docs/nckl_1.jpeg` | Inspected | General launch/services flyer. |
| `docs/nckl_2.jpeg` | Inspected | English Cameroon to Germany/Europe schedule flyer. |
| `docs/nckl_3.jpeg` | Inspected | Drop-off locations flyer. |
| `docs/nckl_4.jpeg` | Inspected | French version of schedule/services flyer. |
| `docs/nckl_5.jpeg` | Inspected | Duplicate or near-duplicate of `nckl_3.jpeg`. |
| `docs/nckl_6.jpeg` | Inspected | Europe shopping assistance / doorstep delivery ad. |
| `docs/nckl_7.jpeg` | Inspected | Consolidated services, conditions, contacts, and locations flyer. |

Detailed extraction is in [13-image-requirements-analysis.md](13-image-requirements-analysis.md).

## Requirements Catalogue

| Requirement area | Verified facts | Unknown or unverified |
| --- | --- | --- |
| Company name | `NCKL Logistics Services` | Legal entity name and registration details are not shown. |
| Slogan | English: `Your Cargo. Our Commitment.` French: `Votre Cargaison. Notre Engagement.` | Whether both slogans should appear in app chrome. |
| Logo and identity | Metallic/silver `NCKL` wordmark with red/white/blue swoosh icon; `LOGISTICS SERVICES` subtext. | Source vector/logo files and usage rules. |
| Brand colors | Dark navy/blue backgrounds, white/silver typography, red emphasis, yellow/gold highlights, Cameroon/Germany flag colors. | Exact color tokens and accessibility contrast targets. |
| Typography | Bold condensed uppercase display text; italic serif slogan; metallic effect on logo/headlines. | Actual font names are not visible. |
| Languages | English and French marketing materials are shown. | Whether the web app should support English, French, German, or all three. Current app supports French/German only. |
| Primary routes | Germany to Cameroon; Cameroon to Germany; Cameroon to Germany & Europe; shipping to all European countries. | Exact European country list, whether all EU/Europe is legally/serviceable. |
| Transit time | Image 1: Germany to Cameroon `10 days`, Cameroon to Germany `3 days`; Image 7: both directions `3 - 10 days`; Images 2/4 show departure July 12, 2026 and arrival in Germany July 16, 2026. | Final promised transit time wording and SLA. |
| Shopping assistance | Shopping assistance in Douala; shopping in Douala and Bamenda; shopping from Europe for products customers cannot buy in Cameroon. | Fees, purchasing limits, payment timing, returns/refunds. |
| Parcel receiving | Receive parcels from all European countries to ship to Cameroon; receive packages from any region in Cameroon. | Accepted handoff method, packaging requirements, liability terms. |
| Package pickup | Package pickup from any travel agency in Douala. | Exact agency list/process and whether it remains current. |
| Forwarding/posting | Post parcels received from Cameroon to any country of customer's choice / all European countries. | Carrier partners and country restrictions. |
| Doorstep delivery | Image 6 says NCKL will buy and deliver desired products to the customer's doorstep in Cameroon. | Coverage area in Cameroon and delivery fees. |
| Shipping items | Foodstuff/food stuff dry, frozen food, clothes, jewelries/bijoux, bags, shoes, cosmetics, hair extensions, dry herbs, documents, phones without battery, small household equipment. | Prohibited items, customs restrictions, food temperature handling. |
| Weight rule | Small household equipment: not more than 31 kg. | Whether 31 kg applies only to small household equipment or all parcels. |
| Phone rule | Phones without battery; examples Samsung/iPhones; Germany to Cameroon only in Image 1. | Whether phones are accepted only DE to CM and whether battery removal is mandatory. |
| Drop-off locations | Bamenda, two Douala/Bonaberi locations, Berlin, Leipzig. | Whether these are permanent, appointment-only, or event-specific. |
| Schedules | Latest drop-off dates: Bamenda July 10, 2026 at 15:00; Douala July 11, 2026 at 17:00; departure July 12, 2026; arrival in Germany July 16, 2026. | Whether these are recurring or one-off campaign dates. |
| Contact | General Germany WhatsApp/call: `+49 1521 2392636`; Berlin WhatsApp only: `+49 15222376184`; Leipzig: `+49 15773620710`; Bamenda: `+237 674574041`, `+237 622441020`; Douala Bonaberi: `+237 675745056`; another Douala contact shown as `+237 674972802`; Image 1 shows `+237 67472802` which appears shorter/possibly cropped or typo. | Primary support number, formatting, and reconciliation of conflicting Cameroon number. |
| Social media | TikTok handle `@nckllogisticsservices`. | Other social channels. |
| Payment | No prices or payment methods are visible. | Pricing, currency, deposit/prepayment, shopping-assistance payment process. |
| Legal information | Not visible. | Privacy, terms, imprint, liability, customs disclaimers. |

## Consolidated Services

| Service | Verified source images | Reusable current feature | Required adaptation |
| --- | --- | --- | --- |
| Germany/Europe to Cameroon parcel shipping | 1, 7 | Transport request, services, pricing, destinations, tracking | Replace SAHA route copy, statuses, destinations, item types, SLA. |
| Cameroon to Germany/Europe parcel forwarding | 1, 2, 4, 7 | Transport request, schedules, tracking | Add bidirectional route fields and Cameroon-origin drop-off flow. |
| Shopping assistance in Douala/Bamenda | 1, 2, 4, 7 | Could reuse service catalogue/request form | Add service type, purchase details, payment fields, admin workflow. |
| Shopping from Europe to Cameroon | 6 | Could reuse request form with service type | New workflow fields for product link, budget, purchase approval, doorstep delivery. |
| Package pickup from Douala travel agencies | 1, 7 | Could reuse pickup location/address fields | Add travel-agency pickup option and instructions. |
| Receive packages from any Cameroon region | 2, 4, 7 | Schedule/location content | Add Cameroon drop-off/pickup region handling. |
| Ship to all European countries | 2, 4, 7 | Destination catalogue | Replace fixed Douala/Yaounde/Bafoussam destination list with European destinations or broad region. |

## Traceability Table

| Source | Extracted requirement | Proposed feature/content location | Existing reusable component | Required adaptation | Validation status |
| --- | --- | --- | --- | --- | --- |
| Image 1 | NCKL brand, slogan, new launch, DE-CM and CM-DE transit times | Home hero, metadata, brand config | Layout, hero, i18n | Replace SAHA brand/route copy | Verified, transit time conflicts with Image 7 |
| Image 1 | Accepted items and conditions | Services page, request form item type, FAQ | Services/pricing/request form | Add item catalogue and condition notes | Verified |
| Image 2 | Cameroon to Germany & Europe schedule and services | Schedule page, loading dates, notifications | LoadingDate, PickupSchedule, notification composer | Add drop-off/departure/arrival model/content | Verified, one-off dates |
| Image 3 | Drop-off locations and contact numbers | Contact page, locations section, admin-managed locations | Contact page, schedule admin | Need location model/config | Verified, Berlin street spelling uncertain |
| Image 4 | French schedule/service content | FR content/i18n | i18n utilities | Add/replace French translations | Verified |
| Image 5 | Duplicate of drop-off locations | Contact page/locations | Same as Image 3 | Deduplicate source | Verified duplicate/near-duplicate |
| Image 6 | Europe shopping assistance and doorstep delivery in Cameroon | Service page, request form workflow | Service catalogue/request form | New purchase-assistance workflow | Verified |
| Image 7 | Consolidated services, contacts, locations, condition `from Germany to Cameroon only` | Services, FAQ, locations, contact, request form | Multiple existing modules | Reconcile conditions and contacts | Verified, one condition scope unclear |

## Implementation Consequence

Recommendation.

The next implementation phase should not merely rebrand SAHA. It should preserve the proven logistics platform but adapt it to NCKL's bidirectional Germany/Cameroon/Europe workflow, shopping-assistance services, admin-managed drop-off locations, richer item acceptance rules, and English/French content requirements. Prices remain unknown and must not be invented.
