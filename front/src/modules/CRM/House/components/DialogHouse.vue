<template>
<s-dialog :title='titleDialog'>
    <div class="home_wrapper">
        <q-form ref="form">

            <div class="mt-base-25 ">
                <s-select-backend
                    v-model="formData.city_id"
                    :getter="getCity"
                    label="Выбор города"
                    option-label="name"
                    option-value="id"
                    search-filter="name"
                    bottom-slots
                    :multiple="false"
                    :use-chips="true"
                    :rules="[
          NotEmpty(),
        ]"
                />
            </div>
            <div class="mt-base-25 ">
                <s-input
                    v-model="formData.name"
                    label="Введите название дома"
                    clearable
                    debounce="600"
                    class="col-12"
                    :rules="[
          NotEmpty(),
        ]"
                />
            </div>

            <div class="mt-base-25 ">
                <s-input
                    v-model="formData.flat_count"
                    label="Введите общее кол-во квартир"
                    clearable
                    type="number"
                    debounce="600"
                    class="col-12"
                    :rules="[
          NotEmpty(),
        ]"
                />
            </div>
 <div class="mt-base-25 ">
                <s-input
                    v-model="formData.geo_adress"
                    label="Введите адрес"
                    clearable
                    type="text"
                    debounce="600"
                    class="col-12"
                    :rules="[
          NotEmpty(),
        ]"
                />
            </div>
            <SBtn
                class="outlined  mt-base-25"
                width="base-xxxl"
                label="Отправить"
                @click="sendRequest"
            />
        </q-form>
    </div>

    <div class="home_wrapper">

    </div>

</s-dialog>
</template>

<script lang="ts">
;
import {
    defineComponent,
    onMounted,
} from 'vue';
import {
    useDialog
} from '../composables/useDialog';
// import SSelectBackend from 'src/components/backend/SSelectBackend.vue';
import useValidation from 'src/composables/useValidation';

export default defineComponent({
    name: 'DialogService',
    components: {
        // SSelectBackend
    },
    props: {
        createService: Function
    },
    setup(props) {
        const {
            onSubmit,
            formData,
            // isEmptyOrNullString,
            // formVisible,
            // getWorkers,
            // getProcessTemplate,
            form,
            // stateOrg,
            getCity
        } = useDialog();

        const {
            NotEmpty,
            MaxLength,
            MinLength,
        } = useValidation()

        const sendRequest = () => {
            try {
                props.createService(onSubmit())
            } catch (e) {
                console.log(e)
            }
        };
        return {
            NotEmpty,
            MaxLength,
            MinLength,
            sendRequest,
            titleDialog: 'Оформление на добавление в группу',
            onSubmit,
            formData,
            getCity,
            form,
        };
    },
});
</script>
