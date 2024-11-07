<template>
  <div class="random-topic">
    <div class="领域">
      <span class="Similarintegrations">推荐领域  &nbsp;  &nbsp;  &nbsp;</span
      >
    </div>
    <div @click="Gomore">查看更多</div>
    <div class="topic-list">
      <TopicItem v-for="item in store.randomTopicList" :topicInfo="item" />
    </div>

  </div>
</template>
<script setup>
import { useCounterStore } from "@/stores/randomTopic";
import TopicItem from "../../../components/topicitem/topicItem.vue";
import { onMounted } from "vue";
const store = useCounterStore();
import router from "@/router/index.js";
onMounted(() => {
  store.getRandomTopicList();
});
const Gomore = ()=>{
  router.push({name:'more'})
}
</script>
<style scoped>
.random-topic {
  background-color: rgb(233, 250, 243);
  width: 100vw;
  padding: 0 10vw;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-top: 60px;
}
.领域 {
  font-size: 30px;
  margin-bottom: 60px;
  display: flex;
  align-items: center;
}
.Similarintegrations {
  margin-right: 10px;
}
.cxksxicon {
  font-size: 30px;
}
.cxksxicon:hover {
  cursor: pointer;
}
.topic-list {
  width: 100%;
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  justify-content: center;
  margin-bottom: 60px;
}
</style>