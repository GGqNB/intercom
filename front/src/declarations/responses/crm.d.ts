export namespace Crm {
  export interface CityBrief {
    name: string,
    id: number,
  }

  export interface CityBare {
    name: string
  }

  export interface HouseBrief {
    id: number,
    name: string,
    geo_adress: string,
    flat_count: number,
    city: CityBrief,
  }

  export interface HouseBare {
    name: string,
    geo_adress: string,
    flat_count: number,
    city_id: number
  }

  export interface EntryBrief {
    id: number,
    name: string,
    flat_first: number,
    flat_last: number,
    house: HouseBrief,
  }

  export interface EntryBare {
    name: string,
    flat_first: number,
    flat_last: number,
    house_id: number
  }

  export interface IntercomBrief {
    id: number,
    name: string,
    entry: EntryBrief
  }

  export interface IntercomBare {
    name: string,
    tech_name: string,
    entry_id: number
  }
}
