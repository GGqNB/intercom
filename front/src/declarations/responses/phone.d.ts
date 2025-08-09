import { Default } from './default'
import { Locks } from './crm'

export namespace Phone {
  export interface PhoneBrief {
    phone: string,
    id: number,
    nfc_keys : Array<Default.DefaultResponse>
  }

  export interface PhoneBare {
   phone: string,
  }

}
