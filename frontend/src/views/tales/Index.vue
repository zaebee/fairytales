<template>
  <v-container fluid>
    <validation-observer ref="observer" v-slot="{ invalid }">
      <v-card class="ma-3 pa-3" outlined tile>
        <v-card-title primary-title>
          <div class="headline primary--text">Fairytales</div>
        </v-card-title>
        <v-card-text>
          <div class="headline font-weight-light">
            Welcome to Fairytales AI generator
          </div>
        </v-card-text>

        <v-row>
          <v-col cols="12" md="6">
            <validation-provider v-slot="{ errors }" rules="required" name="Log line">
              <div class="ma-5">
                <v-textarea
                  v-model="logLine"
                  required
                  :error-messages="errors"
                  label="Write a short log line for your tale"
                  placeholder="For example, A funny tale about two girls: Sasha wand Monica, who discovered that the Wicked Witch with a magic Candle wants to kidnap them to make them witches. They study magic, but all the time they do good deeds and because of this, they get into funny situations."
                ></v-textarea>
              </div>
            </validation-provider>
          </v-col>
          <v-col cols="12" md="6">
            <v-row align="center">
              <v-col cols="12" sm="6">
                <v-select
                  v-model="selectedStyle"
                  :items="taleStyles"
                  label="Tale style"
                  hint="Generate your tale as selected"
                  item-text="name"
                  item-value="abbr"
                  return-object
                  persistent-hint
                ></v-select>
              </v-col>
            </v-row>
            <v-row align="center">
              <v-col cols="12" sm="6">
                <v-subheader class="pl-0">Temperature</v-subheader>
                <v-slider
                  v-model="temperature"
                  min="0"
                  max="1"
                  step="0.05"
                  thumb-label="always"
                ></v-slider>
              </v-col>
            </v-row>
            <v-row align="center">
              <v-col cols="12" sm="6">
                <validation-provider
                  v-slot="{ errors }"
                  rules="required|integer"
                  name="Max tokens"
                >
                  <v-text-field
                    v-model="maxTokens"
                    label="Max token"
                    hide-details="auto"
                    :error-messages="errors"
                  ></v-text-field>
                </validation-provider>
              </v-col>
            </v-row>
          </v-col>
        </v-row>
        <v-card-actions>
          <v-btn
            :disabled="invalid || isLoadingStatus('heroes')"
            outlined
            :loading="isLoadingStatus('heroes')"
            color="primary"
            @click="generateCharacters"
            >Generate heroes
          </v-btn>
        </v-card-actions>
      </v-card>

      <v-stepper v-model="stepper" class="ma-3 pa-3" vertical tile outlined>
        <v-stepper-step :complete="stepper > 0" :editable="stepper > 0" step="1">
          Heroes
          <small>Create heroes of your story</small>
        </v-stepper-step>
        <heroes-component
          :log-line="logLine"
          :max-tokens="maxTokens"
          :temperature="temperature"
          :tale-style="selectedStyle"
          :invalid="invalid"
        />
        <v-stepper-step :complete="stepper > 1" editable step="2">
          Structures
          <small>Create main plots and beats for story</small>
        </v-stepper-step>
        <structures-component
          :log-line="logLine"
          :max-tokens="maxTokens"
          :temperature="temperature"
          :tale-style="selectedStyle"
          :invalid="invalid"
        />
        <v-stepper-step :complete="stepper > 2" :editable="stepper > 2" step="3">
          Stories
          <small>Customize you final story</small>
        </v-stepper-step>
        <stories-component
          :valid="valid"
          :log-line="logLine"
          :max-tokens="maxTokens"
          :temperature="temperature"
          :tale-style="selectedStyle"
        />
        <v-stepper-step :complete="stepper > 3" :editable="stepper > 3" step="4">
          Share with friends
          <small>Send story to your children</small>
        </v-stepper-step>
      </v-stepper>
    </validation-observer>
  </v-container>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import { ValidationProvider, ValidationObserver, extend } from "vee-validate";
import { required, integer } from "vee-validate/dist/rules";

import { ITaleCreate } from "@/interfaces";
import { readStatus, readStepper } from "@/store/tales/getters";
import { dispatchStep, dispatchCreateHeroes } from "@/store/tales/actions";

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
  public maxTokens = 500;
  public temperature = 0.5;
  public selectedStyle = {
    name: "Red Riding Hood by the Grimm brothers",
    abbr: "RED_HOOD",
  };
  public taleStyles = [
    { name: "Mary's child by the Grimm brothers", abbr: "MARY" },
    { name: "Red Riding Hood by the Grimm brothers", abbr: "RED_HOOD" },
    { name: "Tale about a goose", abbr: "GOSE" },
  ];

  get stepper() {
    return readStepper(this.$store);
  }

  set stepper(step: number) {
    dispatchStep(this.$store, step);
  }

  get isLoadingStatus() {
    return readStatus(this.$store);
  }

  public async generateCharacters() {
    const success = await this.$refs.observer.validate();
    if (!success) {
      return;
    }

    const createHeroes: ITaleCreate = {};
    Object.assign(createHeroes, {
      log_line: this.logLine,
      max_tokens: this.maxTokens,
      temperature: this.temperature,
      tale_style: this.selectedStyle.abbr,
    });
    await dispatchCreateHeroes(this.$store, createHeroes);
  }
}
</script>

<style>
.heros-card {
  cursor: pointer;
  opacity: 0.5;
}
.heros-card.selected {
  border: 1px #1976d2 solid;
  opacity: 1;
}
.heros-card:not(.selected):hover {
  border: 1px #1976d2 solid;
  cursor: pointer;
  opacity: 1;
}
</style>
