<template>
  <div class="random-topic">
    <div class="领域">
      <span class="Similarintegrations">Similar integrations</span
      >
      <el-icon class="cxksxicon" @click="刷新"><RefreshRight /></el-icon>
    </div>
    <div class="topic-list">
      <TopicItem v-for="item in store.randomTopicList" :topicInfo="item" />
    </div>
  </div>
</template>
<script setup>
import { useCounterStore } from "@/stores/randomTopic";
import TopicItem from "./topicItem.vue";
import { onMounted } from "vue";
const store = useCounterStore();
onMounted(() => {
  store.getRandomTopicList();
});
const 刷新 = () => {

};
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