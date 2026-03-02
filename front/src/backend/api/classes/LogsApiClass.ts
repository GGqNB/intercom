import axios from 'axios';
import { Crm } from 'src/declarations/responses/crm';
import { LOGS } from 'src/backend/endpoints/logs';
export type LogsData = { data: Crm.LogsBrief[], status: string}
export default class LogsApi {

  public static async list(): Promise<LogsData> {
    const responseData: LogsData = await axios({
      ...LOGS.LIST,
    })
      .then((r): LogsData => r.data);

    return responseData;
  }
  
   public static async clear(): Promise<{status :string}> {
    const responseData: {status :string} = await axios({
      ...LOGS.CLEAR,
    })
      .then((r): {status :string} => r.data);

    return responseData;
  }
  
}
