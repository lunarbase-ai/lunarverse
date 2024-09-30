# Copyright © 2024 Lunarbase (https://lunarbase.ai/) <contact@lunarbase.ai>
#
# SPDX-License-Identifier: GPL-3.0-or-later

GENE_ID = """
{  
  molecularProfiles(
    name: "%s",
  ) {
        nodes {
          id
        }
    }
}
"""

GENE_DETAILS = """
{  
  gene(
    id: %d
  ) {
    comments {
      edges {
        node {
          id
        }
      }
    },
    description,
    entrezId,
    events {
      edges {
        node {
          id
        }
      }
    },
    flagged,
    flags {
      edges {
        node {
          id
        }
      }
    },
    id,
    link,
    myGeneInfoDetails,
    name,
    revisions {
      edges {
        node {
          id
        }
      }
    },
    sources {
      id
    },
    variants {
      edges {
        node {
          id
        }
      }
    }
  } 
}
"""

SOURCE_DETAILS = """
{  
  source(id: %d) {
    abstract
    ascoAbstractId
    authorString
    citation
    citationId
    clinicalTrials {
      id
    }
    comments {
      edges {
        node {
          id
        }
      }
    }
    displayType
    events {
      edges {
        node {
          id
        }
      }
    }
    fullJournalTitle
    fullyCurated
    id
    journal
    lastCommentEvent {
      id
    }
    link
    name
    openAccess
    pmcId
    publicationDate
    publicationDay
    publicationMonth
    publicationYear
    sourceType
    sourceUrl
    title
  }
}
"""

EVIDENCE_ID_THERAPY = """
{  
  evidenceItems(
    molecularProfileName: "%s",
    therapyName: "%s",
  ) {
    nodes {
      id
    }
  }
}
"""

EVIDENCE_ID_DISEASE = """
{  
  evidenceItems(
    molecularProfileName: "%s",
    diseaseName: "%s",
  ) {
    nodes {
      id
    }
  }
}
"""

EVIDENCE_DETAILS = """
{  
  evidenceItem(id: %d) {
    assertions {
      id
    }
    comments {
      edges {
        node {
          id
        }
      }
    }
    description
    disease {
      id
    }
    evidenceDirection
    evidenceLevel
    evidenceRating
    evidenceType
    flagged
    flags {
      edges {
        node {
          id
        }
      }
    }
    id
    link
    molecularProfile {
      id
    }
    name
    phenotypes {
      id
    }
    rejectionEvent {
      id
    }
    revisions {
      edges {
        node {
          id
        }
      }
    }
    significance
    source {
      id
    }
    status
    therapies {
      id
    }
    therapyInteractionType
    variantOrigin
  }
}
"""

THERAPY_DETAILS = """
{  
  therapy(id: %d) {
    id
    link
    myChemInfo {
      chebiDefinition
      chebiId
      chemblId
      chemblMoleculeType
      drugbankId
      firstApproval
      inchikey
      pharmgkbId
      pubchemCid
      rxnorm
    }
    name
    ncitId
    therapyAliases
    therapyUrl
  }
}
"""

DISEASE_DETAILS = """
{  
  disease(id: %d) {
    diseaseAliases
    diseaseUrl
    displayName
    doid
    id
    link
    myDiseaseInfo {
      doDef
      icd10
      icdo
      mesh
      mondoDef
      omim
    }
    name
  }
}
"""