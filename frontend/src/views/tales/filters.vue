<template>
  <validation-observer ref="observer">
    <v-row align="center">
      <v-col cols="12" sm="3">
        <v-select
          v-model="filters.selected_style"
          :items="filters.styles"
          label="Illustration style"
          hint="Generate images in the specified style"
          item-text="name"
          item-value="abbr"
          return-object
          persistent-hint
        ></v-select>
      </v-col>
      <v-col cols="12" sm="6">
        <v-subheader class="pl-0">Temperature</v-subheader>
        <v-slider
          v-model="filters.temperature"
          min="0"
          max="2"
          step="0.05"
          thumb-label="always"
        ></v-slider>
      </v-col>
      <v-col cols="12" sm="3">
        <validation-provider
          v-slot="{ errors }"
          rules="required|integer"
          name="Max tokens"
        >
          <v-text-field
            v-model="filters.max_tokens"
            label="Max token"
            hide-details="auto"
            :error-messages="errors"
          ></v-text-field>
        </validation-provider>
      </v-col>
    </v-row>
  </validation-observer>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import { ValidationProvider, ValidationObserver, extend } from "vee-validate";
import { required, integer } from "vee-validate/dist/rules";
// eslint-disable-next-line
import { IFilter } from "@/interfaces";

// register validation rules
extend("required", { ...required, message: "{_field_} can not be empty" });
extend("integer", { ...integer, message: "{_field_} should be a number" });

@Component({
  components: {
    ValidationObserver,
    ValidationProvider,
  },
  props: {
    filters: {
      type: IFilter,
      required: true,
    },
  },
})
export default class FiltersComponent extends Vue {
  $refs!: {
    observer: InstanceType<typeof ValidationObserver>;
  };
}
</script>
