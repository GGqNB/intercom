export namespace Locks {
  export interface LocksBrief {
    name: string,
    address: string,
    sub_address: number,
    id: number,
    nfc_keys?: Array<NFCkeyBrief>,
    lock_type?: LocksTypeBrief,
    title : string,
    open_time: number,
    is_new?: boolean,
    close_time: number,
  }

  export interface LocksBare {
    name: string
    address: string,
    sub_address: number,
    lock_type_id: number,
    title : string,
    open_time: number,
    close_time: number,
    is_new?: boolean,
    geo_address : string,
  }

  //возможно bare
  export interface LocksTypeBrief {
    name: string,
    id: number,

  }
  export interface NFCkeyBrief {
    key: string,
    id: number,

  }

  export interface LockInNfc{
    id: number,
    title: string,
    name: string,
    address: string,
    lock_type: LocksTypeBrief,
  }

}
