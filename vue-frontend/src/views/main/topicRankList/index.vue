<template>
  <TopicRankComp v-for="(item, index) in 3" class="c5">
    <template #s1>
      {{ title[index] }}
    </template>
  </TopicRankComp>
</template>
  <script setup>
import TopicRankComp from "@/components/topicRankComp/index.vue";
const title = ["python", "c++", "c"];
</script>
  <style scoped>
.c5 {
  margin-top: 20px;
  margin-bottom: 20px;
}
</style>