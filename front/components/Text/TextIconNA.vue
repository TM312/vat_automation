<template>
    <span class="text-muted">n/a
        <b-icon icon="exclamation-triangle" v-b-popover.hover.top="'This information has not been provided in the original file.'" title="Info" variant="warning" class="ml-2" />
    </span>
</template>

<script>
export default {
    name: 'TextIconNA'
}
</script>

<style>

</style>
