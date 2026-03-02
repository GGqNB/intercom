import axios from 'axios';
import { Crm } from 'src/declarations/responses/crm';
import { CITY } from 'src/backend/endpoints/city';
import { PaginatedList } from 'src/declarations/components/pagination';

export type CityList = PaginatedList<Crm.CityBrief>

export default class CityApi {

  public static async list(params : any): Promise<CityList> {
    const responseData: CityList = await axios({
      ...CITY.LIST,
      params
    })
      .then((r): CityList => r.data);

    return responseData;
  }

  public static async create(data : Crm.CityBare): Promise< Crm.CityBare> {
    const responseData: Crm.CityBare = await axios({
      ...CITY.CREATE,
      data,
    })
      .then((r):  Crm.CityBare => r.data);

    return responseData;
  }
  public static async update(data : Crm.CityBare, id: number): Promise< Crm.CityBare> {
    const responseData: Crm.CityBare= await axios({
      ...CITY.UPDATE(id),
      data,
    })
      .then((r):  Crm.CityBare => r.data);

    return responseData;
  }
    public static async delete(id: number): Promise<{success: boolean}> {
    const responseData: {success: boolean} = await axios({
      ...CITY.DELETE(id),
    })
      .then((r): { success: boolean} => r.data);

    return responseData;
  }
}
