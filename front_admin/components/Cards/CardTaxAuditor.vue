<template>
    <b-col cols="4" md="3">
        <b-card :header="taxAuditor.name" header-bg-variant="primary" header-text-variant="white">
            <b-card-text>
                <b>Email:</b> {{ taxAuditor.email }} <br>
                <b>Employer:</b> {{ taxAuditor.employer_name }} <br>
                <b>Registered On:</b> {{ taxAuditor.registered_on }} <br>
            </b-card-text>
        </b-card>
    </b-col>
</template>

<script>
    export default {
        name: 'CardTaxAuditor',
        // eslint-disable-next-line
        props: { taxAuditor: { type: [Array, Object] } }
    }
</script>
