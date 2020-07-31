<template>
    <div>
        <b-container class="my-2" fluid><nuxt-link :to="this.$nuxt.context.from" ><b-icon icon="arrow-left" /> Go Back</nuxt-link></b-container>
    </div>
</template>

<script>

import { BIcon } from "bootstrap-vue";
export default {
    name: 'ContainerRouteBack',
    components: {
        BIcon
    }
}
</script>
