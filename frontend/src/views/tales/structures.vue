<template>
  <v-stepper-content step="2">
    <v-row>
      <v-col cols="9">
        <div class="text-md-h4 font-weight-light mb-7">
          Choose the plots that suits you and generate illustrations.
        </div>
      </v-col>
      <v-col cols="3">
        <v-btn
          outlined
          color="primary"
          class="float-right"
          :disabled="invalid || isLoadingStatus('tale') || !heroes.length"
          :loading="isLoadingStatus('tale')"
          @click="generateTale"
          >Next
          <v-icon>mdi-chevron-right</v-icon>
        </v-btn>
      </v-col>
    </v-row>
    <v-fade-transition>
      <v-overlay absolute="absolute" opacity="0.38" :value="isLoadingStatus('tale')">
      </v-overlay>
    </v-fade-transition>
    <v-row>
      <v-col cols="12" md="4">
        <v-card class="mx-auto" outlined>
          <hero-window-component :filters="filters" :hero-sets="heroSets" />
        </v-card>
      </v-col>
      <v-col cols="12" md="4">
        <v-card class="mx-auto" outlined>
          <v-window v-model="selectedPlotSet">
            <v-window-item v-for="(plotSet, i) in plotSets" :key="i">
              <v-card-actions class="justify-space-between">
                <v-btn text :disabled="isLoadingStatus('image')" @click="prev">
                  <v-icon>mdi-chevron-left</v-icon>
                </v-btn>
                <v-card-title>Plots</v-card-title>
                <v-btn text :disabled="isLoadingStatus('image')" @click="next">
                  <v-icon>mdi-chevron-right</v-icon>
                </v-btn>
              </v-card-actions>
              <v-container>
                <v-row dense>
                  <v-col cols="12">
                    <plot-component
                      v-for="plot in plotSet.parts"
                      :key="plot.id"
                      :plot="plot"
                      :plot-set="i"
                      :filters="filters"
                      :selected-plot="selectedPlot"
                      :selected-plot-set="selectedPlotSet"
                      @select="selectPlot"
                    />
                  </v-col>
                </v-row>
              </v-container>
            </v-window-item>
          </v-window>
        </v-card>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12">
        <v-btn
          class="float-right"
          color="primary"
          :disabled="invalid || selectedPlotSet < 0 || isLoadingStatus('tale')"
          :loading="isLoadingStatus('tale')"
          @click="generateTale"
          >Next
          <v-icon>mdi-chevron-right</v-icon>
        </v-btn>
      </v-col>
    </v-row>
  </v-stepper-content>
</template>

<script lang="ts">
import { Component, Vue, Watch } from "vue-property-decorator";
import { ITaleCreate, IFilter } from "@/interfaces";
import { dispatchCreateTale, dispatchSelectStructure } from "@/store/tales/actions";
import {
  readStatus,
  readHeroes,
  readHeroSets,
  readStructures,
  selectedStructure,
} from "@/store/tales/getters";
import PlotComponent from "./plot.vue";
import HeroWindowComponent from "./heroWindow.vue";

@Component({
  components: {
    PlotComponent,
    HeroWindowComponent,
  },
  props: {
    logLine: { type: String },
    invalid: { type: Boolean },
    filters: { type: IFilter },
  },
})
export default class StructuresComponent extends Vue {
  public selectedPlot = -1;
  public selectedPlotSet = 0;

  @Watch("selectedPlotSet")
  onPlotSetChanged(newVal) {
    if (this.plotSets.length) {
      dispatchSelectStructure(this.$store, newVal);
    }
  }

  next() {
    this.selectedPlotSet =
      this.selectedPlotSet + 1 === this.plotSets.length ? 0 : this.selectedPlotSet + 1;
  }

  prev() {
    this.selectedPlotSet =
      this.selectedPlotSet - 1 < 0
        ? this.plotSets.length - 1
        : this.selectedPlotSet - 1;
  }
  get isLoadingStatus() {
    return readStatus(this.$store);
  }

  get heroes() {
    return readHeroes(this.$store);
  }

  get heroSets() {
    return readHeroSets(this.$store);
  }

  get plotSets() {
    return readStructures(this.$store);
  }

  get structure() {
    return selectedStructure(this.$store);
  }

  public selectPlot(id: number) {
    this.selectedPlot = id;
  }

  public generate() {
    this.$emit("generate");
  }

  public async generateTale() {
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
