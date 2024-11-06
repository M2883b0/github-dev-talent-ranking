<template>
  <TopicRankComp v-for="(item, index) in store.topicRankList2" class="c5" :rankList="item" @cxk-select="onCxkSelect" :index="index">
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
  store.getTopicRank2(title,null);
});
const onCxkSelect = (index,nation)=>{
  store.getTopicRank2(title[index],nation,index);
}
const store = useCounterStore()
</script>
  <style scoped>
.c5 {
  margin-top: 20px;
  margin-bottom: 20px;
}
</style>