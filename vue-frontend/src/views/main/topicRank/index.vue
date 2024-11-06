<template>
  <TopicRankComp :rankList="store.topicRankList" @cxk-select="onCxkSelect">
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
const onCxkSelect = (_,nation)=>{
  store.getTopicRank(nation);
}
</script>
<style scoped>

</style>