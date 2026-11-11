# P05 — UNI 8290 to IFC branch review packet

This packet is ready for explicit owner/domain-expert review. It does **not** record human approval. Automated tests and AI-assisted semantic pre-review cannot satisfy the P05 approval gate by themselves.

AI assessed all 29 non-high-confidence rows. Its decisions and reasons are in `refactor/review/p05-ai-assessment.json`. The open list below contains only questions that need the owner or a domain expert. Explicit branch approval remains unrecorded.

## Review summary

| Root | Branch | Decisions | High | Open | State |
|---|---|---:|---:|---:|---|
| `1.0.0` | load-bearing structures | 11 | 8 | 0 | `awaiting_user_or_domain_expert_approval` |
| `2.0.0` | enclosures | 12 | 11 | 1 | `awaiting_user_or_domain_expert_approval` |
| `3.0.0` | internal partitions | 12 | 9 | 1 | `awaiting_user_or_domain_expert_approval` |
| `4.0.0` | external partitions | 10 | 6 | 0 | `awaiting_user_or_domain_expert_approval` |
| `5.0.0` | building-service systems | 45 | 36 | 6 | `awaiting_user_or_domain_expert_approval` |
| `6.0.0` | safety systems | 18 | 14 | 3 | `awaiting_user_or_domain_expert_approval` |
| `7.0.0` | internal equipment | 4 | 1 | 1 | `awaiting_user_or_domain_expert_approval` |
| `8.0.0` | external equipment | 5 | 3 | 0 | `awaiting_user_or_domain_expert_approval` |

## 1.0.0 — load-bearing structures

| UNI code and hierarchy | Proposed IFC entities | Conditions | Confidence |
|---|---|---|---|
| `1.0.0` — Struttura portante | `IfcBuildingSystem` | PredefinedType=LOADBEARING | `high` |
| `1.1.0` — Struttura portante > Struttura di fondazione | `IfcBuildingSystem` | PredefinedType=FOUNDATION | `high` |
| `1.1.1` — Struttura portante > Struttura di fondazione > Strutture di fondazione dirette | `IfcFooting`, `IfcSlab` | IfcSlab PredefinedType=BASESLAB | `high` |
| `1.1.2` — Struttura portante > Struttura di fondazione > Strutture di fondazione indirette | `IfcDeepFoundation`, `IfcPile`, `IfcCaissonFoundation` | Occurrence transfers loads to deep ground strata | `high` |
| `1.2.0` — Struttura portante > Struttura di elevazione | `IfcBuildingSystem` | PredefinedType=LOADBEARING; above-foundation structural system | `high` |
| `1.2.1` — Struttura portante > Struttura di elevazione > Strutture di elevazione verticali | `IfcWall`, `IfcColumn`, `IfcMember` | Vertical and load-bearing structural role | `high` |
| `1.2.2` — Struttura portante > Struttura di elevazione > Strutture di elevazione orizzontali e inclinate | `IfcBeam`, `IfcSlab`, `IfcMember` | Horizontal or inclined and load-bearing structural role | `high` |
| `1.2.3` — Struttura portante > Struttura di elevazione > Strutture di elevazione spaziali | `IfcElementAssembly` | PredefinedType=BRACED_FRAME, RIGID_FRAME, TRUSS, or another directly applicable spatial load-bearing assembly role | `medium` |
| `1.3.0` — Struttura portante > Struttura di contenimento | `IfcWall`, `IfcSlab` | Structural containment or retaining role | `medium` |
| `1.3.1` — Struttura portante > Struttura di contenimento > Strutture di contenimento verticali | `IfcWall` | PredefinedType=RETAININGWALL or equivalent vertical structural containment role | `high` |
| `1.3.2` — Struttura portante > Struttura di contenimento > Strutture di contenimento orizzontali | `IfcSlab` | Horizontal structural containment role | `medium` |

### Open decisions

No unresolved AI-assessment question remains in this branch; explicit branch approval is still unrecorded.

### AI-assessed decisions

- `1.2.3` (revise): IfcElementAssembly has direct frame and truss types. Individual beams and members are components, not spatial structures.
- `1.3.0` (accept): The UNI definition explicitly concerns resisting earth loads. Retaining walls and structural slabs can directly perform that role under the stated condition.
- `1.3.2` (accept): A horizontal structural slab can resist earth loads; the condition must exclude ordinary floors and roof slabs.

### Branch approval record

- Decision: `awaiting_user_or_domain_expert_approval`
- Reviewer: *(not recorded)*
- Date: *(not recorded)*
- Revisions/evidence: *(not recorded)*

## 2.0.0 — enclosures

| UNI code and hierarchy | Proposed IFC entities | Conditions | Confidence |
|---|---|---|---|
| `2.0.0` — Chiusura | `IfcBuildingSystem` | PredefinedType=OUTERSHELL | `high` |
| `2.1.0` — Chiusura > Chiusura verticale | `IfcWall`, `IfcCurtainWall` | Exterior vertical enclosure role | `high` |
| `2.1.1` — Chiusura > Chiusura verticale > Pareti perimetrali verticali | `IfcWall`, `IfcCurtainWall` | Exterior perimeter enclosure role | `high` |
| `2.1.2` — Chiusura > Chiusura verticale > Infissi esterni verticali | `IfcDoor`, `IfcWindow` | Exterior and predominantly vertical opening closure | `high` |
| `2.2.0` — Chiusura > Chiusura orizzontale inferiore | `IfcSlab` | Lower horizontal exterior enclosure role | `high` |
| `2.2.1` — Chiusura > Chiusura orizzontale inferiore > Solai a terra | `IfcSlab` | PredefinedType=BASESLAB or FLOOR; ground-contact enclosure role | `high` |
| `2.2.2` — Chiusura > Chiusura orizzontale inferiore > Infissi orizzontali | `IfcDoor`, `IfcWindow` | Horizontal lower opening closure; IfcDoor normally PredefinedType=TRAPDOOR | `domain_review_required` |
| `2.3.0` — Chiusura > Chiusura orizzontale su spazi esterni | `IfcSlab` | Horizontal enclosure over an exterior or open space | `high` |
| `2.3.1` — Chiusura > Chiusura orizzontale su spazi esterni > Solai su spazi aperti | `IfcSlab` | PredefinedType=FLOOR; separates conditioned space from open space below | `high` |
| `2.4.0` — Chiusura > Chiusura superiore | `IfcRoof`, `IfcSlab` | IfcSlab PredefinedType=ROOF when used as the upper enclosure | `high` |
| `2.4.1` — Chiusura > Chiusura superiore > Coperture | `IfcRoof`, `IfcSlab`, `IfcCovering` | IfcSlab PredefinedType=ROOF; IfcCovering PredefinedType=ROOFING only for the dependent roof finish | `high` |
| `2.4.2` — Chiusura > Chiusura superiore > Infissi esterni orizzontali | `IfcWindow`, `IfcDoor` | IfcWindow PredefinedType=SKYLIGHT or LIGHTDOME; IfcDoor PredefinedType=TRAPDOOR; exterior horizontal closure | `high` |

### Open decisions

- `2.2.2` (domain_review_required): Does this UNI leaf include both glazed horizontal closures and trapdoors, or should one IFC entity be removed? AI finding: The source has no definition. IFC distinguishes trapdoors and windows, but the intended range of lower horizontal closures is not documented.

### AI-assessed decisions


### Branch approval record

- Decision: `awaiting_user_or_domain_expert_approval`
- Reviewer: *(not recorded)*
- Date: *(not recorded)*
- Revisions/evidence: *(not recorded)*

## 3.0.0 — internal partitions

| UNI code and hierarchy | Proposed IFC entities | Conditions | Confidence |
|---|---|---|---|
| `3.0.0` — Partizione interna | *(empty)* | No concrete IFC 4.3.2 occurrence reliably represents the complete aggregate without a project-specific grouping | `medium` |
| `3.1.0` — Partizione interna > Partizione interna verticale | `IfcWall` | Internal, non-load-bearing vertical partition role | `high` |
| `3.1.1` — Partizione interna > Partizione interna verticale > Pareti interne verticali | `IfcWall` | PredefinedType=PARTITIONING or MOVABLE; internal non-load-bearing role | `high` |
| `3.1.2` — Partizione interna > Partizione interna verticale > Infissi interni verticali | `IfcDoor`, `IfcWindow` | Internal vertical opening closure | `high` |
| `3.1.3` — Partizione interna > Partizione interna verticale > Elementi di protezione | `IfcRailing`, `IfcImpactProtectionDevice` | Internal guard, handrail, or direct impact-protection role | `medium` |
| `3.2.0` — Partizione interna > Partizione interna orizzontale | `IfcSlab` | Internal horizontal subdivision role | `high` |
| `3.2.1` — Partizione interna > Partizione interna orizzontale > Solai | `IfcSlab` | PredefinedType=FLOOR; internal storey-separating role | `high` |
| `3.2.2` — Partizione interna > Partizione interna orizzontale > Soppalchi | `IfcSlab` | PredefinedType=FLOOR; mezzanine role | `high` |
| `3.2.3` — Partizione interna > Partizione interna orizzontale > Infissi interni orizzontali | `IfcDoor` | PredefinedType=TRAPDOOR; internal horizontal opening closure | `medium` |
| `3.3.0` — Partizione interna > Partizione interna inclinata | `IfcStair`, `IfcRamp` | Internal inclined circulation/subdivision role | `high` |
| `3.3.1` — Partizione interna > Partizione interna inclinata > Scale interne | `IfcStair`, `IfcStairFlight` | Internal stair or stair flight | `high` |
| `3.3.2` — Partizione interna > Partizione interna inclinata > Rampe interne | `IfcRamp`, `IfcRampFlight` | Internal ramp or ramp flight | `high` |

### Open decisions

- `3.1.3` (medium): Confirm that the selected family and stated condition match the intended UNI scope; otherwise record the revised entities or an empty mapping. AI finding: IfcRailing protects users; IfcImpactProtectionDevice protects built elements. The undefined UNI leaf does not establish whether both are intended.

### AI-assessed decisions

- `3.0.0` (accept): The UNI aggregate covers several kinds of internal subdivision; the catalogue has no concrete system occurrence with that direct scope. Empty is defensible.
- `3.2.3` (accept): IfcDoor/TRAPDOOR directly represents an internal horizontal opening closure.

### Branch approval record

- Decision: `awaiting_user_or_domain_expert_approval`
- Reviewer: *(not recorded)*
- Date: *(not recorded)*
- Revisions/evidence: *(not recorded)*

## 4.0.0 — external partitions

| UNI code and hierarchy | Proposed IFC entities | Conditions | Confidence |
|---|---|---|---|
| `4.0.0` — Partizione esterna | *(empty)* | No single concrete IFC occurrence represents the external-partition aggregate | `medium` |
| `4.1.0` — Partizione esterna > Partizione esterna verticale | `IfcWall`, `IfcRailing`, `IfcDoor` | External site separation or protection role; IfcDoor PredefinedType=GATE where applicable | `medium` |
| `4.1.1` — Partizione esterna > Partizione esterna verticale > Elementi di protezione | `IfcRailing`, `IfcImpactProtectionDevice` | IfcRailing PredefinedType=GUARDRAIL, HANDRAIL, or BALUSTRADE; direct external protection role | `high` |
| `4.1.2` — Partizione esterna > Partizione esterna verticale > Elementi di separazione | `IfcWall`, `IfcRailing`, `IfcDoor` | Boundary role; IfcRailing PredefinedType=FENCE; IfcDoor PredefinedType=GATE | `high` |
| `4.2.0` — Partizione esterna > Partizione esterna orizzontale | `IfcSlab` | External horizontal platform or subdivision role | `medium` |
| `4.2.1` — Partizione esterna > Partizione esterna orizzontale > Balconi e logge | `IfcSlab` | PredefinedType=FLOOR or LANDING; balcony or loggia platform role | `high` |
| `4.2.2` — Partizione esterna > Partizione esterna orizzontale > Passerelle | `IfcSlab` | External elevated walkway platform role | `medium` |
| `4.3.0` — Partizione esterna > Partizione esterna inclinata | `IfcStair`, `IfcRamp` | External inclined circulation role | `high` |
| `4.3.1` — Partizione esterna > Partizione esterna inclinata > Scale esterne | `IfcStair`, `IfcStairFlight` | External stair or stair flight | `high` |
| `4.3.2` — Partizione esterna > Partizione esterna inclinata > Rampe esterne | `IfcRamp`, `IfcRampFlight` | External ramp or ramp flight | `high` |

### Open decisions

No unresolved AI-assessment question remains in this branch; explicit branch approval is still unrecorded.

### AI-assessed decisions

- `4.0.0` (accept): The source aggregate spans external space division in several orientations; no concrete IFC system occurrence matches it directly. Empty is defensible.
- `4.1.0` (accept): Walls, boundary railings and gates can themselves divide external space when the recorded site-boundary role applies.
- `4.2.0` (accept): A slab can directly form an external horizontal platform or subdivision under the recorded role condition.
- `4.2.2` (accept): IfcSlab can form the deck of an elevated walkway; this selection excludes railings and other possible components.

### Branch approval record

- Decision: `awaiting_user_or_domain_expert_approval`
- Reviewer: *(not recorded)*
- Date: *(not recorded)*
- Revisions/evidence: *(not recorded)*

## 5.0.0 — building-service systems

| UNI code and hierarchy | Proposed IFC entities | Conditions | Confidence |
|---|---|---|---|
| `5.0.0` — Impianto di fornitura servizi | `IfcDistributionSystem` | Building-service distribution system; exclude safety-system contexts classified under root 6.0.0 | `high` |
| `5.1.0` — Impianto di fornitura servizi > Impianto di climatizzazione | `IfcDistributionSystem` | PredefinedType in AIRCONDITIONING, CHILLEDWATER, HEATING, REFRIGERATION, VENTILATION | `high` |
| `5.1.1` — Impianto di fornitura servizi > Impianto di climatizzazione > Alimentazione | `IfcPipeSegment`, `IfcCableSegment` | Direct fuel, thermal-fluid, or electrical supply connection serving the HVAC system | `domain_review_required` |
| `5.1.2` — Impianto di fornitura servizi > Impianto di climatizzazione > Gruppi termici | `IfcBoiler` | Thermal generation group; include associated burner only under separate direct classification | `high` |
| `5.1.3` — Impianto di fornitura servizi > Impianto di climatizzazione > Centrali di trattamento fluidi | `IfcUnitaryEquipment`, `IfcChiller`, `IfcCoolingTower`, `IfcHeatExchanger` | Central fluid-treatment or air-handling plant; IfcUnitaryEquipment normally PredefinedType=AIRHANDLER | `medium` |
| `5.1.4` — Impianto di fornitura servizi > Impianto di climatizzazione > Reti di distribuzione e terminali | `IfcDuctSegment`, `IfcDuctFitting`, `IfcAirTerminal`, `IfcAirTerminalBox`, `IfcPipeSegment`, `IfcPipeFitting`, `IfcSpaceHeater`, `IfcCooledBeam` | Member or terminal of the HVAC distribution network identified by system membership | `high` |
| `5.1.5` — Impianto di fornitura servizi > Impianto di climatizzazione > Reti di scarico condensa | `IfcPipeSegment`, `IfcPipeFitting`, `IfcWasteTerminal` | Condensate drainage function within the HVAC system | `high` |
| `5.1.6` — Impianto di fornitura servizi > Impianto di climatizzazione > Canne di esalazione | `IfcChimney`, `IfcDuctSegment`, `IfcStackTerminal` | Flue or exhaust-stack function serving HVAC combustion equipment | `high` |
| `5.2.0` — Impianto di fornitura servizi > Impianto idrosanitario | `IfcDistributionSystem` | PredefinedType in DOMESTICCOLDWATER, DOMESTICHOTWATER, WATERSUPPLY | `high` |
| `5.2.1` — Impianto di fornitura servizi > Impianto idrosanitario > Allacciamenti | `IfcPipeSegment`, `IfcPipeFitting`, `IfcValve`, `IfcFlowMeter` | Utility/service connection for the domestic water system | `high` |
| `5.2.2` — Impianto di fornitura servizi > Impianto idrosanitario > Macchine idrauliche | `IfcPump` | Hydraulic machine serving the domestic-water system | `high` |
| `5.2.3` — Impianto di fornitura servizi > Impianto idrosanitario > Accumuli | `IfcTank` | PredefinedType=STORAGE, BREAKPRESSURE, or FEEDANDEXPANSION as applicable to water storage | `high` |
| `5.2.4` — Impianto di fornitura servizi > Impianto idrosanitario > Riscaldatori | `IfcBoiler`, `IfcHeatExchanger` | Domestic-water heating function; IfcBoiler normally PredefinedType=WATER | `high` |
| `5.2.5` — Impianto di fornitura servizi > Impianto idrosanitario > Reti di distribuzione acqua fredda e terminali | `IfcPipeSegment`, `IfcPipeFitting`, `IfcValve`, `IfcFlowMeter`, `IfcSanitaryTerminal` | Domestic cold-water network membership; sanitary terminal included only as the delivery endpoint | `high` |
| `5.2.6` — Impianto di fornitura servizi > Impianto idrosanitario > Reti di distribuzione acqua calda e terminali | `IfcPipeSegment`, `IfcPipeFitting`, `IfcValve`, `IfcFlowMeter`, `IfcSanitaryTerminal` | Domestic hot-water network membership; sanitary terminal included only as the delivery endpoint | `high` |
| `5.2.7` — Impianto di fornitura servizi > Impianto idrosanitario > Reti di ricircolo dell'acqua calda | `IfcPipeSegment`, `IfcPipeFitting`, `IfcPump` | Domestic hot-water recirculation system; IfcPump PredefinedType=CIRCULATOR | `high` |
| `5.2.8` — Impianto di fornitura servizi > Impianto idrosanitario > Apparecchi sanitari | `IfcSanitaryTerminal` | Occurrence directly represents a sanitary fixture | `high` |
| `5.3.0` — Impianto di fornitura servizi > Impianto di smaltimento liquidi | `IfcDistributionSystem` | PredefinedType in DRAINAGE, SEWAGE, STORMWATER, WASTEWATER, RAINWATER | `high` |
| `5.3.1` — Impianto di fornitura servizi > Impianto di smaltimento liquidi > Reti di scarico acque fecali | `IfcPipeSegment`, `IfcPipeFitting`, `IfcWasteTerminal` | Blackwater/sewage discharge network membership | `high` |
| `5.3.2` — Impianto di fornitura servizi > Impianto di smaltimento liquidi > Reti di scarico acque domestiche | `IfcPipeSegment`, `IfcPipeFitting`, `IfcWasteTerminal` | Domestic greywater/wastewater discharge network membership | `high` |
| `5.3.3` — Impianto di fornitura servizi > Impianto di smaltimento liquidi > Reti di scarico acque meteoriche | `IfcPipeSegment`, `IfcPipeFitting`, `IfcWasteTerminal`, `IfcStackTerminal` | Stormwater/rainwater drainage; terminals limited to roof drains, gullies, or rainwater hoppers | `high` |
| `5.3.4` — Impianto di fornitura servizi > Impianto di smaltimento liquidi > Reti di ventilazione secondaria | `IfcPipeSegment`, `IfcPipeFitting`, `IfcStackTerminal` | Secondary ventilation of the liquid-waste drainage system | `high` |
| `5.4.0` — Impianto di fornitura servizi > Impianto di smaltimento aeriformi | `IfcDistributionSystem` | PredefinedType=EXHAUST or VENT | `high` |
| `5.4.1` — Impianto di fornitura servizi > Impianto di smaltimento aeriformi > Alimentazione | `IfcCableSegment`, `IfcSwitchingDevice` | Electrical supply dedicated to aeriform-disposal machinery | `domain_review_required` |
| `5.4.2` — Impianto di fornitura servizi > Impianto di smaltimento aeriformi > Macchine | `IfcFan` | Air-moving machine in the aeriform-disposal system | `high` |
| `5.4.3` — Impianto di fornitura servizi > Impianto di smaltimento aeriformi > Reti di canalizzazione | `IfcDuctSegment`, `IfcDuctFitting`, `IfcAirTerminal`, `IfcDamper` | Exhaust/vent duct-network membership | `high` |
| `5.5.0` — Impianto di fornitura servizi > Impianto di smaltimento solidi | `IfcDistributionSystem` | PredefinedType=MUNICIPALSOLIDWASTE or DISPOSAL | `medium` |
| `5.5.1` — Impianto di fornitura servizi > Impianto di smaltimento solidi > Canne di caduta | `IfcConveyorSegment` | PredefinedType=CHUTECONVEYOR; solid-waste drop chute | `high` |
| `5.5.2` — Impianto di fornitura servizi > Impianto di smaltimento solidi > Canne di esalazione | `IfcDuctSegment` | Ventilation duct segment forming the solid-waste installation's exhalation shaft; exclude combustion flues and terminal caps | `medium` |
| `5.6.0` — Impianto di fornitura servizi > Impianto di distribuzione gas | `IfcDistributionSystem` | PredefinedType=GAS | `high` |
| `5.6.1` — Impianto di fornitura servizi > Impianto di distribuzione gas > Allacciamenti | `IfcPipeSegment`, `IfcPipeFitting`, `IfcValve`, `IfcFlowMeter` | Gas service connection, interpreted under gas-distribution parent | `high` |
| `5.6.2` — Impianto di fornitura servizi > Impianto di distribuzione gas > Reti di distribuzione e terminali | `IfcPipeSegment`, `IfcPipeFitting`, `IfcValve`, `IfcFlowMeter` | Gas distribution-network or direct delivery-control function | `high` |
| `5.7.0` — Impianto di fornitura servizi > Impianto elettrico | `IfcDistributionSystem` | PredefinedType=ELECTRICAL | `high` |
| `5.7.1` — Impianto di fornitura servizi > Impianto elettrico > Alimentazione | `IfcTransformer`, `IfcElectricGenerator`, `IfcElectricFlowStorageDevice`, `IfcElectricDistributionBoard` | Incoming, conversion, generation, storage, or main-distribution function supplying the electrical installation | `medium` |
| `5.7.2` — Impianto di fornitura servizi > Impianto elettrico > Allacciamenti | `IfcCableSegment`, `IfcCableFitting`, `IfcJunctionBox` | Electrical service connection, interpreted under electrical-system parent | `high` |
| `5.7.3` — Impianto di fornitura servizi > Impianto elettrico > Apparecchiature elettriche | `IfcElectricDistributionBoard`, `IfcSwitchingDevice`, `IfcProtectiveDevice`, `IfcTransformer`, `IfcElectricFlowTreatmentDevice` | Electrical distribution, switching, protection, conversion, or treatment equipment | `high` |
| `5.7.4` — Impianto di fornitura servizi > Impianto elettrico > Reti di distribuzione e terminali | `IfcCableCarrierSegment`, `IfcCableCarrierFitting`, `IfcCableSegment`, `IfcCableFitting`, `IfcJunctionBox`, `IfcOutlet`, `IfcSwitchingDevice`, `IfcLightFixture` | Electrical distribution network or direct endpoint; entity must be a member of the electrical installation | `high` |
| `5.8.0` — Impianto di fornitura servizi > Impianto di telecomunicazioni | `IfcDistributionSystem` | PredefinedType in COMMUNICATION, DATA, TELEPHONE, TV, AUDIOVISUAL, MOBILENETWORK, FIXEDTRANSMISSIONNETWORK | `high` |
| `5.8.1` — Impianto di fornitura servizi > Impianto di telecomunicazioni > Alimentazione | `IfcCableSegment`, `IfcCableFitting`, `IfcJunctionBox` | Incoming telecommunications service connection or dedicated power/feed path | `medium` |
| `5.8.2` — Impianto di fornitura servizi > Impianto di telecomunicazioni > Macchine | `IfcCommunicationsAppliance`, `IfcAudioVisualAppliance`, `IfcMobileTelecommunicationsAppliance` | Active telecommunications equipment, not a passive endpoint | `high` |
| `5.8.3` — Impianto di fornitura servizi > Impianto di telecomunicazioni > Reti di distribuzione e terminali | `IfcCableCarrierSegment`, `IfcCableCarrierFitting`, `IfcCableSegment`, `IfcCableFitting`, `IfcJunctionBox`, `IfcOutlet`, `IfcCommunicationsAppliance` | Telecommunications network membership; outlet PredefinedType appropriate to communication, data, telephone, or audiovisual service | `high` |
| `5.9.0` — Impianto di fornitura servizi > Impianto fisso di trasporto | `IfcDistributionSystem`, `IfcTransportElement` | IfcDistributionSystem PredefinedType=CONVEYING; fixed building transport occurrence | `high` |
| `5.9.1` — Impianto di fornitura servizi > Impianto fisso di trasporto > Alimentazione | `IfcElectricMotor`, `IfcMotorConnection`, `IfcCableSegment` | Power supply and drive connection dedicated to the fixed transport installation | `medium` |
| `5.9.2` — Impianto di fornitura servizi > Impianto fisso di trasporto > Macchine | `IfcTransportElement` | PredefinedType in ELEVATOR, ESCALATOR, MOVINGWALKWAY, LIFTINGGEAR, HAULINGGEAR | `high` |
| `5.9.3` — Impianto di fornitura servizi > Impianto fisso di trasporto > Parti mobili | `IfcTransportElement`, `IfcConveyorSegment` | Occurrence directly represents the moving transport device or conveyor | `medium` |

### Open decisions

- `5.1.1` (domain_review_required): Which physical occurrences does Alimentazione denote here: fuel/fluid supply, electrical feed, or both? AI finding: The undefined Alimentazione leaf does not say whether HVAC supply means fuel, thermal fluid, electric power, or a subset.
- `5.4.1` (domain_review_required): Does Alimentazione mean the electrical feed to extraction machinery, or another supply medium? AI finding: The undefined Alimentazione leaf does not establish whether this is the electrical feed or another input to the aeriform-disposal system.
- `5.7.1` (medium): Confirm that the selected family and stated condition match the intended UNI scope; otherwise record the revised entities or an empty mapping. AI finding: The undefined electrical Alimentazione leaf does not establish whether the main board is supply or distribution, or which generation and storage equipment belongs here.
- `5.8.1` (medium): Confirm that the selected family and stated condition match the intended UNI scope; otherwise record the revised entities or an empty mapping. AI finding: The undefined telecommunications Alimentazione leaf could mean incoming signal/media or electrical power for equipment; these imply different IFC selections.
- `5.9.1` (medium): Confirm that the selected family and stated condition match the intended UNI scope; otherwise record the revised entities or an empty mapping. AI finding: The undefined transport Alimentazione leaf does not establish whether it includes the drive motor and connection, or only incoming power supply.
- `5.9.3` (medium): Confirm that the selected family and stated condition match the intended UNI scope; otherwise record the revised entities or an empty mapping. AI finding: IfcTransportElement may represent the complete machine, while IfcConveyorSegment is a system segment. The intended modelling of Parti mobili is unspecified.

### AI-assessed decisions

- `5.1.3` (accept): Air handlers, chillers, cooling towers and heat exchangers directly treat HVAC air or liquid; retain only occurrences actually serving this central function.
- `5.5.0` (accept): IfcDistributionSystem has MUNICIPALSOLIDWASTE and DISPOSAL types; the UNI definition explicitly includes removal and accumulation of solid waste.
- `5.5.2` (revise): IfcDuctSegment can form a ventilation shaft. IfcChimney is defined for combustion flues, and IfcStackTerminal represents a cap/terminal rather than the shaft.

### Branch approval record

- Decision: `awaiting_user_or_domain_expert_approval`
- Reviewer: *(not recorded)*
- Date: *(not recorded)*
- Revisions/evidence: *(not recorded)*

## 6.0.0 — safety systems

| UNI code and hierarchy | Proposed IFC entities | Conditions | Confidence |
|---|---|---|---|
| `6.0.0` — Impianto di sicurezza | `IfcDistributionSystem` | PredefinedType in FIREPROTECTION, EARTHING, LIGHTNINGPROTECTION, SECURITY | `high` |
| `6.1.0` — Impianto di sicurezza > Impianto antincendio | `IfcDistributionSystem` | PredefinedType=FIREPROTECTION | `high` |
| `6.1.1` — Impianto di sicurezza > Impianto antincendio > Allacciamenti | `IfcPipeSegment`, `IfcPipeFitting`, `IfcFireSuppressionTerminal` | Fire-service connection; terminal limited to PredefinedType=BREECHINGINLET | `high` |
| `6.1.2` — Impianto di sicurezza > Impianto antincendio > Rilevatori e trasduttori | `IfcSensor` | PredefinedType in FIRESENSOR, SMOKESENSOR, HEATSENSOR, COSENSOR, GASSENSOR as justified by the fire-detection design | `high` |
| `6.1.3` — Impianto di sicurezza > Impianto antincendio > Reti di distribuzione e terminali | `IfcPipeSegment`, `IfcPipeFitting`, `IfcValve`, `IfcFireSuppressionTerminal` | Fire-suppression distribution network and its direct terminal occurrences | `high` |
| `6.1.4` — Impianto di sicurezza > Impianto antincendio > Allarmi | `IfcAlarm` | Fire-alarm function and appropriate alarm PredefinedType | `high` |
| `6.2.0` — Impianto di sicurezza > Impianto di messa a terra | `IfcDistributionSystem` | PredefinedType=EARTHING | `high` |
| `6.2.1` — Impianto di sicurezza > Impianto di messa a terra > Reti di raccolta | `IfcCableSegment` | PredefinedType=CONDUCTORSEGMENT; earthing collection/conductor network | `high` |
| `6.2.2` — Impianto di sicurezza > Impianto di messa a terra > Dispersori | `IfcCableSegment` | PredefinedType=CONDUCTORSEGMENT; modelled occurrence acts as an earth electrode, because IFC 4.3.2 has no dedicated earth-electrode entity | `domain_review_required` |
| `6.3.0` — Impianto di sicurezza > Impianto parafulmine | `IfcDistributionSystem` | PredefinedType=LIGHTNINGPROTECTION | `high` |
| `6.3.1` — Impianto di sicurezza > Impianto parafulmine > Elementi di captazione | `IfcCableSegment` | PredefinedType=CONDUCTORSEGMENT; air-termination/lightning-capture role | `domain_review_required` |
| `6.3.2` — Impianto di sicurezza > Impianto parafulmine > Rete | `IfcCableSegment`, `IfcCableFitting` | Lightning-protection down-conductor/network role | `high` |
| `6.3.3` — Impianto di sicurezza > Impianto parafulmine > Dispersori | `IfcCableSegment` | PredefinedType=CONDUCTORSEGMENT; modelled occurrence acts as a lightning earth electrode | `domain_review_required` |
| `6.4.0` — Impianto di sicurezza > Impianto antifurto ed antiintrusione | `IfcDistributionSystem` | PredefinedType=SECURITY | `high` |
| `6.4.1` — Impianto di sicurezza > Impianto antifurto ed antiintrusione > Alimentazione | `IfcCableSegment`, `IfcElectricFlowStorageDevice` | Power supply dedicated to the anti-intrusion system | `medium` |
| `6.4.2` — Impianto di sicurezza > Impianto antifurto ed antiintrusione > Rilevatori e trasduttori | `IfcSensor` | PredefinedType=CONTACTSENSOR, MOVEMENTSENSOR, SOUNDSENSOR, or other explicitly justified intrusion-detection sensor | `high` |
| `6.4.3` — Impianto di sicurezza > Impianto antifurto ed antiintrusione > Rete | `IfcCableCarrierSegment`, `IfcCableSegment`, `IfcCableFitting`, `IfcJunctionBox` | Security/anti-intrusion communication or power network membership | `high` |
| `6.4.4` — Impianto di sicurezza > Impianto antifurto ed antiintrusione > Allarmi | `IfcAlarm` | Anti-intrusion alarm function | `high` |

### Open decisions

- `6.2.2` (domain_review_required): Is modelling an earth electrode as IfcCableSegment/CONDUCTORSEGMENT acceptable in the intended authoring workflows? AI finding: IFC has no dedicated earth-electrode entity; whether an electrode is modelled as IfcCableSegment/CONDUCTORSEGMENT is a project convention.
- `6.3.1` (domain_review_required): Is an air-termination/capture element represented as IfcCableSegment/CONDUCTORSEGMENT in the intended workflows? AI finding: Whether lightning air-termination elements are modelled as IfcCableSegment/CONDUCTORSEGMENT is a project convention.
- `6.3.3` (domain_review_required): Is a lightning earth electrode represented as IfcCableSegment/CONDUCTORSEGMENT in the intended workflows? AI finding: Whether lightning earth electrodes are modelled as IfcCableSegment/CONDUCTORSEGMENT is a project convention.

### AI-assessed decisions

- `6.4.1` (accept): Dedicated power cabling and a battery or UPS can directly supply the anti-intrusion system under the recorded condition.

### Branch approval record

- Decision: `awaiting_user_or_domain_expert_approval`
- Reviewer: *(not recorded)*
- Date: *(not recorded)*
- Revisions/evidence: *(not recorded)*

## 7.0.0 — internal equipment

| UNI code and hierarchy | Proposed IFC entities | Conditions | Confidence |
|---|---|---|---|
| `7.0.0` — Attrezzatura interna | `IfcFurnishingElement` | Fixed or modelled internal equipment/furnishing occurrence | `medium` |
| `7.1.0` — Attrezzatura interna > Arredo domestico | `IfcFurniture` | Domestic furnishing occurrence | `high` |
| `7.1.1` — Attrezzatura interna > Arredo domestico > Pareti contenitore | `IfcFurniture` | PredefinedType=SHELF or TECHNICALCABINET only when the complete occurrence is an integrated storage wall; exclude individual modular panels | `medium` |
| `7.2.0` — Attrezzatura interna > Blocco servizi | *(empty)* | A prefabricated service block has no reliable dedicated IFC 4.3.2 occurrence; model its constituent services unless a governed project-specific assembly convention is adopted | `domain_review_required` |

### Open decisions

- `7.2.0` (domain_review_required): Should Blocco servizi remain unmapped, or is there a governed IfcElementAssembly convention that reviewers expect? AI finding: The source defines an aggregated service block, but does not establish whether a governed IfcElementAssembly convention exists or an empty mapping is intended.

### AI-assessed decisions

- `7.0.0` (accept): An internal furnishing occurrence can directly receive the broad internal-equipment code; the mapping need not cover every descendant kind.
- `7.1.1` (revise): IfcFurniture can represent a complete storage cabinet or wall. IfcSystemFurnitureElement/PANEL is a component of modular furniture.

### Branch approval record

- Decision: `awaiting_user_or_domain_expert_approval`
- Reviewer: *(not recorded)*
- Date: *(not recorded)*
- Revisions/evidence: *(not recorded)*

## 8.0.0 — external equipment

| UNI code and hierarchy | Proposed IFC entities | Conditions | Confidence |
|---|---|---|---|
| `8.0.0` — Attrezzatura esterna | `IfcFurnishingElement` | Outdoor furnishing occurrence directly classifiable as external equipment; this mapping does not cover the entire UNI aggregate | `medium` |
| `8.1.0` — Attrezzatura esterna > Arredi esterni collettivi | `IfcFurniture` | Collective outdoor furnishing occurrence and exterior/site placement | `high` |
| `8.2.0` — Attrezzatura esterna > Allestimenti esterni | *(empty)* | The external-installations aggregate spans unrelated fences and pavements; classify the concrete child occurrence instead | `medium` |
| `8.2.1` — Attrezzatura esterna > Allestimenti esterni > Recinzioni | `IfcRailing`, `IfcDoor` | IfcRailing PredefinedType=FENCE; IfcDoor PredefinedType=GATE | `high` |
| `8.2.2` — Attrezzatura esterna > Allestimenti esterni > Pavimentazione esterna | `IfcPavement` | External pavement occurrence; use IfcCovering only if separately classifying a dependent finish | `high` |

### Open decisions

No unresolved AI-assessment question remains in this branch; explicit branch approval is still unrecorded.

### AI-assessed decisions

- `8.0.0` (revise): An outdoor furnishing can directly receive the broad external-equipment code, although IfcFurnishingElement does not cover fences or pavements. Clarified the condition.
- `8.2.0` (accept): The source aggregate includes outdoor installations and boundaries; fences and pavements are separately mapped at child level. No single concrete occurrence covers this aggregate.

### Branch approval record

- Decision: `awaiting_user_or_domain_expert_approval`
- Reviewer: *(not recorded)*
- Date: *(not recorded)*
- Revisions/evidence: *(not recorded)*

## Approval procedure

1. Review every row in a branch, including the conditions that cannot be expressed in bSDD's entity-name list.
2. Resolve each open decision as keep, revise, or intentionally empty.
3. Record reviewer identity, review date, evidence/note, and branch state in the status JSON.
4. Regenerate the matrix if selections change and rerun P03/P04 tests.
5. Only after all eight branches are explicitly approved may P06 and P07 treat the mapping set as approved.
