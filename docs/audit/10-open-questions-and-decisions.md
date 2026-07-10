# 10 - Open Questions and Decisions

## Resolved By Image Review

| Topic | Confirmed visible information |
| --- | --- |
| Brand name | `NCKL Logistics Services` |
| Slogan | English: `Your Cargo. Our Commitment.` French: `Votre Cargaison. Notre Engagement.` |
| Core routes | Germany -> Cameroon; Cameroon -> Germany/Europe; all European countries are referenced. |
| Services | Parcel shipping/forwarding, shopping assistance in Douala/Bamenda, shopping from Europe to Cameroon, package pickup from travel agencies in Douala. |
| Accepted items | Dry/frozen foodstuff, clothes, jewelries/bijoux, bags, shoes, cosmetics, hair extensions, dry herbs, documents, phones without battery, small household equipment. |
| Social | TikTok `@nckllogisticsservices`. |
| Visible contacts | Multiple Germany and Cameroon numbers documented in `13-image-requirements-analysis.md`. |

## Blocking Questions

| Priority | Question | Why it matters | Status |
| --- | --- | --- | --- |
| High | What is the final NCKL frontend domain? | Nginx, SSL, metadata, CORS, CSP, emails | Unknown |
| High | What is the final NCKL API domain? | `NEXT_PUBLIC_API_URL`, CORS, CSP, emails | Unknown |
| High | Should the app support English/French, French/German, or English/French/German? | Images are English/French, current app is French/German | Requires owner decision |
| High | Which phone number is the primary Cameroon support number? | Image 1 appears to show `+237 67472802`; Images 6/7 show `+237 674972802`; location-specific numbers also exist | Requires owner clarification |
| High | What is the exact Berlin address spelling? | Flyer appears to show `Eichushallee 53`; must not publish a typo | Requires owner clarification |
| High | What is the exact Douala location list? | Images show Rue 4.670 Bonaberi and another `Dôla service station` location | Requires owner clarification |
| High | Which transit-time claim is correct? | Image 1 says 10 days/3 days; Image 7 says 3-10 days both directions; schedule implies 4 days departure-to-arrival | Requires owner decision |
| High | What are NCKL prices, currencies, commissions, and payment rules? | No image shows prices | Unknown |
| High | What legal/privacy/customs/liability terms should be published? | Needed for public forms, accepted items, food/frozen items, documents, phones | Unknown |
| High | What is the scope of `FROM GERMANY TO CAMEROON ONLY`? | It may apply to phones without battery, but Image 7 is visually ambiguous | Requires owner clarification |
| Medium | Are July 2026 drop-off/departure/arrival dates one-off schedule entries or recurring examples? | Avoid stale hardcoded content | Requires owner decision |
| Medium | Should drop-off locations be admin-managed? | Images show multiple changing operational locations/contact numbers | Recommended yes, owner confirmation needed |
| Medium | Should shopping assistance from Europe be a full web form workflow or WhatsApp-only CTA? | Image 6 says reach out via WhatsApp | Requires owner decision |
| Medium | What documents/photos are customers allowed or required to upload? | Current app supports photos; images mention documents as shippable items | Unknown |
| Medium | What data retention period should NCKL use? | GDPR and storage cleanup | Unknown |
| Medium | Who should receive the initial admin account? | Bootstrap process | Unknown |

## Decisions Already Clear

| Decision | Basis |
| --- | --- |
| Keep the stack unless a real need emerges | User requirement and existing mature implementation |
| Do not use Docker for NCKL production | User requirement |
| Do not run existing SAHA deployment scripts | They target `/home/mignon/saha`, SAHA services/domains/ports |
| NCKL needs a separate database and role | User isolation rule and single-client schema |
| NCKL must not copy customer/request/media/backups from SAHA | User rule and detected ignored artifacts |
| Do not invent prices or legal claims | No pricing/legal information visible in the images |
| Drop-off dates and contacts should be content/configuration, not hardcoded source literals | Flyers show operationally changeable data |

## Decisions To Make Before Implementation

| Decision | Recommended default |
| --- | --- |
| Brand config location | Lightweight single-client config, not multi-tenant |
| Services/prices source | Backend-managed reference data editable by admin; seed initial NCKL records only after confirmation |
| Drop-off locations source | Admin-managed content or structured backend model |
| Contact/legal content | Central config plus static pages; legal text owner-approved |
| Reference prefix | NCKL prefix or non-sequential code after owner approval |
| Route and destination model | Add route direction and broader destination support |
| Deployment naming | Prefix all units/resources with `nckl-` and DB objects with `nckl_` |
| Runtime ports | Pick unused localhost ports after checking server state |
| Secrets | Generate new; never reuse SAHA |
