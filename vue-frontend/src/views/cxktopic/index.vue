<template>
   <TopicItem  :topicInfo="store2.searchData.topic_list[0]" />
   <div>
    关联领域
   </div>
   <div class="cxk10086">
    <TopicItem  :topicInfo="item" v-for="item in store2.relateTopicList"/>
   </div>
   <TopicRankComp :rankList="store2.topicRankList" @cxk-select="onCxkSelect">
    <template #s1>
        {{ store2.searchname }}
    </template>
  </TopicRankComp>
</template>
<script setup>
import TopicRankComp from '@/components/topicRankComp/index.vue' 
import { cxkStore2 } from "@/stores/cxksearchtopic.js";
import TopicItem from "@/components/topicItem/topicItem.vue";
import {  watch } from "vue";
const store2 = cxkStore2();

</script>
<style scoped>
.cxk10086{
    width:100%;
    display: flex;
}
</style>