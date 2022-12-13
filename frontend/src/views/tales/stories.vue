<template>
  <v-stepper-content v-show="tale" step="3">
    <v-card-text>
      <div class="headline font-weight-light">
        {{ (tale && tale.title) || "Unknown Title" }}
        <v-btn v-if="!tale.title" outlined color="primary" disabled>
          Generate title
        </v-btn>
      </div>
    </v-card-text>
    <v-row v-if="tale" class="mb-3">
      <v-col v-for="(story, i) in taleStories" :key="i" cols="12" md="4">
        <v-card
          class="mx-auto hero-card"
          tile
          outlined
          :class="{ selected: selectedStory == i }"
        >
          <v-card-text>
            <div class="text--primary" v-html="story.text"></div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    <v-btn color="primary" :disabled="invalid" @click="finish()">Finish</v-btn>
  </v-stepper-content>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import { dispatchStep } from "@/store/tales/actions";
import {
  readStatus,
  readStepper,
  readTale,
  readStoriesHtml,
} from "@/store/tales/getters";

@Component({
  props: ["invalid", "logLine", "maxTokens", "temperature", "taleStyle"],
})
export default class StoriesComponent extends Vue {
  public selectedStory = -1;

  get stepper() {
    return readStepper(this.$store);
  }

  set stepper(step: number) {
    dispatchStep(this.$store, step);
  }

  get isLoadingStatus() {
    return readStatus(this.$store);
  }

  get tale() {
    return readTale(this.$store);
  }

  get taleStories() {
    return readStoriesHtml(this.$store);
  }

  public selectStory(index: number) {
    if (this.selectedStory == index) {
      this.selectedStory = -1;
    } else {
      this.selectedStory = index;
    }
  }

  public finish() {
    return;
  }
}
</script>
