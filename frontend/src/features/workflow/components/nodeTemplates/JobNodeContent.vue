<template>
  <q-card>
    <NodeContentHeader :name="name" :description="description" :inputs="['FASTA']" :outputs="['PDB']"
      :imageSrc="imageSrc" />
    <NodeContentBody :nodeId="nodeId" :name="name" />
  </q-card>
</template>

<script lang="ts">
import { defineComponent, computed } from 'vue';
import NodeContentHeader from './NodeContentHeader.vue';
import NodeContentBody from './NodeContentBody.vue';

export default defineComponent({
  name: 'JobNodeContent',
  components: {
    NodeContentHeader,
    NodeContentBody,
  },
  props: {
    nodeId: {
      type: String,
      required: true
    },
    name: {
      type: String,
      required: true
    },
    description: {
      type: String,
      required: true
    }
  },
  computed: {
    imageSrc(): string {
      switch (this.name) {
        case 'Esmfold light':
        case 'Rosettafold component':
        case 'Esmfold':
          return '/folding_pic.png';
        case 'DiffDock':
          return '/docking_pic.png';
        case 'Small molecules design':
          return '/small_molecule.jpg';
        case 'RFDiffusion Binder Design':
          return '/rf_diffusion_pic.png';
        case 'Localisation':
          return '/localisation_pic.png';
        case 'Gene ontology':
          return '/gene_ontology_pic.png';
        case 'Conformations':
          return '/conformations_pic.png';
        case 'Binding pockets':
          return '/pocket_prediction_pic.png';
        case 'Solubility':
          return '/solubility_pic.png';
        case 'Msa generation':
          return '/msa_pic.png';
        case 'Blast':
          return '/blast_icon.png';
        case 'ProteinMPNN':
          return '/protmpnn_icon.png';
        case 'Protein affinity characterization':
          return '/Adaptyvbio_small_logo.png';
        case 'Protein binding screening':
          return '/Adaptyvbio_small_logo.png';
        default:
          return '/protein_folding.png';
      }
    }
  },
  mounted() {
    console.log(this.name)
  }
});
</script>
