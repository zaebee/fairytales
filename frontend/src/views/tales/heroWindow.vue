<template>
  <v-card class="mx-auto" outlined>
    <v-window v-model="selectedHeroSet">
      <v-window-item v-for="(heroSet, i) in heroSets" :key="i">
        <v-card-actions class="justify-space-between">
          <v-btn text :disabled="isLoading('portrait')" @click="prev">
            <v-icon>mdi-chevron-left</v-icon>
          </v-btn>
          <v-card-title>Heroes</v-card-title>
          <v-btn text :disabled="isLoading('portrait')" @click="next">
            <v-icon>mdi-chevron-right</v-icon>
          </v-btn>
        </v-card-actions>
        <v-container>
          <v-row dense>
            <v-col cols="12">
              <hero-component
                v-for="hero in heroSet.heroes"
                :key="hero.id"
                :hero="hero"
                :hero-set="i"
                :filters="filters"
                :selected-hero="selectedHero"
                :selected-hero-set="selectedHeroSet"
                @select="selectHero"
              />
            </v-col>
          </v-row>
        </v-container>
      </v-window-item>
    </v-window>
  </v-card>
</template>

<script lang="ts">
import { Component, Vue, Watch } from "vue-property-decorator";
import { IFilter } from "@/interfaces";
import { dispatchSelectHeroSet } from "@/store/tales/actions";
import { readStatus, readHeroSets } from "@/store/tales/getters";
import HeroComponent from "./hero.vue";

@Component({
  components: {
    HeroComponent,
  },
  props: {
    filters: { type: IFilter },
  },
})
export default class HeroWindowComponent extends Vue {
  public selectedHero = -1;
  public selectedHeroSet = 0;

  @Watch("selectedHeroSet")
  onHeroSetChanged(newVal) {
    if (this.heroSets.length) {
      dispatchSelectHeroSet(this.$store, newVal);
    }
  }

  next() {
    this.selectedHeroSet =
      this.selectedHeroSet + 1 === this.heroSets.length ? 0 : this.selectedHeroSet + 1;
  }

  prev() {
    this.selectedHeroSet =
      this.selectedHeroSet - 1 < 0
        ? this.heroSets.length - 1
        : this.selectedHeroSet - 1;
  }

  get isLoading() {
    return readStatus(this.$store);
  }

  get heroSets() {
    return readHeroSets(this.$store);
  }

  public selectHero(id: number) {
    this.selectedHero = id;
  }
}
</script>
