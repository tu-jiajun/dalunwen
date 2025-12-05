export interface ClinicalTrialWarehouse {
  id: number;
  warehouse_id: number;
  nct_number: string | null;
  reg_number: string | null;
  dynamic_extra_fields: string | null;
  created_at?: string;
  updated_at?: string;
}

export interface ClinicalTrialWarehouseWithDetails extends ClinicalTrialWarehouse {
  clinicalUSA?: any;
  clinicalChina?: any;
}