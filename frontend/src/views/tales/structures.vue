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
      <v-overlay
        absolute="absolute"
        opacity="0.38"
        :value="isLoadingStatus('structures')"
      >
      </v-overlay>
    </v-fade-transition>
    <v-row>
      <v-col v-for="(struct, i) in structures" :key="i" cols="12" md="4">
        <v-card class="mx-auto" :class="{ selected: selectedStruct == i }" outlined>
          <v-card-actions>
            <v-btn
              :color="selectedStruct == i ? 'success' : 'primary'"
              :outlined="selectedStruct == i ? false : true"
              @click="selectStruct(i)"
            >
              <span>
                {{ selectedStruct == i ? "Selected plots" : "Select plots" }}
              </span>
            </v-btn>
          </v-card-actions>
          <v-container>
            <v-row dense>
              <v-col cols="12">
                <v-card
                  v-for="(part, index) in struct.parts"
                  :key="index"
                  :disabled="selectedStruct != i"
                  class="mb-5"
                  outlined
                  tile
                >
                  <v-img
                    v-if="part.image"
                    :src="part.image.path"
                    class="grey darken-4 white--text align-end fill-height"
                    aspect-ratio="1.7"
                    contain
                  >
                  </v-img>
                  <v-card-title>{{ part.name }}</v-card-title>
                  <v-card-text class="text--primary">{{ part.text }}</v-card-text>
                  <v-card-actions>
                    <v-btn
                      text
                      color="blue"
                      :loading="isLoadingStatus('image') && isPartSelected(i, part)"
                      @click="generateImage(part)"
                      >Generate illustration
                    </v-btn>
                  </v-card-actions>
                </v-card>
              </v-col>
            </v-row>
          </v-container>
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
import { IPart, ITaleCreate, IStructImageCreate, IFilter } from "@/interfaces";
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
  props: {
    logLine: { type: String },
    invalid: { type: Boolean },
    filters: { type: IFilter },
  },
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

  public generate() {
    this.selectedStruct = -1;
    this.$emit("generate");
  }

  public async generateImage(part: IPart) {
    this.selectedPart = part.id;
    const createStructImage: IStructImageCreate = {
      prompt: part.text,
      scene_id: part.id,
      style: this.filters.selected_style.abbr,
    };
    await dispatchCreateStructImage(this.$store, createStructImage);
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
