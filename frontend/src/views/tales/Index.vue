<template>
  <v-container fluid>
    <v-card class="ma-3 pa-3">
      <v-card-title primary-title>
        <div class="headline primary--text">Fairytales</div>
      </v-card-title>

      <v-card-text>
        <div class="headline font-weight-light ma-5">
          Welcome to Fairytales AI generator
        </div>
      </v-card-text>

      <validation-observer ref="observer" v-slot="{ invalid }">
        <v-row>
          <v-col cols="12" md="6">
            <validation-provider v-slot="{ errors }" rules="required" name="Log Line">
              <v-textarea
                v-model="logLine"
                required
                :error-messages="errors"
                label="Write a short log line for your tale"
                placeholder="For example, A funny tale about two girls: Sasha wand Monica, who discovered that the Wicked Witch with a magic Candle wants to kidnap them to make them witches. They study magic, but all the time they do good deeds and because of this, they get into funny situations."
              ></v-textarea>
            </validation-provider>
          </v-col>
        </v-row>

        <v-card-actions>
          <v-btn :disabled="invalid" color="primary" @click="generateCharacters"
            >Generate characters
          </v-btn>
        </v-card-actions>
      </validation-observer>
    </v-card>

    <v-card v-show="heroes.length" class="ma-3 pa-3">
      <v-card-title primary-title>
        <div class="headline primary--text">Generated Heroes</div>
      </v-card-title>

      <v-card-text>
        <div class="headline font-weight-light ma-5">
          Choose heroes set suit for you
        </div>
      </v-card-text>
      <v-row class="mb-3">
        <v-col v-for="(hero, i) in heroes" :key="i" cols="12" md="4">
          <v-card
            class="mx-auto hero-card"
            tile
            :class="{ selected: selectedHeroes == i }"
            @click="selectHeroes(i)"
          >
            <v-subheader>HEROES SET: #{{ i }}</v-subheader>
            <v-list-item v-for="(name, index) in hero.names" :key="index" three-line>
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
      <v-card-actions>
        <v-btn
          :disabled="selectedHeroes < 0"
          color="primary"
          @click="generateStructures"
          >Generate structure of story
        </v-btn>
      </v-card-actions>
    </v-card>

    <v-card v-show="structures.length" class="ma-3 pa-3">
      <v-card-title primary-title>
        <div class="headline primary--text">Generated structures</div>
      </v-card-title>

      <v-card-text>
        <div class="headline font-weight-light ma-5">Choose strucutre suit for you</div>
      </v-card-text>
      <v-row class="mb-3">
        <v-col v-for="(struct, i) in structures" :key="i" cols="12" md="4">
          <v-card
            class="mx-auto hero-card"
            tile
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
      <v-card-actions>
        <v-btn color="primary" @click="generateTale">Generate fairy tale</v-btn>
      </v-card-actions>
    </v-card>

    <v-card v-show="tale" class="ma-3 pa-3">
      <v-card-title primary-title>
        <div class="headline primary--text">Generated tale</div>
      </v-card-title>

      <v-card-text>
        <div class="headline font-weight-light ma-5">
          {{ (tale && tale.title) || "Unknown Title" }}
        </div>
      </v-card-text>
      <v-row v-if="tale" class="mb-3">
        <v-col v-for="(story, i) in taleStories" :key="i" cols="12" md="4">
          <v-card class="mx-auto hero-card" tile>
            <v-card-text>
              <div class="text--primary" v-html="story.text"></div>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
      <v-card-actions>
        <v-btn color="primary" @click="generateImages">Generate tale images</v-btn>
      </v-card-actions>
    </v-card>
  </v-container>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import { ValidationProvider, ValidationObserver, extend } from "vee-validate";
import { required } from "vee-validate/dist/rules";
import { ITaleCreate } from "@/interfaces";
import {
  dispatchCreateHeroes,
  dispatchCreateStructures,
  dispatchCreateTale,
} from "@/store/tales/actions";
import {
  readHeroes,
  readTale,
  readStoriesHtml,
  readStructuresHtml,
  selectedHeroes,
  selectedStructure,
} from "@/store/tales/getters";

// register validation rules
extend("required", { ...required, message: "{_field_} can not be empty" });

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

  public async generateCharacters() {
    const success = await this.$refs.observer.validate();
    if (!success) {
      return;
    }

    const createHeroes: ITaleCreate = {};
    if (this.logLine) {
      createHeroes.log_line = this.logLine;
    }
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
    await dispatchCreateTale(this.$store, createTale);
  }
  public async generateImages() {
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
