<template>
  <TopicRankComp :rankList="store.topicRankList" >
    <template #s1>
        Overall Score
    </template>
  </TopicRankComp>
</template>
<script setup>
import TopicRankComp from '@/components/topicRankComp/index.vue' 
import { useCounterStore } from "@/stores/topicRank";
import { onMounted } from "vue";
const store = useCounterStore();
onMounted(() => {
  store.getTopicRank();
});
</script>
<style scoped>

</style>