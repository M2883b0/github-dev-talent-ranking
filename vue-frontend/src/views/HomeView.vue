<template>
  <div class="about">
    <div>man</div>
  </div>
</template>
<script setup>
import {useCounterStore} from '@/stores/topicRank'
import { onMounted } from 'vue';
const store = useCounterStore()
onMounted(()=>{
  store.getTopicRank()
})
</script>
<style>

</style>
