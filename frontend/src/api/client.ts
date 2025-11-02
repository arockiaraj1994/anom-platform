import axios from 'axios';

const baseURL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const api = axios.create({
  baseURL,
  headers: { 'Content-Type': 'application/json' },
});

export interface BusinessDefinition {
  id: string;
  name: string;
  description?: string | null;
  created_at: string;
}

export interface BusinessCreate {
  name: string;
  description?: string | null;
}

export interface BusinessUpdate {
  name?: string;
  description?: string | null;
}

export type FieldDataType = 'string' | 'integer' | 'float' | 'boolean' | 'datetime';

export interface FieldDefinition {
  id: string;
  business_id: string;
  name: string;
  data_type: FieldDataType;
  required: boolean;
  description?: string | null;
  created_at: string;
}

export interface FieldDefinitionCreate {
  name: string;
  data_type: FieldDataType;
  required: boolean;
  description?: string | null;
}

export async function listBusinesses() {
  const res = await api.get<BusinessDefinition[]>('/businesses/');
  return res.data;
}

export async function createBusiness(payload: BusinessCreate) {
  const res = await api.post<BusinessDefinition>('/businesses/', payload);
  return res.data;
}

export async function getBusiness(id: string) {
  const res = await api.get<BusinessDefinition>(`/businesses/${id}`);
  return res.data;
}

export async function updateBusiness(id: string, payload: BusinessUpdate) {
  const res = await api.patch<BusinessDefinition>(`/businesses/${id}`, payload);
  return res.data;
}

export async function listFields(businessId: string) {
  const res = await api.get<FieldDefinition[]>(`/businesses/${businessId}/fields`);
  return res.data;
}

export async function addField(businessId: string, payload: FieldDefinitionCreate) {
  const res = await api.post<FieldDefinition>(`/businesses/${businessId}/fields`, payload);
  return res.data;
}
