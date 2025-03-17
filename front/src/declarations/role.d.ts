export type PermissionItem = string;

export type PermissionList = Array<PermissionItem>;

export interface Role {
  id: null | number;
  name: string;
  permissions: PermissionList;
  description: string;
  deletedAt?: null | string;
  isCore: boolean;
}

export type RoleList = Array<Role>;

export type RoleHistory = {
  version: number;
  changedAt: string;
  createdBy: number;
  permission: string;
};

type RoleHistoryList = {
  [key: string]: Array<RoleHistory>;
};

export type RoleUpdate = {
  name: string;
  description: string;
  permissions: string[];
};

export type RoleBrief = {
  id: number;
  name: string;
};

export type PermissionTranslated = {
  permission: string;
  translated: string;
  groupName?: string;
  roles: RoleBrief[];
};
