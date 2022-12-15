<template>
  <v-card
    :loading="isLoading('portrait') && isHeroSelected(hero)"
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
    <v-card-text class="text--primary">{{ hero.description }}</v-card-text>
    <v-card-actions>
      <v-btn
        text
        color="blue"
        :loading="isLoading('portrait') && isHeroSelected(hero)"
        @click="generatePortrait(hero)"
        >Generate portrait
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import { IFilter, IHero, IHeroPortraitCreate } from "@/interfaces";
import { dispatchCreateHeroPortrait } from "@/store/tales/actions";
import { readStatus } from "@/store/tales/getters";

@Component({
  props: {
    hero: { type: IHero },
    heroSet: { type: Number },
    filters: { type: IFilter },
    selectedHero: { type: Number },
    selectedHeroSet: { type: Number },
  },
})
export default class HeroComponent extends Vue {
  get isLoading() {
    return readStatus(this.$store);
  }

  isHeroSelected(hero: IHero) {
    return this.selectedHeroSet == this.heroSet && this.selectedHero == hero.id;
  }

  public async generatePortrait(hero: IHero) {
    this.$emit("select", hero.id);
    const createHeroPortrait: IHeroPortraitCreate = {
      hero_id: hero.id,
      prompt: hero.description,
      style: this.filters.selected_style.abbr,
    };
    await dispatchCreateHeroPortrait(this.$store, createHeroPortrait);
  }
}
</script>
