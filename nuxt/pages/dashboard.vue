<template>
    <b-container fluid class="my-5">
        <b-tabs content-class="my-3">
            <b-tab title="Available Files" active>
                <DownloadField />
            </b-tab>
            <b-tab title="Upload">
                <UploadField />
            </b-tab>
        </b-tabs>
    </b-container>
</template>

<script>
    import DownloadField from "@/components/DownloadField"
    import UploadField from "@/components/UploadField"

    export default {
        middleware: "auth",
        components: {
            DownloadField,
            UploadField
        },
        async fetch({ $axios, store }) {

            let [response_self, response_tax_records] = await Promise.all([
                $axios.$get("/user/self"),
                $axios.$get("/media/tax_record/own"),
                ])

            const self = response_self.data
            const self_tax_records = response_tax_records.data

            store.commit("SET_SELF", self)
            store.commit("SET_SELF_TAX_RECORDS", self_tax_records)
        }
    };
</script>

<style></style>
