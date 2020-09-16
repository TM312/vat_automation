<template>
    <b-tabs content-class="mt-3">
        <b-tab title="Single Client" active><form-add-seller-firm /></b-tab>
        <b-tab title="Form Upload"><lazy-container-add-multiple-seller-firms lazy/></b-tab>
    </b-tabs>
</template>

<script>

export default {
    name: 'ContainerAddClient'

}
</script>

<style>

</style>
