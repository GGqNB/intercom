<template>
<div class="auth__card login__container">

    <div class="auth__title q-mb-xl">
        <div>ДОМОФОНИЛ</div>
        <div>«STOWN»</div>
    </div>
    <q-form ref="form" class="col-xs-12">
        <div class="fw-600 fs-19">Авторизация</div>
        <div class="col-xs-12">
            <s-input
                label="Ключ"
                class="s-mb-lg mt-base-15"
                @keyup.enter="onSubmit"
                v-model.trim="formValue.key"
                :rules="[
                  NotEmpty(),
                  MinLength(4),
                  MaxLength(255),
                ]"
            />
        </div>
        <div class="col-xs-12 row justify-between s-mb-md">
            <router-link to="" class="links-auth">
                <div>Регистрация</div>
            </router-link>
        </div>
        <div class="col-xs-12 row justify-between s-mb-md">
            <router-link to="" class="links-auth">
                <div>Забыли пароль?</div>
            </router-link>
        </div>

        <div class="col-xs-12 row justify-center s-mb-xl mt-base-15">
            <s-btn
                label="Войти"
                fat
                class="full-width"
                @click="onSubmit"
            />
        </div>
    </q-form>
</div>
</template>

<script lang="ts">
import {
    defineComponent,
    ref
} from 'vue';
import {
    makeRequest
} from 'src/composables/useRequest';
import {
    useCurrentUser
} from 'src/composables/useCurrentUser';
import {
    useRouter
} from 'vue-router';
import {
    useNotifications
} from 'src/composables/useNotifications';
import {
    useLoading
} from 'src/composables/useLoading';
import AuthSystemApi from 'src/backend/api/classes/AuthSystemClass';
import {
    QForm
} from 'quasar';
import useValidation from 'src/composables/useValidation';
export default defineComponent({
    name: 'LoginPage',
    components: {},
    setup() {
      const {
            NotEmpty,
            MinLength,
            MaxLength
        } = useValidation();
        
        const formValue = ref({
            key: '',
        });
        const $notify = useNotifications();
        const passwordVisible = ref(false);
        const {
            $userDataSet
        } = useCurrentUser();
        const router = useRouter();
        const form = ref < QForm > ();
        const onSubmit = async () => {

            const isValid = await form.value ?.validate();
            if (!isValid) {
              console.log(form.value)
                $notify.warning('Необходимо заполнить обязательные поля');
                return;
            }

            try {
                const response = await makeRequest(async () =>
                    AuthSystemApi.me(formValue.value.key));
                if (response) {
                    $userDataSet.setToken(response.key);
                    router.push('/')
                    // setUser();
                }
            } catch (error) {}
        }

        // const setUser = async () => {
        //   const response = await makeRequest(async () =>
        //     UserApi.me());
        //     if(response){
        //       $userDataSet.setUser(response);
        //        router.push('/')
        //     }else{
        //       $notify.error('Произошла ошибка');
        //     }
        // }

        return {
            onSubmit,
            passwordVisible,
            formValue,
            NotEmpty,
            form,
            MinLength,
            MaxLength
            
        };
    }

});
</script>
