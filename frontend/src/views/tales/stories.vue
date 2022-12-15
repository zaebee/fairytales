<template>
  <v-stepper-content step="3">
    <v-row>
      <v-col cols="9">
        <div class="text-md-h4 font-weight-light mb-7">
          {{ (tale && tale.title) || "Unknown Title" }}
        </div>
      </v-col>
      <v-col cols="3">
        <v-btn
          outlined
          color="primary"
          class="float-right"
          :loading="isLoading('tale')"
          :disabled="isLoading('tale')"
          @click="$emit('generate')"
        >
          Regenerate stories
        </v-btn>
      </v-col>
    </v-row>
    <v-fade-transition>
      <v-overlay absolute="absolute" opacity="0.38" :value="isLoading('tale')">
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
  props: {
    logLine: { type: String },
    invalid: { type: Boolean },
  },
})
export default class StoriesComponent extends Vue {
  public selectedStory = -1;

  get isLoading() {
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
