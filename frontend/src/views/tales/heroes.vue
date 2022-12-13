<template>
  <v-stepper-content step="1">
    <v-card-text>
      <div class="headline font-weight-light">
        Choose the heroes suitable you and generate portraits.
        <vue-typer
          v-if="readyToNext"
          text="Great! You have created all the portraits and are ready to create the plot of the fairy tale."
          :repeat="0"
          :shuffle="false"
          initial-action="typing"
          :type-delay="20"
          :pre-type-delay="20"
          :erase-delay="250"
          erase-style="select-all"
          :erase-on-complete="false"
          caret-animation="expand"
        ></vue-typer>
        <v-btn
          outlined
          color="primary"
          class="float-right"
          :loading="isLoadingStatus('heroes')"
          :disabled="isLoadingStatus('heroes')"
          @click="$emit('generate')"
        >
          Regenerate heroes
        </v-btn>
      </div>
    </v-card-text>
    <v-row class="mb-3">
      <v-col v-for="(heroSet, i) in heroSets" :key="i" cols="12" md="4">
        <v-card
          outlined
          :loading="isLoadingStatus('portrait') && selectedHeroSet == i"
          class="mx-auto hero-card"
          :class="{ selected: selectedHeroSet == i }"
        >
          <v-card-title primary-title>
            <v-btn
              color="primary"
              :outlined="selectedHeroSet == i ? false : true"
              @click="selectHeroSet(i)"
            >
              <v-icon v-if="selectedHeroSet == i" left>mdi-check</v-icon>
              Select heroes
            </v-btn>
          </v-card-title>
          <v-card
            v-for="(hero, index) in heroSet.heroes"
            :key="index"
            :disabled="selectedHeroSet != i"
            class="mb-5"
          >
            <v-img
              v-if="hero.portrait"
              :src="hero.portrait.path"
              class="grey darken-4 white--text align-end fill-height"
              aspect-ratio="1.7"
              contain
            >
            </v-img>
            <v-card-title>
              {{ hero.name }}
              <v-btn
                color="blue"
                text
                :loading="isLoadingStatus('portrait') && isHeroSelected(i, hero)"
                @click="generatePortrait(hero)"
                >Generate portrait
              </v-btn>
            </v-card-title>
            <v-card-text class="text--primary">{{ hero.description }}</v-card-text>
          </v-card>
        </v-card>
      </v-col>
    </v-row>
    <v-btn
      class="mb-5"
      color="primary"
      :disabled="invalid || isLoadingStatus('structures') || !heroes.length"
      :loading="isLoadingStatus('structures')"
      @click="generateStructures()"
      >Generate structure
    </v-btn>
  </v-stepper-content>
</template>

<script lang="ts">
import { VueTyper } from "vue-typer";
import { Component, Vue } from "vue-property-decorator";
import { ITaleCreate, IHero, IHeroPortraitCreate } from "@/interfaces";
import {
  dispatchCreateStructures,
  dispatchCreateHeroPortrait,
  dispatchSelectHeroSet,
} from "@/store/tales/actions";
import {
  readStatus,
  readHeroes,
  readHeroSets,
  readHeroesPortraitsComplete,
} from "@/store/tales/getters";

@Component({
  components: {
    VueTyper,
  },
  props: ["invalid", "logLine", "maxTokens", "temperature", "taleStyle"],
})
export default class HeroesComponent extends Vue {
  public selectedHero = -1;
  public selectedHeroSet = -1;

  get isLoadingStatus() {
    return readStatus(this.$store);
  }

  get heroes() {
    return readHeroes(this.$store);
  }

  get heroSets() {
    return readHeroSets(this.$store);
  }

  get readyToNext() {
    return (
      !this.invalid &&
      !this.isLoadingStatus("portrait") &&
      readHeroesPortraitsComplete(this.$store)
    );
  }

  isHeroSelected(indexHeroSet: number, hero: IHero) {
    return this.selectedHeroSet == indexHeroSet && this.selectedHero == hero.id;
  }

  public selectHeroSet(index: number) {
    this.selectedHeroSet = this.selectedHeroSet == index ? -1 : index;
    dispatchSelectHeroSet(this.$store, this.selectedHeroSet);
  }

  public async generateStructures() {
    const createStructures: ITaleCreate = {};
    Object.assign(createStructures, {
      heroes: this.heroes,
      log_line: this.logLine,
      max_tokens: this.maxTokens,
      temperature: this.temperature,
      tale_style: this.taleStyle.abbr,
    });
    await dispatchCreateStructures(this.$store, createStructures);
  }

  public async generatePortrait(hero: IHero) {
    this.selectedHero = hero.id;
    const createHeroPortrait: IHeroPortraitCreate = {};
    Object.assign(createHeroPortrait, {
      hero_id: hero.id,
      prompt: hero.description,
    });
    await dispatchCreateHeroPortrait(this.$store, createHeroPortrait);
  }
}
</script>

<style>
.hero-card.selected {
  border: 1px #1976d2 solid;
  opacity: 1;
}
</style>
