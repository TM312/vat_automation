<template>
  <b-card class="h-100">
    <b-card-title>
      <b-row>
        <b-col cols="auto">
          <b-form-input v-if="edit" v-model="form.name" />
          <span v-else>{{ taxTreatment.name }}</span>
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
          {{ taxTreatment.code }}
        </b-col>
        <b-col cols="auto ml-auto">
          <b-button
            v-show="edit"
            variant="success"
            size="sm"
            :disabled="buttonBusy"
            @click="updateTaxTreatment()"
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
      <span v-else>{{ taxTreatment.description }}</span>
    </b-card-text>
  </b-card>
</template>

<script>
export default {
  name: "CardTaxTreatment",

  props: {
    taxTreatment: {
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
        description: null
      },
    }
  },

  watch: {
    /*eslint-disable */
        edit(newVal) {
            if (newVal) {
                this.form.name = this.taxTreatment.name;
                this.form.description = this.taxTreatment.description;
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
                    // only keep not null and changed values
                } else if (obj[key] != null && obj[key] != this.taxTreatment[key]) {
                    data_changes[key] = obj[key]; // copy value
                }
            });

            return data_changes;
        },

        async updateTaxTreatment() {
            this.buttonBusy = true;
            const { store } = this.$nuxt.context;
            const taxTreatmentCode = this.taxTreatment.code;
            const data_changes = this.removeNonChanges();
            const payload = [taxTreatmentCode, data_changes];
            await store.dispatch("tax_treatment/update_in_list", payload);
            this.makeToast();
            this.buttonBusy = false;
            this.edit = false;
        },

        makeToast() {
            this.$bvToast.toast(
                `Tax Treatment "${this.taxTreatment.code}" has been successfully updated!`,
                {
                    title: "Success",
                    variant: "success",
                    autoHideDelay: 5000,
                }
            );
        },
    },
};
</script>

<style>
</style>
