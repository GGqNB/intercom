import axios from 'axios';
import { Crm } from 'src/declarations/responses/crm';
import { IntercomCall } from 'src/declarations/responses/intercom-call';
import { STOWN } from 'src/backend/endpoints/stown';
import { PaginatedList } from 'src/declarations/components/pagination';
import { ResponceObject } from 'src/declarations/responses/default';

export type IntercomList = PaginatedList<Crm.IntercomBrief>
export type IntercomResponce = ResponceObject<Crm.CityBare>

export default class StownApi {


  public static async lockDevices<T>(params?: T): Promise<IntercomCall.BlockDevice[]> {
    const responseData: IntercomCall.BlockDevice[] = await axios({
      ...STOWN.STOWN_DEVICES,
      params 
    })
      .then((r): IntercomCall.BlockDevice[] => r.data);

    return responseData;
  }
    public static async homes<T>(params?: T): Promise<IntercomCall.BlockDevice[]> {
    const responseData: IntercomCall.BlockDevice[] = await axios({
      ...STOWN.HOMES,
      params 
    })
      .then((r): IntercomCall.BlockDevice[] => r.data);

    return responseData;
  }

    public static async flats<T>(home_id: number, params?: T ): Promise<IntercomCall.BlockDevice[]> {
    const responseData: IntercomCall.BlockDevice[] = await axios({
      ...STOWN.FLATS(home_id),
      params 
    })
      .then((r): IntercomCall.BlockDevice[] => r.data);

    return responseData;
  }
}
