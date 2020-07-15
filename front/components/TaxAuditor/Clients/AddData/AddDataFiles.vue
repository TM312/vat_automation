<template>
    <div>
        <!-- <template-card :title="title" :urlEndpointTemplate="urlEndpointTemplate" :templateItems="templateItems" /> -->
        <br />
        <card-data-upload />
    </div>
</template>

<script>
export default {
    name: 'AddDataFiles',

    data() {
        return {
            title: 'Templates',
        }
    }
}
</script>

<style>

</style>
