<template>
    <div>
        <NavbarTax />
        <div class="app-body">
            <!-- <h1>THIS IS THE TAX LAYOUT</h1> -->
            <nuxt />
        </div>
        <Footer />
    </div>
</template>

<script>
    import NavbarTax from "@/components/Navbar/Tax/NavbarTax";
    import Footer from "@/components/Footer";
    export default {
        middleware: "auth-tax",
        components: {
            NavbarTax,
            Footer
        }
    };
</script>
