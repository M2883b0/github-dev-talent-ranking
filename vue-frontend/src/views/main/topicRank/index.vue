<template>
  <TopicRankComp :rankList="store.topicRankList" >
    <template #s1>
        Overall Score
    </template>
  </TopicRankComp>
</template>
<script setup>
import TopicRankComp from '@/components/topicRankComp/index.vue' 
import {useCounterStore} from '@/stores/topicRank'
const store = useCounterStore()
</script>
<style scoped>

</style>