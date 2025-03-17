import { boot } from 'quasar/wrappers';
import SPage from 'src/components/page/SPage.vue';
import SPageContent from 'src/components/page/SPageContent.vue';
import SHeader from 'src/components/page/SHeader.vue';
import SBtn from 'src/components/Buttons/SBtn.vue';
import SBtnIcon from 'src/components/ui/SButtonIcon.vue';
import SInput from 'src/components/ui/SInput.vue';
import SCard from 'src/components/ui/SCard.vue';
import SIcon from 'src/components/ui/SIcon.vue';
import SToggle from 'src/components/ui/SToggle.vue';
import SSelect from 'src/components/ui/SSelect.vue';
import SSelectBackend from 'src/components/backend/SSelectBackend.vue';
import SBaseFilter from 'src/components/Filters/SBaseFilter.vue';
// import SStepper from 'src/components/ui/SStepper.vue';
import SSpinner from 'src/components/Loadings/SSpinner.vue'
import SDialog from 'src/components/Dialog/SDialog.vue';
import SBanner from 'src/components/base/Banner/SBanner.vue';
import STable from 'src/components/Tables/STable.vue';

export default boot(async ({ app }) => {
  app.component('SPage', SPage);
  app.component('STable', STable);
  app.component('SPageContent', SPageContent);
  app.component('SHeader', SHeader);
  app.component('SSpinner', SSpinner);
  app.component('SBtn', SBtn);
  // app.component('SBtnIcon', SBtnIcon);
  app.component('SInput', SInput);
  app.component('SCard', SCard);
  // app.component('SIcon', SIcon);
  // app.component('SToggle', SToggle);
  app.component('SSelect', SSelect);
  // app.component('SSelectBackend', SSelectBackend);
  // app.component('SBaseFilter', SBaseFilter);
  // // app.component('SStepper', SStepper);
  app.component('SDialog', SDialog);
  app.component('SBanner', SBanner);
});
