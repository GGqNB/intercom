export namespace IntercomCall {
  export interface CallBare {
    apartment_number: number;
    hash_room: string;
    indentifier: string;
    blockDevice: BlockDevice;
  }
  export interface BlockDevice {
    id: number;
    name: string;
    owner_id: string;
    addr: string;
    status: number;
    is_owner: boolean;
    id_permission: number;
    is_one_access: boolean;
  }

  export interface CallsBrief {
    apartment_number: number;
    status: string;
    caller_id: number;
    answered_by: string;
  }
}
