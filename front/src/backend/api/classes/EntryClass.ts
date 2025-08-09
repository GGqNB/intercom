import axios from 'axios';
import { Crm } from 'src/declarations/responses/crm';
import { ENTRY } from 'src/backend/endpoints/entry';
import { PaginatedList } from 'src/declarations/components/pagination';
import { ResponceObject } from 'src/declarations/responses/default';

export type EntryList = PaginatedList<Crm.EntryBrief>
export type EntryResponce = ResponceObject<Crm.EntryBare>

export default class EntryApi {

  public static async list(params: any): Promise<EntryList> {
    const responseData: EntryList = await axios({
      ...ENTRY.LIST,
      params
    })
      .then((r): EntryList => r.data);

    return responseData;
  }

  public static async create(data : Crm.EntryBare): Promise< EntryResponce> {
    const responseData: EntryResponce = await axios({
      ...ENTRY.CREATE,
      data,
    })
      .then((r):  EntryResponce => r.data);

    return responseData;
  }
  public static async update(data : Crm.EntryBare, id: number): Promise<EntryResponce> {
    const responseData: EntryResponce = await axios({
      ...ENTRY.UPDATE(id),
      data,
    })
      .then((r):  EntryResponce => r.data);

    return responseData;
  }
    public static async delete(id: number): Promise<{success: boolean}> {
    const responseData: {success: boolean} = await axios({
      ...ENTRY.DELETE(id),
    })
      .then((r): { success: boolean} => r.data);

    return responseData;
  }
}
