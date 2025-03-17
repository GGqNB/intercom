export namespace User {
  export interface UserBrief {
    phone: string,
    uuid: string,
    first_name: string,
    last_name: string,
  }
  
  export interface UserData {
    username: string,
    password: string,
  }

  export interface UserBare {
    uuid: string,
  }

  export interface UserPhone {
    phone: string,
  }

  export interface UserProfileBrief {
    uuid: string,
    first_name: string,
    last_name: string,
  }

  export interface UserToken{
    access_token: string
    token_type: string
  }
  export interface UserNewBare{
    id: number,
    email: string,
    password: string,
    is_active: boolean,
    is_superuser: boolean,
    is_verified: boolean,
    fio: string,
    phone_number : number,
  } 
}
