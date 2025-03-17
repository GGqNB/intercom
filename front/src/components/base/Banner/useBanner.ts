import { computed, reactive } from 'vue';

export type BannerType = 'error' | 'info' | 'success' | 'warning';

export const bannerTypes: Array<BannerType> = ['error', 'info', 'success', 'warning'];

type BannerMessageObject = {
  visibility: boolean;
  type: BannerType;
  text: string;
};

const defaultBannerMessageObject: BannerMessageObject = {
  visibility: false,
  type: 'info',
  text: '',
};

export const useBanner = () => {
  let banner: BannerMessageObject = reactive({ ...defaultBannerMessageObject });

  const isBannerVisible = computed(() => banner.visibility);

  const bannerText = computed(() => banner.text);

  const hideBanner = (): void => {
    banner.visibility = false;
  };

  const showBanner = (): void => {
    banner.visibility = true;
  };

  const showSuccessText = (text: string): void => {
    banner.type = 'success';
    banner.text = text;
    showBanner();
  };

  const showInfoText = (text: string): void => {
    banner.type = 'info';
    banner.text = text;
    showBanner();
  };

  const showErrorText = (text: string): void => {
    banner.type = 'error';
    banner.text = text;
    showBanner();
  };

  const showWarningText = (text: string): void => {
    banner.type = 'warning';
    banner.text = text;
    showBanner();
  };

  const resetBanner = (): void => {
    banner = { ...defaultBannerMessageObject };
  };

  return {
    banner,
    isBannerVisible,
    bannerText,
    hideBanner,
    showBanner,
    showSuccessText,
    showInfoText,
    showErrorText,
    showWarningText,
    resetBanner,
  };
};
