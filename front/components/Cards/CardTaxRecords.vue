<template>
   <div class="mb-5">
                                        <b-row align-h="end" cols="1" cols-lg="2">
                                            <b-col>
                                                <div class="mb-2"><h6>Valid From</h6></div>
                                                <b-calendar v-model="payload.valid_from" value-as-date locale="en">
                                                    <div class="d-flex" dir="rtr">
                                                        <b-button
                                                            size="sm"
                                                            variant="outline-danger"
                                                            v-if="payload.valid_from"
                                                            @click="clearDate('valid_from')"
                                                        > Clear date
                                                        </b-button>
                                                        <b-button
                                                            size="sm"
                                                            variant="outline-primary"
                                                            class="ml-auto"
                                                            @click="setToday('valid_from')"
                                                        > Set Today
                                                        </b-button>
                                                    </div>
                                                </b-calendar>
                                            </b-col>
                                            <b-col>
                                                <div class="mb-2"><h6>Valid To</h6></div>
                                                <b-calendar v-model="payload.valid_to" value-as-date locale="en">
                                                    <div class="d-flex" dir="rtr">
                                                        <b-button
                                                            size="sm"
                                                            variant="outline-danger"
                                                            v-if="payload.valid_to"
                                                            @click="clearDate('valid_to')"
                                                        > Clear date
                                                        </b-button>
                                                        <b-button
                                                            size="sm"
                                                            variant="outline-primary"
                                                            class="ml-auto"
                                                            @click="setToday('valid_to')"
                                                        > Set Today
                                                        </b-button>
                                                    </div>
                                                </b-calendar>

                                            </b-col>
                                        </b-row>
                                    </div>
</template>

<script>
export default {

    methods: {
        setToday(datetype) {
                const now = new Date()
                this.payload[datetype] = new Date(now.getFullYear(), now.getMonth(), now.getDate())
            },

        clearDate(datetype) {
            this.payload[datetype] = ''
        }
    },

}
</script>

<style>

</style>
