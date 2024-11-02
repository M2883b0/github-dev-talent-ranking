<template>
  <div class="about">
   
  </div>
</template>
<script setup>
import {useCounterStore} from '@/stores/topicRank'
const store = useCounterStore()

</script>
<style>
@media (min-width: 1024px) {
  .about {
    min-height: 100vh;
    display: flex;
    align-items: center;
  }
}
</style>
