<template>
    <div>

    </div>
</template>
<script setup>
import { useCounterStore } from "@/stores/allTopic.js";
import { onMounted } from "vue";
const store = useCounterStore();
onMounted(() => {
  store.getAllTopic();
});
</script>
<style scoped>
</style>