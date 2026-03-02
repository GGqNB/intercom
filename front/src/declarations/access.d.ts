import { PermissionList, Role } from './role';
import { WithRelations } from './shared';
import { SystemUser, User } from './user';

export type UserInfo = {
  id: number;
  attachment_id: string | null;
  is_active: boolean;
  name: string | null;
  family_name: string | null;
  patronymic: string | null;
  birthday: string | Date | null;
  email: null | string;
  phone: string | null;
  sex: string | null;
  photo: string | null,
  born_date: Date| string | null,
  email_verified_at : Date| string |null,
  created_at: string | Date | null;
  updated_at: string | Date | null;
  last_login: string | Date | null;
  deleted_at: string | Date | null;
  role: null | Role;
};

export interface AuthTokens {
  token: string;
  refreshToken: string;
}

export interface LoginUserInfo extends AuthTokens{
  user: UserInfo;
}

export interface ResetPassword {
  email: string;
}