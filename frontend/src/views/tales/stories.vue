<template>
  <v-stepper-content step="3">
    <v-card-text>
      <div class="headline font-weight-light">
        {{ (tale && tale.title) || "Unknown Title" }}
        <v-btn v-if="!(tale && tale.title)" outlined color="primary" disabled>
          Generate title
        </v-btn>
        <v-btn
          outlined
          color="primary"
          class="float-right"
          :loading="isLoadingStatus('tale')"
          :disabled="isLoadingStatus('tale')"
          @click="$emit('generate')"
        >
          Regenerate stories
        </v-btn>
      </div>
    </v-card-text>
    <v-fade-transition>
      <v-overlay absolute="absolute" opacity="0.38" :value="isLoadingStatus('tale')">
      </v-overlay>
    </v-fade-transition>
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
    <v-btn class="mb-5" color="primary" :disabled="invalid" @click="finish()"
      >Finish
    </v-btn>
  </v-stepper-content>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import {
  readStatus,
  readTale,
  readHeroes,
  readStoriesHtml,
  selectedStructure,
} from "@/store/tales/getters";

@Component({
  props: ["invalid", "logLine", "maxTokens", "temperature", "taleStyle"],
})
export default class StoriesComponent extends Vue {
  public selectedStory = -1;

  get isLoadingStatus() {
    return readStatus(this.$store);
  }

  get heroes() {
    return readHeroes(this.$store);
  }

  get structure() {
    return selectedStructure(this.$store);
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
