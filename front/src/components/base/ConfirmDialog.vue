<template>
  <q-dialog ref="dialogRef" :persistent="persistent" @hide="onDialogHide">
    <q-card class="s-modal s-modal--extra-small q-dialog-plugin">
      <q-toolbar class="s-modal__header-wrapper">
        <q-toolbar-title class="">
          <span class="s-modal__header-title">{{ title }}</span>
        </q-toolbar-title>
      </q-toolbar>

      <div class="s-modal__body">
        <div v-html="message" />
      </div>

      <div class="s-modal__footer full-width row justify-end q-mt-lg">
        <s-btn v-if="cancel" no-caps class="s-mr-md" :label="cancelLabel" @click="onCancelClick" />
        <s-btn no-caps type="light" :label="confirmLabel" @click="onOKClick" />
      </div>
    </q-card>
  </q-dialog>
</template>

<script lang="ts">
import { defineComponent, onMounted, ref } from 'vue';
import { useDialogPluginComponent } from 'quasar';

export default defineComponent({
  name: 'ConfirmDialog',
  props: {
    title: {
      required: false,
      type: [Number, String],
      default: 'Подтверждение',
    },
    message: {
      required: false,
      type: [Number, String],
      default: 'Вы действительно хотите выполнить?',
    },
    confirmLabel: {
      required: false,
      type: [Number, String],
      default: 'Да',
    },
    cancelLabel: {
      required: false,
      type: [Number, String],
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
  },
  emits: [
    // REQUIRED; need to specify some events that your
    // component will emit through useDialogPluginComponent()
    ...useDialogPluginComponent.emits,
  ],
  setup(props) {
    // REQUIRED; must be called inside of setup()
    const {
      dialogRef, onDialogHide, onDialogOK, onDialogCancel,
    } = useDialogPluginComponent();

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
