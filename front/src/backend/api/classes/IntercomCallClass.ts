import axios from 'axios';
import { IntercomCall } from 'src/declarations/responses/intercom-call';
import { INTERCOM_CALL } from 'src/backend/endpoints/intercom-call';


// export type IntercomList = PaginatedList<Crm.IntercomBrief>
// export type IntercomResponce = ResponceObject<Crm.CityBare>

export default class IntercomCallApi {

  public static async call(data : IntercomCall.CallBare): Promise<{ mes:string }> {
    const responseData: { mes:string } = await axios({
      ...INTERCOM_CALL.CALL,
      data 
    })
      .then((r): { mes:string } => r.data);

    return responseData;
  }

  public static async answer(apartment_number : number): Promise<{ mes:string }> {
    const responseData: { mes:string } = await axios({
      ...INTERCOM_CALL.ANSWER_CALL(apartment_number),
    })
      .then((r):  { mes:string } => r.data);

    return responseData;
  }

 public static async open(lock_id: number, code: string, local_url_base: string): Promise<{ proxy_response: string }> {
    const responseData: { proxy_response: string } = await axios({
      ...INTERCOM_CALL.OPEN(lock_id, code, local_url_base),
    })
      .then((r):  { proxy_response: string } => r.data);

    return responseData;
  }

    public static async abort(apartment_number : number): Promise<{ mes:string }> {
    const responseData: { mes:string } = await axios({
      ...INTERCOM_CALL.ABORT_CALL(apartment_number),
    })
      .then((r):  { mes:string } => r.data);

    return responseData;
  }
}