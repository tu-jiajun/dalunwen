export interface ClinicalTrialUSA {
  nct_number: string;
  study_title: string;
  study_url: string;
  acronym: string | null;
  study_status: string;
  brief_summary: string;
  study_results: string;
  conditions: string;
  interventions: string;
  primary_outcome_measures: string;
  secondary_outcome_measures: string | null; // 原生联合类型，兼容性最好
  other_outcome_measures: string | null;
  sponsor: string;
  collaborators: string | null;
  sex: string;
  age: string;
  phases: string | null;
  enrollment: number;
  funder_type: string;
  study_type: string;
  study_design: string;
  other_ids: string;
  start_date: string;
  primary_completion_date: string;
  completion_date: string;
  first_posted: string;
  results_first_posted: string | null;
  last_update_posted: string;
  locations: string;
  study_documents: string | null;
}

export interface ClinicalTrialChina {
  reg_number: string;
  study_title: string;
  study_url: string;
  acronym: string | null;
  study_status: string;
  brief_summary: string;
  study_results: string;
  conditions: string;
  interventions: string;
  primary_outcome_measures: string;
  secondary_outcome_measures: string | null; // 原生联合类型，兼容性最好
  other_outcome_measures: string | null;
  sponsor: string;
  collaborators: string | null;
  sex: string;
  age: string;
  phases: string | null;
  enrollment: number;
  funder_type: string;
  study_type: string;
  study_design: string;
  other_ids: string;
  start_date: string;
  primary_completion_date: string;
  completion_date: string;
  first_posted: string;
  results_first_posted: string | null;
  last_update_posted: string;
  locations: string;
  study_documents: string | null;
}

export type ClinicalTrial = ClinicalTrialUSA | ClinicalTrialChina;
