<template>
<q-header
    id=""
    reveal
    class="q-header--gold-multi"
>
    <q-toolbar class="s-header--toolbar">
        <div class="row items-center s-header">
            <!-- <q-btn
                class="s-header-menu"
                clickable
                flat
                no-wrap
                dense
                @click="changeVisibilitySidebar"
            >
                <q-icon name="menu" />
            </q-btn> -->
        </div>
        <q-btn flat  @click="changeVisibilitySidebar">
            <q-img
                src="icons/logo.svg"
                width="55px"
                height="75px"
            />
            <!-- <q-img
                
                src="icons/name_stown.svg"
                width="300px"
                color="red"
                height="45px"
                class="text-stown"
            /> -->
            <div class="text-header-btn text-black">STOWN</div>
        </q-btn>
        <!-- <q-btn color="red" @click="logout">Выход</q-btn> -->
        <q-space />
        <q-btn flat>
            <div class="text-header-btn text-black">СДЕЛАНО В ЮГРЕ</div>
            <q-img
                src="icons/inhamao.svg"
                width="70px"
                color="red"
                height="72px"
            />
        </q-btn>

    </q-toolbar>
</q-header>
</template>

<script lang="ts">
import {
    useAppStore
} from 'stores/app.store';
import {
    defineComponent,
    onMounted,
    ref,
    watch
} from 'vue';
import {
    storeToRefs
} from 'pinia';
import {
    routerMainPageName,
    loginPageName
} from 'src/router/router.constants';
import {
    useRouter
} from 'vue-router';
import {
    useCurrentUser
} from 'src/composables/useCurrentUser';
import {
    makeRequest
} from 'src/composables/useRequest';
import {
    useLoading
} from 'src/composables/useLoading';
import AuthSystemApi from 'src/backend/api/classes/AuthSystemClass';
import {
    useDeviceSizes
} from 'src/composables/useDeviceSizes';

export default defineComponent({
    name: 'TheHeader',
    components: {},
    setup() {
        const {
            isMobile
        } = useDeviceSizes();
        const router = useRouter();
        const $currentUser = useCurrentUser();
        const appStore = useAppStore();
        // const authStore = useLocalAuthStore();
        // const userStore = useUserStore();
        const phone = ref('');
        const getUser = async () => {
            try {
                console.log($currentUser.accessToken)
                // const response = await makeRequest(async () =>
                //     AuthSystemApi.me(''));
            } catch {
                phone_flag.value = false;

            }
        }
        const {
            collapseSidebar
        } = storeToRefs(appStore);
        const changeVisibilitySidebar = () => {
            appStore.setCollapseSidebar(!collapseSidebar.value);
        };

        const pastNetworks = ref([]);
        const currentNetwork = ref('');
        const wifi_flag = ref(false);
        const phone_flag = ref(false);

        onMounted(
                () => {
                    console.log(collapseSidebar.value)
                    getUser();
                }
            ),
            function routeTo(routeName) {
                if (routeName === 'exit') {

                    router.push({
                        name: loginPageName
                    });
                } else {
                    router.push({
                        name: routeName
                    });
                }
            }
        const logout = () => {
            $currentUser.$userDataSet.logout()
            router.push('/login')
        }
        return {
            routerMainPageName,
            changeVisibilitySidebar,
            wifi_flag,
            phone_flag,
            phone,
            currentNetwork,
            pastNetworks,
            isMobile,
            logout
        };
    },
});
</script>

<style>
.q-header--gold-multi {
    background: radial-gradient(ellipse farthest-corner at right bottom, #FEDB37 0%, #FDB931 8%, #9f7928 30%, #8A6E2F 40%, transparent 80%),
        radial-gradient(ellipse farthest-corner at left top, #FFFFFF 0%, #FFFFAC 8%, #D1B464 25%, #5d4a1f 62.5%, #5d4a1f 100%);
    color: white;
}

.text-header-btn {
    font-size: 30px;
    padding-right: 15px;
    font-weight: 500;
}
.text-stown{
    margin-left: 15px;
}
</style>
