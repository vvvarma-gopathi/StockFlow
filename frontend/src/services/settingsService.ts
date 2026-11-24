import { api } from "./api";

export interface OrganizationSettings {
  default_low_stock_threshold: number;
  default_low_stock_threshold_enabled: boolean;
}

export async function getOrganizationSettings(): Promise<OrganizationSettings> {
  const response = await api.get<OrganizationSettings>("/settings");
  return response.data;
}

export async function updateOrganizationSettings(
  settings: OrganizationSettings,
): Promise<OrganizationSettings> {
  const response = await api.put<OrganizationSettings>(
    "/settings",
    settings,
  );
  return response.data;
}
