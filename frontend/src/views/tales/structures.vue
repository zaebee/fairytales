<template>
  <v-stepper-content v-show="stepper > 1" step="2">
    <v-card-text>
      <div class="headline font-weight-light">
        Choose the structure that suits you and generate illustrations.
      </div>
    </v-card-text>
    <v-row class="mb-3">
      <v-col v-for="(struct, i) in structures" :key="i" cols="12" md="4">
        <v-card
          outlined
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
          <v-card :disabled="selectedStruct != i" class="mb-5">
            <v-img
              v-if="struct.image"
              :src="struct.image.path"
              class="grey darken-4 white--text align-end fill-height"
              aspect-ratio="1.7"
              contain
            >
            </v-img>
            <v-card-title>
              TEST
              <v-btn
                text
                color="blue"
                :loading="isLoadingStatus('image') && isStructSelected(i)"
                @click="generateImage(i)"
                >Generate illustration
              </v-btn>
            </v-card-title>
            <v-card-text>
              <div class="text--primary" v-html="struct.parts"></div>
            </v-card-text>
          </v-card>
        </v-card>
      </v-col>
    </v-row>
    <v-btn
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
import { ITaleCreate, IStructImageCreate } from "@/interfaces";
import {
  dispatchStep,
  dispatchCreateTale,
  dispatchCreateStructImage,
  dispatchSelectStructure,
} from "@/store/tales/actions";
import {
  readStatus,
  readStepper,
  readHeroes,
  readStructuresHtml,
  selectedStructure,
} from "@/store/tales/getters";

@Component({
  props: ["invalid", "logLine", "maxTokens", "temperature", "taleStyle"],
})
export default class StructuresComponent extends Vue {
  public selectedStruct = -1;

  get stepper() {
    return readStepper(this.$store);
  }

  stepperN(step: number) {
    dispatchStep(this.$store, step);
  }

  get isLoadingStatus() {
    return readStatus(this.$store);
  }

  get heroes() {
    return readHeroes(this.$store);
  }

  get structures() {
    return readStructuresHtml(this.$store);
  }

  get structure() {
    return selectedStructure(this.$store);
  }

  isStructSelected(index: number) {
    return this.selectedStruct == index;
  }

  public selectStruct(index: number) {
    this.selectedStruct = this.selectedStruct == index ? -1 : index;
    dispatchSelectStructure(this.$store, this.selectedStruct);
  }

  public async generateImage(index: number) {
    this.selectedStruct = index;
    const createStructImage: IStructImageCreate = {
      scene_id: this.structure.id,
      prompt: this.structure.parts,
    };
    await dispatchCreateStructImage(this.$store, createStructImage);
  }

  public async generateTale() {
    const success = await this.$refs.observer.validate();
    if (!success) {
      return;
    }
    const createTale: ITaleCreate = {};
    Object.assign(createTale, {
      heroes: this.heroes,
      log_line: this.logLine,
      structure: this.structure,
      max_tokens: this.maxTokens,
      temperature: this.temperature,
      tale_style: this.selectedStyle.abbr,
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
