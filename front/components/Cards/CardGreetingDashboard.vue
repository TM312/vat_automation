<template>
    <div class="my-5">
        <h1>{{ greeting }}</h1>
    </div>
</template>

<script>
export default {
    name: 'CardGreetingDashboard',
    created() {
        this.nowHours = new Date().getHours()
    },

    computed: {
        greeting: function() {
            if (this.nowHours <= 5) {
                return `Good Morning or Good Night, ${ this.$auth.user.name } ?`
            } else if (6 <= this.nowHours && this.nowHours <= 11) {
                return `Good Morning, ${ this.$auth.user.name } !`
            } else if (12 <= this.nowHours && this.nowHours <= 14) {
                return `Happy Lunch Time, ${ this.$auth.user.name } !`
            } else if (15 <= this.nowHours && this.nowHours <= 17) {
                return `Good Afternoon, ${ this.$auth.user.name } !`
            } else {
                return `Good Evening, ${ this.$auth.user.name } !`
            }
        }
    },

}
</script>
