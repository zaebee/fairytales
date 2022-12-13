<template>
  <v-stepper-content step="1">
    <v-row>
      <v-col cols="9">
        <div class="text-md-h4 font-weight-light mb-7">
          Choose heroes suitable for you and generate portraits.
        </div>
      </v-col>
      <v-col cols="3">
        <v-btn
          outlined
          color="primary"
          class="float-right"
          :disabled="invalid || isLoadingStatus('structures') || !heroes.length"
          :loading="isLoadingStatus('structures')"
          @click="generateStructures"
          >Next
          <v-icon>mdi-chevron-right</v-icon>
        </v-btn>
      </v-col>
    </v-row>
    <v-fade-transition>
      <v-overlay absolute="absolute" opacity="0.38" :value="isLoadingStatus('heroes')">
      </v-overlay>
    </v-fade-transition>
    <v-row>
      <v-col v-for="(heroSet, i) in heroSets" :key="i" cols="12" md="4">
        <v-card class="mx-auto" :class="{ selected: selectedHeroSet == i }" outlined>
          <v-card-actions>
            <v-btn
              :color="selectedHeroSet == i ? 'success' : 'primary'"
              :outlined="selectedHeroSet == i ? false : true"
              @click="selectHeroSet(i)"
            >
              <span>
                {{ selectedHeroSet == i ? "Selected heroes" : "Select heroes" }}
              </span>
            </v-btn>
          </v-card-actions>
          <v-container>
            <v-row dense>
              <v-col cols="12">
                <v-card
                  v-for="(hero, index) in heroSet.heroes"
                  :key="index"
                  :disabled="selectedHeroSet != i"
                  :loading="isLoadingStatus('portrait') && isHeroSelected(i, hero)"
                  class="mb-5"
                  outlined
                  tile
                >
                  <v-img
                    v-if="hero.portrait"
                    :src="hero.portrait.path"
                    class="grey darken-4 white--text align-end fill-height"
                    aspect-ratio="1.7"
                    contain
                  >
                  </v-img>
                  <v-card-title>{{ hero.name }}</v-card-title>
                  <v-card-text class="text--primary">
                    {{ hero.description }}
                  </v-card-text>
                  <v-card-actions>
                    <v-btn
                      color="blue"
                      text
                      :loading="isLoadingStatus('portrait') && isHeroSelected(i, hero)"
                      @click="generatePortrait(hero)"
                      >Generate portrait
                    </v-btn>
                  </v-card-actions>
                </v-card>
              </v-col>
            </v-row>
          </v-container>
        </v-card>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12">
        <v-btn
          color="primary"
          class="float-right"
          :disabled="invalid || isLoadingStatus('structures') || !heroes.length"
          :loading="isLoadingStatus('structures')"
          @click="generateStructures()"
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
import { ITaleCreate, IHero, IHeroPortraitCreate, IFilter } from "@/interfaces";
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
  props: {
    logLine: { type: String },
    invalid: { type: Boolean },
    filters: { type: IFilter },
  },
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

  public generate() {
    this.selectedHero = -1;
    this.selectedHeroSet = -1;
    this.$emit("generate");
  }

  public async generateStructures() {
    const createStructures: ITaleCreate = {
      heroes: this.heroes,
      log_line: this.logLine,
      max_tokens: this.filters.max_tokens,
      temperature: this.filters.temperature,
      tale_style: this.filters.selected_style.abbr,
    };
    await dispatchCreateStructures(this.$store, createStructures);
  }

  public async generatePortrait(hero: IHero) {
    this.selectedHero = hero.id;
    const createHeroPortrait: IHeroPortraitCreate = {
      hero_id: hero.id,
      prompt: hero.description,
      style: this.filters.selected_style.abbr,
    };
    await dispatchCreateHeroPortrait(this.$store, createHeroPortrait);
  }
}
</script>
