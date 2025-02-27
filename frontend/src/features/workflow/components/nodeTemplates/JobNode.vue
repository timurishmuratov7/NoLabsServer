<template>
  <q-card dark bordered :class="{'pulsating-border': isRunning || isLocallyRunning}" v-if="!nodeData">
    <q-spinner color="primary" size="3em" />
  </q-card>
  <q-card dark bordered :class="{'pulsating-border': isRunning || isLocallyRunning}" v-if="nodeData" style="width: 600px">
    <q-card-section v-if="nodeData?.data.error">
      <div class="row no-wrap items-center">
        <q-space />
        <q-btn v-if="nodeData?.data.error" color="red" class="q-pm-md">
          <q-icon left name="warning" />
          <div>{{ nodeData?.data.error }}</div>
        </q-btn>
      </div>
    </q-card-section>
    <q-card-section>
      <JobNodeContent :nodeId="nodeId" :name="nodeData?.name" :description="nodeData?.description"/>
    </q-card-section>
    <q-card-section>
      <NodeHandles :nodeId="nodeId" :inputs="nodeData?.data.inputs" :outputs="nodeData?.data.outputs" :defaults="nodeData?.data.defaults" />
    </q-card-section>
    <q-card-actions align="around">
      <q-btn v-if="!isRunning && !isLocallyRunning" @click="startWorkflow" color="info" icon="play_arrow" label="Start" />
      <q-btn :disable="true" v-else>
        <q-spinner color="primary" size="20px" />
        Running...
      </q-btn>
      <q-btn @click="openDialogue" label="Extended view" />
      <q-btn @click="deleteNode" color="negative" icon="delete" label="Delete" />
    </q-card-actions>
  </q-card>
</template>

<script>
import JobNodeContent from './JobNodeContent.vue';
import NodeHandles from './NodeHandles.vue';
import { useWorkflowStore } from 'src/features/workflow/components/storage';
import { startWorkflowComponent } from 'src/features/workflow/refinedApi'

export default {
  name: 'JobNode',
  components: {
    JobNodeContent,
    NodeHandles
  },
  props: {
    nodeId: {
      type: String,
      required: true
    },
    onDeleteNode: Function,
    onOpenSettings: Function,
    onOpenDialog: Function
  },
  data() {
    return {
      isLocallyRunning: false
    };
  },
  computed: {
    nodeData() {
      const workflowStore = useWorkflowStore();
      return workflowStore.getNodeById(this.nodeId);
    },
    isRunning() {
      const workflowStore = useWorkflowStore();
      return workflowStore.runningComponentIds.includes(this.nodeId);
    }
  },
  watch: {
    isRunning(newVal, oldVal) {
      if (newVal !== oldVal) {
        this.isLocallyRunning = newVal;
      }
    }
  },
  methods: {
    async startWorkflow() {
      const workflowStore = useWorkflowStore();
      const experimentId = workflowStore.experimentId;
      try {
        this.isLocallyRunning = true;
        await startWorkflowComponent(experimentId, this.nodeId);
        console.log(`Started workflow component with experiment id: ${experimentId} and nodeId: ${this.nodeId}`);
        setTimeout(() => {
          this.isLocallyRunning = false;
        }, 5000); // Reset isLocallyRunning after 5 seconds
      } catch (error) {
        this.isLocallyRunning = false;
        console.error('Failed to start workflow component', error);
      }
    },
    deleteNode() {
      if (this.onDeleteNode) {
        this.onDeleteNode(this.nodeId);
      }
    },
    openSettings() {
      if (this.onOpenSettings) {
        this.onOpenSettings(this.nodeId);
      }
    },
    openDialogue() {
      if (this.onOpenDialog) {
        this.onOpenDialog(this.nodeId);
      }
    }
  }
};
</script>

<style scoped>
.pulsating-border {
  border: 3px solid #42b983;
  animation: pulsate 1.5s ease-out infinite;
}

@keyframes pulsate {
  0% {
    box-shadow: 0 0 10px 2px rgba(66, 185, 131, 0.5);
  }
  50% {
    box-shadow: 0 0 10px 5px rgba(66, 185, 131, 1);
  }
  100% {
    box-shadow: 0 0 10px 2px rgba(66, 185, 131, 0.5);
  }
}
</style>
