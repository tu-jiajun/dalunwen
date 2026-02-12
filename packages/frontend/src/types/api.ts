export interface ApiResponse<T = any> {
  code: number;
  msg: string;
  data: T;
}

export interface PageResult<T> {
  list: T[];
  total: number;
  pageNum?: number;
  pageSize?: number;
}
