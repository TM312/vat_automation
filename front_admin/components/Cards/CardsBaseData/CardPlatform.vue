<template>
  <b-card class="h-100">
    <b-card-title>
      <b-row>
        <b-col cols="auto">
          <b-form-input
            v-if="edit"
            v-model="form.name"
          />
          <span v-else>{{ platform.name }}</span>
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
          <span>{{ platform.code }}</span>
        </b-col>
        <b-col cols="auto ml-auto">
          <b-button
            v-show="edit"
            variant="success"
            size="sm"
            :disabled="buttonBusy"
            @click="updatePlatform()"
          >
            Update
          </b-button>
        </b-col>
      </b-row>
    </b-card-sub-title>
  </b-card>
</template>

<script>
export default {
  name: 'CardPlatform',

  props: {
    platform: {
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
                this.form.name = this.platform.name;
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
                } else if (obj[key] != null && obj[key] != this.platform[key]) {
                    data_changes[key] = obj[key]; // copy value
                }
            });

            return data_changes;
        },

        async updatePlatform() {
            this.buttonBusy = true;
            const { store } = this.$nuxt.context;
            const platform_code = this.platform.code;
            const data_changes = this.removeNonChanges();
            const payload = [platform_code, data_changes];
            await store.dispatch("platform/update_in_list", payload);
            this.makeToast();
            this.buttonBusy = false;
            this.edit = false;
        },

        makeToast() {
            this.$bvToast.toast(
                `Platform "${this.platform.code}" has been successfully updated!`,
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
