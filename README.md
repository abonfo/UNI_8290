# The UNI 8290 buildingSMART bSDD dictionary
 
The UNI 8290 is an **italian classification system** for the construction industry, used to decompose the building system into functional parts.

We converted this national standard into a **bSDD json dictionary** and published it into the buildingSMART bSDD database. This repository contains the json dictionary published into the bSDD database and will be updated if needed.

Each classification level in the UNI 8290 json dictionary contains one or more references to those buildingSMART **IFC4.3 entities** that are the most related to the level.

## The UNI 8290 bSDD dictionary model

The UNI 8290 dictionary is available in the buildingSMART databse, and its structure can be viewed at this link: https://search.bsdd.buildingsmart.org/uri/AnBo/UNI8290/1.0.

The UNI 8290 bSDD dictionary is mapped against the `Dictionary` and the `Class` concepts of the [buildingSMART Data Dictionary model](https://github.com/buildingSMART/bSDD/blob/master/Documentation/bSDD%20JSON%20import%20model.md). 

There are no fields for the following concepts: `Property`, `ClassProperty`, `ClassRelation`, `AllowedValue` and `PropertyRelation`.

The `Dictionary` concept contains the following fields: 

- `ModelVersion`,
- `OrganizationCode`,
- `DictionaryName`,
- `DictionaryCode`,
- `DictionaryVersion`,
- `ReleaseDate`,
- `Status`,
- `MoreInfoUrl`,
- `UseOwnUri`,
- `LanguageIsoCode`,
- `License`,
- `LicenseUrl`,
- `QualityAssuranceProcedure`,
- `Classifications`.

The `Class` concept contains the following fields:

- `ClassType`,
- `ParentClassCode` (only child classes),
- `Code`,
- `ReferenceCode`,
- `Name`,
- `Definition`,
- `RelatedIfcEntityNamesList`,
- `Status`,
- `ActivationDateUtc`,
- `VersionDateUtc`,
- `RevisionNumber`,
- `CreatorLanguageIsoCode`,
- `CountryOfOrigin`,
- `CountriesOfUse`.


## The UNI 8290 bSDD codes, classes and relations

Each code number reflects the UNI 8290 **numbering structure**, with the addition of the trailing zeroes to the first and second classifications:

- X.0.0 for the **Technological units classes** (Classi di unità tecnologiche),
- X.X.0 for the **Technological units** (Unità tecnologiche).

Each class has a **parent/child relation** to other classes to reflect the UNI 8290 decomposition structure. The parent/child relation is defined with the `ParentClassCode` field of the bSDD model.

Each UNI 8290 class contain one or more **references to the main IFC 4.3 classes** to which the building objects can be related to. These references can be updated in the future to reflect the IFC classes evolution.  

## The UNI 8290 classification

The UNI 8290 building classification system is based on **users needs and on building performance** requirements. The construction elements are not classified based on their physical characteristics but on their main function inside the building.

This standard provides the classification of the technological units and the technical elements that compose the technological system. The decomposition defines three levels of definitions:

- **Technological units classes**: these are the root elements that define the overall function of each section (i.e. Load Bearing Structure; Internal Partitions).
- **Technological units**: these define functions necessary to achieve predetermined performances. They define a more specific function inside the previous building classes (i.e. for Load Bearing Structures: Foundation structures, Elevation structures, Containment structures; for Internal Partitions: Internal vertical partitions, Internal horizontal partitions).
- **Technical elements classes** : these are the elements capable of performing specific functions (i.e. for Foundation Structures: Direct foundations, Indirect foundations; for Internal vertical partitions: Internal vertical walls, Internal vertical doors).

This standard do not specify other child levels (4th, 5th, and others), but allows the classification to be extended beyond the 3rd level assuming these requirements:

- the levels beyond the 3rd level must use a more granular subdivision of elements;
- in each level the elements must be grouped by homogeneous functions;
- in a single level there can be a decomposition based on custom criteria (materials, construction tecnique, complexity, etc.). 

## License

The version 1.0 of the dictionary is distributed under the [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) license.
