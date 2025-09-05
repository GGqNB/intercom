import axios from 'axios';
import { Crm } from 'src/declarations/responses/crm';
import { IntercomCall } from 'src/declarations/responses/intercom-call';
import { INTERCOM } from 'src/backend/endpoints/intercom';
import { PaginatedList } from 'src/declarations/components/pagination';
import { ResponceObject } from 'src/declarations/responses/default';

export type IntercomList = PaginatedList<Crm.IntercomBrief>
export type IntercomResponce = ResponceObject<Crm.CityBare>

export default class IntercomApi {

  public static async list<T>(params?: T): Promise<IntercomList> {
    const responseData: IntercomList = await axios({
      ...INTERCOM.LIST,
      params 
    })
      .then((r): IntercomList => r.data);

    return responseData;
  }

  public static async stownDevices<T>(params?: T): Promise<IntercomCall.BlockDevice[]> {
    const responseData: IntercomCall.BlockDevice[] = await axios({
      ...INTERCOM.STOWN_DEVICES,
      params 
    })
      .then((r): IntercomCall.BlockDevice[] => r.data);

    return responseData;
  }


  public static async create(data : Crm.IntercomBare): Promise< IntercomResponce> {
    const responseData: IntercomResponce = await axios({
      ...INTERCOM.CREATE,
      data,
    })
      .then((r):  IntercomResponce => r.data);

    return responseData;
  }
  public static async update(data : Crm.IntercomBare, id: number): Promise<IntercomResponce> {
    const responseData: IntercomResponce = await axios({
      ...INTERCOM.UPDATE(id),
      data,
    })
      .then((r): IntercomResponce => r.data);

    return responseData;
  }
    public static async delete(id: number): Promise<{success: boolean}> {
    const responseData: {success: boolean} = await axios({
      ...INTERCOM.DELETE(id),
    })
      .then((r): { success: boolean} => r.data);

    return responseData;
  }
}
