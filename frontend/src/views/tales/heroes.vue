<template>
  <v-stepper-content step="1">
    <v-row>
      <v-col cols="12">
        <div class="text-md-h4 font-weight-light mb-3">
          Choose heroes suitable for you and generate portraits.
        </div>
      </v-col>
    </v-row>
    <v-fade-transition>
      <v-overlay absolute="absolute" opacity="0.38" :value="loading">
        <v-progress-circular indeterminate size="64" />
      </v-overlay>
    </v-fade-transition>
    <v-row>
      <v-col cols="12" md="4">
        <v-card class="mx-auto" outlined>
          <hero-window-component :filters="filters" />
        </v-card>
      </v-col>
      <v-col cols="12" md="4">
        <v-btn
          color="primary"
          :disabled="invalid || loading || !heroes.length"
          :loading="loading"
          @click="generatePlots"
          >Next
          <v-icon>mdi-chevron-right</v-icon>
        </v-btn>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" class="d-none d-md-block">
        <v-btn
          color="primary"
          :disabled="invalid || loading || !heroes.length"
          :loading="loading"
          @click="generatePlots"
          >Next
          <v-icon>mdi-chevron-right</v-icon>
        </v-btn>
      </v-col>
    </v-row>
  </v-stepper-content>
</template>

<script lang="ts">
import { VueTyper } from "vue-typer";
import { Component, Vue } from "vue-property-decorator";
import { ITaleCreate, IFilter } from "@/interfaces";
import { dispatchCreateStructures } from "@/store/tales/actions";
import { readStatus, readHeroes } from "@/store/tales/getters";
import HeroWindowComponent from "./heroWindow.vue";

@Component({
  components: {
    VueTyper,
    HeroWindowComponent,
  },
  props: {
    logLine: { type: String },
    invalid: { type: Boolean },
    filters: { type: IFilter },
  },
})
export default class HeroesComponent extends Vue {
  get isLoading() {
    return readStatus(this.$store);
  }

  get loading() {
    return this.isLoading("structures") || this.isLoading("heroes");
  }

  get heroes() {
    return readHeroes(this.$store);
  }

  public generate() {
    this.$emit("generate");
  }

  public async generatePlots() {
    const createStructures: ITaleCreate = {
      heroes: this.heroes,
      log_line: this.logLine,
      max_tokens: this.filters.max_tokens,
      temperature: this.filters.temperature,
      tale_style: this.filters.selected_style.abbr,
    };
    await dispatchCreateStructures(this.$store, createStructures);
  }
}
</script>
