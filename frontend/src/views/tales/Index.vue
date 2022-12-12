<template>
  <v-container fluid>
    <validation-observer ref="observer" v-slot="{ invalid }">
      <v-card class="ma-3 pa-3" outlined>
        <v-card-title primary-title>
          <div class="headline primary--text">Fairytales</div>
        </v-card-title>
        <v-card-text>
          <div class="headline font-weight-light">
            Welcome to Fairytales AI generator
          </div>
        </v-card-text>

        <v-row>
          <v-col cols="12" md="6">
            <validation-provider v-slot="{ errors }" rules="required" name="Log line">
              <div class="ma-5">
                <v-textarea
                  v-model="logLine"
                  required
                  :error-messages="errors"
                  label="Write a short log line for your tale"
                  placeholder="For example, A funny tale about two girls: Sasha wand Monica, who discovered that the Wicked Witch with a magic Candle wants to kidnap them to make them witches. They study magic, but all the time they do good deeds and because of this, they get into funny situations."
                ></v-textarea>
              </div>
            </validation-provider>
          </v-col>
          <v-col cols="12" md="6">
            <v-row align="center">
              <v-col cols="12" sm="6">
                <v-select
                  v-model="selectedStyle"
                  :items="taleStyles"
                  label="Tale style"
                  hint="Generate yuor tale as selected"
                  item-text="name"
                  item-value="abbr"
                  return-object
                  persistent-hint
                ></v-select>
              </v-col>
            </v-row>
            <v-row align="center">
              <v-col cols="12" sm="6">
                <v-subheader class="pl-0">Temperature</v-subheader>
                <v-slider
                  v-model="temperature"
                  min="0"
                  max="1"
                  step="0.05"
                  thumb-label="always"
                ></v-slider>
              </v-col>
            </v-row>
            <v-row align="center">
              <v-col cols="12" sm="6">
                <validation-provider
                  v-slot="{ errors }"
                  rules="required|integer"
                  name="Max tokens"
                >
                  <v-text-field
                    v-model="maxTokens"
                    label="Max token"
                    hide-details="auto"
                    :error-messages="errors"
                  ></v-text-field>
                </validation-provider>
              </v-col>
            </v-row>
          </v-col>
        </v-row>

        <v-card-actions>
          <v-btn
            :disabled="invalid || isLoadingStatus('heroes')"
            color="primary"
            @click="generateCharacters"
            >Generate characters
          </v-btn>
          <v-progress-circular
            v-if="isLoadingStatus('heroes')"
            :size="20"
            color="primary"
            class="ml-2"
            indeterminate
          ></v-progress-circular>
        </v-card-actions>
      </v-card>
    </validation-observer>

    <div class="ma-3">
      <v-stepper v-model="stepper">
        <v-stepper-header>
          <v-stepper-step :complete="stepper > 0" :editable="stepper > 0" step="1">
            Heroes
          </v-stepper-step>
          <v-divider></v-divider>
          <v-stepper-step :complete="stepper > 1" :editable="stepper > 1" step="2">
            Structure
          </v-stepper-step>
          <v-divider></v-divider>
          <v-stepper-step :complete="stepper > 2" :editable="stepper > 2" step="3">
            Stories
          </v-stepper-step>
          <v-divider></v-divider>
          <v-stepper-step :complete="stepper > 3" :editable="stepper > 3" step="4">
            Images
          </v-stepper-step>
        </v-stepper-header>
        <v-stepper-items v-show="stepper > 0">
          <v-stepper-content step="1">
            <v-card class="ma-3 pa-3" color="lighten-1" outlined>
              <v-card-title primary-title>
                <div class="headline primary--text">Generated Heroes</div>
              </v-card-title>

              <v-card-text>
                <div class="headline font-weight-light">
                  Choose the heroes suitable you and
                  <v-btn
                    :disabled="selectedHeroes < 0 || isLoadingStatus('structures')"
                    color="primary"
                    @click="generateStructures"
                    >Generate structure of story
                  </v-btn>
                  <v-progress-circular
                    v-if="isLoadingStatus('structures')"
                    :size="20"
                    color="primary"
                    class="ml-2"
                    indeterminate
                  ></v-progress-circular>
                </div>
              </v-card-text>
              <v-row class="mb-3">
                <v-col v-for="(hero, i) in heroes" :key="i" cols="12" md="4">
                  <v-card
                    class="mx-auto hero-card"
                    tile
                    outlined
                    :class="{ selected: selectedHeroes == i }"
                    @click="selectHeroes(i)"
                  >
                    <v-subheader>HEROES SET: #{{ i }}</v-subheader>
                    <v-list-item
                      v-for="(name, index) in hero.names"
                      :key="index"
                      three-line
                    >
                      <v-list-item-content>
                        <v-list-item-title>
                          {{ name }}
                        </v-list-item-title>
                        <v-list-item-subtitle>
                          {{ hero.descriptions[index] }}
                        </v-list-item-subtitle>
                      </v-list-item-content>
                    </v-list-item>
                  </v-card>
                </v-col>
              </v-row>
            </v-card>
          </v-stepper-content>
          <v-stepper-content v-show="structures.length" step="2">
            <v-card class="ma-3 pa-3" outlined>
              <v-card-title primary-title>
                <div class="headline primary--text">Generated structures</div>
              </v-card-title>

              <v-card-text>
                <div class="headline font-weight-light">
                  Choose the structure that suits you and
                  <v-btn
                    :disabled="selectedStruct < 0 || isLoadingStatus('tale')"
                    color="primary"
                    @click="generateTale"
                  >
                    Generate fairy tale
                  </v-btn>
                  <v-progress-circular
                    v-if="isLoadingStatus('tale')"
                    :size="20"
                    color="primary"
                    class="ml-2"
                    indeterminate
                  ></v-progress-circular>
                </div>
              </v-card-text>
              <v-row class="mb-3">
                <v-col v-for="(struct, i) in structures" :key="i" cols="12" md="4">
                  <v-card
                    class="mx-auto hero-card"
                    tile
                    outlined
                    :class="{ selected: selectedStruct == i }"
                    @click="selectStruct(i)"
                  >
                    <v-card-title primary-title>
                      <div class="headline primary--text">Structure #{{ i }}</div>
                    </v-card-title>
                    <v-card-text>
                      <div class="text--primary" v-html="struct.parts"></div>
                    </v-card-text>
                  </v-card>
                </v-col>
              </v-row>
            </v-card>
          </v-stepper-content>
          <v-stepper-content v-show="tale" step="3">
            <v-card class="ma-3 pa-3" outlined>
              <v-card-title primary-title>
                <div class="headline primary--text">Generated tale</div>
              </v-card-title>

              <v-card-text>
                <div class="headline font-weight-light">
                  {{ (tale && tale.title) || "Unknown Title" }}
                  <v-btn
                    :disabled="selectedStory < 0 || isLoadingStatus('tale')"
                    color="primary"
                    @click="generateImages"
                  >
                    Generate tale images
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
                    @click="selectStory(i)"
                  >
                    <v-card-text>
                      <div class="text--primary" v-html="story.text"></div>
                    </v-card-text>
                  </v-card>
                </v-col>
              </v-row>
            </v-card>
          </v-stepper-content>
        </v-stepper-items>
      </v-stepper>
    </div>
  </v-container>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import { ValidationProvider, ValidationObserver, extend } from "vee-validate";
import { required, integer } from "vee-validate/dist/rules";
import { ITaleCreate } from "@/interfaces";
import {
  dispatchCreateHeroes,
  dispatchCreateStructures,
  dispatchCreateTale,
} from "@/store/tales/actions";
import {
  readStatus,
  readStepper,
  readHeroes,
  readTale,
  readStoriesHtml,
  readStructuresHtml,
  selectedHeroes,
  selectedStructure,
} from "@/store/tales/getters";

// register validation rules
extend("required", { ...required, message: "{_field_} can not be empty" });
extend("integer", { ...integer, message: "{_field_} should be a number" });

@Component({
  components: {
    ValidationObserver,
    ValidationProvider,
  },
})
export default class Dashboard extends Vue {
  $refs!: {
    observer: InstanceType<typeof ValidationObserver>;
  };

  public valid = true;
  public logLine = "";
  public selectedHeroes = -1;
  public selectedStruct = -1;
  public selectedStory = -1;
  public maxTokens = 500;
  public temperature = 0.5;
  public selectedStyle = {
    name: "Red Riding Hood by the Grimm brothers",
    abbr: "RED_HOOD",
  };
  public taleStyles = [
    { name: "Mary's child by the Grimm brothers", abbr: "MARY" },
    { name: "Red Riding Hood by the Grimm brothers", abbr: "RED_HOOD" },
    { name: "Tale about a goose", abbr: "GOSE" },
  ];

  get stepper() {
    return readStepper(this.$store);
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

  get tale() {
    return readTale(this.$store);
  }

  get taleStories() {
    return readStoriesHtml(this.$store);
  }

  get getHeroes() {
    return selectedHeroes(this.$store);
  }

  get getStructure() {
    return selectedStructure(this.$store);
  }

  public selectHeroes(index: number) {
    if (this.selectedHeroes == index) {
      this.selectedHeroes = -1;
    } else {
      this.selectedHeroes = index;
    }
  }

  public selectStruct(index: number) {
    if (this.selectedStruct == index) {
      this.selectedStruct = -1;
    } else {
      this.selectedStruct = index;
    }
  }

  public selectStory(index: number) {
    if (this.selectedStory == index) {
      this.selectedStory = -1;
    } else {
      this.selectedStory = index;
    }
  }

  public async generateCharacters() {
    const success = await this.$refs.observer.validate();
    if (!success) {
      return;
    }

    const createHeroes: ITaleCreate = {};
    if (this.logLine) {
      createHeroes.log_line = this.logLine;
    }
    Object.assign(createHeroes, {
      tale_style: this.selectedStyle.abbr,
      temperature: this.temperature,
      max_tokens: this.maxTokens,
    });
    await dispatchCreateHeroes(this.$store, createHeroes);
  }

  public async generateStructures() {
    const success = await this.$refs.observer.validate();
    if (!success) {
      return;
    }
    const createStructures: ITaleCreate = {};
    const heroes = this.getHeroes(this.selectedHeroes);
    if (this.logLine) {
      createStructures.log_line = this.logLine;
    }
    if (heroes.names.length) {
      createStructures.heroes = heroes;
    }
    Object.assign(createStructures, {
      tale_style: this.selectedStyle.abbr,
      temperature: this.temperature,
      max_tokens: this.maxTokens,
    });
    await dispatchCreateStructures(this.$store, createStructures);
  }

  public async generateTale() {
    const success = await this.$refs.observer.validate();
    if (!success) {
      return;
    }
    const createTale: ITaleCreate = {};
    const heroes = this.getHeroes(this.selectedHeroes);
    const struct = this.getStructure(this.selectedStruct);
    if (this.logLine) {
      createTale.log_line = this.logLine;
    }
    if (heroes.names.length) {
      createTale.heroes = heroes;
    }
    if (struct.parts.length) {
      createTale.structure = struct;
    }
    Object.assign(createTale, {
      tale_style: this.selectedStyle.abbr,
      temperature: this.temperature,
      max_tokens: this.maxTokens,
    });
    await dispatchCreateTale(this.$store, createTale);
  }
  public generateImages() {
    return;
  }
}
</script>

<style>
.hero-card {
  cursor: pointer;
  opacity: 0.5;
}
.hero-card.selected {
  border: 1px #1976d2 solid;
  opacity: 1;
}
.hero-card:not(.selected):hover {
  border: 1px #1976d2 solid;
  cursor: pointer;
  opacity: 1;
}
</style>
