import type { PermissionList, Role } from './role.js';

export interface HasFio {
  firstName: string;
  lastName: string;
  middleName?: string;
}

export interface UserBrief extends HasFio {
  id: number;
  roleId: number;
  departmentId: number;
  email: string;
}

export interface UserBriefWithDepartment extends UserBrief {
  department: any | null;
}

export interface SystemUserIn extends HasFio {
  departmentId: number | null;
  roleId: number | null;
  login: string;
  email: string;
  phone: string;
  post: string | null;
  password: string | null;
  birthday: string | null;
  isActive: boolean;
}

export type SystemUserUpdate = Omit<SystemUserIn, 'password'> &
  Partial<Pick<SystemUserIn, 'password'>>;

export type WithEmail<T> = T & { isSendEmail: boolean };

export interface SystemUser extends SystemUserIn {
  id: number;
  department: any | null;
  role: null | Role;
  loginAt: any;
  deletedAt: any;
  createdAt: any;
}

export type SystemUsers = Array<SystemUser>;

export interface User {
  id: number;
  lastName: string;
  firstName: string;
  middleName: string;
  isTempPassword: boolean;
}
export interface UserHistoryInfo extends SystemUser {
  imageId?: string;
  verificatedAt?: string;
  verificatedBy?: number;
}

export type LoginHistory = {
  id: number;
  ip: string;
  fingerprint: object;
  createdAt: string;
};

export type UserLoginHistory = {
  [K in keyof LoginHistory]: LoginHistory[K];
} & {
  user: UserHistoryInfo;
};
