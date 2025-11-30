export interface UserWarehouse {
  id: number;
  user_id: number;
  warehouse_name: string;
  created_at?: string;
  updated_at?: string;
}

export interface FieldMeta {
  field: string;
  label: string;
  width: string;
  prop: string;
}
