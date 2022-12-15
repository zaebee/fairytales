<template>
  <v-container fluid>
    <validation-observer ref="observer" v-slot="{ invalid }">
      <v-card class="pa-3" outlined tile>
        <v-card-title primary-title>
          <div class="headline primary--text">F[ai]ry tales</div>
        </v-card-title>
        <v-card-text>
          <div class="headline font-weight-light">
            Welcome to Fairytales AI generator
          </div>
        </v-card-text>

        <v-row>
          <v-col cols="12" md="6">
            <validation-provider v-slot="{ errors }" rules="required" name="Log line">
              <v-form class="ma-5">
                <v-textarea
                  v-model="logLine"
                  required
                  :error-messages="errors"
                  label="Write a short log line for your tale"
                  placeholder="For example, A funny tale about two girls: Sasha wand Monica, who discovered that the Wicked Witch with a magic Candle wants to kidnap them to make them witches. They study magic, but all the time they do good deeds and because of this, they get into funny situations."
                ></v-textarea>
                <v-btn
                  outlined
                  class="mt-5"
                  color="primary"
                  :disabled="invalid || isLoadingStatus('heroes')"
                  :loading="isLoadingStatus('heroes')"
                  @click="generateCharacters"
                  >Try it
                </v-btn>
              </v-form>
            </validation-provider>
          </v-col>
          <v-col cols="12" md="6">
            <filters-component :filters="filters" />
          </v-col>
        </v-row>
      </v-card>
      <v-expand-transition>
        <v-stepper v-model="stepper" tile outlined>
          <v-stepper-header>
            <v-stepper-step :complete="stepper > 0" step="1">
              Heroes
              <small>Creates heroes of your story</small>
            </v-stepper-step>
            <v-divider></v-divider>
            <v-stepper-step :complete="stepper > 1" step="2">
              Plots
              <small>Creates main plots and beats for story</small>
            </v-stepper-step>
            <v-divider></v-divider>
            <v-stepper-step :complete="stepper > 2" step="3">
              Stories
              <small>Customize you final story</small>
            </v-stepper-step>
            <v-divider></v-divider>
            <v-stepper-step :complete="stepper > 3" step="4">
              Share with friends
              <small>Send story to your children</small>
            </v-stepper-step>
          </v-stepper-header>
          <v-stepper-items v-show="heroSets">
            <heroes-component
              :invalid="invalid"
              :log-line="logLine"
              :filters="filters"
              @generate="generateCharacters"
            />
            <structures-component
              :invalid="invalid"
              :log-line="logLine"
              :filters="filters"
              @generate="generateStructures"
            />
            <stories-component
              :invalid="valid"
              :log-line="logLine"
              :filters="filters"
              :max-tokens="filters.max_tokens"
              :temperature="filters.temperature"
              :tale-style="filters.selected_style"
              @generate="generateTale"
            />
          </v-stepper-items>
        </v-stepper>
      </v-expand-transition>
    </validation-observer>
  </v-container>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import { ValidationProvider, ValidationObserver, extend } from "vee-validate";
import { required, integer } from "vee-validate/dist/rules";

import { ITaleCreate, IFilter } from "@/interfaces";
import {
  readStatus,
  readStepper,
  readHeroes,
  readHeroSets,
  selectedStructure,
} from "@/store/tales/getters";
import {
  dispatchStep,
  dispatchCreateHeroes,
  dispatchCreateStructures,
  dispatchCreateTale,
} from "@/store/tales/actions";

import FiltersComponent from "./filters.vue";
import HeroesComponent from "./heroes.vue";
import StructuresComponent from "./structures.vue";
import StoriesComponent from "./stories.vue";

// register validation rules
extend("required", { ...required, message: "{_field_} can not be empty" });
extend("integer", { ...integer, message: "{_field_} should be a number" });

@Component({
  components: {
    ValidationObserver,
    ValidationProvider,
    FiltersComponent,
    HeroesComponent,
    StructuresComponent,
    StoriesComponent,
  },
})
export default class Tales extends Vue {
  $refs!: {
    observer: InstanceType<typeof ValidationObserver>;
  };

  public valid = true;
  public logLine =
    "A magical story about the elf Zae and the a bee named Moo. How they went into a dark forest and saw an evil owl that showed them a deep river where an underwater witch lived. The witch wanted to drag the elves to the bottom, but she did not succeed.";
  public filters: IFilter = {
    max_tokens: 500,
    temperature: 0.5,
    selected_style: {
      name: "Modern",
      abbr: "MODERN",
    },
    styles: [
      { name: "Modern", abbr: "MODERN" },
      { name: "SteamPunk", abbr: "STEAMPUNK" },
      { name: "Elfian style", abbr: "ELF" },
      { name: "Dark black/white", abbr: "BW" },
      { name: "Xmas style", abbr: "XMAS" },
      { name: "Pixar movie", abbr: "PIXAR" },
    ],
  };

  get stepper() {
    return readStepper(this.$store);
  }

  set stepper(step: number) {
    dispatchStep(this.$store, step);
  }

  get heroes() {
    return readHeroes(this.$store);
  }

  get heroSets() {
    return readHeroSets(this.$store).length;
  }

  get structure() {
    return selectedStructure(this.$store);
  }

  get isLoadingStatus() {
    return readStatus(this.$store);
  }

  public async generateCharacters() {
    const success = await this.$refs.observer.validate();
    if (!success) {
      return;
    }

    const createHeroes: ITaleCreate = {
      log_line: this.logLine,
      max_tokens: this.filters.max_tokens,
      temperature: this.filters.temperature,
      tale_style: this.filters.selected_style.abbr,
    };
    await dispatchCreateHeroes(this.$store, createHeroes);
  }

  public async generateStructures() {
    const success = await this.$refs.observer.validate();
    if (!success) {
      return;
    }
    const createStructures: ITaleCreate = {
      heroes: this.heroes,
      log_line: this.logLine,
      max_tokens: this.filters.max_tokens,
      temperature: this.filters.temperature,
      tale_style: this.filters.selected_style.abbr,
    };
    await dispatchCreateStructures(this.$store, createStructures);
  }

  public async generateTale() {
    const success = await this.$refs.observer.validate();
    if (!success) {
      return;
    }
    const createTale: ITaleCreate = {
      heroes: this.heroes,
      log_line: this.logLine,
      structure: this.structure,
      max_tokens: this.filters.max_tokens,
      temperature: this.filters.temperature,
      tale_style: this.filters.selected_style.abbr,
    };
    await dispatchCreateTale(this.$store, createTale);
  }
}
</script>

<style>
.v-card--disabled {
  opacity: 0.25;
}
</style>
