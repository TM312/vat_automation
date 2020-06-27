<template>
    <b-navbar toggleable="lg" type="light" variant="light">
        <b-navbar-brand to="/">Tax-Automation</b-navbar-brand>

        <b-navbar-toggle target="nav-collapse" />

        <b-collapse id="nav-collapse" is-nav>
            <b-navbar-nav>
                <b-nav-item to="/tax/dashboard">Dashboard</b-nav-item>
                <!-- ^integrate v-if for multiple user types -->
                <b-nav-item to="/tax/clients">Clients</b-nav-item>
            </b-navbar-nav>

            <!-- Right aligned nav items -->
            <b-navbar-nav class="ml-auto">
                <navbar-tax-auth-avatar-dropdown />
            </b-navbar-nav>
        </b-collapse>
    </b-navbar>
</template>

<script>
    // import { BIcon } from 'bootstrap-vue'
    export default {
        name: "NavbarTaxAuth"
    };
</script>

<style></style>
