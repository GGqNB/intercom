<template>
  <q-dialog ref="dialogRef" :persistent="persistent" @hide="onDialogHide">
    <q-card class="s-modal--form s-modal--form-md q-dialog-plugin">
      <q-toolbar class="s-modal--form__header">
        <q-toolbar-title>
          <span class="s-modal--form__header-title">{{ title }}</span>
        </q-toolbar-title>
      </q-toolbar>

      <div class="s-modal--form__body text-center mt-base-15">
        <div v-html="message" class="font-text-3"></div>

        <div class="s-modal--form__footer full-width row justify-between">
          <s-form-wrapper width="sm">
            <s-btn
              no-caps
              color='deep-orange'
              :label="confirmLabel"
              @click="onOKClick"
            />
          </s-form-wrapper>
          <s-form-wrapper width="sm">
            <s-btn
              v-if="cancel"
              no-caps
              :outline="true"
              :label="cancelLabel"
              @click="onCancelClick"
            />
          </s-form-wrapper>
        </div>
      </div>
    </q-card>
  </q-dialog>
</template>
<script lang="ts">
import { defineComponent } from 'vue';
import { useDialogPluginComponent } from 'quasar';

import SBtn from '../Buttons/SBtn.vue';
import SFormWrapper from '../SFormWrapper.vue';

export default defineComponent({
  name: 'ConfirmDialog',
  components: { SBtn, SFormWrapper },
  props: {
    title: {
      required: false,
      type: [Number, String],
      default: 'Подтверждение',
    },
    message: {
      required: false,
      type: [Number, String],
      default: 'Вы действительно хотите выполнить данное действие?',
    },
    confirmLabel: {
      required: false,
      type: [ String ],
      default: 'Да',
    },
    cancelLabel: {
      required: false,
      type: [ String],
      default: 'Нет',
    },
    cancel: {
      required: false,
      default: true,
      type: Boolean,
    },
    persistent: {
      required: false,
      default: true,
      type: Boolean,
    },
    reverseBtn: {
      required: false,
      default: false,
      type: Boolean,
    },
  },
  emits: [
    // REQUIRED; need to specify some events that your
    // component will emit through useDialogPluginComponent()
    ...useDialogPluginComponent.emits,
  ],
  setup() {
    const { dialogRef, onDialogHide, onDialogOK, onDialogCancel } = useDialogPluginComponent();
    return {
      // This is REQUIRED;
      // Need to inject these (from useDialogPluginComponent() call)
      // into the vue scope for the vue html template
      dialogRef,
      onDialogHide,
      // other methods that we used in our vue html template;
      // these are part of our example (so not required)
      onOKClick() {
        // on OK, it is REQUIRED to
        // call onDialogOK (with optional payload)
        onDialogOK();
        // or with payload: onDialogOK({ ... })
        // ...and it will also hide the dialog automatically
      },
      // we can passthrough onDialogCancel directly
      onCancelClick: onDialogCancel,
    };
  },
});
</script>
