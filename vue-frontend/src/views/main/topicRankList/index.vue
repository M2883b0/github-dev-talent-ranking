<template>
  <TopicRankComp v-for="(item, index) in store.topicRankList2" class="c5" :rankList="item">
    <template #s1>
      {{ title[index] }}
    </template>
  </TopicRankComp>
</template>
  <script setup>
import TopicRankComp from "@/components/topicRankComp/index.vue";
import { onMounted } from "vue";
import {useCounterStore} from '@/stores/topicRank'
const title = ["python", "c++", "c"];

onMounted(() => {
  store.getTopicRank2(title);
});
const store = useCounterStore()
</script>
  <style scoped>
.c5 {
  margin-top: 20px;
  margin-bottom: 20px;
}
</style>