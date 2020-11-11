<template>
  <b-card class="h-100">
    <b-card-title>
      <b-row>
        <b-col cols="auto">
          <b-form-input
            v-if="edit"
            v-model="form.name"
          />
          <span v-else>{{ channel.name }}</span>
        </b-col>
        <b-col cols="auto ml-auto">
          <b-button variant="outline-warning" size="sm" :pressed.sync="edit">
            <span v-show="edit">
              <b-icon icon="x-circle" /> Cancel
            </span>
            <span v-show="!edit">
              <b-icon icon="pencil-square" /> Edit
            </span>
          </b-button>
        </b-col>
      </b-row>
    </b-card-title>
    <b-card-sub-title>
      <b-row>
        <b-col cols="auto">
          <span>{{ channel.code }}</span>
        </b-col>
        <b-col cols="auto ml-auto">
          <b-button
            v-show="edit"
            variant="success"
            size="sm"
            :disabled="buttonBusy"
            @click="updateChannel()"
          >
            Update
          </b-button>
        </b-col>
      </b-row>
    </b-card-sub-title>
    <b-card-text class="mt-3">
      <b-form-textarea
        v-if="edit"
        v-model="form.description"
        rows="3"
        max-rows="6"
      />
      <span v-else>{{ channel.description }}</span>
    </b-card-text>
  </b-card>
</template>

<script>
export default {
  name: 'CardChannel',

  props: {
    channel: {
      type: Object,
      required: true,
    },
  },

  data() {
    return {
      buttonBusy: false,
      edit: false,
      form: {
        name: null,
        description: null,
      },
    }
  },

  watch: {
    /*eslint-disable */
        edit(newVal) {
            if (newVal) {
                this.form.name = this.channel.name;
                this.form.description = this.channel.description;
            }
        },
    },

    methods: {
        removeNonChanges() {
            const data_changes = {};
            const obj = this.form;

            Object.keys(obj).forEach((key) => {
                if (obj[key] && typeof obj[key] === "object") {
                    data_changes[key] = this.removeNonChanges(obj[key]); // recurse
                    // keep only changes and not null values
                } else if (obj[key] != null && obj[key] != this.channel[key]) {
                    data_changes[key] = obj[key]; // copy value
                }
            });

            return data_changes;
        },

        async updateChannel() {
            this.buttonBusy = true;
            const { store } = this.$nuxt.context;
            const channel_code = this.channel.code;
            const data_changes = this.removeNonChanges();
            const payload = [channel_code, data_changes];
            await store.dispatch("channel/update_in_list", payload);
            this.makeToast();
            this.buttonBusy = false;
            this.edit = false;
        },

        makeToast() {
            this.$bvToast.toast(
                `Channel "${this.channel.code}" has been successfully updated!`,
                {
                    title: "Success",
                    variant: "success",
                    autoHideDelay: 5000,
                }
            );
        },
    },

}
</script>

<style>

</style>
