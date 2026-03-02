import { Address } from './responses/network';
import { LevelPreparation } from './responses/level-preparation.d';
import { TaxRateBare, TaxRateBrief } from './responses/tax-rate.d';
import { TaxTypeBare, TaxTypeBrief } from './responses/tax-type.d';
import { AgeCategory } from './responses/age-categories.d';
import { SocialNetwork } from './responses/social-networks';
import { Role } from './responses/roles';

export type RowVariant = Address.CityBrief
                        | Address.RegionBrief
                        | LevelPreparation.LevelPreparationBrief
                        | TaxTypeBrief
                        | TaxRateBrief
                        | AgeCategory.AgeCategoryBrief
                        | Role.RoleBrief;

export type FormVariant = Address.CityBare
                        | Address.RegionBare
                        | LevelPreparation.LevelPreparationBare
                        | TaxTypeBare
                        | TaxRateBare
                        | SocialNetwork.SocialNetworkBare
                        | AgeCategory.AgeCategoryBare;
