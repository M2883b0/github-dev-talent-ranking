<template>
    <div class="pagesss">
    <UserCard :userInfo="store.searchData"/>
    <TopicRankComp :rankList="store.searchData?.relate_rank_list?.rank_list" >
    <template #s1>
        Overall Score
    </template>
  </TopicRankComp>
  </div>

</template>
<script setup>
import { cxkStore } from "@/stores/searchUser.js";
import TopicRankComp from '@/components/topicRankComp/index.vue' 
import UserCard from './userCard/index.vue'
const store = cxkStore();
</script>
<style scoped>
.pagesss{
    display: flex;
  flex-direction: column;
  align-items: center;
}
</style>