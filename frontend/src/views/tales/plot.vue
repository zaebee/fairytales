<template>
  <v-card
    :loading="isLoadingStatus('image') && isSelected(plot)"
    class="mb-5"
    outlined
    tile
  >
    <v-img
      v-if="plot.image"
      :src="plot.image.path"
      class="grey darken-4 white--text align-end fill-height"
      aspect-ratio="1.7"
      contain
    >
    </v-img>
    <v-card-text class="text--primary">{{ plot.text }}</v-card-text>
    <v-card-actions>
      <v-btn
        text
        color="blue"
        :loading="isLoadingStatus('image') && isSelected(plot)"
        @click="generateImage(plot)"
        >Generate illustration
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import { IFilter, IPart, IStructImageCreate } from "@/interfaces";
import { dispatchCreateStructImage } from "@/store/tales/actions";
import { readStatus } from "@/store/tales/getters";

@Component({
  props: {
    plot: { type: IPart },
    plotSet: { type: Number },
    filters: { type: IFilter },
    selectedPlot: { type: Number },
    selectedPlotSet: { type: Number },
  },
})
export default class PlotComponent extends Vue {
  get isLoadingStatus() {
    return readStatus(this.$store);
  }

  isSelected(plot: IPart) {
    return this.selectedPlotSet == this.plotSet && this.selectedPlot == plot.id;
  }

  public async generateImage(plot: IPart) {
    this.$emit("select", plot.id);
    const createStructImage: IStructImageCreate = {
      prompt: plot.text,
      scene_id: plot.id,
      style: this.filters.selected_style.abbr,
    };
    await dispatchCreateStructImage(this.$store, createStructImage);
  }
}
</script>
