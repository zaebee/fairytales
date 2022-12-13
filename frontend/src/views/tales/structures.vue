<template>
  <v-stepper-content step="2">
    <v-card-text>
      <div class="headline font-weight-light">
        Choose the structure that suits you and generate illustrations.
        <v-btn
          outlined
          color="primary"
          class="float-right"
          :loading="isLoadingStatus('structures')"
          :disabled="isLoadingStatus('structures')"
          @click="$emit('generate')"
        >
          Regenerate structures
        </v-btn>
      </div>
    </v-card-text>
    <v-fade-transition>
      <v-overlay
        absolute="absolute"
        opacity="0.38"
        :value="isLoadingStatus('structures')"
      >
      </v-overlay>
    </v-fade-transition>
    <v-row class="mb-3">
      <v-col v-for="(struct, i) in structures" :key="i" cols="12" md="4">
        <v-card
          outlined
          :loading="isLoadingStatus('image') && selectedStruct == i"
          class="mx-auto hero-card"
          :class="{ selected: selectedStruct == i }"
        >
          <v-card-title primary-title>
            <v-btn
              color="primary"
              :outlined="selectedStruct == i ? false : true"
              @click="selectStruct(i)"
            >
              <v-icon v-if="selectedStruct == i" left>mdi-check</v-icon>
              Select structure
            </v-btn>
          </v-card-title>
          <v-card
            v-for="(part, index) in struct.parts"
            :key="index"
            :disabled="selectedStruct != i"
            class="mb-5"
          >
            <v-img
              v-if="part.image"
              :src="part.image.path"
              class="grey darken-4 white--text align-end fill-height"
              aspect-ratio="1.7"
              contain
            >
            </v-img>
            <v-card-title>
              {{ part.name }}
              <v-btn
                text
                color="blue"
                :loading="isLoadingStatus('image') && isPartSelected(i, part)"
                @click="generateImage(part)"
                >Generate illustration
              </v-btn>
            </v-card-title>
            <v-card-text class="text--primary">{{ part.text }}</v-card-text>
          </v-card>
        </v-card>
      </v-col>
    </v-row>
    <v-btn
      class="mb-5"
      color="primary"
      :disabled="invalid || selectedStruct < 0 || isLoadingStatus('tale')"
      :loading="isLoadingStatus('tale')"
      @click="generateTale"
      >Generate tale
    </v-btn>
  </v-stepper-content>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import { IPart, ITaleCreate, IStructImageCreate } from "@/interfaces";
import {
  dispatchCreateTale,
  dispatchCreateStructImage,
  dispatchSelectStructure,
} from "@/store/tales/actions";
import {
  readStatus,
  readHeroes,
  readStructures,
  selectedStructure,
} from "@/store/tales/getters";

@Component({
  props: ["invalid", "logLine", "maxTokens", "temperature", "taleStyle"],
})
export default class StructuresComponent extends Vue {
  public selectedStruct = -1;
  public selectedPart = -1;

  get isLoadingStatus() {
    return readStatus(this.$store);
  }

  get heroes() {
    return readHeroes(this.$store);
  }

  get structures() {
    return readStructures(this.$store);
  }

  get structure() {
    return selectedStructure(this.$store);
  }

  isPartSelected(indexStruct: number, part: IPart) {
    return this.selectedStruct == indexStruct && this.selectedPart == part.id;
  }

  public selectStruct(index: number) {
    this.selectedStruct = this.selectedStruct == index ? -1 : index;
    dispatchSelectStructure(this.$store, this.selectedStruct);
  }

  public async generateImage(part: IPart) {
    this.selectedPart = part.id;
    const createStructImage: IStructImageCreate = {
      scene_id: part.id,
      prompt: part.text,
    };
    await dispatchCreateStructImage(this.$store, createStructImage);
  }

  public async generateTale() {
    const createTale: ITaleCreate = {};
    Object.assign(createTale, {
      heroes: this.heroes,
      log_line: this.logLine,
      structure: this.structure,
      max_tokens: this.maxTokens,
      temperature: this.temperature,
      tale_style: this.taleStyle.abbr,
    });
    await dispatchCreateTale(this.$store, createTale);
  }
}
</script>

<style>
.hero-card.selected {
  border: 1px #1976d2 solid;
  opacity: 1;
}
</style>
