<template>
    <b-container>
        <h1>Socket Status Component</h1>
        <hr>
        <h1>Progress: {{ progress }} </h1>
        <b-button
            @click="getLongTask"
            variant="outline-primary"
        >
            Request Long Task
        </b-button>
        <b-button @click="getEvents" variant="outline-success">
            Get Events
        </b-button>

        <!--  <b-button @click="getDisconnect" variant="outline-danger">
            Request Disconnect
        </b-button> -->
        <hr>
        <h1>Long Task: </h1><br>
        <p>Task ID: {{ taskId }}</p>
        <p>Result: </p>
        <ul>
            <li>Current: {{ result.current }}</li>
            <li>Total: {{ result.total }}</li>
            <li>Status: {{ result.status }}</li>
            <li>Result: {{ result.result }}</li>
            <li>Room: {{ result.room }}</li>
        </ul>

        <br><br>
        <h2>SocketStatus: {{ socketStatus }}</h2>
        <br><br>
        <h2>Connect Message: {{ message }}</h2>
    </b-container>

</template>

<script>
import { mapState } from 'vuex'

export default {
    name: 'SocketsTest',
    layout: "default",
    // middleware: "auth-tax",

    data() {
        return {
            socketStatus: {},
            message: '',
            result: {
                "current": '',
                "total": '',
                "status": '',
                "result": '',
                "room": ''
            }
        }
    },

    computed: {
        ...mapState({
            progress: state => state.status.progress,
            taskId: state => state.status.result.task_id
        })
    },

    mounted() {
        this.socket = this.$nuxtSocket({
            name: 'home',
            channel: '/events',
            reconnection: false
        }),
        /* Listen for events: */
        this.socket
            .on('message', (data) => {
                console.log('message:', data)
            /* Handle event */
                this.message = data['status']
        }),

        this.socketTask = this.$nuxtSocket({
            name: 'home',
            channel: '/status',
            reconnection: false
        }),
        /* Listen for events: */
        this.socketTask
            .on('message', (data) => {
                console.log('message:', data)
            /* Handle event */
                this.result = data
                })
    },

    methods: {
        getEvents() {
            this.socket.emit(
                'join',
                { 'json':
                    { 'room': 2 }
                },
                (res) => {
                    this.message = res
            })
        },

        // getDisconnect() {
        //     this.socket.emit('disconnect', (res) => {
        //         this.message = res
        //     })
        // },

        async getLongTask() {
            const { store } = this.$nuxt.context;
            await store.dispatch("status/get");
        }
    },
}
</script>

<style>

</style>
