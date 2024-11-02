<template>
  <div class="cxk">
    <Search class="cxk1" />
    <TopicRankView class="cxk2" />
    <TopicRankList class="cxk3" />
    <RandomTopic class="cxk4" />
  </div>
</template>
<script setup>
import TopicRankView from "./topicRank/index.vue";
import Search from "./search/index.vue";
import TopicRankList from "./topicRankList/index.vue";
import RandomTopic from "./randomTopic/index.vue";
import { useCounterStore } from "@/stores/topicRank";
import { onMounted } from "vue";
const store = useCounterStore();
onMounted(() => {
  store.getTopicRank();
});
</script>
<style scoped>
.cxk {
  /* width: 100vw; */
  display: flex;
  flex-direction: column;
  align-items: center;
}
.cxk1 {
  margin-top: 50px;
  margin-bottom: 30px;
}
.cxk2 {
  margin-top: 20px;
  margin-bottom: 20px;
}
.cxk3 {
  margin-top: 20px;
  margin-bottom: 20px;
}
.cxk4 {
  margin-top: 20px;
}
</style>