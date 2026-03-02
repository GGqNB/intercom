import axios from 'axios';
import { Crm } from 'src/declarations/responses/crm';
import { HOUSE } from 'src/backend/endpoints/house';
import { PaginatedList } from 'src/declarations/components/pagination';
import { ResponceObject } from 'src/declarations/responses/default';

export type HouseList = PaginatedList<Crm.HouseBrief>
export type HouseResponce = ResponceObject<Crm.HouseBare>

export default class HouseApi {

  public static async list(params: any): Promise<HouseList> {
    const responseData: HouseList = await axios({
      ...HOUSE.LIST,
      params
    })
      .then((r): HouseList => r.data);

    return responseData;
  }

  public static async create(data : Crm.HouseBare): Promise< HouseResponce> {
    const responseData: HouseResponce = await axios({
      ...HOUSE.CREATE,
      data,
    })
      .then((r):  HouseResponce => r.data);

    return responseData;
  }
  public static async update(data : Crm.HouseBare, id: number): Promise< HouseResponce> {
    const responseData: HouseResponce= await axios({
      ...HOUSE.UPDATE(id),
      data,
    })
      .then((r):  HouseResponce => r.data);

    return responseData;
  }
    public static async delete(id: number): Promise<{success: boolean}> {
    const responseData: {success: boolean} = await axios({
      ...HOUSE.DELETE(id),
    })
      .then((r): { success: boolean} => r.data);

    return responseData;
  }
}
