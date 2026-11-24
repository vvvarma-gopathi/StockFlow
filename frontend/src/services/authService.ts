import { ACCESS_TOKEN_STORAGE_KEY, api } from "./api";

export interface SignupPayload {
  organization_name: string;
  email: string;
  password: string;
}

export interface SignupResponse {
  id: number;
  email: string;
  organization: {
    id: number;
    name: string;
  };
}

export interface LoginPayload {
  email: string;
  password: string;
}

export interface AccessTokenResponse {
  access_token: string;
  token_type: "bearer";
  expires_in: number;
}

export async function signup(payload: SignupPayload): Promise<SignupResponse> {
  const response = await api.post<SignupResponse>("/auth/signup", payload);
  return response.data;
}

export async function login(
  payload: LoginPayload,
): Promise<AccessTokenResponse> {
  const response = await api.post<AccessTokenResponse>("/auth/login", payload);
  sessionStorage.setItem(ACCESS_TOKEN_STORAGE_KEY, response.data.access_token);
  return response.data;
}

export function logout(): void {
  sessionStorage.removeItem(ACCESS_TOKEN_STORAGE_KEY);
}